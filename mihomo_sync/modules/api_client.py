import httpx
import asyncio
import logging
import time
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
        self.logger.debug(
            "Mihomo API客户端初始化完成",
            extra={
                "base_url": self.api_base_url,
                "timeout": self.timeout
            }
        )

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
        
        self.logger.debug(
            "开始API请求",
            extra={
                "method": method,
                "endpoint": endpoint,
                "max_retries": max_retries
            }
        )
        
        request_start_time = time.time()
        
        for attempt in range(1, max_retries + 1):
            try:
                request_attempt_start = time.time()
                response = await self.client.request(method, url)
                request_attempt_duration = time.time() - request_attempt_start
                
                # 检查成功的状态码（2xx）
                if 200 <= response.status_code < 300:
                    request_duration = time.time() - request_start_time
                    self.logger.debug(
                        "API请求成功",
                        extra={
                            "endpoint": endpoint,
                            "status_code": response.status_code,
                            "attempt": attempt,
                            "请求耗时_秒": round(request_attempt_duration, 3),
                            "总耗时_秒": round(request_duration, 3)
                        }
                    )
                    return response.json()
                
                # 记录非2xx状态码的错误
                self.logger.error(
                    "API请求失败",
                    extra={
                        "endpoint": endpoint,
                        "status_code": response.status_code,
                        "attempt": attempt,
                        "max_attempts": max_retries,
                        "response_text": response.text[:200]  # 限制响应文本长度
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
                            "delay_seconds": round(delay, 2),
                            "error": str(e),
                            "error_type": type(e).__name__
                        }
                    )
                    await asyncio.sleep(delay)
                else:
                    # 最后一次尝试失败
                    request_duration = time.time() - request_start_time
                    self.logger.error(
                        "API请求在所有重试后仍然失败",
                        extra={
                            "endpoint": endpoint,
                            "attempts": max_retries,
                            "error": str(e),
                            "error_type": type(e).__name__,
                            "总耗时_秒": round(request_duration, 3)
                        }
                    )
                    raise ApiClientError(f"连接到 {url} 失败，经过 {max_retries} 次尝试: {str(e)}")
            except Exception as e:
                # 处理其他异常
                request_duration = time.time() - request_start_time
                self.logger.error(
                    "API请求过程中发生未预期的异常",
                    extra={
                        "endpoint": endpoint,
                        "attempt": attempt,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "总耗时_秒": round(request_duration, 3)
                    }
                )
                raise ApiClientError(f"请求 {url} 时发生异常: {str(e)}")
        
        # 这不应该被到达，但为了保险起见
        raise ApiClientError(f"在请求 {url} 时发生意外错误")

    async def check_connectivity(self) -> bool:
        """
        检查与Mihomo API的连接性。
        
        Returns:
            bool: 如果连接成功返回True，否则返回False。
        """
        self.logger.debug("正在检查API连接性")
        try:
            await self._request("GET", "/configs")
            self.logger.debug("API连接性检查通过")
            return True
        except ApiClientError as e:
            self.logger.warning(
                "API连接性检查失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            return False

    async def get_rules(self) -> Dict[str, Any]:
        """
        从Mihomo API获取规则。
        
        Returns:
            dict: 来自API的规则数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        self.logger.debug("正在获取规则数据")
        start_time = time.time()
        try:
            result = await self._request("GET", "/rules")
            duration = time.time() - start_time
            self.logger.debug(
                "规则数据获取完成",
                extra={
                    "规则数量": len(result.get("rules", [])),
                    "获取耗时_秒": round(duration, 3)
                }
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "获取规则数据失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "获取耗时_秒": round(duration, 3)
                }
            )
            raise

    async def get_proxies(self) -> Dict[str, Any]:
        """
        从Mihomo API获取代理。
        
        Returns:
            dict: 来自API的代理数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        self.logger.debug("正在获取代理数据")
        start_time = time.time()
        try:
            result = await self._request("GET", "/proxies")
            duration = time.time() - start_time
            proxy_count = len(result.get("proxies", {}))
            self.logger.debug(
                "代理数据获取完成",
                extra={
                    "代理数量": proxy_count,
                    "获取耗时_秒": round(duration, 3)
                }
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "获取代理数据失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "获取耗时_秒": round(duration, 3)
                }
            )
            raise

    async def get_rule_providers(self) -> Dict[str, Any]:
        """
        从Mihomo API获取规则提供者。
        
        Returns:
            dict: 来自API的规则提供者数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        self.logger.debug("正在获取规则提供者数据")
        start_time = time.time()
        try:
            result = await self._request("GET", "/providers/rules")
            duration = time.time() - start_time
            provider_count = len(result.get("providers", {}))
            self.logger.debug(
                "规则提供者数据获取完成",
                extra={
                    "提供者数量": provider_count,
                    "获取耗时_秒": round(duration, 3)
                }
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "获取规则提供者数据失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "获取耗时_秒": round(duration, 3)
                }
            )
            raise

    async def get_config(self) -> Dict[str, Any]:
        """
        从Mihomo API获取配置。
        
        Returns:
            dict: 来自API的配置数据。
            
        Raises:
            ApiClientError: 如果请求失败。
        """
        self.logger.debug("正在获取配置数据")
        start_time = time.time()
        try:
            result = await self._request("GET", "/configs")
            duration = time.time() - start_time
            self.logger.debug(
                "配置数据获取完成",
                extra={
                    "获取耗时_秒": round(duration, 3)
                }
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "获取配置数据失败",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "获取耗时_秒": round(duration, 3)
                }
            )
            raise
        
    async def close(self):
        """关闭HTTP客户端会话。"""
        self.logger.debug("正在关闭API客户端")
        await self.client.aclose()
        self.logger.debug("API客户端已关闭")