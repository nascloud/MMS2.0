import logging
from typing import Dict, Any, Set


class PolicyResolver:
    """一个用于解析策略链并找到最终出口节点的类。"""
    
    # 定义标准的返回类型
    DIRECT = "DIRECT"
    PROXY = "PROXY"
    REJECT = "REJECT"
    
    def __init__(self):
        """
        初始化PolicyResolver。
        """
        self.logger = logging.getLogger(__name__)
        # 用于记忆化的缓存，避免重复计算
        self._cache = {}
        # 动态存储策略组类型
        self._strategy_group_types = set()
        
    def resolve(self, policy_name: str, proxies_data: Dict[str, Any]) -> str:
        """
        将策略名称解析为其最终出口节点。
        
        Args:
            policy_name (str): 要解析的策略名称。
            proxies_data (dict): 来自API的所有代理/策略组数据。
            
        Returns:
            str: 标准化的策略结果 (DIRECT, PROXY, 或 REJECT)。
        """
        # 首先检查缓存
        cache_key = f"{policy_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        # 从代理数据中识别策略组类型
        self._identify_strategy_group_types(proxies_data)
            
        # 使用空的已访问集开始解析
        result = self._resolve_recursive(policy_name, set(), proxies_data)
        
        # 标准化返回值
        standardized_result = self._standardize_result(result, policy_name, proxies_data)
        
        # 缓存结果
        self._cache[cache_key] = standardized_result
        return standardized_result
        
    def _identify_strategy_group_types(self, proxies_data: Dict[str, Any]) -> None:
        """
        从代理数据中识别策略组类型。
        
        Args:
            proxies_data (dict): 来自API的所有代理/策略组数据。
        """
        proxies = proxies_data.get("proxies", {})
        for proxy_data in proxies.values():
            proxy_type = proxy_data.get("type")
            # 策略组通常具有包含代理列表的"all"字段
            if proxy_type and "all" in proxy_data and isinstance(proxy_data["all"], list):
                self._strategy_group_types.add(proxy_type)
                
        # 记录识别出的策略组类型
        if self._strategy_group_types:
            self.logger.debug(f"识别出的策略组类型: {self._strategy_group_types}")
        
    def _resolve_recursive(self, policy_name: str, visited: Set[str], proxies_data: Dict[str, Any]) -> str:
        """
        递归解析策略名称，检测循环依赖。
        
        Args:
            policy_name (str): 要解析的策略名称。
            visited (set): 当前解析路径中的策略名称集。
            proxies_data (dict): 来自API的所有代理/策略组数据。
            
        Returns:
            str: 最终出口节点的名称。
        """
        # 检查是否在当前路径中已经访问过此策略（循环依赖）
        if policy_name in visited:
            self.logger.error(
                "策略解析中检测到循环依赖",
                extra={
                    "policy_name": policy_name,
                    "visited_path": list(visited)
                }
            )
            # 当检测到循环依赖时返回默认策略
            return self.DIRECT
            
        # 获取策略数据
        policy_data = proxies_data.get("proxies", {}).get(policy_name)
        if not policy_data:
            self.logger.warning(
                "在代理数据中未找到策略",
                extra={"policy_name": policy_name}
            )
            return self.DIRECT
            
        # 检查这是否为最终节点（非策略组）
        # 使用动态识别的策略组类型
        policy_type = policy_data.get("type")
        is_strategy_group = policy_type in self._strategy_group_types if self._strategy_group_types else \
                           policy_type in ["Selector", "Fallback"]
                           
        if not is_strategy_group:
            # 这是最终节点
            return policy_name
            
        # 这是一个策略组，获取当前选择
        now = policy_data.get("now")
        if not now:
            self.logger.warning(
                "策略组没有当前选择",
                extra={"policy_name": policy_name}
            )
            return self.DIRECT
            
        # 将当前策略添加到已访问集中以检测循环依赖
        new_visited = visited.copy()
        new_visited.add(policy_name)
        
        # 递归解析选定的策略
        return self._resolve_recursive(now, new_visited, proxies_data)
    
    def _standardize_result(self, result: str, original_policy: str, proxies_data: Dict[str, Any]) -> str:
        """
        将结果标准化为DIRECT、PROXY或REJECT之一。
        
        Args:
            result (str): 来自解析的原始结果。
            original_policy (str): 原始策略名称。
            proxies_data (dict): 来自API的所有代理/策略组数据。
            
        Returns:
            str: 标准化结果。
        """
        # 如果已经是标准结果，直接返回
        if result in [self.DIRECT, self.PROXY, self.REJECT]:
            return result
            
        # 获取节点信息以确定类型
        policy_data = proxies_data.get("proxies", {}).get(result)
        if not policy_data:
            self.logger.warning(
                "在代理数据中未找到已解析的策略用于标准化",
                extra={"resolved_policy": result, "original_policy": original_policy}
            )
            return self.DIRECT
            
        # 根据节点类型标准化结果
        policy_type = policy_data.get("type", "").upper()
        policy_name = result.upper()
        
        # 检查是否为拒绝类型
        if policy_type in ["REJECT", "REJECTDROP", "BLOCK"] or "REJECT" in policy_name or "BLOCK" in policy_name:
            return self.REJECT
            
        # 检查是否为直连类型
        if policy_type in ["DIRECT", "STATIC"] or "DIRECT" in policy_name:
            return self.DIRECT
            
        # 检查是否在代理列表中
        # 如果节点类型是代理相关类型，则返回PROXY
        proxy_types = [
            "SHADOWSOCKS", "VMESS", "TROJAN", "SNELL", "SOCKS5", 
            "HTTP", "HTTPS", "ANYTLS", "HYSTERIA", "HYSTERIA2", 
            "TUIC", "WIREGUARD", "SSH", "EXTERNAL", "INTERNAL",
            "VLESS", "PASS", "COMPATIBLE"
        ]
        
        if policy_type in proxy_types:
            return self.PROXY
            
        # 默认情况下，其他所有情况都视为直连
        return self.DIRECT