import logging
import os
import shutil
from typing import Set


class RuleMerger:
    """Merger for combining intermediate files into final Mosdns rule files."""
    
    def __init__(self):
        """Initialize the RuleMerger."""
        self.logger = logging.getLogger(__name__)
    
    def merge_from_intermediate(self, intermediate_path: str, final_output_path: str) -> None:
        """
        Merge rules from intermediate files into final Mosdns rule files.
        
        Args:
            intermediate_path (str): Path to the intermediate files directory
            final_output_path (str): Path to the final output directory
        """
        try:
            # Step 1: Prepare workspace
            self._prepare_workspace(final_output_path)
            
            # Step 2: Process intermediate directory
            self._process_intermediate_directory(intermediate_path, final_output_path)
            
            self.logger.info(
                "Successfully merged all rules",
                extra={
                    "intermediate_path": intermediate_path,
                    "final_output_path": final_output_path
                }
            )
        except Exception as e:
            self.logger.error(
                "Failed to merge rules",
                extra={
                    "intermediate_path": intermediate_path,
                    "final_output_path": final_output_path,
                    "error": str(e)
                }
            )
            raise
    
    def _prepare_workspace(self, final_output_path: str) -> None:
        """
        Prepare the workspace by cleaning and creating the final output directory.
        
        Args:
            final_output_path (str): Path to the final output directory
        """
        if os.path.exists(final_output_path):
            shutil.rmtree(final_output_path)
        os.makedirs(final_output_path)
        self.logger.debug(f"Cleaned and created final output directory: {final_output_path}")
    
    def _process_intermediate_directory(self, intermediate_path: str, final_output_path: str) -> None:
        """
        Process the intermediate directory and merge rules.
        
        Args:
            intermediate_path (str): Path to the intermediate files directory
            final_output_path (str): Path to the final output directory
        """
        # Walk through the intermediate directory structure
        for root, dirs, files in os.walk(intermediate_path):
            # Skip if no files in this directory
            if not files:
                continue
            
            # Determine policy and content type from directory structure
            rel_path = os.path.relpath(root, intermediate_path)
            path_parts = rel_path.split(os.sep)
            
            # We expect path structure like: policy/content_type
            if len(path_parts) != 2:
                continue
                
            policy, content_type = path_parts
            
            # Merge rules in this directory
            self._merge_directory_rules(root, policy, content_type, final_output_path)
    
    def _merge_directory_rules(self, directory_path: str, policy: str, content_type: str, final_output_path: str) -> None:
        """
        Merge all rules in a specific directory.
        
        Args:
            directory_path (str): Path to the directory containing rule files
            policy (str): Policy name
            content_type (str): Content type (domain, ipcidr, etc.)
            final_output_path (str): Path to the final output directory
        """
        try:
            # Step 1: Collect all rules from .list files
            final_rules: Set[str] = set()
            
            for filename in os.listdir(directory_path):
                if filename.endswith(".list"):
                    filepath = os.path.join(directory_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = [line.strip() for line in f.readlines() if line.strip()]
                            final_rules.update(lines)
                    except Exception as e:
                        self.logger.warning(
                            "Failed to read rule file",
                            extra={
                                "rule_file": filepath,
                                "error": str(e)
                            }
                        )
            
            # Step 2: Write final rules if not empty
            if final_rules:
                # Create flat filename based on policy and content_type
                # Convert to lowercase and replace content_type mapping
                policy_lower = policy.lower()
                if content_type == "domain":
                    output_filename = f"{policy_lower}_domain.txt"
                elif content_type == "ipcidr":
                    # Check if we have IPv6 rules in the set by checking for ":"
                    # IPv6 addresses contain ":" while IPv4 addresses don't
                    has_ipv6 = any(":" in rule and "." not in rule for rule in final_rules)
                    has_ipv4 = any("." in rule for rule in final_rules)
                    
                    # If we have both IPv4 and IPv6 rules, create separate files
                    if has_ipv6 and has_ipv4:
                        # Create IPv4 file
                        ipv4_rules = {rule for rule in final_rules if "." in rule}
                        if ipv4_rules:
                            output_filename = f"{policy_lower}_ipv4.txt"
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv4_rules))))
                                self.logger.debug(
                                    "Merged directory rules (IPv4)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv4_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "Failed to write final rule file (IPv4)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                        
                        # Create IPv6 file
                        ipv6_rules = {rule for rule in final_rules if ":" in rule and "." not in rule}
                        if ipv6_rules:
                            output_filename = f"{policy_lower}_ipv6.txt"
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv6_rules))))
                                self.logger.debug(
                                    "Merged directory rules (IPv6)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv6_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "Failed to write final rule file (IPv6)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                        # Skip the default write since we've already written separate files
                        return
                    elif has_ipv6:
                        # Only IPv6 rules
                        output_filename = f"{policy_lower}_ipv6.txt"
                        ipv6_rules = {rule for rule in final_rules if ":" in rule and "." not in rule}
                        if ipv6_rules:
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv6_rules))))
                                self.logger.debug(
                                    "Merged directory rules (IPv6 only)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv6_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "Failed to write final rule file (IPv6 only)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                            return
                    else:
                        # Only IPv4 rules (or mixed but we'll treat as IPv4 for backward compatibility)
                        output_filename = f"{policy_lower}_ipv4.txt"
                else:
                    output_filename = f"{policy_lower}_{content_type}.txt"
                
                # Full output file path
                output_filepath = os.path.join(final_output_path, output_filename)
                
                try:
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(sorted(list(final_rules))))
                    self.logger.debug(
                        "Merged directory rules",
                        extra={
                            "policy": policy,
                            "content_type": content_type,
                            "rules_count": len(final_rules),
                            "output_file": output_filepath
                        }
                    )
                except Exception as e:
                    self.logger.error(
                        "Failed to write final rule file",
                        extra={
                            "output_file": output_filepath,
                            "error": str(e)
                        }
                    )
                    raise
        except Exception as e:
            self.logger.error(
                "Failed to merge directory rules",
                extra={
                    "directory_path": directory_path,
                    "policy": policy,
                    "content_type": content_type,
                    "final_output_path": final_output_path,
                    "error": str(e)
                }
            )
            raise