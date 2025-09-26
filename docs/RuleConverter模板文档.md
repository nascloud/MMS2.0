# RuleConverter 模板文档

## 功能介绍

RuleConverter（规则转换器）是 Mihomo-Mosdns 同步系统中的纯工具类模块，负责将 Mihomo 规则转换为 Mosdns 格式。该模块已重构为无状态的工具类，只提供逻辑转换功能，不执行任何 I/O 或网络操作。所有方法均为静态方法，可以直接通过类名调用。

## 工作流程

1. **单条规则转换**：
   - 接收单条 Mihomo 规则字典
   - 根据规则类型确定内容类型（domain、ipv4、ipv6）
   - 将规则载荷转换为 Mosdns 格式
   - 返回转换后的规则字符串和内容类型

2. **RuleSet 规则处理**：
   - 接收 RuleSet 提供者信息
   - 根据提供者信息判断是从本地文件读取还是从网络下载
   - 对于 mrs 格式，自动转换 URL 为对应的 list 或 yaml 格式
   - 执行下载或读取操作，获取规则集的原始内容
   - 根据规则集的内容格式（通常是一行一条规则），将其解析为字符串列表
   - 根据行为类型（domain、ipcidr、classical）和规则内容自动识别规则类型
   - 返回解析后的规则列表

3. **格式转换**：
   - DOMAIN-SUFFIX → domain:payload (处理通配符如 *.example.com, +.example.com, .example.com)
   - DOMAIN → full:payload
   - DOMAIN-KEYWORD → keyword:payload
   - DOMAIN-REGEX → regexp:payload
   - IP-CIDR → payload (直接返回 CIDR 内容，不带前缀)
   - IP-CIDR6 → payload (直接返回 CIDR 内容，不带前缀)

4. **内容类型判断**：
   - DOMAIN-SUFFIX, DOMAIN, DOMAIN-KEYWORD, DOMAIN-REGEX → domain
   - IP-CIDR → ipv4
   - IP-CIDR6 → ipv6

## 输入参数

### convert_single_rule 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| rule | Dict[str, Any] | 是 | 单条 Mihomo 规则，包含 type 和 payload 等字段 |

### fetch_and_parse_ruleset 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| provider_info | Dict[str, Any] | 是 | RuleSet 提供者信息，包含 url、path、behavior、format 等字段 |

### _determine_content_type 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| rule_type | str | 是 | 规则类型（DOMAIN-SUFFIX、IP-CIDR 等） |

### _convert_format 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| rule_type | str | 是 | 规则类型（DOMAIN-SUFFIX、IP-CIDR 等） |
| content | str | 是 | 规则载荷内容 |

### _parse_domain_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| url | str | 是 | 下载域名规则的 URL |
| path | str | 否 | 本地域名规则文件路径，默认为空 |

### _parse_ipcidr_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| url | str | 是 | 下载 IPCIDR 规则的 URL |
| path | str | 否 | 本地 IPCIDR 规则文件路径，默认为空 |

### _parse_classical_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| url | str | 是 | 下载经典规则的 URL |
| path | str | 否 | 本地经典规则文件路径，默认为空 |

## 输出参数

### convert_single_rule 方法

| 返回类型 | 描述 |
|----------|------|
| Tuple[str | None, str | None] | 元组包含转换后的 Mosdns 格式字符串和内容类型，如果不支持则返回 (None, None) |

### fetch_and_parse_ruleset 方法

| 返回类型 | 描述 |
|----------|------|
| List[str] | 解析后的规则字符串列表 |

### _determine_content_type 方法

| 返回类型 | 描述 |
|----------|------|
| str | 内容类型，可能值为 "domain"、"ipv4"、"ipv6" |

### _convert_format 方法

| 返回类型 | 描述 |
|----------|------|
| str | 转换后的 Mosdns 格式规则，如果规则类型不支持则返回空字符串 |

### _parse_*_rules 方法

| 返回类型 | 描述 |
|----------|------|
| List[str] | 解析后的规则字符串列表