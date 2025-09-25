import httpx
import asyncio
import logging
from typing import Dict, Any, Optional


class ApiClientError(Exception):
    """Custom exception for API client errors."""
    pass


class MihomoApiClient:
    """An asynchronous HTTP client for interacting with the Mihomo API with retry logic."""
    
    def __init__(self, api_base_url: str, timeout: int, retry_config: Dict[str, Any], api_secret: str = ""):
        """
        Initialize the Mihomo API client.
        
        Args:
            api_base_url (str): The base URL of the Mihomo API.
            timeout (int): Request timeout in seconds.
            retry_config (dict): Configuration for retry logic.
            api_secret (str): Secret for API authentication.
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.timeout = timeout
        self.retry_config = retry_config
        self.api_secret = api_secret
        self.logger = logging.getLogger(__name__)
        
        # Initialize the async HTTP client with authentication headers if secret is provided
        headers = {}
        if self.api_secret:
            headers["Authorization"] = f"Bearer {self.api_secret}"
            
        self.client = httpx.AsyncClient(timeout=self.timeout, headers=headers)

    async def _request(self, method: str, endpoint: str) -> Dict[str, Any]:
        """
        Make an HTTP request with exponential backoff retry logic.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint to request.
            
        Returns:
            dict: JSON response from the API.
            
        Raises:
            ApiClientError: If the request fails after all retries.
        """
        url = f"{self.api_base_url}{endpoint}"
        max_retries = self.retry_config.get('max_retries', 3)
        initial_backoff = self.retry_config.get('initial_backoff', 1)
        max_backoff = self.retry_config.get('max_backoff', 16)
        jitter = self.retry_config.get('jitter', True)
        
        for attempt in range(1, max_retries + 1):
            try:
                response = await self.client.request(method, url)
                
                # Check for successful status codes (2xx)
                if 200 <= response.status_code < 300:
                    return response.json()
                
                # Log error for non-2xx status codes
                self.logger.error(
                    "API request failed",
                    extra={
                        "endpoint": endpoint,
                        "status_code": response.status_code,
                        "attempt": attempt,
                        "max_attempts": max_retries
                    }
                )
                
                # For 4xx errors, don't retry
                if 400 <= response.status_code < 500:
                    raise ApiClientError(f"Client error {response.status_code}: {response.text}")
                    
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                # Log retry warning
                if attempt < max_retries:
                    # Calculate delay with exponential backoff and jitter
                    delay = min(max_backoff, initial_backoff * (2 ** (attempt - 1)))
                    if jitter:
                        import random
                        delay *= (0.5 + random.random() * 0.5)  # Add jitter: 0.5 to 1.0 multiplier
                    
                    self.logger.warning(
                        "API request failed, retrying...",
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
                    # Last attempt failed
                    self.logger.error(
                        "API request failed after all retries",
                        extra={
                            "endpoint": endpoint,
                            "attempts": max_retries,
                            "error": str(e)
                        }
                    )
                    raise ApiClientError(f"Failed to connect to {url} after {max_retries} attempts: {str(e)}")
        
        # This shouldn't be reached, but just in case
        raise ApiClientError(f"Unexpected error during request to {url}")

    async def check_connectivity(self) -> bool:
        """
        Check connectivity to the Mihomo API.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        try:
            await self._request("GET", "/configs")
            return True
        except ApiClientError:
            return False

    async def get_rules(self) -> Dict[str, Any]:
        """
        Get rules from the Mihomo API.
        
        Returns:
            dict: Rules data from the API.
            
        Raises:
            ApiClientError: If the request fails.
        """
        return await self._request("GET", "/rules")

    async def get_proxies(self) -> Dict[str, Any]:
        """
        Get proxies from the Mihomo API.
        
        Returns:
            dict: Proxies data from the API.
            
        Raises:
            ApiClientError: If the request fails.
        """
        return await self._request("GET", "/proxies")

    async def get_rule_providers(self) -> Dict[str, Any]:
        """
        Get rule providers from the Mihomo API.
        
        Returns:
            dict: Rule providers data from the API.
            
        Raises:
            ApiClientError: If the request fails.
        """
        return await self._request("GET", "/providers/rules")

    async def get_config(self) -> Dict[str, Any]:
        """
        Get configuration from the Mihomo API.
        
        Returns:
            dict: Configuration data from the API.
            
        Raises:
            ApiClientError: If the request fails.
        """
        return await self._request("GET", "/configs")
        
    async def close(self):
        """Close the HTTP client session."""
        await self.client.aclose()