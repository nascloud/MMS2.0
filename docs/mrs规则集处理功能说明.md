# mrs 规则集处理功能说明

## 概述

本功能扩展了 Mihomo-Mosdns 同步器，使其能够处理 `mrs` 格式的规则集提供者。`mrs` 是 Mihomo 使用的一种预编译、高效的规则格式，但 Mosdns 无法直接使用这种格式。本功能通过获取 `mrs` 规则集的源 URL 并请求其文本格式的变体来解决这个问题。

## 实现原理

根据对 Mihomo API 的分析，我们发现：
1. **API 提供的是运行时状态**：API 接口如 `/rules` 和 `/proxies` 返回的是 Mihomo 当前的运行时状态，不包含规则提供者的静态配置信息。
2. **API 缺少静态配置定义**：API 响应中没有包含 `rule-provider` 的原始配置信息，如 `url`、`type`、`behavior` 或 `format` 等静态配置信息。
3. **必须解析配置文件**：为了获取 `rule-providers` 的静态定义信息，必须访问并解析 Mihomo 的主配置文件。

因此，我们的实现结合了 API 和配置文件解析两种方式：

1. **获取配置信息**：通过 Mihomo API 的 `/configs` 端点获取主配置文件内容
2. **解析提供者信息**：从配置中提取所有规则提供者的完整信息，包括 `url`、`behavior` 和 `format` 属性
3. **识别 mrs 提供者**：检查规则提供者的 URL 是否以 `.mrs` 结尾
4. **根据 behavior 和 format 转换 URL**：
   - 对于 `domain` 和 `ipcidr` 行为的提供者，将 `.mrs` 转换为 `.list`
   - 对于 `classical` 行为的提供者，将 `.mrs` 转换为 `.yaml`
5. **下载规则**：从转换后的 URL 下载规则内容
6. **根据 behavior 解析规则**：
   - `domain` 行为：将每行内容作为域名处理
   - `ipcidr` 行为：将每行内容作为 IP CIDR 处理
   - `classical` 行为：按逗号分隔解析完整规则
7. **转换格式**：将解析的规则转换为 Mosdns 可识别的格式

## 核心功能

### API 客户端扩展

在 `MihomoApiClient` 类中添加了两个新方法：

1. `get_config()` - 获取主配置文件
2. `get_ruleset_content(ruleset_name)` - 获取特定规则集的内容

### 规则生成器增强

在 `MosdnsRuleGenerator` 类中添加了以下方法：

1. `_parse_rule_provider_info(config_data)` - 解析配置文件中的规则提供者完整信息（包括 url、behavior、format）
2. `_download_ruleset_content(provider_name, provider_info)` - 下载规则集内容并处理不同格式和行为

### 规则处理逻辑

修改了 `run()` 方法中的 RULE-SET 规则处理逻辑：

1. 首先通过 `get_config()` 获取主配置文件
2. 使用 `_parse_rule_provider_info()` 解析配置文件中的 `rule-providers` 部分
3. 建立从 provider 名称到完整信息（url、behavior、format）的映射关系
4. 在处理 RULE-SET 规则时，使用 provider 名称查找对应的完整信息
5. 根据 behavior 和 format 属性决定如何处理规则集
6. 如果是 mrs 格式的提供者，则根据 behavior 转换 URL 并下载文本格式内容
7. 根据 behavior 解析下载的内容
8. 如果不是 mrs 格式或下载失败，则回退到原有的 API 方法

## URL 转换规则

根据 behavior 属性决定 URL 转换方式：
- `domain` 或 `ipcidr` 行为：`.mrs` → `.list`
- `classical` 行为：`.mrs` → `.yaml`

例如：
- `https://example.com/google-domain.mrs` → `https://example.com/google-domain.list`
- `https://example.com/classical-rules.mrs` → `https://example.com/classical-rules.yaml`

## 根据 behavior 解析规则

1. **`domain` 行为**：
   - 内容：文件中只包含域名或域名通配符
   - 解析策略：将文件中的每一条目都视为一个域名匹配规则
   - Mosdns 转换：生成 `domain:example.com:Proxy` 格式的规则（将每行内容作为域名后缀处理）

2. **`ipcidr` 行为**：
   - 内容：文件中只包含 IP 地址或 CIDR 地址块
   - 解析策略：将每一条目都视为一个 IP CIDR 规则
   - Mosdns 转换：生成 `ip-cidr:192.168.1.0/24:Proxy` 格式的规则

