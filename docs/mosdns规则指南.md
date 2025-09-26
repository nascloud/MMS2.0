# MosDNS 匹配规则指南

### 匹配类型
| 类型     | 说明 | 示例 |
|----------|------|------|
| `domain` | 匹配域名及其子域名 | `google.com` 匹配 `www.google.com` |
| `full`   | 精确匹配域名 | 仅匹配 `google.com` |
| `keyword`| 包含关键字的域名 | 匹配 `google.com.hk` |
| `regexp` | Golang 正则匹配 | `.+\.google\.com$` |

### 注意事项
1. **优先级**：`full` > `domain` > `regexp` > `keyword`
2. **性能**：
   - `domain`/`full`：O(1) 复杂度，1万域名≈1MB内存
   - `keyword`/`regexp`：O(n) 复杂度，正则较耗资源

## Mihomo 规则对应关系
### yaml格式解析
| 类型        | 对应 MosDNS 类型 | 示例 |
|-----------------|------|------|
| `DOMAIN-SUFFIX` | `domain`         | `google.com` 匹配子域名 |
| `DOMAIN`        | `full`           | 仅匹配 `google.com` |
| `DOMAIN-KEYWORD`| `keyword`        | 匹配含关键字的域名 |
| `DOMAIN-REGEX`  | `regexp`         | 正则表达式匹配 |
| `IP-CIDR`       | 无前缀直接使用   | `192.168.1.0/24` |
| `IP-CIDR6`      | 无前缀直接使用   | `2001:db8::/32` |

### list格式解析

#### 通配符处理

##### [通配符 `*`]
list文件中的通配符 `*` 一次只能匹配一级域名

```
*.baidu.com` 只匹配 `tieba.baidu.com` 而不匹配 `123.tieba.baidu.com` 或者 `baidu.com
```

`*`只匹配 localhost 等没有`.`的主机名

##### [通配符 `+`]
通配符 ＋ 类似 DOMAIN-SUFFIX, 可以一次性匹配多个级别

```
＋.baidu.com` 匹配 `tieba.baidu.com` 和 `123.tieba.baidu.com` 或者 `baidu.com
```

通配符 `＋` 只能用于域名前缀匹配

##### [通配符 `.`]
通配符 . 可以一次性匹配多个级别

```
.baidu.com` 匹配 `tieba.baidu.com` 和 `123.tieba.baidu.com`, 但不能匹配 `baidu.com
```

通配符 `.` 只能用于域名前缀匹配

## 规则处理流程

### 单条规则处理
1. Mihomo 规则通过 RuleConverter 转换为 MosDNS 格式
2. 根据规则类型确定内容类型（domain/ipcidr）
3. 转换后的规则直接写入对应策略的文件

### Rule-Set 规则处理
1. 根据 behavior 类型选择处理方式：
   - `domain`: 使用 _parse_domain_rules 处理
   - `ipcidr`: 使用 _parse_ipcidr_rules 处理
   - `classical`: 使用 _parse_classical_rules 处理
2. 根据 format 类型处理：
   - `mrs`: 自动转换 URL 为对应的 list/yaml 格式
   - `text`: 直接处理文本内容
   - `yaml`: 解析 YAML 格式内容
3. 解析规则内容并转换为 MosDNS 格式
4. 根据规则内容自动识别类型（domain/ipcidr）

## 文件生成规范

### 最终文件命名
- domain 类型：`{policy}_domain.txt`
- ipcidr 类型：
  - 仅 IPv4：`{policy}_ipv4.txt`
  - 仅 IPv6：`{policy}_ipv6.txt`
  - 同时包含：分别生成 `{policy}_ipv4.txt` 和 `{policy}_ipv6.txt`

### 文件内容格式
- 每行一条规则
- 规则按字典序排序
- 自动去重