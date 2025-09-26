#!/usr/bin/env python3
"""
Debug script to test rule generation process.
"""
import asyncio
import logging
import os
import tempfile
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mihomo_sync.logger import setup_logger
from mihomo_sync.config import ConfigManager
from mihomo_sync.modules.api_client import MihomoApiClient
from mihomo_sync.modules.mihomo_config_parser import MihomoConfigParser
from mihomo_sync.modules.policy_resolver import PolicyResolver
from mihomo_sync.modules.rule_parser import RuleParser
from mihomo_sync.modules.rule_converter import RuleConverter
from mihomo_sync.modules.rule_merger import RuleMerger


async def debug_rule_generation():
    """Debug the rule generation process."""
    # Set up logging
    setup_logger("DEBUG")
    logger = logging.getLogger(__name__)
    
    # Also log to console for immediate feedback
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    
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
        
        mihomo_config_parser = MihomoConfigParser()
        
        # Initialize modules
        policy_resolver = PolicyResolver()
        rule_parser = RuleParser()
        rule_converter = RuleConverter()
        rule_merger = RuleMerger()
        
        # Create temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info(f"Using temporary directory: {temp_dir}")
            
            # Get all required data from Mihomo API
            rules_data = await api_client.get_rules()
            proxies_data = await api_client.get_proxies()
            rule_providers_data = await api_client.get_rule_providers()
            config_data = await api_client.get_config()
            
            # Parse Mihomo local configuration file if available
            mihomo_local_config = None
            mihomo_config_path = config_manager.get_mihomo_config_path()
            if mihomo_config_parser and mihomo_config_path:
                mihomo_local_config = mihomo_config_parser.parse_config_file(mihomo_config_path)
            
            # Extract rule provider information from local config if available
            mihomo_rule_provider_info = {}
            if mihomo_local_config and mihomo_config_parser:
                mihomo_rule_provider_info = mihomo_config_parser.extract_rule_providers(mihomo_local_config)
            
            # Parse data using RuleParser
            parsed_rules = rule_parser.parse_rules(rules_data)
            parsed_proxies = rule_parser.parse_proxies(proxies_data)
            parsed_rule_providers = rule_parser.parse_rule_providers(rule_providers_data)
            
            # Use rule provider info from local config if available, otherwise from API config
            parsed_provider_info = mihomo_rule_provider_info if mihomo_rule_provider_info else rule_parser.parse_rule_provider_info(config_data)
            
            logger.info(f"Parsed {len(parsed_rules)} rules")
            logger.info(f"Parsed {len(parsed_proxies)} proxies")
            logger.info(f"Parsed {len(parsed_rule_providers)} rule providers")
            logger.info(f"Parsed provider info: {len(parsed_provider_info)} entries")
            logger.info(f"Parsed provider info keys: {list(parsed_provider_info.keys())}")
            logger.info(f"Local config provider info keys: {list(mihomo_rule_provider_info.keys()) if mihomo_rule_provider_info else 'None'}")
            
            # Process each rule using RuleConverter
            converted_rules_count = 0
            for i, rule in enumerate(parsed_rules):
                # Extract rule components
                rule_type = rule.get("type", "")
                rule_target = rule.get("proxy") or rule.get("provider")
                
                logger.debug(f"Processing rule {i}: type={rule_type}, target={rule_target}")
                
                # Skip rules without a target
                if not rule_target:
                    logger.debug(f"Skipping rule {i} - no target")
                    continue
                    
                # Resolve the final target using PolicyResolver
                final_target = policy_resolver.resolve(rule_target, proxies_data)
                logger.debug(f"Rule {i} final target: {final_target}")
                
                # Convert and save rule using RuleConverter
                try:
                    # Add more debugging for RuleSet rules
                    if rule_type.upper() == "RULE-SET":
                        rule_payload = rule.get("payload", "")
                        logger.debug(f"RuleSet rule {i}: payload={rule_payload}")
                        if rule_payload in parsed_provider_info:
                            logger.debug(f"RuleSet rule {i}: found provider info")
                        else:
                            logger.warning(f"RuleSet rule {i}: provider info not found")
                            logger.warning(f"Available providers: {list(parsed_provider_info.keys())}")
                    
                    rule_converter.convert_and_save(rule, final_target, temp_dir, parsed_provider_info)
                    converted_rules_count += 1
                    logger.debug(f"Converted rule {i}")
                except Exception as e:
                    logger.error(f"Failed to convert rule {i}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
            
            logger.info(f"Converted {converted_rules_count} rules")
            
            # Check what was created in temp directory
            logger.info("Checking temporary directory structure:")
            for root, dirs, files in os.walk(temp_dir):
                level = root.replace(temp_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                logger.info(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    logger.info(f"{subindent}{file}")
                    # Show content of some files for debugging
                    if file.endswith('.txt'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read().strip()
                                logger.info(f"{subindent}  Content: '{content}'")
                        except Exception as e:
                            logger.error(f"{subindent}  Failed to read file: {e}")
            
            # Merge all rules using RuleMerger
            output_dir = config_manager.get_mosdns_config_path()
            logger.info(f"Merging rules to output directory: {output_dir}")
            rule_merger.merge_all_rules(temp_dir, output_dir)
            
            # Check output directory
            logger.info("Checking output directory:")
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    filepath = os.path.join(output_dir, file)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        logger.info(f"  {file} ({size} bytes)")
                        if size > 0:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read().strip()
                                logger.info(f"    First 200 chars: '{content[:200]}'")
            
            # Close API client
            await api_client.close()
            
    except Exception as e:
        logger.exception(f"Error in debug script: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(debug_rule_generation())