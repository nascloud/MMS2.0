import logging
import os
import shutil
from typing import List


class RuleMerger:
    """Merger for combining intermediate files into final Mosdns rule files."""
    
    def __init__(self):
        """Initialize the RuleMerger."""
        self.logger = logging.getLogger(__name__)
    
    def merge_all_rules(self, temp_dir: str, output_dir: str) -> None:
        """
        Merge all intermediate files into final Mosdns rule files.
        
        Args:
            temp_dir (str): Directory containing intermediate files.
            output_dir (str): Directory to save final rule files.
        """
        try:
            # Clean output directory first
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Process all policy directories in temp_dir
            if os.path.exists(temp_dir):
                for policy_dir in os.listdir(temp_dir):
                    policy_temp_dir = os.path.join(temp_dir, policy_dir)
                    if os.path.isdir(policy_temp_dir):
                        # Convert policy name to uppercase for consistency
                        policy = policy_dir.upper()
                        self._merge_policy_rules(policy_temp_dir, policy, output_dir)
            
            self.logger.info(
                "Successfully merged all rules",
                extra={
                    "temp_dir": temp_dir,
                    "output_dir": output_dir
                }
            )
        except Exception as e:
            self.logger.error(
                "Failed to merge rules",
                extra={
                    "temp_dir": temp_dir,
                    "output_dir": output_dir,
                    "error": str(e)
                }
            )
            raise
    
    def _merge_policy_rules(self, policy_temp_dir: str, policy: str, output_dir: str) -> None:
        """
        Merge rules for a specific policy.
        
        Args:
            policy_temp_dir (str): Temporary directory for the policy.
            policy (str): Policy name.
            output_dir (str): Directory to save final rule files.
        """
        # Define content types to process
        content_types = ["domain", "ipv4", "ipv6"]
        
        # Process each content type
        for content_type in content_types:
            content_type_dir = os.path.join(policy_temp_dir, content_type)
            if os.path.exists(content_type_dir):
                self._merge_content_type_rules(content_type_dir, policy, content_type, output_dir)
    
    def _merge_content_type_rules(self, content_type_dir: str, policy: str, content_type: str, output_dir: str) -> None:
        """
        Merge rules for a specific content type.
        
        Args:
            content_type_dir (str): Directory containing rules of a specific content type.
            policy (str): Policy name.
            content_type (str): Content type (domain, ipv4, ipv6).
            output_dir (str): Directory to save final rule files.
        """
        try:
            # Collect all rule files
            rule_files = []
            for filename in os.listdir(content_type_dir):
                if filename.endswith(".txt"):
                    rule_files.append(os.path.join(content_type_dir, filename))
            
            # Sort files for consistent output
            rule_files.sort()
            
            # Generate output filename
            # Convert policy name to lowercase and content type to match expected format
            policy_lower = policy.lower()
            content_type_map = {
                "domain": "domain",
                "ipv4": "ipv4",
                "ipv6": "ipv6"
            }
            content_type_suffix = content_type_map.get(content_type, content_type)
            output_filename = f"{policy_lower}_{content_type_suffix}.txt"
            output_filepath = os.path.join(output_dir, output_filename)
            
            # Merge all rules into the output file
            with open(output_filepath, "w", encoding="utf-8") as output_file:
                for rule_file in rule_files:
                    try:
                        with open(rule_file, "r", encoding="utf-8") as f:
                            rule_content = f.read().strip()
                            if rule_content:
                                output_file.write(rule_content + "\n")
                    except Exception as e:
                        self.logger.warning(
                            "Failed to read rule file",
                            extra={
                                "rule_file": rule_file,
                                "error": str(e)
                            }
                        )
            
            self.logger.debug(
                "Merged content type rules",
                extra={
                    "policy": policy,
                    "content_type": content_type,
                    "rules_count": len(rule_files),
                    "output_file": output_filename
                }
            )
        except Exception as e:
            self.logger.error(
                "Failed to merge content type rules",
                extra={
                    "policy_temp_dir": content_type_dir,
                    "policy": policy,
                    "content_type": content_type,
                    "output_dir": output_dir,
                    "error": str(e)
                }
            )
            raise