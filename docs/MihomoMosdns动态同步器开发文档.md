### **Mihomo-Mosdns 动态同步项目开发文档**

#### 1. 项目概述

**目标**: 本项目旨在实现 `mosdns` 的域名解析规则与 `mihomo` 的动态路由状态进行实时、可靠地同步。

**核心功能**: 开发一个独立的、高度健壮的监控服务。该服务通过 `mihomo` 提供的 API，实施**深度状态监控**，实时追踪流量的最终路由策略，并据此动态生成 `mosdns` 所需的配置文件。在状态发生确定性变化时，通过**防抖动机制**触发 `mosdns` 服务的**安全重载**，确保新规则高效、稳定地生效。

**解决的问题**:
* **自动化**: 替代手动配置 `mosdns`，实现全自动化、无人值守的规则管理。
* **一致性**: 通过精确的**深度状态比对**，确保 DNS 解析层策略（`mosdns`）与代理层策略（`mihomo`）的最终出口（Final Decision）完全一致，杜绝因策略不匹配导致的网络连接问题。
* **动态性与稳定性**: 能够响应 `mihomo` 中的用户操作或规则集自动更新，通过**事件防抖机制**，将短时间内的多次变更合并为一次处理，实现近实时同步的同时避免对 `mosdns` 服务造成不必要的抖动。
* **健壮性 (Resilience)**: 内置启动健康检查、**带指数退避和抖动的网络重试**、**原子化文件写入**以及精细化的错误捕获，确保在网络波动、服务临时不可用等不稳定环境下依然能可靠运行。
* **可观测性 (Observability)**: 全面采用**结构化日志 (JSON)**，为故障排查、系统状态监控和自动化告警提供机器可读的数据支持，极大提升了系统的可维护性。
* **mrs 规则集支持**: 能够处理 `mihomo` 的 `mrs` 格式规则集，通过解析配置文件获取源 URL 并请求文本格式变体，实现对预编译规则集的支持。
* **本地配置文件支持**: 通过解析 Mihomo 的本地配置文件，获取完整的 rule-providers 定义，包括 URL、路径、格式等信息，实现对规则集的完整处理。

#### 2. 系统架构设计

##### 2.1 核心组件

1. **Mihomo**: 作为核心的代理引擎，是所有策略和状态的"唯一事实来源"。
2. **Mihomo API 客户端**: 一个内置的、具有**指数退避重试与超时机制**的模块，负责与 `mihomo` RESTful API 的高容错通信。
3. **Mihomo 配置文件解析器**: 负责解析 Mihomo 的本地配置文件，提取 rule-providers 的完整定义。
4. **状态监视器 (State Monitor)**: 项目的核心驱动。以固定频率轮询 `mihomo` API，通过对关键状态数据进行**哈希摘要比对**来精确检测变更，并利用**防抖（Debounce）逻辑**来触发后续操作。已重构为两阶段生成架构的流程编排器。
5. **规则解析器 (Rule Parser)**: 负责解析 `mihomo` API 响应数据，提取规则、代理和规则提供者信息。
6. **策略追踪器 (Policy Tracer)**: 负责递归追踪 `mihomo` 中复杂的策略链，找出任意规则的最终出口节点，并内置**循环依赖检测**。
7. **规则生成协调器 (Rule Generation Orchestrator)**: 两阶段生成架构的第一阶段。负责从 Mihomo API 获取所有数据，并将其高效地转换为结构化的、按规则来源分类的中间文件。
8. **规则转换器 (Rule Converter)**: 已重构为无状态的纯工具类，只提供逻辑转换功能，不执行任何 I/O 或网络操作。
9. **规则合并器 (Rule Merger)**: 两阶段生成架构的第二阶段。负责读取规则生成协调器生成的结构化中间文件，高效地将它们合并、去重，并生成 Mosdns 使用的最终规则文件。
10. **Mosdns 服务控制器**: 负责执行系统命令安全地重载 `mosdns` 服务，并**捕获执行结果**。
11. **日志记录器 (Logger)**: 贯穿所有模块的日志中心，负责以**结构化 (JSON格式)** 输出所有事件。

##### 2.2 数据与逻辑流程图

