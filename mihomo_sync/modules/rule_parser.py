import logging
from typing import Dict, Any, List


class RuleParser:
    """Parser for Mihomo API response data, extracting rules, proxies, and rule providers information."""
    
    def __init__(self):
        """Initialize the RuleParser."""
        self.logger = logging.getLogger(__name__)
    
    def parse_rules(self, rules_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse rules data from Mihomo API.
        
        Args:
            rules_data (dict): Rules data from the API.
            
        Returns:
            list: List of parsed rules.
        """
        try:
            rules = rules_data.get("rules", [])
            self.logger.debug(
                "Parsed rules data",
                extra={
                    "rules_count": len(rules)
                }
            )
            return rules
        except Exception as e:
            self.logger.error(
                "Failed to parse rules data",
                extra={
                    "error": str(e)
                }
            )
            raise
    
    def parse_proxies(self, proxies_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse proxies data from Mihomo API.
        
        Args:
            proxies_data (dict): Proxies data from the API.
            
        Returns:
            dict: Parsed proxies data.
        """
        try:
            proxies = proxies_data.get("proxies", {})
            self.logger.debug(
                "Parsed proxies data",
                extra={
                    "proxies_count": len(proxies)
                }
            )
            return proxies
        except Exception as e:
            self.logger.error(
                "Failed to parse proxies data",
                extra={
                    "error": str(e)
                }
            )
            raise
    
    def parse_rule_providers(self, rule_providers_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse rule providers data from Mihomo API.
        
        Args:
            rule_providers_data (dict): Rule providers data from the API.
            
        Returns:
            dict: Parsed rule providers data.
        """
        try:
            providers = rule_providers_data.get("providers", {})
            self.logger.debug(
                "Parsed rule providers data",
                extra={
                    "providers_count": len(providers)
                }
            )
            return providers
        except Exception as e:
            self.logger.error(
                "Failed to parse rule providers data",
                extra={
                    "error": str(e)
                }
            )
            raise
    
    def parse_rule_provider_info(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse rule provider information from config data.
        
        Args:
            config_data (dict): Configuration data from the API.
            
        Returns:
            dict: Parsed rule provider information with provider name as key.
        """
        try:
            rule_providers_info = config_data.get("rule-providers", {})
            self.logger.debug(
                "Parsed rule provider info from config",
                extra={
                    "providers_info_count": len(rule_providers_info)
                }
            )
            return rule_providers_info
        except Exception as e:
            self.logger.error(
                "Failed to parse rule provider info from config",
                extra={
                    "error": str(e)
                }
            )
            raise