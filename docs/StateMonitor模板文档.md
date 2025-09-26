# StateMonitor 模板文档

## 功能介绍

StateMonitor（状态监控器）是 Mihomo-Mosdns 同步系统的核心驱动模块，负责深度监控 Mihomo 的状态变化并触发规则生成流程。该模块通过定期轮询 Mihomo API，使用哈希摘要比对精确检测状态变化，并通过防抖机制优化规则生成触发。

## 工作流程

1. **初始化**：接收所有依赖模块的实例（API 客户端、Mosdns 控制器等）和配置参数。

2. **监控循环**：
   - 按配置的时间间隔轮询 Mihomo API
   - 提取关键状态数据（策略组当前选择、规则提供者更新时间）
   - 对状态数据进行排序并生成 SHA-256 哈希摘要
   - 比对当前哈希与上次哈希，检测状态变化

3. **变化处理**：
   - 如果检测到状态变化：
     - 取消任何现有的防抖任务
     - 创建新的防抖任务，在防抖间隔后触发规则生成

4. **防抖机制**：
   - 在防抖间隔内，连续的状态变化只会触发一次规则生成
   - 防抖间隔结束后，执行规则生成流程

5. **规则生成流程**：
   - 创建临时目录用于存储中间文件
   - 从 Mihomo API 获取所有必要数据（规则、代理、规则提供者、配置）
   - 解析 Mihomo 本地配置文件（如果配置了路径）
   - 初始化所有处理模块（策略解析器、规则解析器、规则转换器、规则合并器）
   - 解析 API 数据
   - 处理每条规则：
     - 提取规则目标
     - 使用策略解析器确定最终出口策略
     - 使用规则转换器转换并保存规则
   - 使用规则合并器合并所有中间文件
   - 重载 Mosdns 服务

## 输入参数

### __init__ 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| api_client | MihomoApiClient | 是 | Mihomo API 客户端实例 |
| mosdns_controller | MosdnsServiceController | 是 | Mosdns 服务控制器实例 |
| mosdns_config_path | str | 是 | Mosdns 配置文件输出目录路径 |
| polling_interval | float | 是 | 轮询间隔（秒） |
| debounce_interval | float | 是 | 防抖间隔（秒） |
| mihomo_config_parser | MihomoConfigParser | 否 | Mihomo 配置解析器实例 |
| mihomo_config_path | str | 否 | Mihomo 配置文件路径 |

### start 方法

该方法不需要额外参数。

### _get_state_hash 方法

该方法不需要额外参数。

### _debounce_and_trigger 方法

该方法不需要额外参数。

### _generate_rules 方法

该方法不需要额外参数。

## 输出参数

### __init__ 方法

该方法没有返回值，但会初始化以下实例变量：
- api_client: Mihomo API 客户端实例
- mosdns_controller: Mosdns 服务控制器实例
- mosdns_config_path: Mosdns 配置文件输出目录路径
- polling_interval: 轮询间隔
- debounce_interval: 防抖间隔
- mihomo_config_parser: Mihomo 配置解析器实例
- mihomo_config_path: Mihomo 配置文件路径
- logger: 日志记录器
- _last_state_hash: 上次状态哈希
- _debounce_task: 防抖任务

### start 方法

该方法没有返回值，但会持续运行监控循环直到被中断。

### _get_state_hash 方法

| 返回类型 | 描述 |
|----------|------|
| str | 当前状态的 SHA-256 哈希摘要 |

### _debounce_and_trigger 方法

该方法没有返回值，但在防抖间隔结束后会触发规则生成。

### _generate_rules 方法

该方法没有返回值，但会产生以下副作用：
- 生成中间文件
- 生成最终规则文件
- 重载 Mosdns 服务
- 记录执行日志