```
graph TD
    subgraph "启动阶段"
        Init[服务启动] --> HC{健康检查};
        HC -- Mihomo API可达? --> HC2;
        HC -- 失败 --> LogCrit1[记录CRITICAL日志];
        LogCrit1 --> Exit[打印错误并退出];
        HC2 -- 配置文件可写? --> Run[进入运行状态];
        HC2 -- 失败 --> LogCrit2[记录CRITICAL日志];
        LogCrit2 --> Exit;
    end

    subgraph "运行阶段"
        A[用户操作或规则自动更新] --> B(Mihomo 状态变更);
        C[状态监视器] -- 定时轮询 --> D{Mihomo API};
        D -- /proxies, /providers/rules --> C;
        C -- 计算状态哈希摘要 --> Compare{比对新旧摘要};
        Compare -- 摘要不同 --> Debounce{事件防抖计时器};
        Compare -- 摘要相同 --> C;
        Debounce -- 计时结束 --> E[触发规则生成];
        E -- 获取最新状态 --> D;
        D -- /rules, /proxies, /providers/rules, /configs --> F[规则生成协调器];
        F -- 生成中间文件 --> G[中间文件目录];
        G -- 合并并去重 --> H[规则合并器];
        H -- 生成最终文件 --> I[mosdns规则目录];
        I --> J[Mosdns 服务控制器];
        J -- 执行 reload 命令 --> K(Mosdns 服务);
        K -- 应用新规则 --> L[DNS 解析请求];
    end
    
    subgraph "配置文件解析"
        ConfigParse[Mihomo配置文件解析器] -- 解析rule-providers --> RuleProviders[规则提供者信息];
        RuleProviders --> RuleConverter[规则转换器];
    end
    
    subgraph "日志记录 (贯穿所有阶段)"
        HC -- 记录检查结果 --> Logger[结构化日志系统];
        D -- 记录API请求/重试 --> Logger;
        F -- 记录中间文件生成 --> Logger;
        H -- 记录文件合并结果 --> Logger;
        J -- 记录命令执行结果 --> Logger;
    end

    Init --> A
```

#### 3. 模块化设计详解

##### 3.1 `ConfigManager` (配置管理器)
* **职责**: 负责加载、校验并提供所有应用级别的配置。
* **暴露接口**:
 * `get_mihomo_api_url()`: 返回 Mihomo API 的基础 URL。
 * `get_mihomo_api_timeout()`: 返回 API 请求的超时时间 (秒), e.g., `5`。
 * `get_mihomo_api_retry_config()`: 返回重试参数字典, e.g., `{ "max_retries": 5, "initial_backoff": 1, "max_backoff": 16, "jitter": true }`。
 * `get_polling_interval()`: 返回监控轮询的时间间隔 (秒), e.g., `2`。
 * `get_debounce_interval()`: 返回事件防抖的延迟时间 (秒), e.g., `0.5`。
 * `get_mihomo_config_path()`: 返回 Mihomo 配置文件的绝对路径。
 * `get_mosdns_config_path()`: 返回生成的 `mosdns` 规则文件的绝对路径。
 * `get_mosdns_reload_command()`: 返回用于重载 `mosdns` 服务的完整系统命令。
 * `get_log_level()`: 返回日志级别, e.g., `INFO`, `DEBUG`。

##### 3.2 `MihomoConfigParser` (配置文件解析器)
* **职责**: 解析 Mihomo 的本地配置文件，提取 rule-providers 的完整定义。
* **实现**:
 * 读取并解析 YAML 格式的 Mihomo 配置文件
 * 提取 rule-providers 部分的完整信息，包括 url、path、format、behavior 等属性
 * 提供方法将解析的信息转换为规则转换器可以使用的格式
* **暴露接口**:
 * `parse_config_file(config_path)`: 解析 Mihomo 配置文件
 * `extract_rule_providers(config_data)`: 从配置数据中提取 rule-providers 信息

