import logging
from typing import Dict, Any, List


class RuleParser:
    """Mihomo API响应数据的解析器，提取规则、代理和规则提供者信息。"""
    
    def __init__(self):
        """初始化RuleParser。"""
        self.logger = logging.getLogger(__name__)
    
    def parse_rules(self, rules_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解析来自Mihomo API的规则数据。
        
        Args:
            rules_data (dict): 来自API的规则数据。
            
        Returns:
            list: 解析后的规则列表。
        """
        try:
            rules = rules_data.get("rules", [])
            self.logger.debug(
                "解析规则数据",
                extra={
                    "rules_count": len(rules)
                }
            )
            return rules
        except Exception as e:
            self.logger.error(
                "解析规则数据失败",
                extra={
                    "error": str(e)
                }
            )
            raise
    
    def parse_proxies(self, proxies_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析来自Mihomo API的代理数据。
        
        Args:
            proxies_data (dict): 来自API的代理数据。
            
        Returns:
            dict: 解析后的代理数据。
        """
        try:
            proxies = proxies_data.get("proxies", {})
            self.logger.debug(
                "解析代理数据",
                extra={
                    "proxies_count": len(proxies)
                }
            )
            return proxies
        except Exception as e:
            self.logger.error(
                "解析代理数据失败",
                extra={
                    "error": str(e)
                }
            )
            raise
    
    def parse_rule_providers(self, rule_providers_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析来自Mihomo API的规则提供者数据。
        
        Args:
            rule_providers_data (dict): 来自API的规则提供者数据。
            
        Returns:
            dict: 解析后的规则提供者数据。
        """
        try:
            providers = rule_providers_data.get("providers", {})
            self.logger.debug(
                "解析规则提供者数据",
                extra={
                    "providers_count": len(providers)
                }
            )
            return providers
        except Exception as e:
            self.logger.error(
                "解析规则提供者数据失败",
                extra={
                    "error": str(e)
                }
            )
            raise
    
    def parse_rule_provider_info(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从配置数据中解析规则提供者信息。
        
        Args:
            config_data (dict): 来自API的配置数据。
            
        Returns:
            dict: 解析后的规则提供者信息，以提供者名称为键。
        """
        try:
            rule_providers_info = config_data.get("rule-providers", {})
            self.logger.debug(
                "从配置中解析规则提供者信息",
                extra={
                    "providers_info_count": len(rule_providers_info)
                }
            )
            return rule_providers_info
        except Exception as e:
            self.logger.error(
                "从配置中解析规则提供者信息失败",
                extra={
                    "error": str(e)
                }
            )
            raise