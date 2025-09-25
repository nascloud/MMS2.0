import yaml
import os
import logging
from typing import Dict, Any, Optional


class MihomoConfigParser:
    """Parser for Mihomo local configuration files."""
    
    def __init__(self):
        """Initialize the MihomoConfigParser."""
        self.logger = logging.getLogger(__name__)
    
    def parse_config_file(self, config_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse Mihomo configuration file.
        
        Args:
            config_path (str): Path to the Mihomo configuration file.
            
        Returns:
            dict: Parsed configuration data, or None if parsing failed.
        """
        if not config_path or not os.path.exists(config_path):
            self.logger.warning(
                "Mihomo configuration file not found or path not specified",
                extra={"config_path": config_path}
            )
            return None
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            self.logger.info(
                "Successfully parsed Mihomo configuration file",
                extra={"config_path": config_path}
            )
            
            return config_data
        except Exception as e:
            self.logger.error(
                "Failed to parse Mihomo configuration file",
                extra={
                    "config_path": config_path,
                    "error": str(e)
                }
            )
            return None
    
    def extract_rule_providers(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract rule providers information from parsed configuration.
        
        Args:
            config_data (dict): Parsed Mihomo configuration data.
            
        Returns:
            dict: Rule providers information with provider name as key.
        """
        if not config_data or not isinstance(config_data, dict):
            return {}
            
        rule_providers = config_data.get('rule-providers', {})
        
        self.logger.debug(
            "Extracted rule providers from configuration",
            extra={"providers_count": len(rule_providers)}
        )
        
        return rule_providers