##### 3.3 `MihomoApiClient` (API 客户端)
* **职责**: 封装所有与 `mihomo` API 的高容错 HTTP 通信。
* **实现**:
 * 使用配置的**请求超时 (`timeout`)**。
 * **内置指数退避重试 (Exponential Backoff with Jitter)**: 对于网络错误（如 `ConnectionError`）或 5xx 服务器错误，将执行自动重试。
 * **算法**: 从 `ConfigManager` 获取重试配置。第 `N` 次重试的等待时间 `delay = min(max_backoff, initial_backoff * (2 ** (N-1)))`。如果 `jitter` 为 `true`，则在 `delay` 上增加一个小的随机扰动。
 * 在每次尝试失败并发起重试前，记录一条 `WARN` 级别的**结构化日志**，包含尝试次数、将要等待的时间等上下文。
 * 对 HTTP 状态码进行检查，只接受 `2xx` 为成功。对于 `4xx` (客户端错误) 和 `5xx` (服务器错误)，记录详细的 `ERROR` 级别的**结构化日志**并抛出特定异常。
* **暴露接口**:
 * `async check_connectivity()`: 用于启动健康检查。
 * `async get_rules()`, `async get_proxies()`, `async get_rule_providers()`: 获取数据的方法，均内置上述容错逻辑。
 * `async get_config()`: 获取 Mihomo 的主配置文件。

##### 3.4 `RuleParser` (规则解析器)
* **职责**: 解析 `mihomo` API 响应数据，提取规则、代理和规则提供者信息。
* **暴露接口**:
 * `parse_rules(rules_data)`: 解析规则数据。
 * `parse_proxies(proxies_data)`: 解析代理数据。
 * `parse_rule_providers(rule_providers_data)`: 解析规则提供者数据。
 * `parse_rule_provider_info(config_data)`: 解析配置文件中的规则提供者信息。

##### 3.5 `PolicyResolver` (策略解析器)
* **职责**: 实现核心的策略链追踪算法，并处理潜在的配置错误。
* **实现**:
 * 通过递归和备忘录（memoization）模式来缓存已解析的结果，避免重复计算，提升性能。
 * **内置循环依赖检测**: 在递归调用时，维护一个调用栈（`visited_policies`）。如果在解析一个策略前发现它已经存在于当前调用栈中，则判定为循环依赖。此时，应立即停止解析，记录一条 `ERROR` 级别的**结构化日志**，并返回一个预设的默认策略（如 `DIRECT`）以保证主流程不被中断。
* **暴露接口**:
 * `resolve(policy_name, proxies_data)`: 输入策略组名称和所有代理的数据，返回其最终的出口节点名称。

##### 3.6 `RuleConverter` (规则转换器)
* **职责**: 已重构为无状态的纯工具类，只提供逻辑转换功能，不执行任何 I/O 或网络操作。
* **暴露接口**: 
 * `convert_single_rule(rule)`: 转换单条 Mihomo 规则并返回 Mosdns 格式字符串和内容类型
 * `fetch_and_parse_ruleset(provider_info)`: 获取并解析 RuleSet 提供者的内容
* **内部逻辑**:
 1. **确定内容类型**: 根据规则的 type (如 DOMAIN-SUFFIX, IP-CIDR) 来判断内容是 domain, ipv4 还是 ipv6。
 2. **获取规则内容**: 
    * 对于普通规则，payload 就是内容。
    * 对于 RuleSet 类型，需要根据 provider_info 中的信息处理：
      * 如果是 mrs 格式，将 URL 从 .mrs 转换为 .list 或 .yaml 格式
      * 根据 behavior 属性 (domain, ipcidr, classical) 解析规则内容
      * 下载并解析规则集内容，或从本地文件读取
 3. **格式转换**:
     * DOMAIN-SUFFIX -> domain:payload
     * DOMAIN -> full:payload
     * DOMAIN-KEYWORD -> keyword:payload
     * DOMAIN-REGEX -> regexp:payload
     * IP-CIDR -> ip-cidr:payload

