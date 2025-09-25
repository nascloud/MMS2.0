import yaml
import os


class ConfigManager:
    """A singleton class to manage application configuration."""
    
    _instance = None
    _initialized = False

    def __new__(cls, config_path=None):
        """
        Create a new instance or return the existing singleton instance.
        
        Args:
            config_path (str): Path to the YAML configuration file.
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path=None):
        """
        Initialize the ConfigManager with the given configuration file.
        
        Args:
            config_path (str): Path to the YAML configuration file.
        """
        if not ConfigManager._initialized:
            if config_path is None or not os.path.exists(config_path):
                raise ValueError("Configuration file path is required and must exist.")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            
            # Validate required keys
            required_keys = [
                'mihomo_api_url', 'mihomo_api_timeout', 'api_retry_config',
                'polling_interval', 'debounce_interval', 'mosdns_config_path',
                'mosdns_reload_command', 'log_level'
            ]
            
            for key in required_keys:
                if key not in self._config:
                    raise ValueError(f"Missing required configuration key: {key}")
                
                # Check nested keys for api_retry_config
                if key == 'api_retry_config' and isinstance(self._config[key], dict):
                    retry_keys = ['max_retries', 'initial_backoff', 'max_backoff', 'jitter']
                    for retry_key in retry_keys:
                        if retry_key not in self._config[key]:
                            raise ValueError(f"Missing required configuration key: api_retry_config.{retry_key}")
                elif key == 'api_retry_config' and not isinstance(self._config[key], dict):
                    raise ValueError(f"api_retry_config must be a dictionary, got {type(self._config[key])}")
            
            ConfigManager._initialized = True

    def get_mihomo_api_url(self):
        """Get the Mihomo API base URL."""
        return self._config.get('mihomo_api_url')

    def get_mihomo_api_timeout(self):
        """Get the API request timeout in seconds."""
        return self._config.get('mihomo_api_timeout')
        
    def get_mihomo_api_secret(self):
        """Get the API secret for authentication."""
        return self._config.get('mihomo_api_secret', '')

    def get_api_retry_config(self):
        """Get the API retry configuration dictionary."""
        return self._config.get('api_retry_config')

    def get_polling_interval(self):
        """Get the monitoring polling interval in seconds."""
        return self._config.get('polling_interval')

    def get_debounce_interval(self):
        """Get the event debounce interval in seconds."""
        return self._config.get('debounce_interval')

    def get_mosdns_config_path(self):
        """Get the path to the generated Mosdns rule file."""
        return self._config.get('mosdns_config_path')

    def get_mosdns_reload_command(self):
        """Get the command to reload the Mosdns service."""
        return self._config.get('mosdns_reload_command')

    def get_log_level(self):
        """Get the logging level."""
        return self._config.get('log_level')