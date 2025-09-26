import yaml
import os
import logging
from typing import Dict, Any, Optional


class MihomoConfigParser:
    """Mihomo本地配置文件的解析器。"""
    
    def __init__(self):
        """初始化MihomoConfigParser。"""
        self.logger = logging.getLogger(__name__)
    
    def parse_config_file(self, config_path: str) -> Optional[Dict[str, Any]]:
        """
        解析Mihomo配置文件。
        
        Args:
            config_path (str): Mihomo配置文件的路径。
            
        Returns:
            dict: 解析后的配置数据，如果解析失败则返回None。
        """
        if not config_path or not os.path.exists(config_path):
            self.logger.warning(
                "未找到Mihomo配置文件或未指定路径",
                extra={"config_path": config_path}
            )
            return None
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                # 使用FullLoader来正确处理YAML锚点和合并
                config_data = yaml.load(f, Loader=yaml.FullLoader)
            
            self.logger.info(
                "成功解析Mihomo配置文件",
                extra={"config_path": config_path}
            )
            
            return config_data
        except Exception as e:
            self.logger.error(
                "解析Mihomo配置文件失败",
                extra={
                    "config_path": config_path,
                    "error": str(e)
                }
            )
            return None
    
    def extract_rule_providers(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从解析后的配置中提取规则提供者信息。
        
        Args:
            config_data (dict): 解析后的Mihomo配置数据。
            
        Returns:
            dict: 以提供者名称为键的规则提供者信息。
        """
        if not config_data or not isinstance(config_data, dict):
            return {}
            
        rule_providers = config_data.get('rule-providers', {})
        
        # 处理每个提供者以解析YAML锚点和合并
        processed_providers = {}
        for provider_name, provider_data in rule_providers.items():
            # 创建提供者数据的深拷贝以避免修改原始数据
            processed_provider = {}
            if isinstance(provider_data, dict):
                for key, value in provider_data.items():
                    processed_provider[key] = value
            processed_providers[provider_name] = processed_provider
        
        self.logger.debug(
            "从配置中提取规则提供者",
            extra={"providers_count": len(processed_providers)}
        )
        
        return processed_providers