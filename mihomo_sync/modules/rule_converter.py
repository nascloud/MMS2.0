import logging
import os
from typing import Dict, Any, List, Tuple, Callable


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
            elif rule_type == "IP-SUFFIX":
                # IP-SUFFIX可能是IPv4或IPv6，需要根据内容判断
                # 但由于我们只在这里处理类型名称，返回通用的ipcidr
                # 实际区分将在RuleGenerationOrchestrator中完成
                return "ipcidr"
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
    def parse_ruleset_from_file(file_path: str, behavior: str) -> List[str]:
        """
        从给定的本地文件路径解析规则集。

        Args:
            file_path: 规则集的本地文件路径。
            behavior: 规则的行为 (domain, ipcidr, classical)，决定了解析方式。
            
        Returns:
            Mosdns格式的规则列表。
        """
        if not os.path.exists(file_path):
            logging.getLogger(__name__).warning(f"规则文件不存在，无法解析: {file_path}")
            return []

        parser = RuleConverter._get_parser_for_behavior(behavior)
        if not parser:
            logging.getLogger(__name__).warning(f"不支持的行为类型: {behavior}")
            return []

        try:
            rules = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parsed_rule = parser(line)
                        if parsed_rule:
                            rules.append(parsed_rule)
            return rules
        except Exception as e:
            logging.getLogger(__name__).error(f"解析文件失败: {file_path}, 错误: {e}")
            return []

    # --- 私有解析辅助方法 ---
    
    @staticmethod
    def _get_parser_for_behavior(behavior: str) -> Callable[[str], str] | None:
        """根据行为返回对应的行解析器。"""
        behavior_map = {
            "domain": RuleConverter._parse_domain_line,
            "ipcidr": RuleConverter._parse_ipcidr_line,
            "classical": RuleConverter._parse_classical_line,
        }
        return behavior_map.get(behavior.lower())

    @staticmethod
    def _parse_domain_line(line: str) -> str:
        if line.startswith(("+.", "*.")):
            return f"domain:{line[2:]}"
        if line.startswith("."):
            return f"domain:{line[1:]}"
        return f"domain:{line}"

    @staticmethod
    def _parse_ipcidr_line(line: str) -> str | None:
        return line if '/' in line else None

    @staticmethod
    def _parse_classical_line(line: str) -> str | None:
        parts = line.split(',', 1)
        if len(parts) != 2: return None
        rule_type, content = parts
        
        if rule_type == "DOMAIN-SUFFIX": return f"domain:{content}"
        if rule_type == "DOMAIN": return f"full:{content}"
        if rule_type == "IP-CIDR": return content
        # ...可以补充更多classical类型...
        return None
    
    
    
    
    
    