3. **`classical` 行为**：
   - 内容：文件中可以包含各种路由规则，例如 `DOMAIN-SUFFIX,google.com`、`IP-CIDR,127.0.0.0/8` 等
   - 解析策略：逐行解析，并根据逗号分隔的第一部分来判断规则的具体类型
   - Mosdns 转换：根据规则类型生成相应的格式：
     - `DOMAIN,example.com` → `full:example.com:Proxy`（精确匹配）
     - `DOMAIN-SUFFIX,google.com` → `domain:google.com:Proxy`（后缀匹配）
     - `DOMAIN-KEYWORD,google` → `keyword:google:Proxy`（关键字匹配）
     - `IP-CIDR,192.168.1.0/24` → `ip-cidr:192.168.1.0/24:Proxy`
     - `IP-CIDR6,2001:db8::/32` → `ip-cidr6:2001:db8::/32:Proxy`

## 支持的格式

1. **`yaml` 格式**：
   - 结构：文件是一个 YAML 文件，其中规则内容被包含在一个名为 `payload` 的键下
   - 解析策略：使用 YAML 解析器读取文件，提取 `payload` 键对应的值

2. **`text` 格式**：
   - 结构：文件是一个纯文本文件，每一行就是一条规则
   - 解析策略：直接按行读取文件

3. **`mrs` 格式**：
   - 结构：这是一种预编译的二进制格式，无法直接通过文本解析
   - 解析策略：转换 URL 后按 `text`/`yaml` 方式解析

## 正确的 Mihomo 到 MosDNS 规则转换

根据 mosdns 规则指南，正确的转换关系如下：

| Mihomo 类型        | MosDNS 类型 | 说明 |
|-------------------|-------------|------|
| `DOMAIN`          | `full`      | 精确匹配域名 |
| `DOMAIN-SUFFIX`   | `domain`    | 匹配域名及其子域名 |
| `DOMAIN-KEYWORD`  | `keyword`   | 包含关键字的域名 |
| `DOMAIN-REGEX`    | `regexp`    | Golang 正则匹配 |
| `IP-CIDR`         | `ip-cidr`   | IPv4 CIDR 匹配 |
| `IP-CIDR6`        | `ip-cidr6`  | IPv6 CIDR 匹配 |

## 错误处理

1. 如果无法下载 `.list` 或 `.yaml` 格式的规则，会记录警告日志并回退到原有逻辑
2. 如果原有 API 方法也失败，会添加注释规则而不是跳过
3. 所有 HTTP 请求都有适当的超时和错误处理

## 使用示例

假设有以下 Mihomo 配置：

```
rule-providers:
  google-domain:
    type: http
    behavior: domain
    format: mrs
    url: "https://example.com/google-domain.mrs"
    path: "./rule-providers/google-domain.mrs"
  classical-rules:
    type: http
    behavior: classical
    format: mrs
    url: "https://example.com/classical-rules.mrs"
    path: "./rule-providers/classical-rules.mrs"

rules:
  - RULE-SET,google-domain,Proxy
  - RULE-SET,classical-rules,Proxy
```

处理流程：

1. 通过 `/configs` API 获取配置文件内容
2. 解析配置文件，建立 provider 名称到完整信息的映射：
   - `google-domain`: {url: "https://example.com/google-domain.mrs", behavior: "domain", format: "mrs"}
   - `classical-rules`: {url: "https://example.com/classical-rules.mrs", behavior: "classical", format: "mrs"}
3. 在处理 RULE-SET 规则时：
   - 对于 `google-domain`，识别为 domain 行为的 mrs 提供者，转换 URL 为 `.list` 格式
   - 对于 `classical-rules`，识别为 classical 行为的 mrs 提供者，转换 URL 为 `.yaml` 格式
4. 下载 `.list` 或 `.yaml` 文件内容
5. 根据 behavior 解析文件内容：
   - `domain` 行为：将每行内容作为域名后缀处理，生成 `domain:example.com:Proxy` 格式的规则
   - `classical` 行为：按逗号分隔解析完整规则，并根据规则类型正确转换：
     - `DOMAIN,example.com` → `full:example.com:Proxy`
     - `DOMAIN-SUFFIX,google.com` → `domain:google.com:Proxy`
     - `DOMAIN-KEYWORD,google` → `keyword:google:Proxy`
6. 解析文件中的规则并转换为 Mosdns 格式
7. 生成正确的 Mosdns 规则格式

## 优势

1. **无缝集成**：无需修改现有配置即可支持 mrs 格式
2. **向后兼容**：对非 mrs 格式的规则集保持原有处理逻辑
3. **智能处理**：根据 behavior 和 format 属性智能选择处理策略
4. **正确转换**：严格按照 mosdns 规则指南进行规则类型转换
5. **高效处理**：直接从源 URL 获取文本格式，避免了解析二进制格式的复杂性
6. **错误恢复**：多重回退机制确保规则处理的可靠性
7. **完整实现**：结合 API 和配置文件解析，完整实现了规则转换器所需的所有信息获取