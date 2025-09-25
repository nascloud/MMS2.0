import asyncio
import logging
import os
from typing import Dict, Any


class MosdnsServiceController:
    """Controller for managing the Mosdns service."""
    
    def __init__(self, reload_command: str):
        """
        Initialize the MosdnsServiceController.
        
        Args:
            reload_command (str): Command to reload the Mosdns service
        """
        self.reload_command = reload_command
        self.logger = logging.getLogger(__name__)

    async def reload(self) -> bool:
        """
        Reload the Mosdns service.
        
        Returns:
            bool: True if reload was successful, False otherwise
        """
        try:
            self.logger.info("Reloading Mosdns service")
            
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                self.reload_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for the process to complete
            stdout, stderr = await process.communicate()
            
            # Check return code
            if process.returncode == 0:
                self.logger.info(
                    "Mosdns service reloaded successfully",
                    extra={
                        "return_code": process.returncode,
                        "stdout": stdout.decode().strip() if stdout else ""
                    }
                )
                return True
            else:
                self.logger.error(
                    "Failed to reload Mosdns service",
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
                "Exception occurred while reloading Mosdns service",
                extra={
                    "command": self.reload_command,
                    "error": str(e)
                }
            )
            return False