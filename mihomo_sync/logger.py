import logging
from pythonjsonlogger.json import JsonFormatter
import sys


def setup_logger(log_level='INFO'):
    """
    Set up a global JSON logger with the specified log level.
    
    Args:
        log_level (str): The logging level (e.g., 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
    """
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Set the log level
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Create a JSON formatter with additional fields for structured logging
    json_formatter = JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        rename_fields={'asctime': 'timestamp', 'name': 'logger', 'levelname': 'level'},
        static_fields={'service_name': 'mihomo-mosdns-sync'}
    )
    
    # Create a stream handler that outputs to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(json_formatter)
    
    # Add the handler to the root logger
    if not root_logger.handlers:
        root_logger.addHandler(stream_handler)