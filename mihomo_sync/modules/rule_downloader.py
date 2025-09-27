import asyncio
import aiohttp
import os
import hashlib
import logging


class RuleDownloader:
    """规则下载器类，负责下载并缓存规则文件"""
    
    def __init__(self, cache_dir: str, session: aiohttp.ClientSession):
        """
        初始化规则下载器
        
        Args:
            cache_dir: 缓存目录路径
            session: aiohttp.ClientSession 实例
        """
        self.cache_dir = cache_dir
        self.session = session
        
        # 确保缓存目录存在
        os.makedirs(cache_dir, exist_ok=True)
        
        # 获取日志记录器
        self.logger = logging.getLogger(__name__)
    
    def _get_cache_key(self, url: str) -> str:
        """
        生成URL的缓存键（SHA256哈希值）
        
        Args:
            url: 规则文件的URL
            
        Returns:
            URL的SHA256哈希值的十六进制摘要
        """
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    async def _download_and_cache(self, url: str):
        """
        下载单个URL并更新其缓存
        
        Args:
            url: 要下载的规则文件URL
        """
        try:
            self.logger.info(f"开始下载规则文件: {url}")
            
            # 发起HTTP请求
            async with self.session.get(url) as response:
                # 检查HTTP状态码
                if response.status != 200:
                    self.logger.error(f"下载失败: {url}, HTTP状态码: {response.status}")
                    return
                
                # 读取响应内容
                content = await response.text()
                
                # 获取缓存文件名和完整路径
                cache_key = self._get_cache_key(url)
                cache_file_path = os.path.join(self.cache_dir, f"{cache_key}.txt")
                
                # 将内容写入缓存文件
                with open(cache_file_path, 'w', encoding='utf-8') as cache_file:
                    cache_file.write(content)
                
                self.logger.info(f"成功下载并缓存规则文件: {url} -> {cache_file_path}")
                
        except aiohttp.ClientError as e:
            self.logger.error(f"下载规则文件时发生网络错误: {url}, 错误: {str(e)}")
        except IOError as e:
            self.logger.error(f"写入缓存文件时发生IO错误: {url}, 错误: {str(e)}")
        except Exception as e:
            self.logger.error(f"下载规则文件时发生未知错误: {url}, 错误: {str(e)}")
    
    async def download_rules(self, urls_to_update: list[str]):
        """
        并发下载多个规则文件
        
        Args:
            urls_to_update: 待更新的URL列表
        """
        if not urls_to_update:
            self.logger.warning("没有提供需要下载的规则文件URL")
            return
        
        self.logger.info(f"开始并发下载 {len(urls_to_update)} 个规则文件")
        
        # 为每个URL创建下载任务
        tasks = [self._download_and_cache(url) for url in urls_to_update]
        
        # 并发执行所有任务
        await asyncio.gather(*tasks)
        
        self.logger.info("所有规则文件下载任务已完成")