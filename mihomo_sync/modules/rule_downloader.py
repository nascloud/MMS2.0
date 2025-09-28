import asyncio
import httpx
import os
import hashlib
import json
import logging
import random
from typing import List, Optional

class RuleDownloader:
    """
    一个高效的规则下载器，负责并发下载和基于ETag的缓存管理。
    """

    def __init__(self, client: httpx.AsyncClient, cache_dir: str, max_retries: int = 5, 
                 initial_backoff: float = 1.0, max_backoff: float = 16.0, jitter: bool = True):
        """
        初始化规则下载器。

        Args:
            client: 一个共享的 httpx.AsyncClient 实例。
            cache_dir: 用于存储规则文件和元数据的缓存目录。
            max_retries: 最大重试次数。
            initial_backoff: 初始退避时间（秒）。
            max_backoff: 最大退避时间（秒）。
            jitter: 是否添加抖动以减少重试冲突。
        """
        self.client = client
        self.cache_dir = cache_dir
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        self.jitter = jitter
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_path_for_url(self, url: str) -> str:
        """
        根据URL获取其在本地缓存中的文件路径。
        这是一个无I/O的确定性方法，用于给其他模块查询路径。
        """
        key = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return os.path.join(self.cache_dir, f"{key}.list")

    async def _exponential_backoff_with_jitter(self, attempt: int) -> float:
        """
        计算带抖动的指数退避时间。
        
        Args:
            attempt: 当前尝试次数（从0开始）。
            
        Returns:
            退避时间（秒）。
        """
        # 指数退避：backoff_time = initial_backoff * (2 ^ attempt)
        base_time = min(self.initial_backoff * (2 ** attempt), self.max_backoff)
        
        if self.jitter:
            # 在 [0, base_time] 范围内添加随机抖动
            return random.uniform(0, base_time)
        else:
            # 不使用抖动，返回固定退避时间
            return base_time

    async def _download_with_retry(self, url: str, headers: dict) -> Optional[httpx.Response]:
        """
        使用指数退避和重试机制下载URL内容。
        
        Args:
            url: 要下载的URL。
            headers: 请求头。
            
        Returns:
            HTTP响应对象，如果失败则返回None。
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.get(url, timeout=30, headers=headers)
                
                if response.status_code != 304:
                    response.raise_for_status()
                
                # 成功，返回响应
                return response
                
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                last_exception = e
                
                # 如果是最后一次尝试，直接退出
                if attempt == self.max_retries:
                    self.logger.error(f"下载规则时经过 {self.max_retries} 次重试后仍然失败: {url}, 错误: {e}")
                    break
                
                # 计算退避时间
                backoff_time = await self._exponential_backoff_with_jitter(attempt)
                
                self.logger.warning(
                    f"下载规则失败 (尝试 {attempt + 1}/{self.max_retries + 1}): {url}, "
                    f"将在 {backoff_time:.2f} 秒后重试。错误: {e}"
                )
                
                # 等待退避时间
                await asyncio.sleep(backoff_time)
        
        # 所有重试都失败了
        return None

    async def _ensure_rule_updated(self, url: str):
        """
        确保单个URL的规则文件是最新的。
        如果本地缓存有效，则跳过下载；否则，下载并更新缓存。
        """
        content_path = self.get_cache_path_for_url(url)
        meta_path = content_path.replace(".list", ".meta.json")
        headers = {}
        
        # 1. 检查本地缓存元数据，获取ETag
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    etag = json.load(f).get('etag')
                if etag:
                    headers['If-None-Match'] = etag
            except (IOError, json.JSONDecodeError):
                self.logger.warning(f"无法读取元数据: {meta_path}")

        # 2. 使用重试机制发起异步条件请求
        response = await self._download_with_retry(url, headers)
        
        if response is None:
            # 所有重试都失败了
            return

        if response.status_code == 304:
            self.logger.info(f"缓存命中 (304): {url}")
            return

        # 3. 下载新内容并更新缓存
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        new_etag = response.headers.get('ETag')
        if new_etag:
            with open(meta_path, 'w') as f:
                json.dump({'etag': new_etag}, f)
        elif os.path.exists(meta_path):
            os.remove(meta_path)
        
        self.logger.info(f"成功更新缓存: {url}")

    async def download_rules(self, urls: List[str]):
        """
        并发地确保所有提供的URL规则文件都已下载并更新到本地缓存。
        """
        if not urls:
            return
        
        self.logger.info(f"开始并发检查/下载 {len(urls)} 个规则文件...")
        tasks = [self._ensure_rule_updated(url) for url in urls]
        await asyncio.gather(*tasks)
        self.logger.info("所有规则文件下载任务完成。")