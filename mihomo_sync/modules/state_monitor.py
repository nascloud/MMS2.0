import asyncio
import hashlib
import json
import logging
from typing import Callable, Dict, Any


class StateMonitor:
    """A monitor that detects changes in Mihomo's state and triggers actions with debounce logic."""
    
    def __init__(self, api_client, polling_interval: float, debounce_interval: float, 
                 on_change_callback: Callable):
        """
        Initialize the StateMonitor.
        
        Args:
            api_client: An instance of MihomoApiClient
            polling_interval (float): Time interval between polling in seconds
            debounce_interval (float): Time to wait before triggering action after change in seconds
            on_change_callback (Callable): Function to call when a change is confirmed
        """
        self.api_client = api_client
        self.polling_interval = polling_interval
        self.debounce_interval = debounce_interval
        self.on_change_callback = on_change_callback
        self.logger = logging.getLogger(__name__)
        self._last_state_hash = None
        self._debounce_task = None

    async def _get_state_hash(self) -> str:
        """
        Get a hash digest representing the current state of Mihomo.
        
        Returns:
            str: SHA-256 hash of the current state
        """
        try:
            # Get proxies and rule providers data
            proxies_data = await self.api_client.get_proxies()
            rule_providers_data = await self.api_client.get_rule_providers()
            
            # Create a state snapshot with only the essential information
            state_snapshot = {
                "proxies": {},
                "rule_providers": {}
            }
            
            # Extract proxy information (strategy groups and their current selection)
            for name, proxy in proxies_data.get("proxies", {}).items():
                if proxy.get("type") in ["Selector", "Fallback"]:
                    state_snapshot["proxies"][name] = {
                        "name": name,
                        "now": proxy.get("now")
                    }
            
            # Extract rule provider information (name and update time)
            for name, provider in rule_providers_data.get("providers", {}).items():
                state_snapshot["rule_providers"][name] = {
                    "name": name,
                    "updatedAt": provider.get("updatedAt")
                }
            
            # Sort the snapshot to ensure consistent hashing
            sorted_snapshot = json.dumps(state_snapshot, sort_keys=True, separators=(',', ':'))
            
            # Generate SHA-256 hash
            return hashlib.sha256(sorted_snapshot.encode('utf-8')).hexdigest()
            
        except Exception as e:
            self.logger.error(
                "Failed to get state hash",
                extra={
                    "error": str(e)
                }
            )
            raise

    async def start(self):
        """Start the monitoring loop."""
        self.logger.info("Starting state monitor")
        
        while True:
            try:
                # Get current state hash
                current_state_hash = await self._get_state_hash()
                
                # Compare with previous state
                if self._last_state_hash is not None and current_state_hash != self._last_state_hash:
                    self.logger.info(
                        "State change detected",
                        extra={
                            "previous_hash": self._last_state_hash,
                            "current_hash": current_state_hash
                        }
                    )
                    
                    # Cancel any existing debounce task
                    if self._debounce_task and not self._debounce_task.done():
                        self._debounce_task.cancel()
                        try:
                            await self._debounce_task
                        except asyncio.CancelledError:
                            pass
                    
                    # Create a new debounce task
                    self._debounce_task = asyncio.create_task(self._debounce_and_trigger())
                
                # Update last state hash
                self._last_state_hash = current_state_hash
                
                # Wait for the next polling interval
                await asyncio.sleep(self.polling_interval)
                
            except Exception as e:
                self.logger.error(
                    "Error in monitoring loop",
                    extra={
                        "error": str(e)
                    }
                )
                # Wait before retrying
                await asyncio.sleep(self.polling_interval)

    async def _debounce_and_trigger(self):
        """Wait for the debounce interval and then trigger the callback."""
        try:
            await asyncio.sleep(self.debounce_interval)
            self.logger.info("Debounce period completed, triggering callback")
            await self.on_change_callback()
        except Exception as e:
            self.logger.error(
                "Error in debounce trigger",
                extra={
                    "error": str(e)
                }
            )