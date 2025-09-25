#!/usr/bin/env python3
"""
Main entry point for the Mihomo-Mosdns synchronization service.
"""
import asyncio
import logging
import os
import signal
import sys
from typing import Optional
from mihomo_sync.logger import setup_logger
from mihomo_sync.config import ConfigManager
from mihomo_sync.modules.api_client import MihomoApiClient
from mihomo_sync.modules.mosdns_controller import MosdnsServiceController, MosdnsRuleGenerator
from mihomo_sync.modules.state_monitor import StateMonitor


class MihomoMosdnsSyncService:
    """Main service class for Mihomo-Mosdns synchronization."""
    
    def __init__(self):
        """Initialize the service."""
        self.logger = logging.getLogger(__name__)
        self.config_manager: Optional[ConfigManager] = None
        self.api_client: Optional[MihomoApiClient] = None
        self.mosdns_controller: Optional[MosdnsServiceController] = None
        self.rule_generator: Optional[MosdnsRuleGenerator] = None
        self.state_monitor: Optional[StateMonitor] = None
        self.shutdown_event = asyncio.Event()

    async def initialize(self):
        """Initialize all components of the service."""
        self.logger.info("Initializing Mihomo-Mosdns sync service")
        
        try:
            # Load configuration
            config_path = os.environ.get('CONFIG_PATH', 'config/config.yaml')
            self.config_manager = ConfigManager(config_path)
            
            # Set up logger with configured level
            setup_logger(self.config_manager.get_log_level())
            
            # Reinitialize logger after setup_logger call
            self.logger = logging.getLogger(__name__)
            
            # Initialize API client
            self.api_client = MihomoApiClient(
                api_base_url=self.config_manager.get_mihomo_api_url(),
                timeout=self.config_manager.get_mihomo_api_timeout(),
                retry_config=self.config_manager.get_api_retry_config(),
                api_secret=self.config_manager.get_mihomo_api_secret()
            )
            
            # Initialize Mosdns controller
            self.mosdns_controller = MosdnsServiceController(
                reload_command=self.config_manager.get_mosdns_reload_command()
            )
            
            # Initialize rule generator
            self.rule_generator = MosdnsRuleGenerator(
                api_client=self.api_client,
                mosdns_controller=self.mosdns_controller,
                mosdns_config_path=self.config_manager.get_mosdns_config_path()
            )
            
            # Initialize state monitor
            self.state_monitor = StateMonitor(
                api_client=self.api_client,
                polling_interval=self.config_manager.get_polling_interval(),
                debounce_interval=self.config_manager.get_debounce_interval(),
                on_change_callback=self.rule_generator.run
            )
            
            self.logger.info("Service initialization completed")
        except Exception as e:
            self.logger.exception("Error during service initialization")
            raise

    async def health_check(self):
        """
        Perform health checks before starting the service.
        
        Returns:
            bool: True if all health checks pass, False otherwise
        """
        self.logger.info("Performing health checks")
        
        # Check Mihomo API connectivity
        if self.api_client is None:
            self.logger.critical("API client not initialized")
            return False
            
        try:
            is_connected = await self.api_client.check_connectivity()
            if not is_connected:
                self.logger.critical(
                    "Health check failed: Cannot connect to Mihomo API",
                    extra={
                        "api_url": self.config_manager.get_mihomo_api_url() if self.config_manager else "Unknown"
                    }
                )
                return False
            self.logger.info("Mihomo API connectivity check passed")
        except Exception as e:
            self.logger.critical(
                "Health check failed: Exception during API connectivity check",
                extra={
                    "error": str(e)
                }
            )
            return False
        
        # Check if Mosdns config directory is writable
        if self.config_manager is None:
            self.logger.critical("Config manager not initialized")
            return False
            
        config_path = self.config_manager.get_mosdns_config_path()
        config_dir = os.path.dirname(config_path)
        
        if not os.path.exists(config_dir):
            self.logger.critical(
                "Health check failed: Mosdns config directory does not exist",
                extra={
                    "config_dir": config_dir
                }
            )
            return False
            
        if not os.access(config_dir, os.W_OK):
            self.logger.critical(
                "Health check failed: Mosdns config directory is not writable",
                extra={
                    "config_dir": config_dir
                }
            )
            return False
            
        self.logger.info(
            "Mosdns config directory check passed",
            extra={
                "config_dir": config_dir
            }
        )
        
        return True

    async def start(self):
        """Start the synchronization service."""
        try:
            # Initialize the service
            await self.initialize()
            
            # Perform health checks
            if not await self.health_check():
                self.logger.critical("Health checks failed. Exiting.")
                return 1
            
            # Set up signal handlers for graceful shutdown (only on Unix-like systems)
            if os.name != 'nt':  # Not Windows
                loop = asyncio.get_running_loop()
                for sig in (signal.SIGTERM, signal.SIGINT):
                    loop.add_signal_handler(sig, self._signal_handler, sig)
            
            # Check that required components are initialized
            if self.rule_generator is None or self.state_monitor is None:
                self.logger.critical("Required components not initialized")
                return 1
                
            # Run initial rule generation to ensure Mosdns has a config
            self.logger.info("Performing initial rule generation")
            await self.rule_generator.run()
            
            # Start the state monitor
            self.logger.info("Starting state monitor")
            await self.state_monitor.start()
            
        except Exception as e:
            self.logger.critical(
                "Unhandled exception in main service",
                extra={
                    "error": str(e)
                },
                exc_info=True
            )
            return 1
        finally:
            await self.cleanup()
        
        return 0

    def _signal_handler(self, signum):
        """
        Handle shutdown signals.
        
        Args:
            signum: The signal number
        """
        signame = signal.Signals(signum).name
        self.logger.info(f"Received signal {signame}, initiating shutdown")
        self.shutdown_event.set()

    async def cleanup(self):
        """Clean up resources."""
        self.logger.info("Cleaning up resources")
        
        # Close API client
        if self.api_client:
            await self.api_client.close()
        
        self.logger.info("Cleanup completed")


async def main():
    """Main async function."""
    service = MihomoMosdnsSyncService()
    exit_code = await service.start()
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)