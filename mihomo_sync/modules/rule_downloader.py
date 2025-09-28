import asyncio
import httpx
import os
import hashlib
import json
import logging
from typing import List

class RuleDownloader:
    """
    一个高效的规则下载器，负责并发下载和基于ETag的缓存管理。
    """

    def __init__(self, client: httpx.AsyncClient, cache_dir: str):
        """
        初始化规则下载器。

        Args:
            client: 一个共享的 httpx.AsyncClient 实例。
            cache_dir: 用于存储规则文件和元数据的缓存目录。
        """
        self.client = client
        self.cache_dir = cache_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_path_for_url(self, url: str) -> str:
        """
        根据URL获取其在本地缓存中的文件路径。
        这是一个无I/O的确定性方法，用于给其他模块查询路径。
        """
        key = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return os.path.join(self.cache_dir, f"{key}.list")

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

        try:
            # 2. 发起异步条件请求
            response = await self.client.get(url, timeout=30, headers=headers)

            if response.status_code == 304:
                self.logger.info(f"缓存命中 (304): {url}")
                return

            response.raise_for_status()

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

        except httpx.HTTPStatusError as e:
            self.logger.error(f"下载规则时HTTP错误: {url}, 状态码: {e.response.status_code}")
        except httpx.RequestError as e:
            self.logger.error(f"下载规则时网络错误: {url}, 错误: {e}")

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