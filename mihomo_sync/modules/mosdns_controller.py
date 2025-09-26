import asyncio
import logging
import os
from typing import Dict, Any


class MosdnsServiceController:
    """Mosdns服务的控制器。"""
    
    def __init__(self, reload_command: str):
        """
        初始化MosdnsServiceController。
        
        Args:
            reload_command (str): 重新加载Mosdns服务的命令
        """
        self.reload_command = reload_command
        self.logger = logging.getLogger(__name__)

    async def reload(self) -> bool:
        """
        重新加载Mosdns服务。
        
        Returns:
            bool: 如果重新加载成功返回True，否则返回False
        """
        try:
            self.logger.info("正在重新加载Mosdns服务")
            
            # 创建子进程
            process = await asyncio.create_subprocess_shell(
                self.reload_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # 等待进程完成
            stdout, stderr = await process.communicate()
            
            # 检查返回码
            if process.returncode == 0:
                self.logger.info(
                    "Mosdns服务重新加载成功",
                    extra={
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else ""
                    }
                )
                return True
            else:
                self.logger.error(
                    "重新加载Mosdns服务失败",
                    extra={
                        "command": self.reload_command,
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else "",
                        "stderr": stderr.decode().strip() if stderr else ""
                    }
                )
                return False
                
        except Exception as e:
            self.logger.error(
                "重新加载Mosdns服务时发生异常",
                extra={
                    "command": self.reload_command,
                    "error": str(e)
                }
            )
            return False