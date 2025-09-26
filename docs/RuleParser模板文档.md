# RuleParser 模板文档

## 功能介绍

RuleParser（规则解析器）是 Mihomo-Mosdns 同步系统中的数据解析模块，负责解析从 Mihomo API 获取的原始数据，提取规则、代理和规则提供者信息。该模块将 API 返回的 JSON 数据转换为系统内部使用的结构化数据格式。

## 工作流程

1. **接收 API 数据**：接收来自 StateMonitor 的 Mihomo API 响应数据，包括规则、代理和规则提供者信息。

2. **解析规则数据**：从 API 响应中提取规则列表，验证数据结构并记录规则数量。

3. **解析代理数据**：从 API 响应中提取代理信息，验证数据结构并记录代理数量。

4. **解析规则提供者数据**：从 API 响应中提取规则提供者信息，验证数据结构并记录提供者数量。

5. **解析配置数据中的规则提供者信息**：从 Mihomo 配置数据中提取规则提供者定义，用于 RuleSet 规则的处理。

6. **返回结构化数据**：将解析后的数据以标准化格式返回给调用者。

## 输入参数

### parse_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| rules_data | Dict[str, Any] | 是 | 来自 Mihomo API 的规则数据 |

### parse_proxies 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| proxies_data | Dict[str, Any] | 是 | 来自 Mihomo API 的代理数据 |

### parse_rule_providers 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| rule_providers_data | Dict[str, Any] | 是 | 来自 Mihomo API 的规则提供者数据 |

### parse_rule_provider_info 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| config_data | Dict[str, Any] | 是 | 来自 Mihomo API 的配置数据 |

## 输出参数

### parse_rules 方法

| 返回类型 | 描述 |
|----------|------|
| List[Dict[str, Any]] | 解析后的规则列表，每个元素为一条规则的字典表示 |

### parse_proxies 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | 解析后的代理数据，以代理名称为键的字典 |

### parse_rule_providers 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | 解析后的规则提供者数据，以提供者名称为键的字典 |

### parse_rule_provider_info 方法

| 返回类型 | 描述 |
|----------|------|
| Dict[str, Any] | 解析后的规则提供者信息，以提供者名称为键的字典 |