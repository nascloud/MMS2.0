# rule-provider

```{.yaml linenums="1"}
rule-providers:
  google:
    type: http
    path: ./rule1.yaml
    url: "https://raw.githubusercontent.com/../Google.yaml"
    interval: 600
    proxy: DIRECT
    behavior: classical
    format: yaml
    size-limit: 0
    payload:
      - 'DOMAIN-SUFFIX,google.com'
```

## name

必须，如`google`,不能重复

## type

必须，`provider`类型，可选`http` / `file` / `inline`

## url

类型为`http`则必须配置

## path

可选，文件路径，不可重复，不填写时会使用 url 的 MD5 作为此文件的文件名

由于安全问题，此路径将限制只允许在 `HomeDir`(有启动参数 -d 配置) 中，如果想存储到其他位置，请通过设置 `SAFE_PATHS` 环境变量指定额外的安全路径。该环境变量的语法同本操作系统的PATH环境变量解析规则（即Windows下以分号分割，其他系统下以冒号分割）

## interval

更新`provider`的时间，单位为秒

## proxy

经过指定代理进行下载/更新

## behavior

行为，可选`domain`/`ipcidr`/`classical`，对应不同格式的 rule-provider 文件格式，请按实际格式填写

## format

格式，可选 `yaml`/`text`/`mrs`，默认 `yaml`

`mrs`目前 `behavior` 仅支持 `domain`/`ipcidr`，可以通过`mihomo convert-ruleset domain/ipcidr yaml/text XXX.yaml XXX.mrs`转换得到

## size-limit

限制下载文件的最大大小，默认为 0 即不限制文件大小，单位为字节 (`b`)

## payload

内容，仅 `type` 为 `inline` 时生效

## 配置处理说明

### 本地配置文件解析

Mihomo-Mosdns 同步器会解析 Mihomo 的本地配置文件以获取完整的 rule-providers 定义，包括：
- URL 地址（用于下载远程规则集）
- 本地路径（用于读取本地规则集）
- 格式类型（如 mrs 格式）
- 行为类型（domain, ipcidr, classical）

### MRS 格式处理

当 rule-provider 配置为 mrs 格式时，同步器会自动转换 URL：
- behavior 为 domain/ipcidr 时，将 .mrs 后缀替换为 .list
- behavior 为 classical 时，将 .mrs 后缀替换为 .yaml

### 优先级处理

配置文件中的 rule-providers 信息优先级高于 API 获取的信息，确保本地配置的准确性。