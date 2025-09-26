# MihomoConfigParser 模板文档

## 功能介绍

MihomoConfigParser（Mihomo 配置解析器）是 Mihomo-Mosdns 同步系统的配置文件处理模块，负责解析 Mihomo 的本地配置文件以获取完整的 rule-providers 定义。该模块使用 YAML 解析器处理配置文件，并提取规则提供者的完整信息，包括 URL、路径、格式、行为等属性。

## 工作流程

1. **配置文件解析**：
   - 检查配置文件路径是否存在
   - 使用 YAML FullLoader 解析配置文件
   - 处理 YAML 锚点和合并
   - 返回解析后的配置数据

2. **规则提供者信息提取**：
   - 从配置数据中提取 rule-providers 部分
   - 处理每个提供者的数据，创建深拷贝以避免修改原始数据
   - 返回以提供者名称为键的字典

## 输入参数

### __init__ 方法

该方法不需要额外参数。

### parse_config_file 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| config_path | str | 是 | Mihomo 配置文件的路径 |

### extract_rule_providers 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| config_data | Dict[str, Any] | 是 | 解析后的 Mihomo 配置数据 |

## 输出参数

### __init__ 方法

该方法没有返回值，但会初始化以下实例变量：
- logger: 日志记录器

### parse_config_file 方法

| 返回类型 | 描述 |
|----------|------|
| Optional[Dict[str, Any]] | 解析后的配置数据，如果解析失败则返回 None |

### extract_rule_providers 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | 规则提供者信息字典，以提供者名称为键 |