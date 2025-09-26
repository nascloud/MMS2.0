import logging
import os
import shutil
from typing import Dict, Any, List, Set, Tuple
from mihomo_sync.modules.rule_converter import RuleConverter
from mihomo_sync.modules.policy_resolver import PolicyResolver


class RuleGenerationOrchestrator:
    """Orchestrator for the dispatch phase of rule generation."""
    
    # 定义固定的策略名称
    FIXED_POLICIES = ["DIRECT", "PROXY", "REJECT"]
    
    def __init__(self, api_client, config):
        """
        Initialize the RuleGenerationOrchestrator.
        
        Args:
            api_client: An instance of MihomoApiClient
            config: ConfigManager instance
        """
        self.api_client = api_client
        self.config = config
        self.intermediate_dir = self.config.get_mosdns_config_path() + "_intermediate"
        self.logger = logging.getLogger(__name__)
        self.policy_resolver = PolicyResolver()
    
    async def run(self) -> str:
        """
        Execute the complete dispatch phase workflow.
        
        Returns:
            str: Path to the generated intermediate directory
        """
        self.logger.info("Starting rule generation orchestration...")
        
        # Step 1: Prepare workspace
        self._prepare_workspace()
        
        # Step 2: Fetch data from API
        rules_data = await self.api_client.get_rules()
        rule_providers_data = await self.api_client.get_rule_providers()
        proxies_data = await self.api_client.get_proxies()
        
        # Step 3: Initialize memory aggregator
        # 初始化固定策略的聚合器
        aggregated_rules = {policy: {} for policy in self.FIXED_POLICIES}
        
        # Step 4: Process rules
        await self._process_rules(rules_data, rule_providers_data, proxies_data, aggregated_rules)
        
        # Step 5: Write intermediate files
        self._write_intermediate_files(aggregated_rules)
        
        self.logger.info(f"Intermediate files successfully generated at: {self.intermediate_dir}")
        return self.intermediate_dir
    
    def _prepare_workspace(self) -> None:
        """Prepare the workspace by cleaning and creating the intermediate directory."""
        if os.path.exists(self.intermediate_dir):
            shutil.rmtree(self.intermediate_dir)
        os.makedirs(self.intermediate_dir)
        self.logger.debug(f"Cleaned and created intermediate directory: {self.intermediate_dir}")
    
    async def _process_rules(self, rules_data: Dict[str, Any], rule_providers_data: Dict[str, Any], 
                             proxies_data: Dict[str, Any],
                             aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        Process all rules and aggregate them in memory.
        
        Args:
            rules_data: Rules data from Mihomo API
            rule_providers_data: Rule providers data from Mihomo API
            proxies_data: Proxies data from Mihomo API
            aggregated_rules: Memory aggregator for rules with fixed policies
        """
        # Extract rule providers info
        providers_info = rule_providers_data.get("providers", {})
        
        # Process each rule
        for rule in rules_data.get("rules", []):
            rule_type = rule.get("type", "")
            
            if rule_type == "RULE-SET":
                # Process RULE-SET type rules
                await self._process_rule_set_rule(rule, providers_info, proxies_data, aggregated_rules)
            else:
                # Process single rules
                self._process_single_rule(rule, proxies_data, aggregated_rules)
    
    async def _process_rule_set_rule(self, rule: Dict[str, Any], providers_info: Dict[str, Any],
                                     proxies_data: Dict[str, Any],
                                     aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        Process a RULE-SET type rule.
        
        Args:
            rule: The RULE-SET rule to process
            providers_info: Information about all rule providers
            proxies_data: Proxies data from Mihomo API
            aggregated_rules: Memory aggregator for rules with fixed policies
        """
        try:
            policy = rule.get("proxy") or rule.get("provider", "")
            provider_name = rule.get("payload", "")
            
            # Skip if no policy or provider name
            if not policy or not provider_name:
                self.logger.warning(f"Skipping RULE-SET rule with missing policy or provider: {rule}")
                return
            
            # Resolve the final policy using PolicyResolver
            resolved_policy = self.policy_resolver.resolve(policy, proxies_data)
            
            # Only process rules with fixed policies
            if resolved_policy not in self.FIXED_POLICIES:
                self.logger.debug(f"Skipping RULE-SET rule with non-fixed policy: {resolved_policy}")
                return
            
            # Find provider info
            if provider_name not in providers_info:
                self.logger.warning(f"Provider '{provider_name}' not found in provider info")
                return
                
            provider_info = providers_info[provider_name]
            
            # Fetch and parse ruleset content
            content_list = RuleConverter.fetch_and_parse_ruleset(provider_info)
            
            # Determine content type based on provider behavior
            behavior = provider_info.get("behavior", "domain")
            content_type = "domain" if behavior == "domain" else "ipcidr" if behavior == "ipcidr" else "domain"
            
            # Add to aggregator
            aggregated_rules.setdefault(resolved_policy, {}).setdefault(content_type, {}).setdefault(provider_name, set()).update(content_list)
            
            self.logger.debug(f"Processed RULE-SET rule: {provider_name} -> {len(content_list)} rules for policy {resolved_policy}")
        except Exception as e:
            self.logger.error(f"Error processing RULE-SET rule: {e}", exc_info=True)
    
    def _process_single_rule(self, rule: Dict[str, Any], proxies_data: Dict[str, Any],
                             aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        Process a single rule (not RULE-SET).
        
        Args:
            rule: The single rule to process
            proxies_data: Proxies data from Mihomo API
            aggregated_rules: Memory aggregator for rules with fixed policies
        """
        try:
            policy = rule.get("proxy") or rule.get("provider", "")
            
            # Skip if no policy
            if not policy:
                self.logger.warning(f"Skipping single rule with missing policy: {rule}")
                return
            
            # Resolve the final policy using PolicyResolver
            resolved_policy = self.policy_resolver.resolve(policy, proxies_data)
            
            # Only process rules with fixed policies
            if resolved_policy not in self.FIXED_POLICIES:
                self.logger.debug(f"Skipping single rule with non-fixed policy: {resolved_policy}")
                return
            
            # Convert single rule
            mosdns_rule, content_type = RuleConverter.convert_single_rule(rule)
            
            # Skip if conversion failed
            if mosdns_rule is None or content_type is None:
                self.logger.debug(f"Skipping unsupported rule: {rule}")
                return
            
            # Add to aggregator with special _inline provider name
            aggregated_rules.setdefault(resolved_policy, {}).setdefault(content_type, {}).setdefault("_inline", set()).add(mosdns_rule)
            
            self.logger.debug(f"Processed single rule: {rule} -> {mosdns_rule} for policy {resolved_policy}")
        except Exception as e:
            self.logger.error(f"Error processing single rule: {e}", exc_info=True)
    
    def _write_intermediate_files(self, aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        Write aggregated rules to intermediate files.
        
        Args:
            aggregated_rules: Memory aggregator containing all rules
        """
        # 确保固定策略文件夹都存在，即使没有规则
        for policy in self.FIXED_POLICIES:
            if policy not in aggregated_rules:
                aggregated_rules[policy] = {}
        
        for policy, types in aggregated_rules.items():
            # 只处理固定策略
            if policy not in self.FIXED_POLICIES:
                continue
                
            for content_type, providers in types.items():
                for provider_name, rule_set in providers.items():
                    # Skip empty rule sets
                    if not rule_set:
                        continue
                    
                    # Create target directory
                    target_dir = os.path.join(self.intermediate_dir, policy, content_type)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Determine filename
                    filename = f"provider_{provider_name}.list" if provider_name != "_inline" else "_inline_rules.list"
                    filepath = os.path.join(target_dir, filename)
                    
                    # Write rules to file
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(sorted(list(rule_set))))
                        self.logger.debug(f"Wrote {len(rule_set)} rules to {filepath}")
                    except Exception as e:
                        self.logger.error(f"Failed to write intermediate file {filepath}: {e}")