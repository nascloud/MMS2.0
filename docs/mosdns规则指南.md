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

### list格式解析

### [通配符 `*`]

list文件中的 的通配符 `*` 一次只能匹配一级域名

```
*.baidu.com` 只匹配 `tieba.baidu.com` 而不匹配 `123.tieba.baidu.com` 或者 `baidu.com
```

`*`只匹配 localhost 等没有`.`的主机名

### [通配符 `+`]
通配符 ＋ 类似 DOMAIN-SUFFIX, 可以一次性匹配多个级别

```
＋.baidu.com` 匹配 `tieba.baidu.com` 和 `123.tieba.baidu.com` 或者 `baidu.com
```

通配符 `＋` 只能用于域名前缀匹配

### [通配符 `.`]

通配符 . 可以一次性匹配多个级别

```
.baidu.com` 匹配 `tieba.baidu.com` 和 `123.tieba.baidu.com`, 但不能匹配 `baidu.com
```

通配符 `.` 只能用于域名前缀匹配