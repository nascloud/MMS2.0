import asyncio
import hashlib
import json
import logging
import tempfile
from typing import Dict, Any, Optional


class StateMonitor:
    """A monitor that detects changes in Mihomo's state and triggers actions with debounce logic."""
    
    def __init__(self, api_client, mosdns_controller, mosdns_config_path: str, 
                 polling_interval: float, debounce_interval: float,
                 mihomo_config_parser=None, mihomo_config_path: str = ""):
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
        """
        self.api_client = api_client
        self.mosdns_controller = mosdns_controller
        self.mosdns_config_path = mosdns_config_path
        self.polling_interval = polling_interval
        self.debounce_interval = debounce_interval
        self.mihomo_config_parser = mihomo_config_parser
        self.mihomo_config_path = mihomo_config_path
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
        """Generate Mosdns rules based on Mihomo's state."""
        try:
            self.logger.info("Starting rule generation process")
            
            # Create temporary directory for intermediate files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Get all required data from Mihomo API
                rules_data = await self.api_client.get_rules()
                proxies_data = await self.api_client.get_proxies()
                rule_providers_data = await self.api_client.get_rule_providers()
                config_data = await self.api_client.get_config()
                
                # Parse Mihomo local configuration file if available
                mihomo_local_config = None
                if self.mihomo_config_parser and self.mihomo_config_path:
                    mihomo_local_config = self.mihomo_config_parser.parse_config_file(self.mihomo_config_path)
                
                # Extract rule provider information from local config if available
                mihomo_rule_provider_info = {}
                if mihomo_local_config and self.mihomo_config_parser:
                    mihomo_rule_provider_info = self.mihomo_config_parser.extract_rule_providers(mihomo_local_config)
                
                # Initialize modules
                from mihomo_sync.modules.policy_resolver import PolicyResolver
                from mihomo_sync.modules.rule_parser import RuleParser
                from mihomo_sync.modules.rule_converter import RuleConverter
                from mihomo_sync.modules.rule_merger import RuleMerger
                
                policy_resolver = PolicyResolver()
                rule_parser = RuleParser()
                rule_converter = RuleConverter()
                rule_merger = RuleMerger()
                
                # Parse data using RuleParser
                parsed_rules = rule_parser.parse_rules(rules_data)
                parsed_proxies = rule_parser.parse_proxies(proxies_data)
                parsed_rule_providers = rule_parser.parse_rule_providers(rule_providers_data)
                
                # Use rule provider info from local config if available, otherwise from API config
                parsed_provider_info = mihomo_rule_provider_info if mihomo_rule_provider_info else rule_parser.parse_rule_provider_info(config_data)
                
                # Process each rule using RuleConverter
                for rule in parsed_rules:
                    # Extract rule components
                    rule_type = rule.get("type", "")
                    rule_target = rule.get("proxy") or rule.get("provider")
                    
                    # Skip rules without a target
                    if not rule_target:
                        continue
                        
                    # Resolve the final target using PolicyResolver
                    final_target = policy_resolver.resolve(rule_target, proxies_data)
                    
                    # Convert and save rule using RuleConverter
                    rule_converter.convert_and_save(rule, final_target, temp_dir, parsed_provider_info)
                
                # Merge all rules using RuleMerger
                rule_merger.merge_all_rules(temp_dir, self.mosdns_config_path)
                
                self.logger.info(
                    "Rules generated and written to files successfully",
                    extra={
                        "output_dir": self.mosdns_config_path
                    }
                )
                
                # Reload Mosdns service
                reload_success = await self.mosdns_controller.reload()
                
                if reload_success:
                    self.logger.info("Rule generation and service reload completed successfully")
                else:
                    self.logger.error("Rule generation completed but service reload failed")
                    
        except Exception as e:
            self.logger.error(
                "Error in rule generation process",
                extra={
                    "error": str(e)
                }
            )
            raise