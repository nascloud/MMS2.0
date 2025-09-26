# MihomoApiClient 模板文档

## 功能介绍

MihomoApiClient（Mihomo API 客户端）是 Mihomo-Mosdns 同步系统中的网络通信模块，负责与 Mihomo RESTful API 进行高容错通信。该模块内置指数退避重试机制和超时控制，确保在网络不稳定环境下依然能可靠地获取 Mihomo 状态数据。

## 工作流程

1. **初始化**：根据配置创建异步 HTTP 客户端，设置超时时间和认证头（如果提供了 API 密钥）。

2. **请求处理**：
   - 构造完整的 API URL
   - 根据重试配置执行指数退避重试：
     - 发起 HTTP 请求
     - 检查响应状态码（只接受 2xx 为成功）
     - 对于网络错误（超时、连接错误）或 5xx 服务器错误，执行重试
     - 对于 4xx 客户端错误，直接抛出异常
     - 计算下一次重试的延迟时间（指数退避 + 抖动）

3. **数据获取**：
   - get_rules(): 获取规则数据
   - get_proxies(): 获取代理数据
   - get_rule_providers(): 获取规则提供者数据
   - get_config(): 获取配置数据
   - check_connectivity(): 检查 API 连接性

4. **资源清理**：关闭 HTTP 客户端连接。

## 输入参数

### __init__ 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| api_base_url | str | 是 | Mihomo API 的基础 URL |
| timeout | int | 是 | 请求超时时间（秒） |
| retry_config | Dict[str, Any] | 是 | 重试配置，包含 max_retries、initial_backoff、max_backoff、jitter |
| api_secret | str | 否 | API 认证密钥，默认为空字符串 |

### _request 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| method | str | 是 | HTTP 方法（GET、POST 等） |
| endpoint | str | 是 | API 端点（如 "/rules"、"/proxies"） |

### get_rules, get_proxies, get_rule_providers, get_config, check_connectivity 方法

这些方法不需要额外参数。

## 输出参数

### __init__ 方法

该方法没有返回值，但会初始化以下实例变量：
- client: 异步 HTTP 客户端
- logger: 日志记录器

### _request 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | API 响应的 JSON 数据 |

### get_rules 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | Mihomo 规则数据 |

### get_proxies 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | Mihomo 代理数据 |

### get_rule_providers 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | Mihomo 规则提供者数据 |

### get_config 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | Mihomo 配置数据 |

### check_connectivity 方法

| 返回类型 | 描述 |
|----------|------|
| bool | 连接性检查结果，True 表示连接成功，False 表示连接失败 |

### close 方法

该方法没有返回值，但会关闭 HTTP 客户端连接。