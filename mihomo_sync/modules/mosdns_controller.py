import asyncio
import logging
import os
from typing import Dict, Any


class MosdnsServiceController:
    """Controller for managing the Mosdns service."""
    
    def __init__(self, reload_command: str):
        """
        Initialize the MosdnsServiceController.
        
        Args:
            reload_command (str): Command to reload the Mosdns service
        """
        self.reload_command = reload_command
        self.logger = logging.getLogger(__name__)

    async def reload(self) -> bool:
        """
        Reload the Mosdns service.
        
        Returns:
            bool: True if reload was successful, False otherwise
        """
        try:
            self.logger.info("Reloading Mosdns service")
            
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                self.reload_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for the process to complete
            stdout, stderr = await process.communicate()
            
            # Check return code
            if process.returncode == 0:
                self.logger.info(
                    "Mosdns service reloaded successfully",
                    extra={
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else ""
                    }
                )
                return True
            else:
                self.logger.error(
                    "Failed to reload Mosdns service",
                    extra={
                        "command": self.reload_command,
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else "",
                        "stderr": stderr.decode().strip() if stderr else ""
                    }
                )
                return False
                
        except Exception as e:
            self.logger.error(
                "Exception occurred while reloading Mosdns service",
                extra={
                    "command": self.reload_command,
                    "error": str(e)
                }
            )
            return False


class MosdnsRuleGenerator:
    """Generator for Mosdns rules based on Mihomo's state."""
    
    def __init__(self, api_client, mosdns_controller: MosdnsServiceController, mosdns_config_path: str):
        """
        Initialize the MosdnsRuleGenerator.
        
        Args:
            api_client: An instance of MihomoApiClient
            mosdns_controller (MosdnsServiceController): Controller for Mosdns service
            mosdns_config_path (str): Path to the Mosdns configuration file
        """
        self.api_client = api_client
        self.mosdns_controller = mosdns_controller
        self.mosdns_config_path = mosdns_config_path
        self.logger = logging.getLogger(__name__)

    async def run(self):
        """Generate Mosdns rules and reload the service."""
        try:
            self.logger.info("Starting rule generation process")
            
            # Get all required data from Mihomo API
            rules_data = await self.api_client.get_rules()
            proxies_data = await self.api_client.get_proxies()
            rule_providers_data = await self.api_client.get_rule_providers()
            
            # Initialize policy resolver
            from mihomo_sync.modules.policy_resolver import PolicyResolver
            policy_resolver = PolicyResolver(proxies_data)
            
            # Process rules and generate Mosdns configuration
            mosdns_rules = []
            
            # Process each rule
            for rule in rules_data.get("rules", []):
                # Extract rule components
                rule_type = rule.get("type")
                rule_payload = rule.get("payload")
                rule_target = rule.get("proxy")
                
                # Skip rules without a target
                if not rule_target:
                    continue
                    
                # Resolve the final target using PolicyResolver
                final_target = policy_resolver.resolve(rule_target)
                
                # Generate Mosdns rule based on type
                if rule_type == "DOMAIN":
                    mosdns_rules.append(f"domain:{rule_payload}:{final_target}")
                elif rule_type == "DOMAIN-SUFFIX":
                    mosdns_rules.append(f"domain-suffix:{rule_payload}:{final_target}")
                elif rule_type == "DOMAIN-KEYWORD":
                    mosdns_rules.append(f"domain-keyword:{rule_payload}:{final_target}")
                elif rule_type == "IP-CIDR":
                    mosdns_rules.append(f"ip-cidr:{rule_payload}:{final_target}")
                elif rule_type == "IP-CIDR6":
                    mosdns_rules.append(f"ip-cidr6:{rule_payload}:{final_target}")
                elif rule_type == "GEOIP":
                    mosdns_rules.append(f"geoip:{rule_payload}:{final_target}")
                elif rule_type == "GEOSITE":
                    mosdns_rules.append(f"geosite:{rule_payload}:{final_target}")
                elif rule_type == "DST-PORT":
                    mosdns_rules.append(f"dst-port:{rule_payload}:{final_target}")
                elif rule_type == "SRC-PORT":
                    mosdns_rules.append(f"src-port:{rule_payload}:{final_target}")
                elif rule_type == "RULE-SET":
                    # Handle rule providers
                    provider_name = rule.get("provider", "")
                    if provider_name:
                        # Resolve the final target for the provider
                        final_target = policy_resolver.resolve(provider_name)
                        # Add a comment for rule-set (as they are handled by the provider)
                        mosdns_rules.append(f"# Rule-SET: {rule_payload} -> {final_target}")
                # Add more rule types as needed
            
            # Write rules to temporary file first (atomic write)
            temp_path = self.mosdns_config_path + ".tmp"
            
            try:
                # Write to temporary file
                with open(temp_path, "w", encoding="utf-8") as f:
                    for rule in mosdns_rules:
                        f.write(rule + "\n")
                
                # Atomically rename temp file to final path
                os.replace(temp_path, self.mosdns_config_path)
                
                self.logger.info(
                    "Rules generated and written to file successfully",
                    extra={
                        "config_path": self.mosdns_config_path,
                        "rules_count": len(mosdns_rules)
                    }
                )
                
                # Reload Mosdns service
                reload_success = await self.mosdns_controller.reload()
                
                if reload_success:
                    self.logger.info("Rule generation and service reload completed successfully")
                else:
                    self.logger.error("Rule generation completed but service reload failed")
                    
            except Exception as e:
                # Clean up temp file if it exists
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
                self.logger.critical(
                    "Failed to write rules to file",
                    extra={
                        "config_path": self.mosdns_config_path,
                        "error": str(e)
                    }
                )
                raise
                
        except Exception as e:
            self.logger.error(
                "Error in rule generation process",
                extra={
                    "error": str(e)
                }
            )
            raise