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
- **两阶段架构**: 采用分发-合并的两阶段规则生成架构，提高可维护性和可调试性
- **动态策略组识别**: 自动识别各种类型的策略组，包括自定义类型如 LoadBalance 和 Relay
- **智能状态检测**: 仅在最终出口策略（DIRECT/PROXY/REJECT）发生变化时触发规则生成

## 工作原理

服务通过"轮询-比对-生成-重载"的工作流程实现自动化同步：

1. **定时轮询**: 以固定间隔轮询 Mihomo API 获取策略状态
2. **智能比对**: 使用PolicyResolver解析策略组的最终出口，仅当DIRECT/PROXY/REJECT分类发生变化时才触发更新
3. **防抖处理**: 使用防抖机制平滑处理连续变化
4. **规则生成**: 采用两阶段架构生成对应的 Mosdns 规则文件
   - **阶段一（分发）**: RuleGenerationOrchestrator 从 Mihomo API 获取数据并生成结构化的中间文件
   - **阶段二（合并）**: RuleMerger 读取中间文件，合并去重生成最终规则文件
5. **原子写入**: 原子化写入配置文件确保完整性
6. **服务重载**: 安全地重载 Mosdns 服务应用新规则

## 日志系统优化

v2.0版本对日志系统进行了全面优化，提供更详细的运行信息：

### 增强的日志格式
- 添加了毫秒级时间戳，便于精确追踪事件时间
- 包含进程ID、文件名和行号，便于定位问题
- 支持中文日志级别显示，提高可读性
- 添加了服务版本信息

### 详细的性能监控
- 记录各阶段执行耗时（API请求、规则处理、文件写入等）
- 监控重试次数和延迟时间
- 统计规则数量和处理进度

### 丰富的上下文信息
- 记录API调用详情（URL、状态码、响应内容）
- 跟踪规则处理过程（规则集名称、规则数量等）
- 记录配置变更和状态变化

### 改进的错误处理
- 提供详细的错误类型和错误信息
- 记录异常堆栈跟踪，便于调试
- 区分不同级别的错误（警告、错误、严重）

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
polling_interval: 10      # 轮询间隔(秒) - 增加到10秒以减少误触发
debounce_interval: 2      # 防抖间隔(秒) - 增加到2秒以过滤临时波动

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

如果需要使用 TUN 模式（推荐），请使用提供的 docker-compose.yml 文件：

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

或者直接使用 docker run 命令（需要添加特定的 capabilities）：

```bash
docker run -d \
  --name mihomo-mosdns-sync \
  --cap-add=NET_ADMIN \
  --cap-add=SYS_ADMIN \
  -v /dev/net/tun:/dev/net/tun \
  -v /path/to/config:/app/config \
  -v /etc/mosdns/rules:/etc/mosdns/rules \
  -v /path/to/mihomo/config.yaml:/etc/mihomo/config.yaml \
  --restart unless-stopped \
  mihomo-mosdns-sync:latest
```

### Docker Compose

使用项目根目录下的 `docker-compose.yml` 文件来部署完整的服务栈：

```yaml
version: '3.8'

services:
  mms:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: mms
    ports:
      # MosDNS DNS服务
      - "53:53/tcp"
      - "53:53/udp"
      # Mihomo 服务
      - "1053:1053/tcp"
      - "1053:1053/udp"
      - "7890:7890"  # Mihomo 混合端口
      - "7891:7891"  # Mihomo SOCKS代理
      - "7892:7892"  # Mihomo HTTP代理
      - "9090:9090"  # Mihomo 控制面板
    volumes:
      # 配置文件卷
      - ./config/mihomo.yaml:/etc/mihomo/config.yaml
      - ./config/mosdns.yaml:/etc/mosdns/config.yaml
      # 规则文件卷
      - ./config/rules:/etc/mosdns/rules
      # 日志卷
      - ./logs:/app/logs
      # 确保可以访问宿主机的 TUN 设备
      - /dev/net/tun:/dev/net/tun
    # 需要网络和系统权限
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
    # 额外的 sysctl 设置
    sysctls:
      - net.ipv4.conf.all.rp_filter=0
      - net.ipv4.ip_forward=1
      - net.ipv6.conf.all.forwarding=1
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
  "时间": "2023-10-27T10:05:00.500Z",
  "级别": "信息",
  "模块": "mihomo_sync.modules.mosdns_controller",
  "消息": "Rules generated and written to file successfully",
  "服务名称": "mihomo-mosdns-sync",
  "版本": "2.0",
  "配置路径": "/etc/mosdns/rules/mihomo_generated.list",
  "规则数量": 152,
  "执行耗时_秒": 0.234
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
    ├── mosdns_controller.py # Mosdns 控制器
    ├── mihomo_config_parser.py # Mihomo 配置文件解析器
    ├── rule_parser.py     # 规则解析器
    ├── rule_converter.py  # 规则转换器
    ├── rule_generation_orchestrator.py # 规则生成协调器（第一阶段）
    └── rule_merger.py     # 规则合并器（第二阶段）
```

### 本地运行

```bash
# 安装依赖
pip install -e .

# 运行服务
python main.py
```

### 文档

详细的模块文档请查看 [docs/模板文档索引.md](docs/模板文档索引.md) 和 [docs/MihomoMosdns动态同步器开发文档.md](docs/MihomoMosdns动态同步器开发文档.md)。