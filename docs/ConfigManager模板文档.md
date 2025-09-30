# ConfigManager 模板文档

## 功能介绍

ConfigManager（配置管理器）是 Mihomo-Mosdns 同步系统的配置中心模块，负责加载、校验并提供所有应用级别的配置。该模块使用单例模式确保整个应用使用统一的配置，并在初始化时验证所有必需的配置项。

## 工作流程

1. **单例模式实现**：
   - 使用类变量 _instance 和 _initialized 实现单例模式
   - 确保整个应用只有一个 ConfigManager 实例

2. **配置加载**：
   - 读取指定路径的 YAML 配置文件
   - 使用 yaml.safe_load 解析配置文件

3. **配置验证**：
   - 验证所有必需的配置项是否存在
   - 验证 api_retry_config 的嵌套键是否存在
   - 验证配置项的数据类型

4. **配置提供**：
   - 提供各种配置项的获取方法
   - 返回配置项的值

## 输入参数

### __new__ 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| cls | class | 是 | ConfigManager 类 |
| config_path | str | 否 | 配置文件路径 |

### __init__ 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| config_path | str | 否 | 配置文件路径 |

## 输出参数

### __new__ 方法

| 返回类型 | 描述 |
|----------|------|
| ConfigManager | ConfigManager 实例 |

### __init__ 方法

该方法没有返回值，但会初始化以下实例变量：
- _config: 解析后的配置数据
- _initialized: 初始化标志

### 配置获取方法

| 方法名 | 返回类型 | 描述 |
|--------|----------|------|
| get_mihomo_api_url | str | Mihomo API 基础 URL |
| get_mihomo_api_timeout | int | API 请求超时时间（秒） |
| get_mihomo_api_secret | str | API 认证密钥 |
| get_mihomo_config_path | str | Mihomo 配置文件路径 |
| get_api_retry_config | Dict[str, Any] | API 重试配置 |
| get_polling_interval | float | 监控轮询间隔（秒） |
| get_debounce_interval | float | 事件防抖间隔（秒） |
| get_mosdns_rules_path | str | Mosdns 配置文件输出目录路径 |
| get_cache_dir_path | str | 缓存目录路径，用于存储下载的规则文件 |
| get_mosdns_reload_command | str | Mosdns 服务重载命令 |
| get_log_level | str | 日志级别 |
| get_log_file_path | str | 日志文件路径 |