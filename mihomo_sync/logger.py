import logging
from pythonjsonlogger.json import JsonFormatter
import sys
import json


class ChineseJsonFormatter(JsonFormatter):
    """支持中文日志级别的JSON格式化器。"""
    
    # 日志级别的中文映射
    LEVEL_CHINESE = {
        'DEBUG': '调试',
        'INFO': '信息',
        'WARNING': '警告',
        'WARN': '警告',
        'ERROR': '错误',
        'CRITICAL': '严重'
    }
    
    def format(self, record):
        # 将英文日志级别转换为中文
        if hasattr(record, 'levelname') and record.levelname in self.LEVEL_CHINESE:
            record.levelname = self.LEVEL_CHINESE[record.levelname]
        return super().format(record)
    
    def serialize_log_record(self, log_record):
        """重写序列化方法，确保中文正确显示"""
        return json.dumps(log_record, ensure_ascii=False)


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
    
    # 创建带有附加字段的自定义JSON格式化器，用于结构化日志记录
    json_formatter = ChineseJsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        rename_fields={'asctime': '时间', 'name': '模块', 'levelname': '级别'},
        static_fields={'服务名称': 'mihomo-mosdns-sync'}
    )
    
    # 创建一个将输出到stdout的流处理器
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(json_formatter)
    
    # 将处理器添加到根记录器
    if not root_logger.handlers:
        root_logger.addHandler(stream_handler)