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
        
        Args:
            intermediate_path (str): 中间文件目录路径
            final_output_path (str): 最终输出目录路径
        """
        # 遍历中间目录结构
        for root, dirs, files in os.walk(intermediate_path):
            # 如果此目录中没有文件则跳过
            if not files:
                continue
            
            # 从目录结构确定策略和内容类型
            rel_path = os.path.relpath(root, intermediate_path)
            path_parts = rel_path.split(os.sep)
            
            # 我们期望的路径结构为: policy/content_type
            if len(path_parts) != 2:
                continue
                
            policy, content_type = path_parts
            
            # 合并此目录中的规则
            self._merge_directory_rules(root, policy, content_type, final_output_path)
    
    def _merge_directory_rules(self, directory_path: str, policy: str, content_type: str, final_output_path: str) -> None:
        """
        合并特定目录中的所有规则。
        
        Args:
            directory_path (str): 包含规则文件的目录路径
            policy (str): 策略名称
            content_type (str): 内容类型 (domain, ipcidr等)
            final_output_path (str): 最终输出目录路径
        """
        try:
            # 步骤1：从.list文件收集所有规则
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
                            "读取规则文件失败",
                            extra={
                                "rule_file": filepath,
                                "error": str(e)
                            }
                        )
            
            # 步骤2：如果非空则写入最终规则
            if final_rules:
                # 根据策略和内容类型创建平面文件名
                # 转换为小写并替换内容类型映射
                policy_lower = policy.lower()
                if content_type == "domain":
                    output_filename = f"{policy_lower}_domain.txt"
                elif content_type == "ipcidr":
                    # 检查集合中是否有IPv6规则
                    # IPv6地址包含":"但不包含"."，IPv4地址包含"."
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
                                    "合并目录规则 (IPv4)",
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
                                    "合并目录规则 (IPv6)",
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
                        # 跳过默认写入，因为我们已经写入了单独的文件
                        return
                    elif has_ipv6:
                        # 仅IPv6规则
                        output_filename = f"{policy_lower}_ipv6.txt"
                    else:
                        # 仅IPv4规则
                        output_filename = f"{policy_lower}_ipv4.txt"
                else:
                    output_filename = f"{policy_lower}_{content_type}.txt"
                
                # 完整的输出文件路径
                output_filepath = os.path.join(final_output_path, output_filename)
                
                try:
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(sorted(list(final_rules))))
                    self.logger.debug(
                        "合并目录规则",
                        extra={
                            "policy": policy,
                            "content_type": content_type,
                            "rules_count": len(final_rules),
                            "output_file": output_filepath
                        }
                    )
                except Exception as e:
                    self.logger.error(
                        "写入最终规则文件失败",
                        extra={
                            "output_file": output_filepath,
                            "error": str(e)
                        }
                    )
                    raise
        except Exception as e:
            self.logger.error(
                "合并目录规则失败",
                extra={
                    "directory_path": directory_path,
                    "policy": policy,
                    "content_type": content_type,
                    "final_output_path": final_output_path,
                    "error": str(e)
                }
            )
            raise