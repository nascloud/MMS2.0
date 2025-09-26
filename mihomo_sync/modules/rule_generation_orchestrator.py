import logging
import os
import shutil
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
    
    async def run(self) -> str:
        """
        执行完整的分发阶段工作流。
        
        Returns:
            str: 生成的中间目录路径
        """
        self.logger.info("正在启动规则生成协调...")
        
        # 步骤1：准备工作空间
        self._prepare_workspace()
        
        # 步骤2：从API获取数据
        rules_data = await self.api_client.get_rules()
        rule_providers_data = await self.api_client.get_rule_providers()
        proxies_data = await self.api_client.get_proxies()
        
        # 步骤3：如果可用，从配置文件获取规则提供者信息
        config_provider_info = {}
        if self.mihomo_config_parser and self.mihomo_config_path and os.path.exists(self.mihomo_config_path):
            try:
                config_data = self.mihomo_config_parser.parse_config_file(self.mihomo_config_path)
                if config_data:
                    config_provider_info = self.mihomo_config_parser.extract_rule_providers(config_data)
                    self.logger.debug(f"从配置文件加载了 {len(config_provider_info)} 个规则提供者")
            except Exception as e:
                self.logger.warning(f"从配置文件加载规则提供者失败: {e}")
        
        # 步骤4：合并API和配置提供者信息
        # 配置文件信息优先于API信息
        providers_info = rule_providers_data.get("providers", {})
        providers_info.update(config_provider_info)
        
        # 步骤5：初始化内存聚合器
        # 初始化固定策略的聚合器
        aggregated_rules = {policy: {} for policy in self.FIXED_POLICIES}
        
        # 步骤6：处理规则
        await self._process_rules(rules_data, providers_info, proxies_data, aggregated_rules)
        
        # 步骤7：写入中间文件
        self._write_intermediate_files(aggregated_rules)
        
        self.logger.info(f"中间文件成功生成于: {self.intermediate_dir}")
        return self.intermediate_dir
    
    def _prepare_workspace(self) -> None:
        """通过清理和创建中间目录来准备工作空间。"""
        if os.path.exists(self.intermediate_dir):
            shutil.rmtree(self.intermediate_dir)
        os.makedirs(self.intermediate_dir)
        self.logger.debug(f"已清理并创建中间目录: {self.intermediate_dir}")
    
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
        # 处理每个规则
        for rule in rules_data.get("rules", []):
            rule_type = rule.get("type", "")
            
            if rule_type.lower() == "ruleset":
                # 处理RULE-SET类型规则
                await self._process_rule_set_rule(rule, providers_info, proxies_data, aggregated_rules)
            else:
                # 处理单个规则
                self._process_single_rule(rule, proxies_data, aggregated_rules)
    
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
                self.logger.warning(f"跳过缺少策略或提供者的RULE-SET规则: {rule}")
                return
            
            # 使用PolicyResolver解析最终策略
            resolved_policy = self.policy_resolver.resolve(policy, proxies_data)
            
            # 仅处理具有固定策略的规则
            if resolved_policy not in self.FIXED_POLICIES:
                self.logger.debug(f"跳过具有非固定策略的RULE-SET规则: {resolved_policy}")
                return
            
            # 查找提供者信息
            if provider_name not in providers_info:
                self.logger.warning(f"在提供者信息中未找到提供者 '{provider_name}'")
                return
                
            provider_info = providers_info[provider_name]
            
            # 获取和解析规则集内容
            content_list = RuleConverter.fetch_and_parse_ruleset(provider_info)
            
            # 分离域名和ipcidr规则
            domain_rules = set()
            ipcidr_rules = set()
            
            for rule_item in content_list:
                if rule_item.startswith(("domain:", "full:", "keyword:", "regexp:")):
                    domain_rules.add(rule_item)
                elif rule_item.startswith(("ip-cidr:", "ip-cidr6:")) or any(c in rule_item for c in [".", ":"]) and "/" in rule_item:
                    # IP-CIDR规则通常包含"."或":"和"/"
                    ipcidr_rules.add(rule_item)
                else:
                    # 对于未知类型默认为域名规则
                    domain_rules.add(rule_item)
            
            # 如果有任何域名规则，则添加到聚合器
            if domain_rules:
                aggregated_rules.setdefault(resolved_policy, {}).setdefault("domain", {}).setdefault(provider_name, set()).update(domain_rules)
            
            # 如果有任何ipcidr规则，则添加到聚合器
            if ipcidr_rules:
                aggregated_rules.setdefault(resolved_policy, {}).setdefault("ipcidr", {}).setdefault(provider_name, set()).update(ipcidr_rules)
            
            self.logger.debug(f"已处理RULE-SET规则: {provider_name} -> {len(domain_rules)} 个域名规则, {len(ipcidr_rules)} 个ipcidr规则，策略为 {resolved_policy}")
        except Exception as e:
            self.logger.error(f"处理RULE-SET规则时出错: {e}", exc_info=True)
    
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
                self.logger.warning(f"跳过缺少策略的单个规则: {rule}")
                return
            
            # 使用PolicyResolver解析最终策略
            resolved_policy = self.policy_resolver.resolve(policy, proxies_data)
            
            # 仅处理具有固定策略的规则
            if resolved_policy not in self.FIXED_POLICIES:
                self.logger.debug(f"跳过具有非固定策略的单个规则: {resolved_policy}")
                return
            
            # 转换单个规则
            mosdns_rule, content_type = RuleConverter.convert_single_rule(rule)
            
            # 如果转换失败则跳过
            if mosdns_rule is None or content_type is None:
                self.logger.debug(f"跳过不支持的规则: {rule}")
                return
            
            # 使用特殊 _inline 提供者名称添加到聚合器
            aggregated_rules.setdefault(resolved_policy, {}).setdefault(content_type, {}).setdefault("_inline", set()).add(mosdns_rule)
            
            self.logger.debug(f"已处理单个规则: {rule} -> {mosdns_rule}，策略为 {resolved_policy}")
        except Exception as e:
            self.logger.error(f"处理单个规则时出错: {e}", exc_info=True)
    
    def _write_intermediate_files(self, aggregated_rules: Dict[str, Dict[str, Dict[str, Set[str]]]]) -> None:
        """
        将聚合的规则写入中间文件。
        
        Args:
            aggregated_rules: 包含所有规则的内存聚合器
        """
        # 确保固定策略文件夹都存在，即使没有规则
        for policy in self.FIXED_POLICIES:
            if policy not in aggregated_rules:
                aggregated_rules[policy] = {}
        
        for policy, types in aggregated_rules.items():
            # 只处理固定策略
            if policy not in self.FIXED_POLICIES:
                continue
                
            for content_type, providers in types.items():
                for provider_name, rule_set in providers.items():
                    # 跳过空规则集
                    if not rule_set:
                        continue
                    
                    # 创建目标目录
                    target_dir = os.path.join(self.intermediate_dir, policy, content_type)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # 确定文件名
                    filename = f"provider_{provider_name}.list" if provider_name != "_inline" else "_inline_rules.list"
                    filepath = os.path.join(target_dir, filename)
                    
                    # 将规则写入文件
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(sorted(list(rule_set))))
                        self.logger.debug(f"已将 {len(rule_set)} 条规则写入 {filepath}")
                    except Exception as e:
                        self.logger.error(f"写入中间文件 {filepath} 失败: {e}")