##### 3.7 `RuleGenerationOrchestrator` (规则生成协调器)
* **职责**: 两阶段生成架构的第一阶段。负责从 Mihomo API 获取所有数据，并将其高效地转换为结构化的、按规则来源分类的中间文件。
* **暴露接口**: `run()`
* **内部逻辑**:
 1. **准备工作**: 彻底清理或删除旧的中间目录，确保每次运行都是一个全新的开始。
 2. **一次性数据获取**: 调用 Mihomo API 获取所有规则列表和 RULE-SET 提供者的详细信息。
 3. **初始化内存聚合器**: 创建一个三层嵌套的字典，用于在内存中对规则进行分类和聚合。
 4. **遍历API规则列表**: 
    * 对于 RULE-SET 类型的规则，调用 RuleConverter.fetch_and_parse_ruleset 获取解析后的内容列表
    * 对于单条规则，调用 RuleConverter.convert_single_rule 转换为 Mosdns 格式
    * 将所有规则按策略、内容类型和提供者进行分类聚合
 5. **写入中间文件**: 将聚合后的规则写入结构化的中间文件，路径结构为 {intermediate_dir}/{policy}/{content_type}/provider_{provider_name}.list

##### 3.8 `RuleMerger` (规则合并器)
* **职责**: 两阶段生成架构的第二阶段。负责读取规则生成协调器生成的结构化中间文件，高效地将它们合并、去重，并生成 Mosdns 使用的最终规则文件。
* **暴露接口**: `merge_from_intermediate(intermediate_path, final_output_path)`
* **内部逻辑**:
 1. **准备工作**: 彻底清理或删除旧的最终输出目录。
 2. **遍历中间目录**: 使用 os.walk 遍历中间目录下的所有策略和内容类型子目录。
 3. **合并与去重**: 对于每一个策略和内容类型的子目录，使用集合自动处理所有跨文件的重复规则。
 4. **写入最终文件**: 将去重后的规则排序后写入最终的文件中，使用扁平化的命名方式，并区分IPv4和IPv6规则：
    * DIRECT 策略的 domain 规则 → `direct_domain.txt`
    * PROXY 策略的 domain 规则 → `proxy_domain.txt`
    * REJECT 策略的 domain 规则 → `reject_domain.txt`
    * DIRECT 策略的 IPv4 规则 → `direct_ipv4.txt`
    * PROXY 策略的 IPv4 规则 → `proxy_ipv4.txt`
    * REJECT 策略的 IPv4 规则 → `reject_ipv4.txt`
    * DIRECT 策略的 IPv6 规则 → `direct_ipv6.txt`
    * PROXY 策略的 IPv6 规则 → `proxy_ipv6.txt`
    * REJECT 策略的 IPv6 规则 → `reject_ipv6.txt`
    * 如果一个策略同时包含IPv4和IPv6规则，则会生成两个独立的文件
 5. **错误处理**: 对于无法读取的文件，记录警告日志并继续处理其他文件。

##### 3.9 `MosdnsServiceController` (服务控制器)
* **职责**: 与操作系统交互，控制 `mosdns` 服务并处理执行结果。
* **暴露接口**: `reload()`
 * 使用 `subprocess` 模块执行 `ConfigManager` 中定义的重载命令。
 * 检查命令的返回码。如果非零，表示执行失败。
 * 记录 `ERROR` 级别的**结构化日志**，其中必须包含 `command`, `return_code`, `stdout`, `stderr` 等字段，为诊断问题提供完整上下文。

#### 4. MosDNS 格式转换规范

根据 MosDNS 规则指南，Mihomo 规则类型与 MosDNS 格式的对应关系如下：

| Mihomo 规则类型    | MosDNS 格式      | 说明 |
|-------------------|------------------|------|
| `DOMAIN-SUFFIX`   | `domain:payload` | 匹配域名及其子域名 |
| `DOMAIN`          | `full:payload`   | 精确匹配域名 |
| `DOMAIN-KEYWORD`  | `keyword:payload`| 包含关键字的域名 |
| `DOMAIN-REGEX`    | `regexp:payload` | Golang 正则匹配 |
| `IP-CIDR`         | `ip-cidr:payload`| IP CIDR 匹配 |

**注意事项**:
1. **优先级**：MosDNS 中 `full` > `domain` > `regexp` > `keyword`，转换时需保持此优先级关系。
2. **性能考虑**：
   - `domain`/`full` 类型具有 O(1) 复杂度，性能最佳
   - `keyword`/`regexp` 类型具有 O(n) 复杂度，正则表达式较消耗资源
