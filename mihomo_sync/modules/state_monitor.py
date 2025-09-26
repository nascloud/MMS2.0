import asyncio
import hashlib
import json
import logging
import tempfile
from typing import Dict, Any, Optional
from mihomo_sync.modules.rule_generation_orchestrator import RuleGenerationOrchestrator
from mihomo_sync.modules.rule_merger import RuleMerger


class StateMonitor:
    """A monitor that detects changes in Mihomo's state and triggers actions with debounce logic."""
    
    def __init__(self, api_client, mosdns_controller, mosdns_config_path: str, 
                 polling_interval: float, debounce_interval: float,
                 mihomo_config_parser=None, mihomo_config_path: str = "",
                 orchestrator: Optional[RuleGenerationOrchestrator] = None, 
                 merger: Optional[RuleMerger] = None):
        """
        Initialize the StateMonitor.
        
        Args:
            api_client: An instance of MihomoApiClient
            mosdns_controller: Controller for Mosdns service
            mosdns_config_path (str): Path to the output directory for Mosdns configuration files
            polling_interval (float): Time interval between polling in seconds
            debounce_interval (float): Time to wait before triggering action after change in seconds
            mihomo_config_parser: Parser for Mihomo local configuration files
            mihomo_config_path (str): Path to the Mihomo configuration file
            orchestrator: RuleGenerationOrchestrator instance
            merger: RuleMerger instance
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
        Get a hash digest representing the current state of Mihomo.
        
        Returns:
            str: SHA-256 hash of the current state
        """
        try:
            # Get proxies and rule providers data
            proxies_data = await self.api_client.get_proxies()
            rule_providers_data = await self.api_client.get_rule_providers()
            
            # Create a state snapshot with only the essential information
            state_snapshot = {
                "proxies": {},
                "rule_providers": {}
            }
            
            # Extract proxy information (strategy groups and their current selection)
            for name, proxy in proxies_data.get("proxies", {}).items():
                if proxy.get("type") in ["Selector", "Fallback"]:
                    state_snapshot["proxies"][name] = {
                        "name": name,
                        "now": proxy.get("now")
                    }
            
            # Extract rule provider information (name and update time)
            for name, provider in rule_providers_data.get("providers", {}).items():
                state_snapshot["rule_providers"][name] = {
                    "name": name,
                    "updatedAt": provider.get("updatedAt")
                }
            
            # Sort the snapshot to ensure consistent hashing
            sorted_snapshot = json.dumps(state_snapshot, sort_keys=True, separators=(',', ':'))
            
            # Generate SHA-256 hash
            return hashlib.sha256(sorted_snapshot.encode('utf-8')).hexdigest()
            
        except Exception as e:
            self.logger.error(
                "Failed to get state hash",
                extra={
                    "error": str(e)
                }
            )
            raise

    async def start(self):
        """Start the monitoring loop."""
        self.logger.info("Starting state monitor")
        
        while True:
            try:
                # Get current state hash
                current_state_hash = await self._get_state_hash()
                
                # Compare with previous state
                if self._last_state_hash is not None and current_state_hash != self._last_state_hash:
                    self.logger.info(
                        "State change detected",
                        extra={
                            "previous_hash": self._last_state_hash,
                            "current_hash": current_state_hash
                        }
                    )
                    
                    # Cancel any existing debounce task
                    if self._debounce_task and not self._debounce_task.done():
                        self._debounce_task.cancel()
                        try:
                            await self._debounce_task
                        except asyncio.CancelledError:
                            pass
                    
                    # Create a new debounce task
                    self._debounce_task = asyncio.create_task(self._debounce_and_trigger())
                
                # Update last state hash
                self._last_state_hash = current_state_hash
                
                # Wait for the next polling interval
                await asyncio.sleep(self.polling_interval)
                
            except Exception as e:
                self.logger.error(
                    "Error in monitoring loop",
                    extra={
                        "error": str(e)
                }
            )
                # Wait before retrying
                await asyncio.sleep(self.polling_interval)

    async def _debounce_and_trigger(self):
        """Wait for the debounce interval and then trigger the rule generation process."""
        try:
            await asyncio.sleep(self.debounce_interval)
            self.logger.info("Debounce period completed, triggering rule generation")
            await self._generate_rules()
        except Exception as e:
            self.logger.error(
                "Error in debounce trigger",
                extra={
                    "error": str(e)
                }
            )
    
    async def _generate_rules(self):
        """Generate Mosdns rules based on Mihomo's state using the new two-phase approach."""
        self.logger.info("检测到状态变化，开始执行规则生成流程...")
        try:
            # Check that required components are available
            if self.orchestrator is None or self.merger is None:
                self.logger.error("Orchestrator or Merger not initialized")
                return
                
            # 阶段一：分发。调用 Orchestrator 生成中间文件。
            self.logger.info("阶段一：正在生成中间规则文件...")
            intermediate_path = await self.orchestrator.run()
            self.logger.info(f"中间文件成功生成于: {intermediate_path}")

            # 阶段二：合并。调用 Merger 生成最终文件。
            self.logger.info("阶段二：正在合并规则文件...")
            final_path = self.mosdns_config_path
            self.merger.merge_from_intermediate(intermediate_path, final_path)
            self.logger.info(f"最终规则文件成功生成于: {final_path}")

            # 阶段三：重载。通知 Mosdns 应用新规则。
            self.logger.info("阶段三：正在重载 Mosdns 服务...")
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