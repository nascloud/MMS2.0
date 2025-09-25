# Mihomo-Mosdns 动态同步器

这是一个用于实时同步 Mihomo 代理策略与 Mosdns 域名解析规则的自动化服务。

## 特性

- **实时同步**: 监控 Mihomo 策略变化并自动更新 Mosdns 规则
- **高健壮性**: 内置指数退避重试机制和错误处理
- **精确检测**: 通过深度状态比对精确检测变化
- **防抖机制**: 合并短时间内的多次变更，避免频繁重载
- **结构化日志**: JSON 格式日志便于监控和调试
- **容器化部署**: 提供 Docker 镜像便于部署
- **原子化操作**: 配置文件写入和重载操作保证原子性
- **规则集支持**: 支持解析 Mihomo 的 rule-providers 规则集

## 工作原理

服务通过"轮询-比对-生成-重载"的工作流程实现自动化同步：

1. **定时轮询**: 以固定间隔轮询 Mihomo API 获取策略状态
2. **深度比对**: 通过哈希摘要比对精确检测状态变化
3. **防抖处理**: 使用防抖机制平滑处理连续变化
4. **规则生成**: 生成对应的 Mosdns 规则文件
5. **原子写入**: 原子化写入配置文件确保完整性
6. **服务重载**: 安全地重载 Mosdns 服务应用新规则

## 快速开始

### 配置

创建 `config/config.yaml` 文件：

```yaml
# Mihomo API Configuration
mihomo_api_url: "http://127.0.0.1:9090"  # Mihomo API 地址
mihomo_api_timeout: 5                    # API 请求超时时间(秒)
mihomo_api_secret: ""                    # API 认证密钥(如果需要)

# Mihomo Configuration File Path
# Path to the Mihomo configuration file (e.g., "C:/path/to/mihomo/config.yaml")
# This is needed to access static rule-provider definitions that are not available via API
mihomo_config_path: ""                   

# API 重试配置 (指数退避与抖动)
api_retry_config:
  max_retries: 5          # 最大重试次数
  initial_backoff: 1      # 初始退避时间(秒)
  max_backoff: 16         # 最大退避时间(秒)
  jitter: true            # 是否添加抖动

# 监控配置
polling_interval: 2       # 轮询间隔(秒)
debounce_interval: 0.5    # 防抖间隔(秒)

# Mosdns 配置
mosdns_config_path: "/etc/mosdns/rules/mihomo_generated.list"  # 生成的规则文件路径
mosdns_reload_command: "sudo mosdns reload -d /etc/mosdns"     # 重载 Mosdns 服务的命令

# 日志配置
log_level: "INFO"         # 日志级别
```

### Mihomo 配置文件解析

为了正确处理 Mihomo 的 rule-providers 规则集，特别是 mrs 格式的规则集，需要配置 `mihomo_config_path` 指向 Mihomo 的主配置文件。

Mihomo 的配置文件通常包含 rule-providers 部分，定义了规则集的来源：

```yaml
# Rule providers
rule-providers:
  # Domain rule provider from URL
  google_domains:
    type: http
    behavior: domain
    url: "https://example.com/google_domains.list"
    path: "./rules/google_domains.list"
    interval: 86400

  # MRS format rule provider
  mrs_domains:
    type: http
    behavior: domain
    format: mrs
    url: "https://example.com/mrs_domains.mrs"
    path: "./rules/mrs_domains.list"
    interval: 86400
```

当配置了 `mihomo_config_path` 后，服务会解析该配置文件以获取 rule-providers 的完整定义，包括：
- URL 地址（用于下载远程规则集）
- 本地路径（用于读取本地规则集）
- 格式类型（如 mrs 格式）
- 行为类型（domain, ipcidr, classical）

这使得服务能够正确处理 mrs 格式的规则集，将其转换为标准格式进行处理。

### Docker 运行

```bash
docker run -d \
  --name mihomo-mosdns-sync \
  -v /path/to/config:/home/appuser/app/config \
  -v /etc/mosdns/rules:/etc/mosdns/rules \
  -v /path/to/mihomo/config.yaml:/home/appuser/app/mihomo_config.yaml \
  --restart unless-stopped \
  mihomo-mosdns-sync:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  mihomo:
    image: ghcr.io/mihomo-party-org/mihomo-party
    # ... mihomo 配置

  mosdns:
    image: irinesistiana/mosdns-cn:latest
    # ... mosdns 配置

  mihomo-mosdns-sync:
    build: .
    depends_on:
      - mihomo
      - mosdns
    volumes:
      - ./config:/home/appuser/app/config
      - /etc/mosdns/rules:/etc/mosdns/rules
      - ./mihomo_config.yaml:/home/appuser/app/mihomo_config.yaml
    restart: unless-stopped
```

## 日志查看

服务输出结构化的 JSON 日志，便于分析和监控：

```bash
# 查看容器日志
docker logs mihomo-mosdns-sync

# 使用 jq 过滤特定级别日志
docker logs mihomo-mosdns-sync | jq 'select(.level == "ERROR")'

# 使用 jq 过滤特定模块日志
docker logs mihomo-mosdns-sync | jq 'select(.module == "MosdnsRuleGenerator")'
```

典型的日志格式：
```json
{
  "timestamp": "2023-10-27T10:05:00.500Z",
  "level": "INFO",
  "logger": "mihomo_sync.modules.mosdns_controller",
  "message": "Rules generated and written to file successfully",
  "service_name": "mihomo-mosdns-sync",
  "config_path": "/etc/mosdns/rules/mihomo_generated.list",
  "rules_count": 152
}
```

## 开发

### 项目结构

```
mihomo_sync/
├── config.py              # 配置管理器
├── logger.py              # 日志配置
├── main.py                # 主入口点
└── modules/
    ├── api_client.py      # Mihomo API 客户端
    ├── policy_resolver.py # 策略解析器
    ├── state_monitor.py   # 状态监视器
    ├── mosdns_controller.py # Mosdns 控制器和规则生成器
    ├── mihomo_config_parser.py # Mihomo 配置文件解析器
    ├── rule_parser.py     # 规则解析器
    ├── rule_converter.py  # 规则转换器
    └── rule_merger.py     # 规则合并器
```

### 本地运行

```bash
# 安装依赖
pip install -e .

# 运行服务
python main.py
```