3. **RuleSet 处理**：
   - 对于 `domain` 行为的 RuleSet，每条规则将转换为对应的 MosDNS 格式（domain:、full:、keyword:、regexp:）
   - 对于 `ipcidr` 行为的 RuleSet，每条规则将转换为 ip-cidr: 格式
   - 对于 `classical` 行为的 RuleSet，需要解析每行规则的类型并分别转换

**特殊处理**:
- 对于 list 格式的 RuleSet 文件中的通配符：
  - `*` 通配符：一次只能匹配一级域名，转换为MosDNS时需要特殊处理
  - `+` 通配符：类似 DOMAIN-SUFFIX，可匹配多个级别，转换为MosDNS的domain:格式
  - `.` 通配符：可匹配多个级别，但不能匹配根域名，转换为MosDNS的domain:格式

**通配符转换规则**:
- Mihomo list格式中的 `*.example.com` → MosDNS `domain:example.com` (注意：移除*前缀，因为MosDNS的domain:本身就匹配子域名)
- Mihomo list格式中的 `+.example.com` → MosDNS `domain:example.com`
- Mihomo list格式中的 `.example.com` → MosDNS `domain:example.com`
- Mihomo list格式中的 `*` (单独的星号) → MosDNS `keyword:` (空关键字，匹配没有"."的主机名)

#### 5. 执行逻辑与算法

##### 5.1 初始化与健康检查
服务启动时，在进入主监控循环前，必须执行一次性的**健康检查**:
1. **Mihomo API 连通性**: 调用 `MihomoApiClient.check_connectivity()`。若失败，记录 `CRITICAL` 日志并退出。
2. **配置文件路径可写性**: 检查目标目录是否具有写入权限。若失败，记录 `CRITICAL` 日志并退出。
3. **Mihomo 配置文件存在性**: 如果配置了 `mihomo_config_path`，检查该文件是否存在。若配置了但文件不存在，记录 `CRITICAL` 日志并退出。
4. 通过所有检查后，记录一条 `INFO` 日志，表明服务启动成功，然后立即执行一次完整的规则生成流程，为 `mosdns` 提供初始配置，并将 `mihomo` 的初始状态哈希存入缓存。

##### 5.2 监控循环与变更检测
1. **轮询**: `StateMonitor` 按预设间隔（如 2 秒）请求 `mihomo` API。
2. **变更检测**: 按照 3.4 中描述的**深度状态比对**逻辑，精确检测变化。
3. **调度任务**: 如果检测到不一致，`StateMonitor` 的防抖机制会**调度**一次规则生成任务的执行。在设定的防抖间隔内（如 500ms）的连续变更只会触发一次最终的执行。

##### 5.3 Mihomo 配置文件解析
1. **解析配置**: 在规则生成过程中，如果配置了 `mihomo_config_path`，使用 `MihomoConfigParser` 解析 Mihomo 的本地配置文件。
2. **提取信息**: 从配置文件中提取 `rule-providers` 部分的完整信息，包括 URL、路径、格式、行为等属性。
3. **优先使用**: 在处理 RULE-SET 规则时，优先使用从本地配置文件获取的 provider 信息，只有在未配置本地配置文件时才回退到 API 获取的信息。

##### 5.4 mrs 规则集处理
1. **获取配置**: 通过 `MihomoConfigParser` 从本地配置文件或 `MihomoApiClient.get_config()` 获取主配置文件内容。
2. **解析信息**: 使用 `extract_rule_providers()` 方法解析配置文件中的 `rule-providers` 部分，建立 provider 名称到完整信息（url、behavior、format）的映射关系。
3. **识别 mrs**: 在处理 RULE-SET 规则时，使用 provider 名称查找对应的完整信息，检查提供者是否为 mrs 格式。
4. **URL 转换**: 根据 behavior 属性决定 URL 转换方式：
   - `domain` 或 `ipcidr` 行为：`.mrs` → `.list`
   - `classical` 行为：`.mrs` → `.yaml`
