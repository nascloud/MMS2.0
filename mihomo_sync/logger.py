import logging
from pythonjsonlogger.json import JsonFormatter
import sys
import json
import os
from datetime import datetime


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
        
        # 添加进程ID和线程信息
        if not hasattr(record, 'pid'):
            record.pid = os.getpid()
            
        # 添加时间戳（毫秒级）
        if hasattr(record, 'asctime'):
            # 解析原始时间并添加毫秒
            try:
                dt = datetime.strptime(record.asctime, "%Y-%m-%d %H:%M:%S,%f")
                record.timestamp_ms = int(dt.timestamp() * 1000)
            except:
                record.timestamp_ms = int(datetime.now().timestamp() * 1000)
        
        return super().format(record)
    
    def serialize_log_record(self, log_record):
        """重写序列化方法，确保中文正确显示"""
        return json.dumps(log_record, ensure_ascii=False, separators=(',', ':'))


def setup_logger(log_level='INFO', log_file_path=None):
    """
    设置具有指定日志级别的全局JSON记录器。
    
    Args:
        log_level (str): 日志级别 (例如: 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        log_file_path (str): 日志文件路径（可选）
    """
    # 获取根记录器
    root_logger = logging.getLogger()
    
    # 清除现有处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()
    
    # 设置日志级别
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # 创建带有附加字段的自定义JSON格式化器，用于结构化日志记录
    json_formatter = ChineseJsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d',
        rename_fields={
            'asctime': '时间', 
            'name': '模块', 
            'levelname': '级别',
            'filename': '文件',
            'lineno': '行号'
        },
        static_fields={
            '服务名称': 'mihomo-mosdns-sync',
            '版本': '2.0'
        }
    )
    
    # 创建一个将输出到stdout的流处理器
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(json_formatter)
    
    # 将处理器添加到根记录器
    root_logger.addHandler(stream_handler)
    
    # 如果指定了日志文件路径，则添加文件处理器
    if log_file_path:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(json_formatter)
        root_logger.addHandler(file_handler)
        
        # 记录日志配置信息
        root_logger.info(
            "日志系统初始化完成",
            extra={
                "日志级别": log_level,
                "控制台输出": True,
                "文件输出": log_file_path
            }
        )