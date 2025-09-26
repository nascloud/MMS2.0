import asyncio
import hashlib
import json
import logging
import tempfile
from typing import Dict, Any, Optional
from mihomo_sync.modules.rule_generation_orchestrator import RuleGenerationOrchestrator
from mihomo_sync.modules.rule_merger import RuleMerger


class StateMonitor:
    """一个监控器，用于检测Mihomo状态的变化并使用去抖动逻辑触发操作。"""
    
    def __init__(self, api_client, mosdns_controller, mosdns_config_path: str, 
                 polling_interval: float, debounce_interval: float,
                 mihomo_config_parser=None, mihomo_config_path: str = "",
                 orchestrator: Optional[RuleGenerationOrchestrator] = None, 
                 merger: Optional[RuleMerger] = None):
        """
        初始化StateMonitor。
        
        Args:
            api_client: MihomoApiClient的实例
            mosdns_controller: Mosdns服务的控制器
            mosdns_config_path (str): Mosdns配置文件的输出目录路径
            polling_interval (float): 轮询时间间隔（秒）
            debounce_interval (float): 变化后触发操作前的等待时间（秒）
            mihomo_config_parser: Mihomo本地配置文件的解析器
            mihomo_config_path (str): Mihomo配置文件的路径
            orchestrator: RuleGenerationOrchestrator实例
            merger: RuleMerger实例
        """
        self.api_client = api_client
        self.mosdns_controller = mosdns_controller
        self.mosdns_config_path = mosdns_config_path
        self.polling_interval = polling_interval
        self.debounce_interval = debounce_interval
        self.mihomo_config_parser = mihomo_config_parser
        self.mihomo_config_path = mihomo_config_path
        self.orchestrator = orchestrator
        self.merger = merger
        self.logger = logging.getLogger(__name__)
        self._last_state_hash = None
        self._debounce_task = None

    async def _get_state_hash(self) -> str:
        """
        获取表示Mihomo当前状态的哈希摘要。
        
        Returns:
            str: 当前状态的SHA-256哈希
        """
        try:
            # 获取代理和规则提供者数据
            proxies_data = await self.api_client.get_proxies()
            rule_providers_data = await self.api_client.get_rule_providers()
            
            # 创建仅包含基本信息的状态快照
            state_snapshot = {
                "proxies": {},
                "rule_providers": {}
            }
            
            # 提取代理信息（策略组及其当前选择）
            for name, proxy in proxies_data.get("proxies", {}).items():
                if proxy.get("type") in ["Selector", "Fallback"]:
                    state_snapshot["proxies"][name] = {
                        "name": name,
                        "now": proxy.get("now")
                    }
            
            # 提取规则提供者信息（名称和更新时间）
            for name, provider in rule_providers_data.get("providers", {}).items():
                state_snapshot["rule_providers"][name] = {
                    "name": name,
                    "updatedAt": provider.get("updatedAt")
                }
            
            # 对快照进行排序以确保一致的哈希
            sorted_snapshot = json.dumps(state_snapshot, sort_keys=True, separators=(',', ':'))
            
            # 生成SHA-256哈希
            return hashlib.sha256(sorted_snapshot.encode('utf-8')).hexdigest()
            
        except Exception as e:
            self.logger.error(
                "获取状态哈希失败",
                extra={
                    "error": str(e)
                }
            )
            raise

    async def start(self):
        """启动监控循环。"""
        self.logger.info("正在启动状态监控器")
        
        while True:
            try:
                # 获取当前状态哈希
                current_state_hash = await self._get_state_hash()
                
                # 与之前的状态进行比较
                if self._last_state_hash is not None and current_state_hash != self._last_state_hash:
                    self.logger.info(
                        "检测到状态变化",
                        extra={
                            "previous_hash": self._last_state_hash,
                            "current_hash": current_state_hash
                        }
                    )
                    
                    # 取消任何现有的去抖动任务
                    if self._debounce_task and not self._debounce_task.done():
                        self._debounce_task.cancel()
                        try:
                            await self._debounce_task
                        except asyncio.CancelledError:
                            pass
                    
                    # 创建新的去抖动任务
                    self._debounce_task = asyncio.create_task(self._debounce_and_trigger())
                
                # 更新最后状态哈希
                self._last_state_hash = current_state_hash
                
                # 等待下一个轮询间隔
                await asyncio.sleep(self.polling_interval)
                
            except Exception as e:
                self.logger.error(
                    "监控循环中发生错误",
                    extra={
                        "error": str(e)
                }
            )
                # 等待后重试
                await asyncio.sleep(self.polling_interval)

    async def _debounce_and_trigger(self):
        """等待去抖动间隔，然后触发规则生成过程。"""
        try:
            await asyncio.sleep(self.debounce_interval)
            self.logger.info("去抖动期完成，正在触发规则生成")
            await self._generate_rules()
        except Exception as e:
            self.logger.error(
                "去抖动触发中发生错误",
                extra={
                    "error": str(e)
                }
            )
    
    async def _generate_rules(self):
        """使用新的两阶段方法基于Mihomo的状态生成Mosdns规则。"""
        self.logger.info("检测到状态变化，开始执行规则生成流程...")
        try:
            # 检查所需组件是否可用
            if self.orchestrator is None or self.merger is None:
                self.logger.error("Orchestrator或Merger未初始化")
                return
                
            # 阶段一：分发。调用Orchestrator生成中间文件。
            self.logger.info("阶段一：正在生成中间规则文件...")
            intermediate_path = await self.orchestrator.run()
            self.logger.info(f"中间文件成功生成于: {intermediate_path}")

            # 阶段二：合并。调用Merger生成最终文件。
            self.logger.info("阶段二：正在合并规则文件...")
            final_path = self.mosdns_config_path
            self.merger.merge_from_intermediate(intermediate_path, final_path)
            self.logger.info(f"最终规则文件成功生成于: {final_path}")

            # 阶段三：重载。通知Mosdns应用新规则。
            self.logger.info("阶段三：正在重载Mosdns服务...")
            reload_success = await self.mosdns_controller.reload()
            if reload_success:
                self.logger.info("规则生成与重载流程全部成功完成！")
            else:
                self.logger.error("规则生成完成但服务重载失败")
                    
        except Exception as e:
            self.logger.error(
                "规则生成流程失败",
                extra={
                    "error": str(e)
                },
                exc_info=True
            )