5. **下载内容**: 从转换后的 URL 下载规则内容，或从本地路径读取规则内容。
6. **根据 behavior 解析**: 
   - `domain` 行为：将每行内容作为域名处理
   - `ipcidr` 行为：将每行内容作为 IP CIDR 处理
   - `classical` 行为：按逗号分隔解析完整规则
7. **格式转换**: 将解析的规则转换为 Mosdns 格式。
8. **回退机制**: 如果 mrs 处理失败，回退到原有的 API 方法。

##### 5.5 behavior 和 format 属性详解

根据提供的参考资料，详细解释 `behavior` 和 `format` 这两个属性如何帮助我们更好地解析 `rule-set` 规则。

`behavior` 和 `format` 这两个属性共同定义了一个 `rule-provider` 文件的内容类型和文件结构，它们是正确解析规则集的关键元数据。

###### 5.5.1 `behavior`: 决定规则内容的"类型"

`behavior` 属性定义了规则集文件内部包含的是哪种类型的规则。了解 `behavior` 可以让我们确定如何解释文件中的每一行文本。它有三个可选值：`domain`、`ipcidr` 和 `classical`。

*   **`domain`**:

    *   **内容**: 文件中只包含域名或域名通配符。

    *   **解析策略**: 当 `behavior` 为 `domain` 时，解析器应将文件中的每一条目都视为一个域名匹配规则。例如，`.blogger.com` 或 `books.itunes.apple.com`。在转换为 `mosdns` 格式时，这些通常会被处理为 `domain` 或 `full` 类型的匹配。

*   **`ipcidr`**:

    *   **内容**: 文件中只包含 IP 地址或 CIDR 地址块。

    *   **解析策略**: 当 `behavior` 为 `ipcidr` 时，解析器应将每一条目都视为一个 IP CIDR 规则，例如 `192.168.1.0/24`。

*   **`classical`**:

    *   **内容**: 这是最灵活的类型，文件中可以包含 `mihomo` 支持的各种路由规则，例如 `DOMAIN-SUFFIX,google.com`、`IP-CIDR,127.0.0.0/8`、`GEOIP,CN` 等，但不包含 `RULE-SET` 或 `SUB-RULE`。

    *   **解析策略**: 当 `behavior` 为 `classical` 时，解析器需要逐行解析，并根据逗号分隔的第一部分（如 `DOMAIN-SUFFIX`）来判断规则的具体类型，然后进行相应的转换。

###### 5.5.2 `format`: 决定规则文件的"结构"

`format` 属性定义了规则集文件的存储格式或编码方式，它告诉我们应该如何读取和解码文件内容。它有三个可选值：`yaml`、`text` 和 `mrs`。

*   **`yaml`**:

    *   **结构**: 文件是一个 YAML 文件，其中规则内容被包含在一个名为 `payload` 的键下，其值为一个规则列表。

    *   **解析策略**: 需要使用 YAML 解析器来读取文件，然后提取 `payload` 键对应的值（一个数组），再根据 `behavior` 逐一处理数组中的每个元素。

*   **`text`**:

    *   **结构**: 文件是一个纯文本文件，每一行就是一条规则。这是最常见的格式之一。

    *   **解析策略**: 直接按行读取文件，然后根据 `behavior` 逐行处理。

*   **`mrs`**:

    *   **结构**: 这是一种预编译的二进制格式，无法直接通过文本解析。

    *   **解析策略**: 正如之前提到的，不应尝试直接解析 `.mrs` 文件。当 `format` 为 `mrs` 时，我们的策略应该是：

        1.  从配置文件中找到该 `rule-provider` 的 `url`。

        2.  将 URL 的后缀从 `.mrs` 修改为 `.list` (通常对应 `format: text`) 或 `.yaml`。

        3.  下载修改后 URL 的内容，并按照 `text` 或 `yaml` 的方式进行解析。

        4.  资料明确指出，`mrs` 格式目前仅支持 `domain` 和 `ipcidr` 两种 `behavior`。

###### 5.5.3 解析矩阵

`behavior` 和 `format` 属性共同构成了一个解析矩阵，为我们提供了清晰的指导：

