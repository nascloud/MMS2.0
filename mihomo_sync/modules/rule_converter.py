import logging
import os
import hashlib
from typing import Dict, Any, List
import httpx


class RuleConverter:
    """Converter for transforming Mihomo rules to Mosdns format and generating intermediate files."""
    
    def __init__(self):
        """Initialize the RuleConverter."""
        self.logger = logging.getLogger(__name__)
    
    def convert_and_save(self, mihomo_rule: Dict[str, Any], final_policy: str, temp_dir: str, provider_info: Dict[str, Any]) -> None:
        """
        Convert a single Mihomo rule to Mosdns format and save as intermediate file.
        
        Args:
            mihomo_rule (dict): A single rule from Mihomo.
            final_policy (str): The final policy name.
            temp_dir (str): Temporary directory to save intermediate files.
            provider_info (dict): Information about rule providers.
        """
        try:
            rule_type = mihomo_rule.get("type", "")
            rule_payload = mihomo_rule.get("payload", "")
            
            # Determine content type based on rule type or payload
            content_type = self._determine_content_type(rule_type, rule_payload)
            
            # Get rule content
            rule_contents = self._get_rule_content(rule_type, rule_payload, provider_info)
            
            self.logger.debug(
                "Got rule contents",
                extra={
                    "rule_type": rule_type,
                    "rule_payload": rule_payload,
                    "rule_contents_count": len(rule_contents),
                    "first_few_contents": rule_contents[:3] if rule_contents else []
                }
            )
            
            # Convert format
            mosdns_rules = []
            # For RuleSet, the content is already in the correct format
            if rule_type == "RULE-SET":
                # For RuleSet, rule_contents already contains the correctly formatted rules
                mosdns_rules = rule_contents
                self.logger.debug(
                    "RuleSet: using rule_contents directly",
                    extra={
                        "rule_contents_count": len(rule_contents),
                        "mosdns_rules_count": len(mosdns_rules)
                    }
                )
            else:
                # For other rule types, convert each content
                for content in rule_contents:
                    mosdns_rule = self._convert_format(rule_type, content)
                    if mosdns_rule:
                        mosdns_rules.append(mosdns_rule)
                self.logger.debug(
                    "Non-RuleSet: converted contents",
                    extra={
                        "rule_type": rule_type,
                        "rule_contents_count": len(rule_contents),
                        "mosdns_rules_count": len(mosdns_rules)
                    }
                )
            
            self.logger.debug(
                "Processing rule",
                extra={
                    "rule_type": rule_type,
                    "rule_payload": rule_payload,
                    "final_policy": final_policy,
                    "content_type": content_type,
                    "rule_contents_count": len(rule_contents),
                    "mosdns_rules_count": len(mosdns_rules)
                }
            )
            
            # Save intermediate files
            self._save_intermediate_files(mosdns_rules, final_policy, content_type, temp_dir)
            
            self.logger.debug(
                "Converted and saved rule",
                extra={
                    "rule_type": rule_type,
                    "final_policy": final_policy,
                    "content_type": content_type,
                    "rules_count": len(mosdns_rules)
                }
            )
        except Exception as e:
            self.logger.error(
                "Failed to convert and save rule",
                extra={
                    "rule": mihomo_rule,
                    "error": str(e)
                }
            )
            raise
    
    def _determine_content_type(self, rule_type: str, rule_payload: str) -> str:
        """
        Determine content type based on rule type or payload.
        
        Args:
            rule_type (str): Type of the rule.
            rule_payload (str): Payload of the rule.
            
        Returns:
            str: Content type (domain, ipv4, ipv6).
        """
        # For RuleSet, determine by payload if needed
        if rule_type == "RULE-SET":
            # Default to domain for RuleSet, will be refined when processing content
            return "domain"
        
        # Determine by rule type
        domain_types = ["DOMAIN-SUFFIX", "DOMAIN", "DOMAIN-KEYWORD", "DOMAIN-REGEX", "DomainSuffix"]
        ip_types = ["IP-CIDR", "IP-CIDR6", "IPCIDR"]
        
        if rule_type in domain_types:
            return "domain"
        elif rule_type in ip_types:
            if rule_type == "IP-CIDR6":
                return "ipv6"
            else:
                return "ipv4"
        else:
            # Default to domain for unknown types
            return "domain"
    
    def _get_rule_content(self, rule_type: str, rule_payload: str, provider_info: Dict[str, Any]) -> List[str]:
        """
        Get rule content based on rule type.
        
        Args:
            rule_type (str): Type of the rule.
            rule_payload (str): Payload of the rule.
            provider_info (dict): Information about rule providers.
            
        Returns:
            list: List of rule contents.
        """
        self.logger.debug(
            "Getting rule content",
            extra={
                "rule_type": rule_type,
                "rule_payload": rule_payload,
                "provider_info_keys": list(provider_info.keys()) if provider_info else []
            }
        )
        
        if rule_type == "RULE-SET":
            # Handle RuleSet type
            provider_name = rule_payload
            if provider_name in provider_info:
                provider = provider_info[provider_name]
                self.logger.debug(
                    "Found provider info for RuleSet",
                    extra={
                        "provider_name": provider_name,
                        "provider": provider
                    }
                )
                result = self._process_rule_set(provider)
                self.logger.debug(
                    "Processed RuleSet provider",
                    extra={
                        "provider_name": provider_name,
                        "result_count": len(result),
                        "first_few_results": result[:3] if result else []
                    }
                )
                return result
            else:
                self.logger.warning(
                    "Rule provider not found in provider info",
                    extra={
                        "provider_name": provider_name,
                        "available_providers": list(provider_info.keys()),
                        "rule_payload": rule_payload
                    }
                )
                return [rule_payload]  # Return the payload as content if provider not found
        else:
            # For normal rules, payload is the content
            return [rule_payload] if rule_payload else []
    
    def _process_rule_set(self, provider: Dict[str, Any]) -> List[str]:
        """
        Process RuleSet provider and extract rules.
        
        Args:
            provider (dict): Provider information.
            
        Returns:
            list: List of rules from the provider.
        """
        try:
            format_type = provider.get("format", "text")
            behavior = provider.get("behavior", "domain")
            url = provider.get("url", "")
            path = provider.get("path", "")
            
            self.logger.debug(
                "Processing RuleSet provider",
                extra={
                    "format_type": format_type,
                    "behavior": behavior,
                    "url": url,
                    "path": path
                }
            )
            
            # Handle mrs format
            if format_type == "mrs":
                # Convert URL for mrs format
                original_url = url
                if behavior in ["domain", "ipcidr"]:
                    url = url.replace(".mrs", ".list")
                elif behavior == "classical":
                    url = url.replace(".mrs", ".yaml")
                
                self.logger.debug(
                    "Converted mrs URL",
                    extra={
                        "original_url": original_url,
                        "converted_url": url,
                        "behavior": behavior
                    }
                )
            
            # Download and parse content based on behavior
            result = []
            if behavior == "domain":
                result = self._parse_domain_rules(url, path)
            elif behavior == "ipcidr":
                result = self._parse_ipcidr_rules(url, path)
            elif behavior == "classical":
                result = self._parse_classical_rules(url, path)
            else:
                self.logger.warning(
                    "Unsupported behavior type",
                    extra={
                        "behavior": behavior
                    }
                )
                result = []
            
            self.logger.debug(
                "RuleSet processing result",
                extra={
                    "result_count": len(result),
                    "first_few_results": result[:5] if result else [],
                    "behavior": behavior,
                    "url": url,
                    "path": path
                }
            )
            
            return result
        except Exception as e:
            self.logger.error(
                "Failed to process rule set",
                extra={
                    "provider": provider,
                    "error": str(e)
                }
            )
            # Fallback to empty list
            return []
    
    def _parse_domain_rules(self, url: str, path: str = "") -> List[str]:
        """
        Parse domain rules from URL or local file path.
        
        Args:
            url (str): URL to download domain rules.
            path (str): Local file path for domain rules.
            
        Returns:
            list: List of domain rules.
        """
        try:
            self.logger.debug(
                "Parsing domain rules",
                extra={
                    "url": url,
                    "path": path
                }
            )
            
            # If path is provided, read from local file
            if path:
                if os.path.exists(path):
                    rules = []
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Convert to Mosdns format
                                if line.startswith("*."):
                                    # *.example.com -> domain:example.com
                                    line = line[2:]
                                    rules.append(f"domain:{line}")
                                elif line.startswith("+."):
                                    # +.example.com -> domain:example.com
                                    line = line[2:]
                                    rules.append(f"domain:{line}")
                                elif line.startswith("."):
                                    # .example.com -> domain:example.com
                                    line = line[1:]
                                    rules.append(f"domain:{line}")
                                elif line == "*":
                                    # * -> keyword:
                                    rules.append("keyword:")
                                else:
                                    # Normal domain
                                    rules.append(f"domain:{line}")
                    self.logger.debug(
                        "Parsed domain rules from local file",
                        extra={
                            "path": path,
                            "rules_count": len(rules),
                            "first_few_rules": rules[:5] if rules else []
                        }
                    )
                    return rules
                else:
                    self.logger.warning(
                        "Local domain rules file not found",
                        extra={"path": path}
                    )
            
            # If URL is provided, download and parse
            if url:
                try:
                    self.logger.debug(
                        "Downloading domain rules from URL",
                        extra={"url": url}
                    )
                    response = httpx.get(url, timeout=30)
                    response.raise_for_status()
                    
                    rules = []
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Convert to Mosdns format
                            if line.startswith("*."):
                                # *.example.com -> domain:example.com
                                line = line[2:]
                                rules.append(f"domain:{line}")
                            elif line.startswith("+."):
                                # +.example.com -> domain:example.com
                                line = line[2:]
                                rules.append(f"domain:{line}")
                            elif line.startswith("."):
                                # .example.com -> domain:example.com
                                line = line[1:]
                                rules.append(f"domain:{line}")
                            elif line == "*":
                                # * -> keyword:
                                rules.append("keyword:")
                            else:
                                # Normal domain
                                rules.append(f"domain:{line}")
                    
                    self.logger.debug(
                        "Downloaded and parsed domain rules from URL",
                        extra={
                            "url": url,
                            "rules_count": len(rules),
                            "first_few_rules": rules[:5] if rules else []
                        }
                    )
                    return rules
                except Exception as e:
                    self.logger.error(
                        "Failed to download domain rules",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # Fallback to empty list
            self.logger.debug(
                "No domain rules found, returning empty list",
                extra={
                    "url": url,
                    "path": path
                }
            )
            return []
        except Exception as e:
            self.logger.error(
                "Failed to parse domain rules",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []
    
    def _parse_ipcidr_rules(self, url: str, path: str = "") -> List[str]:
        """
        Parse IPCIDR rules from URL or local file path.
        
        Args:
            url (str): URL to download IPCIDR rules.
            path (str): Local file path for IPCIDR rules.
            
        Returns:
            list: List of IPCIDR rules.
        """
        try:
            self.logger.debug(
                "Parsing IPCIDR rules",
                extra={
                    "url": url,
                    "path": path
                }
            )
            
            # If path is provided, read from local file
            if path:
                if os.path.exists(path):
                    rules = []
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Determine if it's IPv6 or IPv4
                                if ':' in line and '.' not in line:
                                    rules.append(f"ip-cidr6:{line}")
                                else:
                                    rules.append(f"ip-cidr:{line}")
                    self.logger.debug(
                        "Parsed IPCIDR rules from local file",
                        extra={
                            "path": path,
                            "rules_count": len(rules),
                            "first_few_rules": rules[:5] if rules else []
                        }
                    )
                    return rules
                else:
                    self.logger.warning(
                        "Local IPCIDR rules file not found",
                        extra={"path": path}
                    )
            
            # If URL is provided, download and parse
            if url:
                try:
                    response = httpx.get(url, timeout=30)
                    response.raise_for_status()
                    
                    rules = []
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Determine if it's IPv6 or IPv4
                            if ':' in line and '.' not in line:
                                rules.append(f"ip-cidr6:{line}")
                            else:
                                rules.append(f"ip-cidr:{line}")
                    self.logger.debug(
                        "Downloaded and parsed IPCIDR rules from URL",
                        extra={
                            "url": url,
                            "rules_count": len(rules),
                            "first_few_rules": rules[:5] if rules else []
                        }
                    )
                    return rules
                except Exception as e:
                    self.logger.error(
                        "Failed to download IPCIDR rules",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # Fallback to empty list
            return []
        except Exception as e:
            self.logger.error(
                "Failed to parse IPCIDR rules",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []
    
    def _parse_classical_rules(self, url: str, path: str = "") -> List[str]:
        """
        Parse classical rules from URL or local file path.
        
        Args:
            url (str): URL to download classical rules.
            path (str): Local file path for classical rules.
            
        Returns:
            list: List of classical rules.
        """
        try:
            self.logger.debug(
                "Parsing classical rules",
                extra={
                    "url": url,
                    "path": path
                }
            )
            
            # If path is provided, read from local file
            if path:
                if os.path.exists(path):
                    rules = []
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Parse classical rule format (DOMAIN-SUFFIX,example.com)
                                if line.startswith("DOMAIN-SUFFIX,"):
                                    domain = line.split(",", 1)[1]
                                    rules.append(f"domain:{domain}")
                                elif line.startswith("DOMAIN,"):
                                    domain = line.split(",", 1)[1]
                                    rules.append(f"full:{domain}")
                                elif line.startswith("DOMAIN-KEYWORD,"):
                                    keyword = line.split(",", 1)[1]
                                    rules.append(f"keyword:{keyword}")
                                elif line.startswith("DOMAIN-REGEX,"):
                                    regex = line.split(",", 1)[1]
                                    rules.append(f"regexp:{regex}")
                                elif line.startswith("IP-CIDR,"):
                                    cidr = line.split(",", 1)[1]
                                    rules.append(f"ip-cidr:{cidr}")
                                elif line.startswith("IP-CIDR6,"):
                                    cidr6 = line.split(",", 1)[1]
                                    rules.append(f"ip-cidr6:{cidr6}")
                    self.logger.debug(
                        "Parsed classical rules from local file",
                        extra={
                            "path": path,
                            "rules_count": len(rules),
                            "first_few_rules": rules[:5] if rules else []
                        }
                    )
                    return rules
                else:
                    self.logger.warning(
                        "Local classical rules file not found",
                        extra={"path": path}
                    )
            
            # If URL is provided, download and parse
            if url:
                try:
                    response = httpx.get(url, timeout=30)
                    response.raise_for_status()
                    
                    rules = []
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Parse classical rule format (DOMAIN-SUFFIX,example.com)
                            if line.startswith("DOMAIN-SUFFIX,"):
                                domain = line.split(",", 1)[1]
                                rules.append(f"domain:{domain}")
                            elif line.startswith("DOMAIN,"):
                                domain = line.split(",", 1)[1]
                                rules.append(f"full:{domain}")
                            elif line.startswith("DOMAIN-KEYWORD,"):
                                keyword = line.split(",", 1)[1]
                                rules.append(f"keyword:{keyword}")
                            elif line.startswith("DOMAIN-REGEX,"):
                                regex = line.split(",", 1)[1]
                                rules.append(f"regexp:{regex}")
                            elif line.startswith("IP-CIDR,"):
                                cidr = line.split(",", 1)[1]
                                rules.append(f"ip-cidr:{cidr}")
                            elif line.startswith("IP-CIDR6,"):
                                cidr6 = line.split(",", 1)[1]
                                rules.append(f"ip-cidr6:{cidr6}")
                    self.logger.debug(
                        "Downloaded and parsed classical rules from URL",
                        extra={
                            "url": url,
                            "rules_count": len(rules),
                            "first_few_rules": rules[:5] if rules else []
                        }
                    )
                    return rules
                except Exception as e:
                    self.logger.error(
                        "Failed to download classical rules",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # Fallback to empty list
            return []
        except Exception as e:
            self.logger.error(
                "Failed to parse classical rules",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []
    
    def _convert_format(self, rule_type: str, content: str) -> str:
        """
        Convert Mihomo rule format to Mosdns format.
        
        Args:
            rule_type (str): Type of the rule.
            content (str): Content of the rule.
            
        Returns:
            str: Converted Mosdns format rule.
        """
        self.logger.debug(
            "Converting rule format",
            extra={
                "rule_type": rule_type,
                "content": content
            }
        )
        
        # Handle special cases for list format wildcards
        if rule_type == "DOMAIN-SUFFIX" or rule_type == "DomainSuffix":
            # Handle wildcards in list format
            if content.startswith("*."):
                # *.example.com -> domain:example.com
                content = content[2:]
                return f"domain:{content}"
            elif content.startswith("+."):
                # +.example.com -> domain:example.com
                content = content[2:]
                return f"domain:{content}"
            elif content.startswith("."):
                # .example.com -> domain:example.com
                content = content[1:]
                return f"domain:{content}"
            elif content == "*":
                # * -> keyword:
                return "keyword:"
            else:
                # Normal domain suffix
                return f"domain:{content}"
        elif rule_type == "DOMAIN":
            return f"full:{content}"
        elif rule_type == "DOMAIN-KEYWORD":
            return f"keyword:{content}"
        elif rule_type == "DOMAIN-REGEX":
            return f"regexp:{content}"
        elif rule_type == "IP-CIDR" or rule_type == "IPCIDR":
            return f"ip-cidr:{content}"
        elif rule_type == "IP-CIDR6":
            return f"ip-cidr6:{content}"
        else:
            # For unsupported types, return empty string
            self.logger.warning(
                "Unsupported rule type for conversion",
                extra={
                    "rule_type": rule_type,
                    "content": content
                }
            )
            return ""
    
    def _save_intermediate_files(self, mosdns_rules: List[str], final_policy: str, content_type: str, temp_dir: str) -> None:
        """
        Save Mosdns rules as intermediate files.
        
        Args:
            mosdns_rules (list): List of Mosdns rules.
            final_policy (str): The final policy name.
            content_type (str): Content type (domain, ipv4, ipv6).
            temp_dir (str): Temporary directory to save files.
        """
        # Sanitize policy name for use as directory name (remove/replace invalid characters for Windows)
        sanitized_policy = final_policy
        invalid_chars = '<>:"|?*/\\'
        for char in invalid_chars:
            sanitized_policy = sanitized_policy.replace(char, '_')
        
        # Create directory structure: temp_dir/policy/content_type/
        policy_dir = os.path.join(temp_dir, sanitized_policy.lower())
        content_type_dir = os.path.join(policy_dir, content_type)
        
        # Ensure directories exist
        os.makedirs(content_type_dir, exist_ok=True)
        
        # Save each rule as a separate file
        for rule in mosdns_rules:
            # Generate unique filename using hash
            filename = hashlib.md5(rule.encode('utf-8')).hexdigest() + ".txt"
            filepath = os.path.join(content_type_dir, filename)
            
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rule)
            except Exception as e:
                self.logger.error(
                    "Failed to save intermediate file",
                    extra={
                        "filepath": filepath,
                        "rule": rule,
                        "error": str(e)
                    }
                )
                raise