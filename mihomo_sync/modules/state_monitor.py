import asyncio
import hashlib
import json
import logging
import tempfile
import time
from typing import Dict, Any, Optional
from mihomo_sync.modules.rule_generation_orchestrator import RuleGenerationOrchestrator
from mihomo_sync.modules.rule_merger import RuleMerger
from mihomo_sync.modules.policy_resolver import PolicyResolver


class StateMonitor:
    """一个监控器，用于检测Mihomo状态的变化并使用去抖动逻辑触发操作。"""
    
    def __init__(self, api_client, mosdns_controller, mosdns_rules_path: str, 
                 polling_interval: float, debounce_interval: float,
                 mihomo_config_parser=None, mihomo_config_path: str = "",
                 orchestrator: Optional[RuleGenerationOrchestrator] = None, 
                 merger: Optional[RuleMerger] = None):
        """
        初始化StateMonitor。
        
        Args:
            api_client: MihomoApiClient的实例
            mosdns_controller: Mosdns服务的控制器
            mosdns_rules_path (str): Mosdns配置文件的输出目录路径
            polling_interval (float): 轮询时间间隔（秒）
            debounce_interval (float): 变化后触发操作前的等待时间（秒）
            mihomo_config_parser: Mihomo本地配置文件的解析器
            mihomo_config_path (str): Mihomo配置文件的路径
            orchestrator: RuleGenerationOrchestrator实例
            merger: RuleMerger实例
        """
        self.api_client = api_client
        self.mosdns_controller = mosdns_controller
        self.mosdns_config_path = mosdns_rules_path
        self.polling_interval = polling_interval
        self.debounce_interval = debounce_interval
        self.mihomo_config_parser = mihomo_config_parser
        self.mihomo_config_path = mihomo_config_path
        self.orchestrator = orchestrator
        self.merger = merger
        self.logger = logging.getLogger(__name__)
        self._last_state_hash = None
        self._last_state_snapshot = None
        self._debounce_task = None
        self.policy_resolver = PolicyResolver()
        self.logger.info(
            "状态监控器初始化完成",
            extra={
                "polling_interval": polling_interval,
                "debounce_interval": debounce_interval,
                "mosdns_config_path": mosdns_rules_path
            }
        )

    async def _get_state_hash(self) -> str:
        """
        获取表示Mihomo当前状态的哈希摘要。
        
        Returns:
            str: 当前状态的SHA-256哈希
        """
        self.logger.debug("正在获取状态哈希")
        start_time = time.time()
        
        try:
            # 获取代理和规则提供者数据
            proxies_start = time.time()
            proxies_data = await self.api_client.get_proxies()
            proxies_duration = time.time() - proxies_start
            
            providers_start = time.time()
            rule_providers_data = await self.api_client.get_rule_providers()
            providers_duration = time.time() - providers_start
            
            # 创建仅包含重要信息的状态快照
            state_snapshot = {
                "proxies": {},
                "rule_providers": {}
            }
            
            # 提取代理信息（仅关注策略组的最终解析结果DIRECT/PROXY/REJECT的分类有没有变化）
            proxy_count = 0
            for name, proxy in proxies_data.get("proxies", {}).items():
                proxy_type = proxy.get("type")
                # 识别策略组类型
                is_strategy_group = self._is_strategy_group(proxy)
                
                # 如果是策略组，使用PolicyResolver解析其最终出口
                if is_strategy_group:
                    # 获取当前选择
                    now = proxy.get("now")
                    if now:
                        # 使用PolicyResolver解析最终出口
                        resolved_policy = self.policy_resolver.resolve(now, proxies_data)
                        state_snapshot["proxies"][name] = {
                            "name": name,
                            "resolved_policy": resolved_policy  # 存储解析后的标准化策略
                        }
                        proxy_count += 1
            
            # 提取规则提供者信息（仅关注name和updatedAt字段）
            provider_count = 0
            for name, provider in rule_providers_data.get("providers", {}).items():
                # 只提取关键字段，忽略可能频繁变化的字段
                state_snapshot["rule_providers"][name] = {
                    "name": name,
                    "updatedAt": provider.get("updatedAt"),
                    "vehicleType": provider.get("vehicleType")  # 添加vehicleType以区分不同类型的提供者
                }
                provider_count += 1
            
            # 对快照进行排序以确保一致的哈希
            sorted_snapshot = json.dumps(state_snapshot, sort_keys=True, separators=(',', ':'))
            
            # 生成SHA-256哈希
            hash_result = hashlib.sha256(sorted_snapshot.encode('utf-8')).hexdigest()
            
            duration = time.time() - start_time
            self.logger.debug(
                "状态哈希获取完成",
                extra={
                    "代理数量": proxy_count,
                    "提供者数量": provider_count,
                    "获取代理耗时_秒": round(proxies_duration, 3),
                    "获取提供者耗时_秒": round(providers_duration, 3),
                    "总耗时_秒": round(duration, 3),
                    "哈希值": hash_result[:16] + "..."  # 只显示部分哈希值
                }
            )
            
            # 如果这是第一次运行，保存初始状态用于比较
            if self._last_state_snapshot is None:
                self._last_state_snapshot = state_snapshot
            else:
                # 比较状态变化并记录详细信息
                self._log_state_changes(self._last_state_snapshot, state_snapshot)
                # 更新最后状态快照
                self._last_state_snapshot = state_snapshot
            
            return hash_result
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "获取状态哈希失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "耗时_秒": round(duration, 3)
                }
            )
            raise

    def _log_state_changes(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> None:
        """
        记录状态变化的详细信息。
        
        Args:
            old_state (dict): 之前的状态快照
            new_state (dict): 当前的状态快照
        """
        # 检查代理变化
        old_proxies = old_state.get("proxies", {})
        new_proxies = new_state.get("proxies", {})
        
        # 检查新增的代理
        for name, proxy in new_proxies.items():
            if name not in old_proxies:
                self.logger.debug(
                    f"检测到新增策略组: {name}",
                    extra={
                        "resolved_policy": proxy.get("resolved_policy"),
                        "type": "新增"
                    }
                )
            elif old_proxies[name] != proxy:
                self.logger.debug(
                    f"检测到策略组变化: {name}",
                    extra={
                        "old_policy": old_proxies[name].get("resolved_policy"),
                        "new_policy": proxy.get("resolved_policy"),
                        "type": "修改"
                    }
                )
        
        # 检查删除的代理
        for name in old_proxies:
            if name not in new_proxies:
                self.logger.debug(
                    f"检测到删除策略组: {name}",
                    extra={
                        "old_policy": old_proxies[name].get("resolved_policy"),
                        "type": "删除"
                    }
                )
        
        # 检查规则提供者变化
        old_providers = old_state.get("rule_providers", {})
        new_providers = new_state.get("rule_providers", {})
        
        # 检查新增的提供者
        for name, provider in new_providers.items():
            if name not in old_providers:
                self.logger.debug(
                    f"检测到新增规则提供者: {name}",
                    extra={
                        "updatedAt": provider.get("updatedAt"),
                        "vehicleType": provider.get("vehicleType"),
                        "type": "新增"
                    }
                )
            elif old_providers[name] != provider:
                old_provider = old_providers[name]
                new_provider = provider
                changes = {}
                if old_provider.get("updatedAt") != new_provider.get("updatedAt"):
                    changes["updatedAt"] = {
                        "old": old_provider.get("updatedAt"),
                        "new": new_provider.get("updatedAt")
                    }
                if old_provider.get("vehicleType") != new_provider.get("vehicleType"):
                    changes["vehicleType"] = {
                        "old": old_provider.get("vehicleType"),
                        "new": new_provider.get("vehicleType")
                    }
                
                if changes:
                    self.logger.debug(
                        f"检测到规则提供者变化: {name}",
                        extra={
                            "changes": changes,
                            "type": "修改"
                        }
                    )
        
        # 检查删除的提供者
        for name in old_providers:
            if name not in new_providers:
                old_provider = old_providers[name]
                self.logger.debug(
                    f"检测到删除规则提供者: {name}",
                    extra={
                        "old_updatedAt": old_provider.get("updatedAt"),
                        "old_vehicleType": old_provider.get("vehicleType"),
                        "type": "删除"
                    }
                )

    def _is_strategy_group(self, proxy_data: Dict[str, Any]) -> bool:
        """
        判断代理数据是否为策略组。
        
        Args:
            proxy_data (dict): 代理数据
            
        Returns:
            bool: 如果是策略组返回True，否则返回False
        """
        proxy_type = proxy_data.get("type", "").lower()
        # 策略组类型包括select, fallback, url-test, load-balance, relay等
        # 同时包括一些可能的变体如loadbalance(无连字符)
        strategy_group_types = [
            "select", "selector",  # 选择器
            "fallback",  # 自动回退
            "url-test", "urltest",  # 自动选择
            "load-balance", "loadbalance",  # 负载均衡
            "relay"  # 链式代理
        ]
        return bool(proxy_type and proxy_type in strategy_group_types)

    async def start(self):
        """启动监控循环。"""
        self.logger.info("状态监控器启动成功")
        monitor_start_time = time.time()
        cycle_count = 0
        
        while True:
            cycle_start_time = time.time()
            cycle_count += 1
            
            try:
                # 获取当前状态哈希
                current_state_hash = await self._get_state_hash()
                
                # 与之前的状态进行比较
                if self._last_state_hash is not None and current_state_hash != self._last_state_hash:
                    self.logger.info(
                        "检测到状态变化,开始更新...",
                        extra={
                            "previous_hash": self._last_state_hash[:16] + "...",
                            "current_hash": current_state_hash[:16] + "...",
                            "cycle_count": cycle_count
                        }
                    )
                    
                    # 取消任何现有的去抖动任务
                    if self._debounce_task and not self._debounce_task.done():
                        self._debounce_task.cancel()
                        try:
                            await self._debounce_task
                        except asyncio.CancelledError:
                            pass
                        self.logger.debug("已取消之前的去抖动任务")
                    
                    # 创建新的去抖动任务
                    self._debounce_task = asyncio.create_task(self._debounce_and_trigger())
                    self.logger.debug(
                        "已创建新的去抖动任务",
                        extra={
                            "debounce_interval": self.debounce_interval
                        }
                    )
                elif self._last_state_hash is None:
                    self.logger.debug("首次状态检查完成，未检测到变化")
                else:
                    # 将无变化的日志等级调至debug，避免过多的日志输出
                    self.logger.debug("状态检查完成，未检测到变化")
                
                # 更新最后状态哈希
                self._last_state_hash = current_state_hash
                
                # 记录周期信息（将无变化情况下的周期信息调整为debug级别）
                cycle_duration = time.time() - cycle_start_time
                self.logger.debug(
                    "监控周期完成",
                    extra={
                        "cycle_number": cycle_count,
                        "cycle_duration_seconds": round(cycle_duration, 3),
                        "total_duration_seconds": round(time.time() - monitor_start_time, 3)
                    }
                )
                
                # 等待下一个轮询间隔
                await asyncio.sleep(self.polling_interval)
                
            except Exception as e:
                cycle_duration = time.time() - cycle_start_time
                self.logger.error(
                    "监控循环中发生错误",
                    extra={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "cycle_duration_seconds": round(cycle_duration, 3)
                    }
                )
                # 等待后重试
                await asyncio.sleep(self.polling_interval)

    async def _debounce_and_trigger(self):
        """等待去抖动间隔，然后触发规则生成过程。"""
        self.logger.debug(
            "开始去抖动等待",
            extra={
                "debounce_interval": self.debounce_interval
            }
        )
        
        try:
            debounce_start_time = time.time()
            await asyncio.sleep(self.debounce_interval)
            debounce_duration = time.time() - debounce_start_time
            
            self.logger.info(
                "去抖动期完成，正在触发规则生成",
                extra={
                    "等待时间_秒": round(debounce_duration, 3)
                }
            )
            await self._generate_rules()
        except asyncio.CancelledError:
            self.logger.debug("去抖动任务被取消")
            raise
        except Exception as e:
            self.logger.error(
                "去抖动触发中发生错误",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
    
    async def _generate_rules(self):
        """使用新的两阶段方法基于Mihomo的状态生成Mosdns规则。"""
        self.logger.info("检测到状态变化，开始执行规则生成流程...")
        generation_start_time = time.time()
        
        try:
            # 检查所需组件是否可用
            if self.orchestrator is None or self.merger is None:
                self.logger.error("Orchestrator或Merger未初始化")
                return
                
            # 阶段一：分发。调用Orchestrator生成中间文件。
            self.logger.debug("阶段一：正在生成中间规则文件...")
            intermediate_start_time = time.time()
            intermediate_path = await self.orchestrator.run()
            intermediate_duration = time.time() - intermediate_start_time
            
            self.logger.debug(
                f"中间文件成功生成于: {intermediate_path}",
                extra={
                    "阶段一耗时_秒": round(intermediate_duration, 3)
                }
            )

            # 阶段二：合并。调用Merger生成最终文件。
            self.logger.debug("阶段二：正在合并规则文件...")
            merge_start_time = time.time()
            final_path = self.mosdns_config_path
            self.merger.merge_from_intermediate(intermediate_path, final_path)
            merge_duration = time.time() - merge_start_time
            
            self.logger.debug(
                f"最终规则文件成功生成于: {final_path}",
                extra={
                    "阶段二耗时_秒": round(merge_duration, 3)
                }
            )

            # 阶段三：重载。通知Mosdns应用新规则。
            self.logger.info("正在重新加载Mosdns服务...")
            reload_start_time = time.time()
            reload_success = await self.mosdns_controller.reload()
            reload_duration = time.time() - reload_start_time
            
            total_duration = time.time() - generation_start_time
            
            # 添加文件更新确认日志
            self.logger.info(
                "DNS规则文件更新完成",
                extra={
                    "output_directory": final_path,
                    "更新时间": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "总耗时_秒": round(total_duration, 3)
                }
            )

            if reload_success:
                self.logger.info(
                    f"DNS规则同步流程已成功完成，耗时 {round(total_duration, 3)} 秒！",
                    extra={
                        "总耗时_秒": round(total_duration, 3),
                        "reload_success": reload_success
                    }
                )
            else:
                self.logger.error(
                    "规则生成完成但服务重载失败",
                    extra={
                        "总耗时_秒": round(total_duration, 3)
                    }
                )
                    
        except Exception as e:
            total_duration = time.time() - generation_start_time
            self.logger.error(
                "规则生成流程失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "总耗时_秒": round(total_duration, 3)
                },
                exc_info=True
            )