| `format` \ `behavior` | `domain`                                   | `ipcidr`                                 | `classical`                                        |
| --------------------- | ------------------------------------------ | ---------------------------------------- | -------------------------------------------------- |
| **`yaml`**            | 解析 `payload` 列表，每项为域名            | 解析 `payload` 列表，每项为 IP CIDR      | 解析 `payload` 列表，每项为完整的 `mihomo` 规则    |
| **`text`**            | 逐行读取，每行为一个域名                   | 逐行读取，每行为一个 IP CIDR             | 逐行读取，每行为一个完整的 `mihomo` 规则           |
| **`mrs`**             | 转换 URL 后按 `text`/`yaml` 方式解析域名   | 转换 URL 后按 `text`/`yaml` 方式解析 IP  | (不支持)                                           |

因此，通过在解析 `rule-set` 之前检查其 `rule-provider` 定义中的 `behavior` 和 `format` 属性，我们可以构建一个健壮且准确的转换逻辑，以应对不同来源和类型的规则集文件。

#### 6. 整体工作流程

整合上述模块，整个流程如下：

1. **启动**: "监控模块"开始按设定的频率轮询 mihomo API。

2. **变更检测**: "监控模块"发现规则或代理组的哈希值发生变化，定位到具体的变更规则。

3. **数据解析**: "API解析模块"获取最新的 API 数据并进行结构化处理。

4. **配置文件解析**: 如果配置了 Mihomo 配置文件路径，"配置文件解析模块"解析本地配置文件获取 rule-providers 的完整信息。

5. **策略确定**: 对于每条变更的规则，"策略追踪模块"通过递归查询确定其最终的出口策略（Direct, Proxy, Reject）。

6. **单条转换**: "规则转换模块"将该规则转换为 mosdns 格式，并更新或创建对应的中间文件。

7. **触发合并**: 中间文件的变动触发"规则合并模块"。

8. **生成最终文件**: "规则合并模块"读取所有中间文件，重新生成那9个最终的 mosdns 规则列表文件。mosdns 感知到文件变化后会自动重载规则。

#### 7. 错误处理、系统韧性与可观测性

本系统将韧性与可观测性作为一级设计目标。

##### 7.1 结构化日志 (Structured Logging)

系统内所有日志输出**必须**为 JSON 格式。

* **目的**: 替代难以分析的纯文本日志，为 Loki, Elasticsearch 等日志聚合系统提供高质量的数据源，实现高效的故障排查、仪表盘监控和自动化告警。
* **标准字段**: 每条日志记录都应至少包含以下字段：
 * `timestamp`: ISO 8601 格式的时间戳 (e.g., `"2023-10-27T10:00:00.123Z"`)。
 * `level`: 日志级别 (e.g., `"INFO"`, `"WARN"`, `"ERROR"`, `"CRITICAL"`)。
 * `service_name`: 服务名称 (e.g., `"mihomo-mosdns-sync"`)。
 * `module`: 产生日志的模块名 (e.g., `"MihomoApiClient"`)。
 * `message`: 人类可读的日志信息。
* **上下文(Contextual)字段**: 日志记录应根据事件附加上下文信息。

* **日志示例**:
 * **成功同步**:
 ```json
 {
 "timestamp": "2023-10-27T10:05:00.500Z",
 "level": "INFO",
 "service_name": "mihomo-mosdns-sync",
 "module": "MosdnsRuleGenerator",
 "message": "Successfully synchronized rules and reloaded mosdns.",
 "context": {
 "rules_generated": 152,
 "config_path": "/etc/mosdns/rules/mihomo_generated.list",
 "duration_ms": 350
 }
 }
 ```
 * **API 重试**:
 ```json
 {
 "timestamp": "2023-10-27T10:10:01.200Z",
 "level": "WARN",
 "service_name": "mihomo-mosdns-sync",
 "module": "MihomoApiClient",
 "message": "API request failed, retrying...",
 "context": {
 "endpoint": "/proxies",
 "attempt": 2,
 "max_attempts": 5,
 "delay_seconds": 2.1,
 "error": "Connection timed out"
 }
 }
 ```
 * **Mosdns 重载失败**:
 ```json
 {
 "timestamp": "2023-10-27T10:15:30.800Z",
 "level": "ERROR",
 "service_name": "mihomo-mosdns-sync",
 "module": "MosdnsServiceController",
 "message": "Failed to execute mosdns reload command.",
 "context": {
 "command": "sudo mosdns reload -d /etc/mosdns",
 "return_code": 1,
 "stdout": "",
 "stderr": "Error: config file validation failed at line 42: unknown tag 'invalid_tag'"
 }
 }
 ```

