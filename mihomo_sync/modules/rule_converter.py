import logging
import os
import httpx
from typing import Dict, Any, List, Tuple


class RuleConverter:
    """Converter for transforming Mihomo rules to Mosdns format."""
    
    @staticmethod
    def convert_single_rule(rule: Dict[str, Any]) -> Tuple[str | None, str | None]:
        """
        Convert a single Mihomo rule to Mosdns format.
        
        Args:
            rule (dict): A single rule from Mihomo.
            
        Returns:
            tuple: (converted Mosdns format string, content type) or (None, None) if unsupported.
        """
        try:
            rule_type = rule.get("type", "")
            rule_payload = rule.get("payload", "")
            
            # Determine content type based on rule type
            content_type = RuleConverter._determine_content_type(rule_type)
            
            # Convert format
            mosdns_rule = RuleConverter._convert_format(rule_type, rule_payload)
            
            if mosdns_rule:
                return mosdns_rule, content_type
            else:
                return None, None
        except Exception as e:
            logging.getLogger(__name__).error(
                "Failed to convert single rule",
                extra={
                    "rule": rule,
                    "error": str(e)
                }
            )
            return None, None
    
    @staticmethod
    def fetch_and_parse_ruleset(provider_info: Dict[str, Any]) -> List[str]:
        """
        Fetch and parse a RULE-SET provider's content.
        
        Args:
            provider_info (dict): Information about the rule provider.
            
        Returns:
            list: List of rules in Mosdns format.
        """
        try:
            format_type = provider_info.get("format", "text")
            behavior = provider_info.get("behavior", "domain")
            url = provider_info.get("url", "")
            path = provider_info.get("path", "")
            
            # Handle mrs format
            if format_type == "mrs":
                # Convert URL for mrs format
                if behavior in ["domain", "ipcidr"]:
                    url = url.replace(".mrs", ".list")
                elif behavior == "classical":
                    url = url.replace(".mrs", ".yaml")
            
            # Process based on behavior
            if behavior == "domain":
                return RuleConverter._parse_domain_rules(url, path)
            elif behavior == "ipcidr":
                return RuleConverter._parse_ipcidr_rules(url, path)
            elif behavior == "classical":
                return RuleConverter._parse_classical_rules(url, path)
            else:
                logging.getLogger(__name__).warning(
                    "Unsupported behavior type",
                    extra={
                        "behavior": behavior
                    }
                )
                return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "Failed to fetch and parse ruleset",
                extra={
                    "provider_info": provider_info,
                    "error": str(e)
                }
            )
            return []
    
    @staticmethod
    def _determine_content_type(rule_type: str) -> str:
        """
        Determine content type based on rule type.
        
        Args:
            rule_type (str): Type of the rule.
            
        Returns:
            str: Content type (domain, ipv4, ipv6).
        """
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
    
    @staticmethod
    def _convert_format(rule_type: str, content: str) -> str:
        """
        Convert Mihomo rule format to Mosdns format.
        
        Args:
            rule_type (str): Type of the rule.
            content (str): Content of the rule.
            
        Returns:
            str: Converted Mosdns format rule.
        """
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
            logging.getLogger(__name__).warning(
                "Unsupported rule type for conversion",
                extra={
                    "rule_type": rule_type,
                    "content": content
                }
            )
            return ""
    
    @staticmethod
    def _parse_domain_rules(url: str, path: str = "") -> List[str]:
        """
        Parse domain rules from URL or local file path.
        
        Args:
            url (str): URL to download domain rules.
            path (str): Local file path for domain rules.
            
        Returns:
            list: List of domain rules.
        """
        try:
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
                    return rules
            
            # If URL is provided, download and parse
            if url:
                try:
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
                    return rules
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "Failed to download domain rules",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # Fallback to empty list
            return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "Failed to parse domain rules",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []
    
    @staticmethod
    def _parse_ipcidr_rules(url: str, path: str = "") -> List[str]:
        """
        Parse IPCIDR rules from URL or local file path.
        
        Args:
            url (str): URL to download IPCIDR rules.
            path (str): Local file path for IPCIDR rules.
            
        Returns:
            list: List of IPCIDR rules.
        """
        try:
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
                    return rules
            
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
                    return rules
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "Failed to download IPCIDR rules",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # Fallback to empty list
            return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "Failed to parse IPCIDR rules",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []
    
    @staticmethod
    def _parse_classical_rules(url: str, path: str = "") -> List[str]:
        """
        Parse classical rules from URL or local file path.
        
        Args:
            url (str): URL to download classical rules.
            path (str): Local file path for classical rules.
            
        Returns:
            list: List of classical rules.
        """
        try:
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
                    return rules
            
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
                    return rules
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "Failed to download classical rules",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # Fallback to empty list
            return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "Failed to parse classical rules",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []