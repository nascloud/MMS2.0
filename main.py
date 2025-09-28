#!/usr/bin/env python3
"""
Mihomo-Mosdns同步服务的主入口点。
"""
import asyncio
import logging
import os
import signal
import sys
import time
import httpx
from typing import Optional
from mihomo_sync.logger import setup_logger
from mihomo_sync.config import ConfigManager
from mihomo_sync.modules.api_client import MihomoApiClient
from mihomo_sync.modules.mosdns_controller import MosdnsServiceController
from mihomo_sync.modules.state_monitor import StateMonitor
from mihomo_sync.modules.mihomo_config_parser import MihomoConfigParser
from mihomo_sync.modules.rule_generation_orchestrator import RuleGenerationOrchestrator
from mihomo_sync.modules.rule_merger import RuleMerger
from mihomo_sync.modules.rule_downloader import RuleDownloader


class MihomoMosdnsSyncService:
    """Mihomo-Mosdns同步的主服务类。"""
    
    def __init__(self):
        """初始化服务。"""
        self.logger = logging.getLogger(__name__)
        self.config_manager: Optional[ConfigManager] = None
        self.mihomo_config_parser: Optional[MihomoConfigParser] = None
        self.api_client: Optional[MihomoApiClient] = None
        self.mosdns_controller: Optional[MosdnsServiceController] = None
        self.state_monitor: Optional[StateMonitor] = None
        self.rule_orchestrator: Optional[RuleGenerationOrchestrator] = None
        self.rule_merger: Optional[RuleMerger] = None
        # 注意：RuleDownloader现在由RuleGenerationOrchestrator内部管理
        self.shutdown_event = asyncio.Event()
        self.start_time = None

    async def initialize(self, httpx_client=None):
        """初始化服务的所有组件。"""
        self.logger.info("正在初始化Mihomo-Mosdns同步服务")
        self.start_time = time.time()
        
        try:
            # 加载配置
            config_path = os.environ.get('CONFIG_PATH', 'config/config.yaml')
            self.config_manager = ConfigManager(config_path)
            
            # 使用配置的级别设置记录器
            log_file_path = self.config_manager.get_log_file_path()
            setup_logger(self.config_manager.get_log_level(), log_file_path if log_file_path else None)
            
            # 在setup_logger调用后重新初始化记录器
            self.logger = logging.getLogger(__name__)
            
            self.logger.info(
                "配置加载完成",
                extra={
                    "config_path": config_path,
                    "log_level": self.config_manager.get_log_level()
                }
            )
            
            # 初始化Mihomo配置解析器
            self.mihomo_config_parser = MihomoConfigParser()
            
            # 初始化API客户端
            self.api_client = MihomoApiClient(
                api_base_url=self.config_manager.get_mihomo_api_url(),
                timeout=self.config_manager.get_mihomo_api_timeout(),
                retry_config=self.config_manager.get_api_retry_config(),
                api_secret=self.config_manager.get_mihomo_api_secret()
            )
            
            self.logger.debug(
                "API客户端初始化完成",
                extra={
                    "api_url": self.config_manager.get_mihomo_api_url(),
                    "timeout": self.config_manager.get_mihomo_api_timeout()
                }
            )
            
            # 初始化Mosdns控制器
            self.mosdns_controller = MosdnsServiceController(
                reload_command=self.config_manager.get_mosdns_reload_command()
            )
            
            self.logger.debug(
                "Mosdns控制器初始化完成",
                extra={
                    "reload_command": self.config_manager.get_mosdns_reload_command()
                }
            )
            
            # 初始化新的规则处理组件
            self.rule_merger = RuleMerger()
            # 现在RuleDownloader由RuleGenerationOrchestrator内部管理，不需要单独初始化
            self.rule_orchestrator = RuleGenerationOrchestrator(
                api_client=self.api_client,
                config=self.config_manager,
                mihomo_config_parser=self.mihomo_config_parser,
                mihomo_config_path=self.config_manager.get_mihomo_config_path()
            )
            
            self.logger.debug("规则处理组件初始化完成")
            
            # 使用新组件初始化状态监控器
            self.state_monitor = StateMonitor(
                api_client=self.api_client,
                mosdns_controller=self.mosdns_controller,
                mosdns_config_path=self.config_manager.get_mosdns_config_path(),
                polling_interval=self.config_manager.get_polling_interval(),
                debounce_interval=self.config_manager.get_debounce_interval(),
                mihomo_config_parser=self.mihomo_config_parser,
                mihomo_config_path=self.config_manager.get_mihomo_config_path(),
                orchestrator=self.rule_orchestrator,
                merger=self.rule_merger
            )
            
            self.logger.debug(
                "状态监控器初始化完成",
                extra={
                    "polling_interval": self.config_manager.get_polling_interval(),
                    "debounce_interval": self.config_manager.get_debounce_interval()
                }
            )
            
            init_duration = time.time() - self.start_time
            self.logger.info(
                "服务初始化完成",
                extra={
                    "初始化耗时_秒": round(init_duration, 3)
                }
            )
        except Exception as e:
            self.logger.exception(
                "服务初始化期间发生错误",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            )
            raise

    async def health_check(self):
        """
        在启动服务之前执行健康检查。
        
        Returns:
            bool: 如果所有健康检查通过返回True，否则返回False
        """
        self.logger.info("正在执行健康检查")
        health_start_time = time.time()
        
        # 检查Mihomo API连接性
        if self.api_client is None:
            self.logger.critical("API客户端未初始化")
            return False
            
        try:
            is_connected = await self.api_client.check_connectivity()
            if not is_connected:
                self.logger.critical(
                    "健康检查失败：无法连接到Mihomo API",
                    extra={
                        "api_url": self.config_manager.get_mihomo_api_url() if self.config_manager else "未知"
                    }
                )
                return False
            self.logger.info("Mihomo API连接性检查通过")
        except Exception as e:
            self.logger.critical(
                "健康检查失败：API连接性检查期间发生异常",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            return False
        
        # 检查Mosdns配置目录是否可写
        if self.config_manager is None:
            self.logger.critical("配置管理器未初始化")
            return False
            
        config_dir = self.config_manager.get_mosdns_config_path()
        
        if not os.path.exists(config_dir):
            self.logger.critical(
                "健康检查失败：Mosdns配置目录不存在",
                extra={
                    "config_dir": config_dir
                }
            )
            return False
            
        if not os.access(config_dir, os.W_OK):
            self.logger.critical(
                "健康检查失败：Mosdns配置目录不可写",
                extra={
                    "config_dir": config_dir
                }
            )
            return False
            
        self.logger.info(
            "Mosdns配置目录检查通过",
            extra={
                "config_dir": config_dir
            }
        )
        
        # 检查Mihomo配置文件（如果指定了）
        mihomo_config_path = self.config_manager.get_mihomo_config_path()
        if mihomo_config_path:
            if not os.path.exists(mihomo_config_path):
                self.logger.warning(
                    "Mihomo配置文件不存在（这可能不是问题，如果完全依赖API）",
                    extra={
                        "config_path": mihomo_config_path
                    }
                )
            else:
                self.logger.info(
                    "Mihomo配置文件检查通过",
                    extra={
                        "config_path": mihomo_config_path
                    }
                )
        
        health_duration = time.time() - health_start_time
        self.logger.info(
            "健康检查完成",
            extra={
                "检查耗时_秒": round(health_duration, 3),
                "结果": "通过"
            }
        )
        
        return True

    async def start(self, httpx_client=None):
        """启动同步服务。"""
        start_time = time.time()
        self.logger.info("正在启动同步服务")
        
        try:
            # 初始化服务
            await self.initialize(httpx_client)
            
            # 执行健康检查
            if not await self.health_check():
                self.logger.critical("健康检查失败。退出。")
                return 1
            
            # 为优雅关闭设置信号处理程序（仅在类Unix系统上）
            if os.name != 'nt':  # 非Windows系统
                loop = asyncio.get_running_loop()
                for sig in (signal.SIGTERM, signal.SIGINT):
                    loop.add_signal_handler(sig, self._signal_handler, sig)
            
            # 检查所需组件是否已初始化
            if self.state_monitor is None:
                self.logger.critical("所需组件未初始化")
                return 1
                
            # 执行初始规则生成以确保Mosdns有配置
            self.logger.info("正在执行初始规则生成")
            # 创建一个临时方法来调用内部规则生成
            await self.state_monitor._generate_rules()
            
            # 启动状态监控器
            self.logger.info("正在启动状态监控器")
            await self.state_monitor.start()
            
        except Exception as e:
            self.logger.critical(
                "主服务中未处理的异常",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
            return 1
        finally:
            await self.cleanup()
            total_duration = time.time() - start_time
            self.logger.info(
                "服务运行结束",
                extra={
                    "总运行时间_秒": round(total_duration, 3)
                }
            )
        
        return 0

    def _signal_handler(self, signum):
        """
        处理关闭信号。
        
        Args:
            signum: 信号编号
        """
        signame = signal.Signals(signum).name
        self.logger.info(
            f"收到信号 {signame}，正在启动关闭程序",
            extra={
                "信号": signame,
                "信号编号": signum
            }
        )
        self.shutdown_event.set()

    async def cleanup(self):
        """清理资源。"""
        self.logger.info("正在清理资源")
        cleanup_start_time = time.time()
        
        # 关闭API客户端
        if self.api_client:
            await self.api_client.close()
            self.logger.debug("API客户端已关闭")
        
        cleanup_duration = time.time() - cleanup_start_time
        self.logger.info(
            "清理完成",
            extra={
                "清理耗时_秒": round(cleanup_duration, 3)
            }
        )


async def main():
    """主异步函数。"""
    async with httpx.AsyncClient() as client:
        service = MihomoMosdnsSyncService()
        exit_code = await service.start(client)
        return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)