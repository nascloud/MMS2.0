#!/usr/bin/env python3
"""
Script to check the actual format of rules returned by the API.
"""
import asyncio
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mihomo_sync.logger import setup_logger
from mihomo_sync.config import ConfigManager
from mihomo_sync.modules.api_client import MihomoApiClient


async def check_rules_format():
    """Check the format of rules returned by the API."""
    # Set up logging
    setup_logger("DEBUG")
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config_manager = ConfigManager("config/config.yaml")
        
        # Initialize components
        api_client = MihomoApiClient(
            api_base_url=config_manager.get_mihomo_api_url(),
            timeout=config_manager.get_mihomo_api_timeout(),
            retry_config=config_manager.get_api_retry_config(),
            api_secret=config_manager.get_mihomo_api_secret()
        )
        
        # Get rules data from Mihomo API
        rules_data = await api_client.get_rules()
        rules = rules_data.get("rules", [])
        
        logger.info(f"Total rules: {len(rules)}")
        
        # Check for RuleSet rules
        ruleset_rules = []
        for i, rule in enumerate(rules):
            rule_type = rule.get("type", "")
            rule_payload = rule.get("payload", "")
            rule_proxy = rule.get("proxy", "")
            rule_provider = rule.get("provider", "")
            
            logger.info(f"Rule {i}: type={rule_type}, payload={rule_payload}, proxy={rule_proxy}, provider={rule_provider}")
            
            if "ruleset" in rule_type.lower() or "rule-set" in rule_type.lower():
                ruleset_rules.append((i, rule))
        
        logger.info(f"Found {len(ruleset_rules)} potential RuleSet rules")
        
        for i, rule in ruleset_rules:
            logger.info(f"RuleSet rule {i}: {rule}")
        
        # Close API client
        await api_client.close()
        
    except Exception as e:
        logger.exception(f"Error in check script: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(check_rules_format())