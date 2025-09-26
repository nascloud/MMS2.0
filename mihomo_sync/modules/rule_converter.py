import logging
import os
import httpx
from typing import Dict, Any, List, Tuple


class RuleConverter:
    """将Mihomo规则转换为Mosdns格式的转换器。"""
    
    @staticmethod
    def convert_single_rule(rule: Dict[str, Any]) -> Tuple[str | None, str | None]:
        """
        转换单个Mihomo规则为Mosdns格式。
        
        Args:
            rule (dict): 来自Mihomo的单个规则。
            
        Returns:
            tuple: (转换后的Mosdns格式字符串, 内容类型) 或 (None, None) 如果不支持。
        """
        try:
            rule_type = rule.get("type", "")
            rule_payload = rule.get("payload", "")
            
            # 根据规则类型确定内容类型
            content_type = RuleConverter._determine_content_type(rule_type)
            
            # 转换格式
            mosdns_rule = RuleConverter._convert_format(rule_type, rule_payload)
            
            if mosdns_rule:
                return mosdns_rule, content_type
            else:
                return None, None
        except Exception as e:
            logging.getLogger(__name__).error(
                "转换单个规则失败",
                extra={
                    "rule": rule,
                    "error": str(e)
                }
            )
            return None, None
    
    @staticmethod
    def fetch_and_parse_ruleset(provider_info: Dict[str, Any]) -> List[str]:
        """
        获取并解析RULE-SET提供者的内容。
        
        Args:
            provider_info (dict): 关于规则提供者的信息。
            
        Returns:
            list: Mosdns格式的规则列表。
        """
        try:
            format_type = provider_info.get("format", "text")
            behavior = provider_info.get("behavior", "domain")
            url = provider_info.get("url", "")
            path = provider_info.get("path", "")
            
            # 处理mrs格式
            if format_type == "mrs":
                # 转换mrs格式的URL
                if behavior.lower() in ["domain", "ipcidr"]:
                    url = url.replace(".mrs", ".list")
                elif behavior.lower() == "classical":
                    url = url.replace(".mrs", ".yaml")
            
            # 根据行为处理（不区分大小写比较）
            behavior_lower = behavior.lower()
            if behavior_lower == "domain":
                return RuleConverter._parse_domain_rules(url, path)
            elif behavior_lower == "ipcidr":
                return RuleConverter._parse_ipcidr_rules(url, path)
            elif behavior_lower == "classical":
                return RuleConverter._parse_classical_rules(url, path)
            else:
                logging.getLogger(__name__).warning(
                    "不支持的行为类型",
                    extra={
                        "behavior": behavior
                    }
                )
                return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "获取和解析规则集失败",
                extra={
                    "provider_info": provider_info,
                    "error": str(e)
                }
            )
            return []
    
    @staticmethod
    def _determine_content_type(rule_type: str) -> str:
        """
        根据规则类型确定内容类型。
        
        Args:
            rule_type (str): 规则的类型。
            
        Returns:
            str: 内容类型 (domain, ipv4, ipv6)。
        """
        # 根据规则类型确定
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
            # 对于未知类型，默认为domain
            return "domain"
    
    @staticmethod
    def _convert_format(rule_type: str, content: str) -> str:
        """
        将Mihomo规则格式转换为Mosdns格式。
        
        Args:
            rule_type (str): 规则的类型。
            content (str): 规则的内容。
            
        Returns:
            str: 转换后的Mosdns格式规则。
        """
        # 处理列表格式通配符的特殊情况
        if rule_type == "DOMAIN-SUFFIX" or rule_type == "DomainSuffix":
            # 处理列表格式的通配符
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
                # 正常的域名后缀
                return f"domain:{content}"
        elif rule_type == "DOMAIN":
            return f"full:{content}"
        elif rule_type == "DOMAIN-KEYWORD":
            return f"keyword:{content}"
        elif rule_type == "DOMAIN-REGEX":
            return f"regexp:{content}"
        elif rule_type == "IP-CIDR" or rule_type == "IPCIDR":
            return content  # 直接返回CIDR内容，不带前缀
        elif rule_type == "IP-CIDR6":
            return content  # 直接返回CIDR内容，不带前缀
        else:
            # 对于不支持的类型，返回空字符串
            logging.getLogger(__name__).warning(
                "不支持的规则类型转换",
                extra={
                    "rule_type": rule_type,
                    "content": content
                }
            )
            return ""
    
    @staticmethod
    def _parse_domain_rules(url: str, path: str = "") -> List[str]:
        """
        从URL或本地文件路径解析域名规则。
        
        Args:
            url (str): 下载域名规则的URL。
            path (str): 域名规则的本地文件路径。
            
        Returns:
            list: 域名规则列表。
        """
        try:
            # 如果提供了路径，则从本地文件读取
            if path:
                if os.path.exists(path):
                    rules = []
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # 转换为Mosdns格式
                                if line.startswith("*."):
                                    # *.example.com -> domain:example.com
                                    line = line[2:]
                                    rules.append(f"domain:{line}")
                                elif line.startswith("+.") or line.startswith(".+"):
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
                                    # 正常域名
                                    rules.append(f"domain:{line}")
                    return rules
            
            # 如果提供了URL，则下载并解析
            if url:
                try:
                    response = httpx.get(url, timeout=30)
                    response.raise_for_status()
                    
                    rules = []
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # 转换为Mosdns格式
                            if line.startswith("*."):
                                # *.example.com -> domain:example.com
                                line = line[2:]
                                rules.append(f"domain:{line}")
                            elif line.startswith("+.") or line.startswith(".+"):
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
                                # 正常域名
                                rules.append(f"domain:{line}")
                    return rules
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "下载域名规则失败",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # 回退到空列表
            return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "解析域名规则失败",
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
        从URL或本地文件路径解析IPCIDR规则。
        
        Args:
            url (str): 下载IPCIDR规则的URL。
            path (str): IPCIDR规则的本地文件路径。
            
        Returns:
            list: IPCIDR规则列表。
        """
        try:
            # 如果提供了路径，则从本地文件读取
            if path:
                if os.path.exists(path):
                    rules = []
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # 直接添加行，不带前缀
                                rules.append(line)
                    return rules
            
            # 如果提供了URL，则下载并解析
            if url:
                try:
                    response = httpx.get(url, timeout=30)
                    response.raise_for_status()
                    
                    rules = []
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # 直接添加行，不带前缀
                            rules.append(line)
                    return rules
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "下载IPCIDR规则失败",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # 回退到空列表
            return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "解析IPCIDR规则失败",
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
        从URL或本地文件路径解析经典规则。
        
        Args:
            url (str): 下载经典规则的URL。
            path (str): 经典规则的本地文件路径。
            
        Returns:
            list: 经典规则列表。
        """
        try:
            # 如果提供了路径，则从本地文件读取
            if path:
                if os.path.exists(path):
                    rules = []
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # 解析经典规则格式 (DOMAIN-SUFFIX,example.com)
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
                                    # 直接添加CIDR，不带前缀
                                    rules.append(cidr)
                                elif line.startswith("IP-CIDR6,"):
                                    cidr6 = line.split(",", 1)[1]
                                    # 直接添加CIDR，不带前缀
                                    rules.append(cidr6)
                    return rules
            
            # 如果提供了URL，则下载并解析
            if url:
                try:
                    response = httpx.get(url, timeout=30)
                    response.raise_for_status()
                    
                    rules = []
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # 解析经典规则格式 (DOMAIN-SUFFIX,example.com)
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
                                # 直接添加CIDR，不带前缀
                                rules.append(cidr)
                            elif line.startswith("IP-CIDR6,"):
                                cidr6 = line.split(",", 1)[1]
                                # 直接添加CIDR，不带前缀
                                rules.append(cidr6)
                    return rules
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "下载经典规则失败",
                        extra={
                            "url": url,
                            "error": str(e)
                        }
                    )
            
            # 回退到空列表
            return []
        except Exception as e:
            logging.getLogger(__name__).error(
                "解析经典规则失败",
                extra={
                    "url": url,
                    "path": path,
                    "error": str(e)
                }
            )
            return []