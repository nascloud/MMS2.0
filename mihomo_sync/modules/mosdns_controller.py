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
        self.logger.debug(f"Mosdns服务控制器初始化完成, reload_command: {reload_command}")

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
                stdout_str = stdout.decode().strip() if stdout else ""
                self.logger.info(f"Mosdns服务重新加载成功, return_code: {process.returncode}, stdout: {stdout_str}, 执行耗时_秒: {round(reload_duration, 3)}")
                # 检查服务状态
                status = await self.status()
                self.logger.info(f"正在检查Mosdns服务状态: {status}")
                return True
            else:
                stdout_str = stdout.decode().strip() if stdout else ""
                stderr_str = stderr.decode().strip() if stderr else ""
                self.logger.error(f"重新加载Mosdns服务失败, command: {self.reload_command}, return_code: {process.returncode}, stdout: {stdout_str}, stderr: {stderr_str}, 执行耗时_秒: {round(reload_duration, 3)}")
                return False
        except Exception as e:
            reload_duration = time.time() - reload_start_time
            self.logger.error(f"重新加载Mosdns服务时发生异常, command: {self.reload_command}, error: {str(e)}, error_type: {type(e).__name__}, 执行耗时_秒: {round(reload_duration, 3)}")
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
                stdout_str = stdout.decode().strip()
                self.logger.info(f"Mosdns服务已成功重启, stdout: {stdout_str}, 耗时: {round(duration, 3)}")
                return True
            else:
                stderr_str = stderr.decode().strip()
                self.logger.error(f"Mosdns服务重启失败, stderr: {stderr_str}, 耗时: {round(duration, 3)}")
                return False
        except Exception as e:
            self.logger.error(f"重启Mosdns服务时发生异常, error: {str(e)}")
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
                stdout_str = stdout.decode().strip()
                self.logger.info(f"Mosdns服务已成功停止, stdout: {stdout_str}, 耗时: {round(duration, 3)}")
                return True
            else:
                stderr_str = stderr.decode().strip()
                self.logger.error(f"Mosdns服务停止失败, stderr: {stderr_str}, 耗时: {round(duration, 3)}")
                return False
        except Exception as e:
            self.logger.error(f"停止Mosdns服务时发生异常, error: {str(e)}")
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
                self.logger.info(f"Mosdns服务当前状态: {status_output}")
                return status_output
            else:
                error_output = stderr.decode().strip()
                self.logger.error(f"查询Mosdns服务状态失败: {error_output}")
                return error_output
        except Exception as e:
            self.logger.error(f"查询Mosdns服务状态时发生异常: {str(e)}")
            return str(e)