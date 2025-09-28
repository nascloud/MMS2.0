import logging
import os
import shutil
from typing import Set


class RuleMerger:
    """将中间文件合并为最终Mosdns规则文件的合并器。"""
    
    def __init__(self):
        """初始化RuleMerger。"""
        self.logger = logging.getLogger(__name__)
    
    def merge_from_intermediate(self, intermediate_path: str, final_output_path: str) -> None:
        """
        将中间文件中的规则合并为最终的Mosdns规则文件。
        
        Args:
            intermediate_path (str): 中间文件目录路径
            final_output_path (str): 最终输出目录路径
        """
        try:
            # 步骤1：准备工作空间
            self._prepare_workspace(final_output_path)
            
            # 步骤2：处理中间目录
            self._process_intermediate_directory(intermediate_path, final_output_path)
            
            # 添加文件更新验证
            if os.path.exists(final_output_path):
                file_count = len([f for f in os.listdir(final_output_path) if os.path.isfile(os.path.join(final_output_path, f))])
                self.logger.info(
                    "文件更新验证完成",
                    extra={
                        "output_directory": final_output_path,
                        "文件数量": file_count
                    }
                )

            self.logger.info(
                "所有规则合并成功",
                extra={
                    "intermediate_path": intermediate_path,
                    "final_output_path": final_output_path
                }
            )
        except Exception as e:
            self.logger.error(
                "合并规则失败",
                extra={
                    "intermediate_path": intermediate_path,
                    "final_output_path": final_output_path,
                    "error": str(e)
                }
            )
            raise
    
    def _prepare_workspace(self, final_output_path: str) -> None:
        """
        通过清理和创建最终输出目录来准备工作空间。
        
        Args:
            final_output_path (str): 最终输出目录路径
        """
        if os.path.exists(final_output_path):
            shutil.rmtree(final_output_path)
        os.makedirs(final_output_path)
        self.logger.debug(f"已清理并创建最终输出目录: {final_output_path}")
    
    def _process_intermediate_directory(self, intermediate_path: str, final_output_path: str) -> None:
        """
        处理中间目录并合并规则。
        """
        for policy in ["direct", "proxy", "reject"]:
            policy_dir = os.path.join(intermediate_path, policy)
            if not os.path.isdir(policy_dir):
                continue
            # 合并 domain 规则
            domain_dir = os.path.join(policy_dir, "domain")
            domain_rules = set()
            if os.path.isdir(domain_dir):
                for fname in os.listdir(domain_dir):
                    if fname.endswith(".list"):
                        fpath = os.path.join(domain_dir, fname)
                        try:
                            with open(fpath, "r", encoding="utf-8") as f:
                                for line in f:
                                    rule = line.strip()
                                    if rule:
                                        domain_rules.add(rule)
                        except Exception as e:
                            self.logger.warning(
                                "读取域名规则文件失败",
                                extra={"rule_file": fpath, "error": str(e)}
                            )
            if domain_rules:
                output_filename = f"{policy}_domain.txt"
                output_filepath = os.path.join(final_output_path, output_filename)
                with open(output_filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(sorted(domain_rules)))
                self.logger.debug(
                    "合并域名规则文件",
                    extra={
                        "policy": policy,
                        "rules_count": len(domain_rules),
                        "output_file": output_filepath
                    }
                )
            # 合并 ipv4/ipv6/ipcidr 文件
            for fname in [f"{policy}_ipv4.txt", f"{policy}_ipv6.txt", f"{policy}_ipcidr.txt"]:
                src_path = os.path.join(policy_dir, fname)
                if os.path.isfile(src_path):
                    with open(src_path, "r", encoding="utf-8") as f:
                        rules = [line.strip() for line in f if line.strip()]
                    if rules:
                        dst_path = os.path.join(final_output_path, fname)
                        with open(dst_path, "w", encoding="utf-8") as fout:
                            fout.write("\n".join(sorted(rules)))
                        self.logger.debug(
                            "合并IP规则文件",
                            extra={
                                "policy": policy,
                                "output_file": dst_path,
                                "rules_count": len(rules)
                            }
                        )
    
    def _merge_file_rules(self, file_path: str, policy: str, content_type: str, final_output_path: str) -> None:
        """
        合并特定文件中的规则。
        
        Args:
            file_path (str): 规则文件的路径
            policy (str): 策略名称
            content_type (str): 内容类型 (domain, ipv4, ipv6等)
            final_output_path (str): 最终输出目录路径
        """
        try:
            # 步骤1：从文件收集所有规则
            final_rules: Set[str] = set()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                    final_rules.update(lines)
            except Exception as e:
                self.logger.warning(
                    "读取规则文件失败",
                    extra={
                        "rule_file": file_path,
                        "error": str(e)
                    }
                )
        
            # 步骤2：如果非空则写入最终规则
            if final_rules:
                # 根据策略和内容类型创建平面文件名
                policy_lower = policy.lower()
                
                # 对于IPv4类型的特殊处理：如果内容中包含IPv6规则，需要拆分
                if content_type == "ipv4":
                    # 检查内容中是否有IPv6规则
                    has_ipv6 = any(":" in rule and "." not in rule for rule in final_rules)
                    has_ipv4 = any("." in rule for rule in final_rules)
                    
                    # 如果同时有IPv4和IPv6规则，则需要分离
                    if has_ipv6 and has_ipv4:
                        ipv4_rules = {rule for rule in final_rules if "." in rule}
                        if ipv4_rules:
                            output_filename = f"{policy_lower}_ipv4.txt"
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv4_rules))))
                                self.logger.debug(
                                    "合并文件规则 (IPv4)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv4_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "写入最终规则文件失败 (IPv4)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                        
                        # 创建IPv6文件
                        ipv6_rules = {rule for rule in final_rules if ":" in rule and "." not in rule}
                        if ipv6_rules:
                            output_filename = f"{policy_lower}_ipv6.txt"
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv6_rules))))
                                self.logger.debug(
                                    "合并文件规则 (IPv6)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv6_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "写入最终规则文件失败 (IPv6)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                    else:
                        # 只有一类IP规则，直接写入
                        output_filename = f"{policy_lower}_{content_type}.txt"
                        output_filepath = os.path.join(final_output_path, output_filename)
                        
                        with open(output_filepath, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(sorted(list(final_rules))))
                        self.logger.debug(
                            "合并文件规则",
                            extra={
                                "policy": policy,
                                "content_type": content_type,
                                "rules_count": len(final_rules),
                                "output_file": output_filepath
                            }
                        )
                elif content_type == "domain":
                    # 域名规则直接写入
                    output_filename = f"{policy_lower}_{content_type}.txt"
                    output_filepath = os.path.join(final_output_path, output_filename)
                    
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(sorted(list(final_rules))))
                    self.logger.debug(
                        "合并文件规则",
                        extra={
                            "policy": policy,
                            "content_type": content_type,
                            "rules_count": len(final_rules),
                            "output_file": output_filepath
                        }
                    )
                elif content_type == "ipcidr":
                    # 检查内容中是否有IPv6规则
                    has_ipv6 = any(":" in rule and "." not in rule for rule in final_rules)
                    has_ipv4 = any("." in rule for rule in final_rules)
                    
                    # 如果我们同时有IPv4和IPv6规则，则创建单独的文件
                    if has_ipv6 and has_ipv4:
                        # 创建IPv4文件
                        ipv4_rules = {rule for rule in final_rules if "." in rule}
                        if ipv4_rules:
                            output_filename = f"{policy_lower}_ipv4.txt"
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv4_rules))))
                                self.logger.debug(
                                    "合并文件规则 (IPv4)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv4_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "写入最终规则文件失败 (IPv4)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                        
                        # 创建IPv6文件
                        ipv6_rules = {rule for rule in final_rules if ":" in rule and "." not in rule}
                        if ipv6_rules:
                            output_filename = f"{policy_lower}_ipv6.txt"
                            output_filepath = os.path.join(final_output_path, output_filename)
                            try:
                                with open(output_filepath, 'w', encoding='utf-8') as f:
                                    f.write('\n'.join(sorted(list(ipv6_rules))))
                                self.logger.debug(
                                    "合并文件规则 (IPv6)",
                                    extra={
                                        "policy": policy,
                                        "content_type": content_type,
                                        "rules_count": len(ipv6_rules),
                                        "output_file": output_filepath
                                    }
                                )
                            except Exception as e:
                                self.logger.error(
                                    "写入最终规则文件失败 (IPv6)",
                                    extra={
                                        "output_file": output_filepath,
                                        "error": str(e)
                                    }
                                )
                                raise
                    elif has_ipv6:
                        # 仅IPv6规则
                        output_filename = f"{policy_lower}_ipv6.txt"
                        output_filepath = os.path.join(final_output_path, output_filename)
                        
                        with open(output_filepath, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(sorted(list(final_rules))))
                        self.logger.debug(
                            "合并文件规则",
                            extra={
                                "policy": policy,
                                "content_type": content_type,
                                "rules_count": len(final_rules),
                                "output_file": output_filepath
                            }
                        )
                    else:
                        # 仅IPv4规则
                        output_filename = f"{policy_lower}_ipv4.txt"
                        output_filepath = os.path.join(final_output_path, output_filename)
                        
                        with open(output_filepath, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(sorted(list(final_rules))))
                        self.logger.debug(
                            "合并文件规则",
                            extra={
                                "policy": policy,
                                "content_type": content_type,
                                "rules_count": len(final_rules),
                                "output_file": output_filepath
                            }
                        )
                else:
                    # 其他内容类型直接写入
                    output_filename = f"{policy_lower}_{content_type}.txt"
                    output_filepath = os.path.join(final_output_path, output_filename)
                    
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(sorted(list(final_rules))))
                    self.logger.debug(
                        "合并文件规则",
                        extra={
                            "policy": policy,
                            "content_type": content_type,
                            "rules_count": len(final_rules),
                            "output_file": output_filepath
                        }
                    )
        except Exception as e:
            self.logger.error(
                "合并文件规则失败",
                extra={
                    "file_path": file_path,
                    "policy": policy,
                    "content_type": content_type,
                    "final_output_path": final_output_path,
                    "error": str(e)
                }
            )
            raise