##### 7.2 配置文件解析错误处理

当解析 Mihomo 配置文件时，系统需要处理以下错误情况：

* **文件不存在**: 如果配置了 `mihomo_config_path` 但文件不存在，系统应记录 `ERROR` 级别日志并跳过本地配置文件解析。
* **文件格式错误**: 如果配置文件不是有效的 YAML 格式，系统应记录 `ERROR` 级别日志并跳过本地配置文件解析。
* **缺少必要字段**: 如果配置文件中缺少 `rule-providers` 字段，系统应记录 `WARN` 级别日志并继续使用 API 获取的信息。

##### 7.3 本地文件读取错误处理

在读取 rule-providers 的本地文件时，系统需要处理以下错误情况：

* **文件不存在**: 如果配置了 `path` 但文件不存在，系统应记录 `WARN` 级别日志并尝试从 URL 下载文件。
* **文件读取失败**: 如果无法读取本地文件，系统应记录 `ERROR` 级别日志并尝试从 URL 下载文件。
* **文件格式错误**: 如果本地文件格式不符合预期，系统应记录 `ERROR` 级别日志并尝试从 URL 下载文件。

#### 8. 配置说明

##### 8.1 配置文件格式

Mihomo 配置文件使用 YAML 格式，其中 `rule-providers` 部分定义了规则集的来源：

```
# Rule providers
rule-providers:
  # Domain rule provider from URL
  google_domains:
    type: http
    behavior: domain
    url: "https://example.com/google_domains.list"
    path: "./rules/google_domains.list"
    interval: 86400

  # IPCIDR rule provider from URL
  private_ips:
    type: http
    behavior: ipcidr
    url: "https://example.com/private_ips.list"
    path: "./rules/private_ips.list"
    interval: 86400

  # Classical rule provider from URL
  ads_rules:
    type: http
    behavior: classical
    url: "https://example.com/ads_rules.yaml"
    path: "./rules/ads_rules.yaml"
    interval: 86400

  # Rule provider from local file
  local_domains:
    type: file
    behavior: domain
    path: "./rules/local_domains.list"

  # MRS format rule provider
  mrs_domains:
    type: http
    behavior: domain
    format: mrs
    url: "https://example.com/mrs_domains.mrs"
    path: "./rules/mrs_domains.list"
    interval: 86400
```

##### 8.2 配置项说明

* **type**: 定义规则集的类型，可以是 `http`（从URL获取）或 `file`（从本地文件获取）
* **behavior**: 定义规则集的行为类型，可以是 `domain`、`ipcidr` 或 `classical`
* **format**: 定义规则集的格式，可以是 `yaml`、`text` 或 `mrs`
* **url**: 当 type 为 `http` 时，定义获取规则集的URL
* **path**: 定义本地文件路径，可以用于缓存远程规则集或直接使用本地规则集
* **interval**: 定义自动更新间隔（秒）

#### 9. 测试策略

为了确保系统的稳定性和正确性，需要实施以下测试策略：

##### 9.1 单元测试

* **MihomoConfigParser**: 测试配置文件解析功能，包括正常情况和异常情况
* **RuleConverter**: 测试规则转换功能，包括各种规则类型和格式
* **RuleMerger**: 测试规则合并功能，确保生成正确的输出文件

##### 9.2 集成测试

* **API客户端**: 测试与 Mihomo API 的交互，包括正常响应和错误处理
* **状态监控**: 测试状态变化检测和防抖机制
* **端到端流程**: 测试从规则变化检测到 Mosdns 重载的完整流程

##### 9.3 性能测试

* **大规则集处理**: 测试处理大量规则时的性能表现
* **并发处理**: 测试在高并发情况下的系统稳定性
* **资源使用**: 监控系统资源使用情况，确保不会过度消耗CPU和内存