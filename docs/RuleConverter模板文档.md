# RuleConverter 模板文档

## 功能介绍

RuleConverter（规则转换器）是 Mihomo-Mosdns 同步系统中的核心模块之一，负责将 Mihomo 规则转换为 Mosdns 格式，并生成中间文件。该模块处理各种类型的规则，包括普通规则和 RuleSet 规则，并支持多种规则提供者格式（domain、ipcidr、classical）和文件格式（yaml、text、mrs）。

## 工作流程

1. **接收规则输入**：接收来自 StateMonitor 的单条 Mihomo 规则、最终策略名称、临时目录路径和规则提供者信息。

2. **确定内容类型**：根据规则类型（如 DOMAIN-SUFFIX、IP-CIDR 等）或规则载荷确定内容类型（domain、ipv4、ipv6）。

3. **获取规则内容**：
   - 对于普通规则，直接使用规则载荷作为内容
   - 对于 RuleSet 规则，根据提供者信息处理规则集：
     - 如果是 mrs 格式，将 URL 从 .mrs 转换为 .list 或 .yaml 格式
     - 根据 behavior 属性（domain、ipcidr、classical）解析规则内容
     - 从 URL 下载或从本地路径读取规则内容

4. **格式转换**：
   - 对于 RuleSet 规则，规则内容已经过处理，直接使用
   - 对于其他规则类型，将每条内容转换为 Mosdns 格式：
     - DOMAIN-SUFFIX → domain:payload
     - DOMAIN → full:payload
     - DOMAIN-KEYWORD → keyword:payload
     - DOMAIN-REGEX → regexp:payload
     - IP-CIDR → ip-cidr:payload
     - IP-CIDR6 → ip-cidr6:payload

5. **保存中间文件**：
   - 为每条 Mosdns 规则生成唯一的文件名（使用 MD5 哈希）
   - 根据最终策略名称和内容类型创建目录结构：temp_dir/policy/content_type/
   - 将每条规则保存为单独的 .txt 文件

## 输入参数

### convert_and_save 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| mihomo_rule | Dict[str, Any] | 是 | 单条 Mihomo 规则，包含 type 和 payload 等字段 |
| final_policy | str | 是 | 最终策略名称（DIRECT、PROXY、REJECT） |
| temp_dir | str | 是 | 临时目录路径，用于保存中间文件 |
| provider_info | Dict[str, Any] | 是 | 规则提供者信息，包含 url、path、behavior、format 等字段 |

## 输出参数

### convert_and_save 方法

该方法没有返回值，但会产生以下副作用：

1. **中间文件生成**：在 temp_dir 目录下创建以下目录结构并生成文件：
   ```
   temp_dir/
   ├── policy_name/
   │   ├── domain/
   │   │   ├── md5_hash1.txt
   │   │   ├── md5_hash2.txt
   │   │   └── ...
   │   ├── ipv4/
   │   │   ├── md5_hash3.txt
   │   │   └── ...
   │   └── ipv6/
   │       ├── md5_hash4.txt
   │       └── ...
   ```

2. **日志记录**：记录规则转换过程中的关键信息和错误。

### _determine_content_type 方法

| 返回类型 | 描述 |
|----------|------|
| str | 内容类型，可能值为 "domain"、"ipv4"、"ipv6" |

### _get_rule_content 方法

| 返回类型 | 描述 |
|----------|------|
| List[str] | 规则内容列表，每个元素为一条规则 |

### _convert_format 方法

| 返回类型 | 描述 |
|----------|------|
| str | 转换后的 Mosdns 格式规则，如果规则类型不支持则返回空字符串 |