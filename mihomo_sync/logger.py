import logging
from pythonjsonlogger.json import JsonFormatter
import sys


def setup_logger(log_level='INFO'):
    """
    设置具有指定日志级别的全局JSON记录器。
    
    Args:
        log_level (str): 日志级别 (例如: 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
    """
    # 获取根记录器
    root_logger = logging.getLogger()
    
    # 设置日志级别
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # 创建带有附加字段的JSON格式化器，用于结构化日志记录
    json_formatter = JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        rename_fields={'asctime': 'timestamp', 'name': 'module', 'levelname': 'level'},
        static_fields={'service_name': 'mihomo-mosdns-sync'}
    )
    
    # 创建一个将输出到stdout的流处理器
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(json_formatter)
    
    # 将处理器添加到根记录器
    if not root_logger.handlers:
        root_logger.addHandler(stream_handler)