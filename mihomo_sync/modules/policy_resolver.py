import logging
from typing import Dict, Any, Set


class PolicyResolver:
    """A class to resolve policy chains and find the final出口 node."""
    
    # 定义标准的返回类型
    DIRECT = "DIRECT"
    PROXY = "PROXY"
    REJECT = "REJECT"
    
    def __init__(self):
        """
        Initialize the PolicyResolver.
        """
        self.logger = logging.getLogger(__name__)
        # Cache for memoization to avoid repeated calculations
        self._cache = {}
        # Store strategy group types dynamically
        self._strategy_group_types = set()
        
    def resolve(self, policy_name: str, proxies_data: Dict[str, Any]) -> str:
        """
        Resolve a policy name to its final出口 node.
        
        Args:
            policy_name (str): The name of the policy to resolve.
            proxies_data (dict): All proxy/strategy group data from the API.
            
        Returns:
            str: The standardized policy result (DIRECT, PROXY, or REJECT).
        """
        # Check cache first
        cache_key = f"{policy_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        # Identify strategy group types from the proxies data
        self._identify_strategy_group_types(proxies_data)
            
        # Start resolution with an empty visited set
        result = self._resolve_recursive(policy_name, set(), proxies_data)
        
        # 标准化返回值
        standardized_result = self._standardize_result(result, policy_name, proxies_data)
        
        # Cache the result
        self._cache[cache_key] = standardized_result
        return standardized_result
        
    def _identify_strategy_group_types(self, proxies_data: Dict[str, Any]) -> None:
        """
        Identify strategy group types from proxies data.
        
        Args:
            proxies_data (dict): All proxy/strategy group data from the API.
        """
        proxies = proxies_data.get("proxies", {})
        for proxy_data in proxies.values():
            proxy_type = proxy_data.get("type")
            # Strategy groups typically have an "all" field containing a list of proxies
            if proxy_type and "all" in proxy_data and isinstance(proxy_data["all"], list):
                self._strategy_group_types.add(proxy_type)
                
        # Log the identified strategy group types
        if self._strategy_group_types:
            self.logger.debug(f"Identified strategy group types: {self._strategy_group_types}")
        
    def _resolve_recursive(self, policy_name: str, visited: Set[str], proxies_data: Dict[str, Any]) -> str:
        """
        Recursively resolve a policy name, detecting circular dependencies.
        
        Args:
            policy_name (str): The name of the policy to resolve.
            visited (set): Set of policy names in the current resolution path.
            proxies_data (dict): All proxy/strategy group data from the API.
            
        Returns:
            str: The name of the final出口 node.
        """
        # Check if we've already visited this policy in the current path (circular dependency)
        if policy_name in visited:
            self.logger.error(
                "Circular dependency detected in policy resolution",
                extra={
                    "policy_name": policy_name,
                    "visited_path": list(visited)
                }
            )
            # Return a default policy when circular dependency is detected
            return self.DIRECT
            
        # Get policy data
        policy_data = proxies_data.get("proxies", {}).get(policy_name)
        if not policy_data:
            self.logger.warning(
                "Policy not found in proxies data",
                extra={"policy_name": policy_name}
            )
            return self.DIRECT
            
        # Check if this is a final node (not a strategy group)
        # Use dynamically identified strategy group types
        policy_type = policy_data.get("type")
        is_strategy_group = policy_type in self._strategy_group_types if self._strategy_group_types else \
                           policy_type in ["Selector", "Fallback"]
                           
        if not is_strategy_group:
            # This is a final node
            return policy_name
            
        # This is a strategy group, get the current selection
        now = policy_data.get("now")
        if not now:
            self.logger.warning(
                "Strategy group has no current selection",
                extra={"policy_name": policy_name}
            )
            return self.DIRECT
            
        # Add current policy to visited set for circular dependency detection
        new_visited = visited.copy()
        new_visited.add(policy_name)
        
        # Recursively resolve the selected policy
        return self._resolve_recursive(now, new_visited, proxies_data)
    
    def _standardize_result(self, result: str, original_policy: str, proxies_data: Dict[str, Any]) -> str:
        """
        Standardize the result to one of DIRECT, PROXY, or REJECT.
        
        Args:
            result (str): The raw result from resolution.
            original_policy (str): The original policy name.
            proxies_data (dict): All proxy/strategy group data from the API.
            
        Returns:
            str: The standardized result.
        """
        # 如果已经是标准结果，直接返回
        if result in [self.DIRECT, self.PROXY, self.REJECT]:
            return result
            
        # 获取节点信息以确定类型
        policy_data = proxies_data.get("proxies", {}).get(result)
        if not policy_data:
            self.logger.warning(
                "Resolved policy not found in proxies data for standardization",
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