import logging
import os
import shutil
import time
from typing import Dict, Any, List, Set, Tuple
from mihomo_sync.modules.rule_converter import RuleConverter
from mihomo_sync.modules.policy_resolver import PolicyResolver
from mihomo_sync.modules.mihomo_config_parser import MihomoConfigParser


class RuleGenerationOrchestrator:
    """规则生成分发阶段的协调器。"""
    
    # 定义固定的策略名称
    FIXED_POLICIES = ["DIRECT", "PROXY", "REJECT"]
    
    def __init__(self, api_client, config, mihomo_config_parser=None, mihomo_config_path=""):
        """
        初始化RuleGenerationOrchestrator。
        
        Args:
            api_client: MihomoApiClient的实例
            config: ConfigManager实例
            mihomo_config_parser: MihomoConfigParser实例（可选）
            mihomo_config_path: Mihomo配置文件路径（可选）
        """
        self.api_client = api_client
        self.config = config
        self.mihomo_config_parser = mihomo_config_parser
        self.mihomo_config_path = mihomo_config_path
        self.intermediate_dir = self.config.get_mosdns_config_path() + "_intermediate"
        self.logger = logging.getLogger(__name__)
        self.policy_resolver = PolicyResolver()
        self.logger.debug(
            "规则生成协调器初始化完成",
            extra={
                "intermediate_dir": self.intermediate_dir,
                "mihomo_config_path": mihomo_config_path
            }
        )
    
    async def run(self) -> str:
        """
        执行完整的分发阶段工作流。
        
        Returns:
            str: 生成的中间目录路径
        """
        self.logger.info("正在启动规则生成协调...")
        start_time = time.time()
        
        try:
            # 步骤1：准备工作空间
            self._prepare_workspace()
            
            # 步骤2：从API获取数据
            self.logger.debug("正在从API获取数据...")
            api_start_time = time.time()
            
            rules_data = await self.api_client.get_rules()
            rule_providers_data = await self.api_client.get_rule_providers()
            proxies_data = await self.api_client.get_proxies()
            
            api_duration = time.time() - api_start_time
            self.logger.debug(
                "API数据获取完成",
                extra={
                    "获取耗时_秒": round(api_duration, 3),
                    "规则数量": len(rules_data.get("rules", [])),
                    "提供者数量": len(rule_providers_data.get("providers", {})),
                    "代理数量": len(proxies_data.get("proxies", {}))
                }
            )
            
            # 步骤3：如果可用，从配置文件获取规则提供者信息
            config_provider_info = {}
            config_duration = 0
            if self.mihomo_config_parser and self.mihomo_config_path and os.path.exists(self.mihomo_config_path):
                try:
                    self.logger.debug("正在从配置文件获取规则提供者信息...")
                    config_start_time = time.time()
                    config_data = self.mihomo_config_parser.parse_config_file(self.mihomo_config_path)
                    if config_data:
                        config_provider_info = self.mihomo_config_parser.extract_rule_providers(config_data)
                        config_duration = time.time() - config_start_time
                        self.logger.debug(
                            f"从配置文件加载了 {len(config_provider_info)} 个规则提供者",
                            extra={
                                "加载耗时_秒": round(config_duration, 3)
                            }
                        )
                except Exception as e:
                    self.logger.warning(
                        f"从配置文件加载规则提供者失败: {e}",
                        extra={
                            "error": str(e),
                            "error_type": type(e).__name__
                        }
                    )
            else:
                self.logger.debug("未提供配置文件或文件不存在，跳过配置文件解析")
        
            # 步骤4：合并API和配置提供者信息
            # 配置文件信息优先于API信息
            providers_info = rule_providers_data.get("providers", {})
            providers_info.update(config_provider_info)
            self.logger.debug(
                f"合并后共有 {len(providers_info)} 个规则提供者",
                extra={
                    "api_providers": len(rule_providers_data.get("providers", {})),
                    "config_providers": len(config_provider_info)
                }
            )
            
            # 步骤5：初始化内存聚合器
            # 初始化固定策略的聚合器
            aggregated_rules = {policy: {} for policy in self.FIXED_POLICIES}
            
            # 步骤6：处理规则
            self.logger.debug("正在处理规则...")
            process_start_time = time.time()
            await self._process_rules(rules_data, providers_info, proxies_data, aggregated_rules)
            process_duration = time.time() - process_start_time
            
            self.logger.debug(
                "规则处理完成",
                extra={
                    "处理耗时_秒": round(process_duration, 3)
                }
            )
            
            # 步骤7：写入中间文件
            self.logger.debug("正在写入中间文件...")
            write_start_time = time.time()
            self._write_intermediate_files(aggregated_rules)
            write_duration = time.time() - write_start_time
            
            total_duration = time.time() - start_time
            self.logger.info(
                f"中间文件成功生成于: {self.intermediate_dir}",
                extra={
                    "总耗时_秒": round(total_duration, 3),
                    "API获取耗时_秒": round(api_duration, 3),
                    "配置解析耗时_秒": round(config_duration, 3),
                    "规则处理耗时_秒": round(process_duration, 3),
                    "文件写入耗时_秒": round(write_duration, 3)
                }
            )
            
            return self.intermediate_dir
            
        except Exception as e:
            total_duration = time.time() - start_time
            self.logger.error(
                "规则生成协调过程中发生错误",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "总耗时_秒": round(total_duration, 3)
                }
            )
            raise
    
    def _prepare_workspace(self) -> None:
        """通过清理和创建中间目录来准备工作空间。"""
        start_time = time.time()
        if os.path.exists(self.intermediate_dir):
            shutil.rmtree(self.intermediate_dir)
            self.logger.debug(f"已清理中间目录: {self.intermediate_dir}")
        
        os.makedirs(self.intermediate_dir)
        duration = time.time() - start_time
        self.logger.debug(
            f"已创建中间目录: {self.intermediate_dir}",
            extra={
                "准备耗时_秒": round(duration, 3)
            }
        )
    
    def _write_intermediate_files(self, aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        将聚合的规则写入中间文件。
        
        Args:
            aggregated_rules: 聚合的规则数据
        """
        self.logger.debug("开始写入中间文件...")
        start_time = time.time()
        
        # 为每个策略创建文件
        for policy, rule_types in aggregated_rules.items():
            policy_dir = os.path.join(self.intermediate_dir, policy.lower())
            os.makedirs(policy_dir, exist_ok=True)
            
            # 写入域名规则
            if "domain" in rule_types:
                domain_file_path = os.path.join(policy_dir, "domain.txt")
                with open(domain_file_path, "w", encoding="utf-8") as f:
                    # 收集所有域名规则
                    all_domain_rules = set()
                    for provider_rules in rule_types["domain"].values():
                        all_domain_rules.update(provider_rules)
                    
                    # 写入规则，每行一个
                    for rule in sorted(all_domain_rules):
                        f.write(rule + "\n")
                
                self.logger.debug(
                    f"已写入域名规则文件: {domain_file_path}",
                    extra={
                        "策略": policy,
                        "规则数量": len(all_domain_rules)
                    }
                )
            
            # 写入IP CIDR规则
            if "ipcidr" in rule_types:
                ipcidr_file_path = os.path.join(policy_dir, "ipcidr.txt")
                with open(ipcidr_file_path, "w", encoding="utf-8") as f:
                    # 收集所有IP CIDR规则
                    all_ipcidr_rules = set()
                    for provider_rules in rule_types["ipcidr"].values():
                        all_ipcidr_rules.update(provider_rules)
                    
                    # 写入规则，每行一个
                    for rule in sorted(all_ipcidr_rules):
                        f.write(rule + "\n")
                
                self.logger.debug(
                    f"已写入IP CIDR规则文件: {ipcidr_file_path}",
                    extra={
                        "策略": policy,
                        "规则数量": len(all_ipcidr_rules)
                    }
                )
        
        duration = time.time() - start_time
        self.logger.debug(
            "中间文件写入完成",
            extra={
                "写入耗时_秒": round(duration, 3)
            }
        )
    
    async def _process_rules(self, rules_data: Dict[str, Any], providers_info: Dict[str, Any], 
                             proxies_data: Dict[str, Any],
                             aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        处理所有规则并在内存中聚合它们。
        
        Args:
            rules_data: 来自Mihomo API的规则数据
            providers_info: 所有规则提供者的信息（从API和配置合并）
            proxies_data: 来自Mihomo API的代理数据
            aggregated_rules: 用于固定策略的规则内存聚合器
        """
        self.logger.debug("开始处理规则...")
        start_time = time.time()
        
        rules = rules_data.get("rules", [])
        self.logger.debug(f"共有 {len(rules)} 条规则需要处理")
        
        processed_count = 0
        rule_set_count = 0
        single_rule_count = 0
        
        # 处理每个规则
        for i, rule in enumerate(rules):
            rule_type = rule.get("type", "")
            
            if rule_type.lower() == "ruleset":
                # 处理RULE-SET类型规则
                await self._process_rule_set_rule(rule, providers_info, proxies_data, aggregated_rules)
                rule_set_count += 1
            else:
                # 处理单个规则
                self._process_single_rule(rule, proxies_data, aggregated_rules)
                single_rule_count += 1
            
            processed_count += 1
            
            # 每处理100条规则记录一次进度
            if processed_count % 100 == 0:
                self.logger.debug(
                    f"已处理 {processed_count}/{len(rules)} 条规则",
                    extra={
                        "rule_set_count": rule_set_count,
                        "single_rule_count": single_rule_count
                    }
                )
        
        duration = time.time() - start_time
        self.logger.debug(
            "规则处理完成",
            extra={
                "总规则数": len(rules),
                "已处理规则数": processed_count,
                "RULE_SET规则数": rule_set_count,
                "单个规则数": single_rule_count,
                "处理耗时_秒": round(duration, 3)
            }
        )
    
    async def _process_rule_set_rule(self, rule: Dict[str, Any], providers_info: Dict[str, Any],
                                     proxies_data: Dict[str, Any],
                                     aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        处理RULE-SET类型规则。
        
        Args:
            rule: 要处理的RULE-SET规则
            providers_info: 所有规则提供者的信息
            proxies_data: 来自Mihomo API的代理数据
            aggregated_rules: 用于固定策略的规则内存聚合器
        """
        try:
            policy = rule.get("proxy") or rule.get("provider", "")
            provider_name = rule.get("payload", "")
            
            # 如果没有策略或提供者名称则跳过
            if not policy or not provider_name:
                self.logger.warning(
                    f"跳过缺少策略或提供者的RULE-SET规则: {rule}",
                    extra={
                        "policy": policy,
                        "provider_name": provider_name
                    }
                )
                return
            
            # 使用PolicyResolver解析最终策略
            resolved_policy = self.policy_resolver.resolve(policy, proxies_data)
            
            # 仅处理具有固定策略的规则
            if resolved_policy not in self.FIXED_POLICIES:
                self.logger.debug(
                    f"跳过具有非固定策略的RULE-SET规则: {resolved_policy}",
                    extra={
                        "original_policy": policy,
                        "resolved_policy": resolved_policy
                    }
                )
                return
            
            # 查找提供者信息
            if provider_name not in providers_info:
                self.logger.warning(
                    f"在提供者信息中未找到提供者 '{provider_name}'",
                    extra={
                        "provider_name": provider_name,
                        "available_providers": list(providers_info.keys())[:10]  # 只显示前10个
                    }
                )
                return
                
            provider_info = providers_info[provider_name]
            
            # 获取和解析规则集内容
            self.logger.debug(
                f"正在获取规则集内容: {provider_name}",
                extra={
                    "provider_name": provider_name
                }
            )
            
            content_list = RuleConverter.fetch_and_parse_ruleset(provider_info)
            self.logger.debug(
                f"规则集 {provider_name} 包含 {len(content_list)} 条规则"
            )
            
            # 分离域名和ipcidr规则
            domain_rules = set()
            ipcidr_rules = set()
            
            for rule_item in content_list:
                if rule_item.startswith(("domain:", "full:", "keyword:", "regexp:")):
                    domain_rules.add(rule_item)
                elif "/" in rule_item and (any(c in rule_item for c in [".", ":"])):  # IP规则通常包含"/"和IP地址字符
                    ipcidr_rules.add(rule_item)
                else:
                    # 对于未知类型默认为域名规则
                    domain_rules.add(rule_item)
            
            # 如果有任何域名规则，则添加到聚合器
            if domain_rules:
                aggregated_rules.setdefault(resolved_policy, {}).setdefault("domain", {}).setdefault(provider_name, set()).update(domain_rules)
            
            # 检查并分离IPv4和IPv6规则
            ipv4_rules = set()
            ipv6_rules = set()
            
            for rule in ipcidr_rules:
                if ":" in rule and "." not in rule:  # IPv6规则
                    ipv6_rules.add(rule)
                else:  # IPv4规则
                    ipv4_rules.add(rule)
            
            # 如果有任何IPv4规则，则添加到IPv4聚合器
            if ipv4_rules:
                aggregated_rules.setdefault(resolved_policy, {}).setdefault("ipv4", {}).setdefault(provider_name, set()).update(ipv4_rules)
                
            # 如果有任何IPv6规则，则添加到IPv6聚合器
            if ipv6_rules:
                aggregated_rules.setdefault(resolved_policy, {}).setdefault("ipv6", {}).setdefault(provider_name, set()).update(ipv6_rules)
            
            self.logger.debug(
                f"已处理RULE-SET规则: {provider_name} -> {len(domain_rules)} 个域名规则, {len(ipcidr_rules)} 个ipcidr规则，策略为 {resolved_policy}",
                extra={
                    "provider_name": provider_name,
                    "domain_rules_count": len(domain_rules),
                    "ipcidr_rules_count": len(ipcidr_rules),
                    "resolved_policy": resolved_policy
                }
            )
        except Exception as e:
            self.logger.error(
                f"处理RULE-SET规则时出错: {e}",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "rule": rule
                },
                exc_info=True
            )
    
    def _process_single_rule(self, rule: Dict[str, Any], proxies_data: Dict[str, Any],
                             aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        处理单个规则（非RULE-SET）。
        
        Args:
            rule: 要处理的单个规则
            proxies_data: 来自Mihomo API的代理数据
            aggregated_rules: 用于固定策略的规则内存聚合器
        """
        try:
            policy = rule.get("proxy") or rule.get("provider", "")
            
            # 如果没有策略则跳过
            if not policy:
                self.logger.warning(
                    f"跳过缺少策略的单个规则: {rule}",
                    extra={
                        "rule": rule
                    }
                )
                return
            
            # 使用PolicyResolver解析最终策略
            resolved_policy = self.policy_resolver.resolve(policy, proxies_data)
            
            # 仅处理具有固定策略的规则
            if resolved_policy not in self.FIXED_POLICIES:
                self.logger.debug(
                    f"跳过具有非固定策略的单个规则: {resolved_policy}",
                    extra={
                        "original_policy": policy,
                        "resolved_policy": resolved_policy
                    }
                )
                return
            
            # 使用RuleConverter转换规则，这会处理我们支持的规则类型
            mosdns_rule, content_type = RuleConverter.convert_single_rule(rule)
            
            # 如果转换成功，则处理转换后的规则
            if mosdns_rule and content_type:
                # 根据内容类型确定要使用的聚合器
                if content_type == "domain":
                    aggregated_rules.setdefault(resolved_policy, {}).setdefault("domain", {}).setdefault("single_rules", set()).add(mosdns_rule)
                elif content_type == "ipcidr":
                    # 对于IP CIDR规则，需要进一步区分IPv4和IPv6
                    if ":" in mosdns_rule and "." not in mosdns_rule:  # IPv6规则
                        aggregated_rules.setdefault(resolved_policy, {}).setdefault("ipv6", {}).setdefault("single_rules", set()).add(mosdns_rule)
                    else:  # IPv4规则
                        aggregated_rules.setdefault(resolved_policy, {}).setdefault("ipv4", {}).setdefault("single_rules", set()).add(mosdns_rule)
                elif content_type in ["ipv4", "ipv6"]:
                    # 如果RuleConverter已经明确指定了IPv4或IPv6
                    aggregated_rules.setdefault(resolved_policy, {}).setdefault(content_type, {}).setdefault("single_rules", set()).add(mosdns_rule)
            
            self.logger.debug(
                f"已处理单个规则: 类型={rule.get('type', '')}, 策略={resolved_policy}",
                extra={
                    "rule_type": rule.get("type", ""),
                    "payload": rule.get("payload", ""),
                    "resolved_policy": resolved_policy
                }
            )
        except Exception as e:
            self.logger.error(
                f"处理单个规则时出错: {e}",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "rule": rule
                }
            )