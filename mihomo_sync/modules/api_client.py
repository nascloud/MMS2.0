import httpx
import asyncio
import logging
from typing import Dict, Any, Optional


class ApiClientError(Exception):
    """API客户端错误的自定义异常。"""
    pass


class MihomoApiClient:
    """一个用于与Mihomo API交互的异步HTTP客户端，具有重试逻辑。"""
    
    def __init__(self, api_base_url: str, timeout: int, retry_config: Dict[str, Any], api_secret: str = ""):
        """
        初始化Mihomo API客户端。
        
        Args:
            api_base_url (str): Mihomo API的基础URL。
            timeout (int): 请求超时时间（秒）。
            retry_config (dict): 重试逻辑的配置。
            api_secret (str): API认证密钥。
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.timeout = timeout
        self.retry_config = retry_config
        self.api_secret = api_secret
        self.logger = logging.getLogger(__name__)
        
        # 如果提供了密钥，则使用认证头初始化异步HTTP客户端
        headers = {}
        if self.api_secret:
            headers["Authorization"] = f"Bearer {self.api_secret}"
            
        self.client = httpx.AsyncClient(timeout=self.timeout, headers=headers)

    async def _request(self, method: str, endpoint: str) -> Dict[str, Any]:
        """
        发送带有指数退避重试逻辑的HTTP请求。
        
        Args:
            method (str): HTTP方法（GET、POST等）
            endpoint (str): 要请求的API端点。
            
        Returns:
            dict: 来自API的JSON响应。
            
        Raises:
            ApiClientError: 如果所有重试后请求仍然失败。
        """
        url = f"{self.api_base_url}{endpoint}"
        max_retries = self.retry_config.get('max_retries', 3)
        initial_backoff = self.retry_config.get('initial_backoff', 1)
        max_backoff = self.retry_config.get('max_backoff', 16)
        jitter = self.retry_config.get('jitter', True)
        
        for attempt in range(1, max_retries + 1):
            try:
                response = await self.client.request(method, url)
                
                # 检查成功的状态码（2xx）
                if 200 <= response.status_code < 300:
                    return response.json()
                
                # 记录非2xx状态码的错误
                self.logger.error(
                    "API请求失败",
                    extra={
                        "endpoint": endpoint,
                        "status_code": response.status_code,
                        "attempt": attempt,
                        "max_attempts": max_retries
                    }
                )
                
                # 对于4xx错误，不重试
                if 400 <= response.status_code < 500:
                    raise ApiClientError(f"客户端错误 {response.status_code}: {response.text}")
                    
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                # 记录重试警告
                if attempt < max_retries:
                    # 使用指数退避和抖动计算延迟
                    delay = min(max_backoff, initial_backoff * (2 ** (attempt - 1)))
                    if jitter:
                        import random
                        delay *= (0.5 + random.random() * 0.5)  # 添加抖动：0.5到1.0的乘数
                    
                    self.logger.warning(
                        "API请求失败，正在重试...",
                        extra={
                            "endpoint": endpoint,
                            "attempt": attempt,
                            "max_attempts": max_retries,
                            "delay_seconds": delay,
                            "error": str(e)
                        }
                    )
                    await asyncio.sleep(delay)
                else:
                    # 最后一次尝试失败
                    self.logger.error(
                        "API请求在所有重试后仍然失败",
                        extra={
                            "endpoint": endpoint,
                            "attempts": max_retries,
                            "error": str(e)
                        }
                    )
                    raise ApiClientError(f"连接到 {url} 失败，经过 {max_retries} 次尝试: {str(e)}")
        
        # 这不应该被到达，但为了保险起见
        raise ApiClientError(f"在请求 {url} 时发生意外错误")

    async def check_connectivity(self) -> bool:
        """
        检查与Mihomo API的连接性。
        
        Returns:
            bool: 如果连接成功返回True，否则返回False。
        """
        try:
            await self._request("GET", "/configs")
            return True
        except ApiClientError:
            return False

    async def get_rules(self) -> Dict[str, Any]:
        """
        从Mihomo API获取规则。
        
        Returns:
            dict: 来自API的规则数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        return await self._request("GET", "/rules")

    async def get_proxies(self) -> Dict[str, Any]:
        """
        从Mihomo API获取代理。
        
        Returns:
            dict: 来自API的代理数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        return await self._request("GET", "/proxies")

    async def get_rule_providers(self) -> Dict[str, Any]:
        """
        从Mihomo API获取规则提供者。
        
        Returns:
            dict: 来自API的规则提供者数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        return await self._request("GET", "/providers/rules")

    async def get_config(self) -> Dict[str, Any]:
        """
        从Mihomo API获取配置。
        
        Returns:
            dict: 来自API的配置数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        return await self._request("GET", "/configs")
        
    async def close(self):
        """关闭HTTP客户端会话。"""
        await self.client.aclose()