import logging
from typing import Dict, Any, Set


class PolicyResolver:
    """A class to resolve policy chains and find the final出口 node."""
    
    def __init__(self, proxies_data: Dict[str, Any]):
        """
        Initialize the PolicyResolver with proxies data.
        
        Args:
            proxies_data (dict): All proxy/strategy group data from the API.
        """
        self.proxies_data = proxies_data
        self.logger = logging.getLogger(__name__)
        # Cache for memoization to avoid repeated calculations
        self._cache = {}
        
    def resolve(self, policy_name: str) -> str:
        """
        Resolve a policy name to its final出口 node.
        
        Args:
            policy_name (str): The name of the policy to resolve.
            
        Returns:
            str: The name of the final出口 node.
        """
        # Check cache first
        if policy_name in self._cache:
            return self._cache[policy_name]
            
        # Start resolution with an empty visited set
        result = self._resolve_recursive(policy_name, set())
        
        # Cache the result
        self._cache[policy_name] = result
        return result
        
    def _resolve_recursive(self, policy_name: str, visited: Set[str]) -> str:
        """
        Recursively resolve a policy name, detecting circular dependencies.
        
        Args:
            policy_name (str): The name of the policy to resolve.
            visited (set): Set of policy names in the current resolution path.
            
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
            return "DIRECT"
            
        # Get policy data
        policy_data = self.proxies_data.get("proxies", {}).get(policy_name)
        if not policy_data:
            self.logger.warning(
                "Policy not found in proxies data",
                extra={"policy_name": policy_name}
            )
            return "DIRECT"
            
        # Check if this is a final node (not a strategy group)
        if policy_data.get("type") != "Selector" and policy_data.get("type") != "Fallback":
            # This is a final node
            return policy_name
            
        # This is a strategy group, get the current selection
        now = policy_data.get("now")
        if not now:
            self.logger.warning(
                "Strategy group has no current selection",
                extra={"policy_name": policy_name}
            )
            return "DIRECT"
            
        # Add current policy to visited set for circular dependency detection
        new_visited = visited.copy()
        new_visited.add(policy_name)
        
        # Recursively resolve the selected policy
        return self._resolve_recursive(now, new_visited)