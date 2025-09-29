import asyncio
import logging
import os
import time
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
        self.logger.debug(
            "Mosdns服务控制器初始化完成",
            extra={
                "reload_command": reload_command
            }
        )

    async def reload(self) -> bool:
        """
        重新加载Mosdns服务，并检查服务状态。
        Returns:
            bool: 如果重新加载和状态检查都成功返回True，否则返回False
        """
        self.logger.debug("正在重新加载Mosdns服务")
        reload_start_time = time.time()
        try:
            process = await asyncio.create_subprocess_shell(
                self.reload_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            reload_duration = time.time() - reload_start_time
            if process.returncode == 0:
                self.logger.info(
                    "Mosdns服务重新加载成功",
                    extra={
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else "",
                        "执行耗时_秒": round(reload_duration, 3)
                    }
                )
                # 检查服务状态
                status = await self.status()
                self.logger.info("正在检查Mosdns服务状态", extra={"status": status})
                return True
            else:
                self.logger.error(
                    "重新加载Mosdns服务失败",
                    extra={
                        "command": self.reload_command,
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else "",
                        "stderr": stderr.decode().strip() if stderr else "",
                        "执行耗时_秒": round(reload_duration, 3)
                    }
                )
                return False
        except Exception as e:
            reload_duration = time.time() - reload_start_time
            self.logger.error(
                "重新加载Mosdns服务时发生异常",
                extra={
                    "command": self.reload_command,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "执行耗时_秒": round(reload_duration, 3)
                }
            )
            return False

    async def restart(self) -> bool:
        """
        重启Mosdns服务。
        Returns:
            bool: 如果重启成功返回True，否则返回False
        """
        command = "mosdns service restart"
        self.logger.debug("正在重启Mosdns服务")
        start_time = time.time()
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            duration = time.time() - start_time
            if process.returncode == 0:
                self.logger.info("Mosdns服务已成功重启", extra={"stdout": stdout.decode().strip(), "耗时": round(duration, 3)})
                return True
            else:
                self.logger.error("Mosdns服务重启失败", extra={"stderr": stderr.decode().strip(), "耗时": round(duration, 3)})
                return False
        except Exception as e:
            self.logger.error("重启Mosdns服务时发生异常", extra={"error": str(e)})
            return False

    async def stop(self) -> bool:
        """
        停止Mosdns服务。
        Returns:
            bool: 如果停止成功返回True，否则返回False
        """
        command = "mosdns service stop"
        self.logger.debug("正在停止Mosdns服务")
        start_time = time.time()
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            duration = time.time() - start_time
            if process.returncode == 0:
                self.logger.info("Mosdns服务已成功停止", extra={"stdout": stdout.decode().strip(), "耗时": round(duration, 3)})
                return True
            else:
                self.logger.error("Mosdns服务停止失败", extra={"stderr": stderr.decode().strip(), "耗时": round(duration, 3)})
                return False
        except Exception as e:
            self.logger.error("停止Mosdns服务时发生异常", extra={"error": str(e)})
            return False

    async def status(self) -> str:
        """
        查询Mosdns服务状态。
        Returns:
            str: 服务状态输出
        """
        command = "mosdns service status"
        self.logger.debug("查询Mosdns服务状态")
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                status_output = stdout.decode().strip()
                self.logger.info("Mosdns服务当前状态:", extra={"status": status_output})
                return status_output
            else:
                error_output = stderr.decode().strip()
                self.logger.error("查询Mosdns服务状态失败", extra={"error": error_output})
                return error_output
        except Exception as e:
            self.logger.error("查询Mosdns服务状态时发生异常", extra={"error": str(e)})
            return str(e)