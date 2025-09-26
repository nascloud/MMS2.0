# rule-providers 文件内容

## classical

`classical` 支持[路由规则](../rules/index.md)的全部类型 (rule-set/sub-rule 除外)

=== "yaml"
    ```{.yaml linenums="1"}
    payload:
    - DOMAIN-SUFFIX,google.com
    - DOMAIN-KEYWORD,google
    - DOMAIN,ad.com
    - SRC-IP-CIDR,192.168.1.201/32
    - IP-CIDR,127.0.0.0/8
    - GEOIP,CN
    - DST-PORT,80
    - SRC-PORT,7777
    ```

=== "text"
    ```text
    DOMAIN-SUFFIX,google.com
    DOMAIN-KEYWORD,google
    DOMAIN,ad.com
    SRC-IP-CIDR,192.168.1.201/32
    IP-CIDR,127.0.0.0/8
    GEOIP,CN
    DST-PORT,80
    SRC-PORT,7777
    ```

## domain

`domain`类规则集合内容通配应遵守[clash 通配符](../../handbook/syntax.md#_8)

=== "yaml"
    ```{.yaml linenums="1"}
    payload:
    - '.blogger.com'
    - '*.*.microsoft.com'
    - 'books.itunes.apple.com'
    ```

=== "text"
    ```text
    .blogger.com
    *.*.microsoft.com
    books.itunes.apple.com
    ```

## ipcidr

=== "yaml"
    ```{.yaml linenums="1"}
    payload:
    - '192.168.1.0/24'
    - '10.0.0.0.1/32'
    ```

=== "text"
    ```text
    192.168.1.0/24
    10.0.0.0.1/32
    ```

## 格式处理说明

### YAML 格式
YAML 格式的 rule-providers 使用 `payload` 字段包含规则列表，每个规则占一行。

### Text 格式
Text 格式的 rule-providers 每行直接包含一个规则，不使用 YAML 结构。

### MRS 格式
MRS 格式是 Mihomo 特有的二进制格式，需要转换为对应的文本格式进行处理：
- behavior 为 domain 时，转换为 text 格式处理
- behavior 为 ipcidr 时，转换为 text 格式处理
- behavior 为 classical 时，转换为 yaml 格式处理

## 内容类型识别

RuleConverter 会根据 rule-provider 的 behavior 字段和规则内容自动识别内容类型：

1. **domain 类型**：
   - 处理通配符格式（.example.com, *.example.com, +.example.com）
   - 转换为 MosDNS 的 domain:、full:、keyword: 格式

2. **ipcidr 类型**：
   - 直接使用 CIDR 格式
   - 自动识别 IPv4 和 IPv6 规则

3. **classical 类型**：
   - 根据规则前缀识别类型
   - DOMAIN-SUFFIX → domain:
   - DOMAIN → full:
   - DOMAIN-KEYWORD → keyword:
   - DOMAIN-REGEX → regexp:
   - IP-CIDR/IP-CIDR6 → 直接使用 CIDR 格式