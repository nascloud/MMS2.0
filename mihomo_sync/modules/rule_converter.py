import logging
import os
import httpx
from typing import Dict, Any, List, Tuple


class RuleConverter:
    """将Mihomo规则转换为Mosdns格式的转换器。支持DOMAIN, DOMAIN-SUFFIX, DOMAIN-KEYWORD, DOMAIN-WILDCARD, DOMAIN-REGEX, IP-CIDR, IP-CIDR6, IP-SUFFIX, RULE-SET规则类型。"""
    
    @staticmethod
    def convert_single_rule(rule: Dict[str, Any]) -> Tuple[str | None, str | None]:
        """
        转换单个Mihomo规则为Mosdns格式。
        仅处理支持的规则类型：DOMAIN, DOMAIN-SUFFIX, DOMAIN-KEYWORD, DOMAIN-WILDCARD, DOMAIN-REGEX, IP-CIDR, IP-CIDR6, IP-SUFFIX, RULE-SET。
        其他规则类型将被跳过。
        
        Args:
            rule (dict): 来自Mihomo的单个规则。
            
        Returns:
            tuple: (转换后的Mosdns格式字符串, 内容类型) 或 (None, None) 如果不支持。
        """
        try:
            rule_type = rule.get("type", "")
            
            # 检查规则类型是否是我们支持的类型
            supported_types = {
                "DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", 
                "DOMAIN-WILDCARD", "DOMAIN-REGEX", 
                "IP-CIDR", "IP-CIDR6", "IP-SUFFIX", 
                "RULE-SET", "DomainSuffix", "IPCIDR"
            }
            
            if rule_type not in supported_types:
                # 不支持的规则类型，跳过
                logging.getLogger(__name__).debug(
                    "跳过不支持的规则类型",
                    extra={
                        "rule_type": rule_type
                    }
                )
                return None, None
            
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
        domain_types = ["DOMAIN-SUFFIX", "DOMAIN", "DOMAIN-KEYWORD", "DOMAIN-REGEX", "DOMAIN-WILDCARD", "DomainSuffix"]
        ip_types = ["IP-CIDR", "IP-CIDR6", "IP-SUFFIX", "IPCIDR"]
        
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
        elif rule_type == "DOMAIN-WILDCARD":
            # 处理通配符模式，例如 *.google.com -> domain:google.com
            if content.startswith("*."):
                # *.example.com -> domain:example.com
                domain_part = content[2:]
                return f"domain:{domain_part}"
            elif content.startswith("*"):
                # 如果只是"*"，则转换为keyword
                return "keyword:"
            else:
                # 其他情况，尝试移除通配符并转换为domain
                # 需要更复杂的通配符处理，先暂时转为keyword
                return f"keyword:{content}"
        elif rule_type == "DOMAIN-REGEX":
            return f"regexp:{content}"
        elif rule_type == "IP-CIDR" or rule_type == "IPCIDR":
            return content  # 直接返回CIDR内容，不带前缀
        elif rule_type == "IP-CIDR6":
            return content  # 直接返回CIDR内容，不带前缀
        elif rule_type == "IP-SUFFIX":
            # IP-SUFFIX 格式为 IP 地址加上掩码长度，如 8.8.8.8/24
            # 直接返回，无需前缀
            return content
        elif rule_type == "RULE-SET":
            # RULE-SET 类型的规则格式通常是: RULE-SET,providername,target-policy
            # 这里我们只处理providername部分，target-policy是mihomo的策略，Mosdns不需要
            # RULE-SET规则需要引用已定义的规则集，这里我们简单返回providername
            # 但实际使用中需要根据providername获取对应的规则集内容
            logging.getLogger(__name__).debug(
                "检测到RULE-SET规则",
                extra={
                    "rule_type": rule_type,
                    "content": content
                }
            )
            # 由于RULE-SET规则需要引用外部规则集，在当前上下文中无法直接转换
            # 实际转换应通过fetch_and_parse_ruleset方法处理规则集提供者
            # 返回空字符串表示此规则需要特殊处理
            return ""
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
        仅处理DOMAIN-SUFFIX类型的规则（以*.或+.开头的域名模式）。
        
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
                                    # 正常域名，但需要判断是否包含通配符
                                    if "*" in line:
                                        # 如果包含*通配符，按DOMAIN-WILDCARD处理
                                        if line.startswith("*."):
                                            # *.example.com -> domain:example.com
                                            domain_part = line[2:]
                                            rules.append(f"domain:{domain_part}")
                                        elif line.startswith("*"):
                                            # * -> keyword:
                                            rules.append("keyword:")
                                        else:
                                            # 其他通配符情况，暂时转为keyword
                                            rules.append(f"keyword:{line}")
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
                                # 正常域名，但需要判断是否包含通配符
                                # 优先处理通配符模式
                                if line.startswith("*."):
                                    # *.example.com -> domain:example.com
                                    domain_part = line[2:]
                                    rules.append(f"domain:{domain_part}")
                                elif line.startswith("*"):
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
        仅处理IP-CIDR和IP-SUFFIX规则。
        
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
                                # 检查规则格式，确保是IP-CIDR或IP-SUFFIX格式
                                if '/' in line:  # CIDR格式，如 192.168.0.0/16 或 8.8.8.8/24
                                    rules.append(line)
                                else:
                                    # 不是有效的IP格式，跳过
                                    pass
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
                            # 检查规则格式，确保是IP-CIDR或IP-SUFFIX格式
                            if '/' in line:  # CIDR格式，如 192.168.0.0/16 或 8.8.8.8/24
                                rules.append(line)
                            else:
                                # 不是有效的IP格式，跳过
                                pass
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
                                # 检查并解析支持的经典规则格式 (DOMAIN-SUFFIX,example.com)
                                if line.startswith("DOMAIN-SUFFIX,"):
                                    domain = line.split(",", 1)[1]
                                    rules.append(f"domain:{domain}")
                                elif line.startswith("DOMAIN,"):
                                    domain = line.split(",", 1)[1]
                                    rules.append(f"full:{domain}")
                                elif line.startswith("DOMAIN-KEYWORD,"):
                                    keyword = line.split(",", 1)[1]
                                    rules.append(f"keyword:{keyword}")
                                elif line.startswith("DOMAIN-WILDCARD,"):
                                    wildcard_content = line.split(",", 1)[1]
                                    # 处理通配符模式，例如 *.google.com -> domain:google.com
                                    if wildcard_content.startswith("*."):
                                        domain_part = wildcard_content[2:]
                                        rules.append(f"domain:{domain_part}")
                                    elif wildcard_content.startswith("*"):
                                        rules.append("keyword:")
                                    else:
                                        # 其他情况，暂时转为keyword
                                        rules.append(f"keyword:{wildcard_content}")
                                elif line.startswith("DOMAIN-REGEX,"):
                                    regex = line.split(",", 1)[1]
                                    rules.append(f"regexp:{regex}")
                                elif line.startswith("IP-CIDR,"):
                                    cidr = line.split(",")[1]
                                    # 直接添加CIDR，不带前缀
                                    rules.append(cidr)
                                elif line.startswith("IP-CIDR6,"):
                                    cidr6 = line.split(",", 1)[1]
                                    # 直接添加CIDR，不带前缀
                                    rules.append(cidr6)
                                elif line.startswith("IP-SUFFIX,"):
                                    ip_suffix = line.split(",", 1)[1]
                                    # 直接添加IP-SUFFIX，不带前缀
                                    rules.append(ip_suffix)
                                # 其他规则类型（如GEOSITE, GEOIP等）将被跳过
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
                            # 检查并解析支持的经典规则格式 (DOMAIN-SUFFIX,example.com)
                            if line.startswith("DOMAIN-SUFFIX,"):
                                domain = line.split(",", 1)[1]
                                rules.append(f"domain:{domain}")
                            elif line.startswith("DOMAIN,"):
                                domain = line.split(",", 1)[1]
                                rules.append(f"full:{domain}")
                            elif line.startswith("DOMAIN-KEYWORD,"):
                                keyword = line.split(",", 1)[1]
                                rules.append(f"keyword:{keyword}")
                            elif line.startswith("DOMAIN-WILDCARD,"):
                                wildcard_content = line.split(",", 1)[1]
                                # 处理通配符模式，例如 *.google.com -> domain:google.com
                                if wildcard_content.startswith("*."):
                                    domain_part = wildcard_content[2:]
                                    rules.append(f"domain:{domain_part}")
                                elif wildcard_content.startswith("*"):
                                    rules.append("keyword:")
                                else:
                                    # 其他情况，暂时转为keyword
                                    rules.append(f"keyword:{wildcard_content}")
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
                            elif line.startswith("IP-SUFFIX,"):
                                ip_suffix = line.split(",", 1)[1]
                                # 直接添加IP-SUFFIX，不带前缀
                                rules.append(ip_suffix)
                            # 其他规则类型（如GEOSITE, GEOIP等）将被跳过
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