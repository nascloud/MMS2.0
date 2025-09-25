### **Mihomo-Mosdns 动态同步项目 AI 辅助开发计划**

**项目技术栈推荐**:
* **语言**: Python 3.9+
* **核心框架**: `asyncio` (用于异步 I/O)
* **主要依赖**:
 * `httpx`: 用于异步 HTTP 请求和客户端构建。
 * `PyYAML`: 用于加载 YAML 配置文件。
 * `python-json-logger`: 用于生成结构化 JSON 日志。

---

### **阶段 0: 项目奠基与核心工具集 (Project Foundation & Core Utilities)** ✅ 已完成

**目标**: 搭建项目的基本骨架、配置管理和日志系统，为后续功能开发提供坚实的基础。

---

#### **任务 0.1: 项目结构初始化** ✅ 已完成

* **目标**: 创建标准的 Python 项目目录结构和配置文件。
* **AI 编程提示词**:
 > 请为我生成一个名为 `mihomo_sync` 的 Python 项目的目录结构和基础配置文件。目录结构应包含：
 > 1. `mihomo_sync/`: 主应用代码目录。
 > 2. `mihomo_sync/modules/`: 用于存放核心模块（如 `api_client.py`, `state_monitor.py` 等）。
 > 3. `config/`: 存放配置文件的目录。
 > 4. `main.py`: 项目的启动入口。
 >
 > 同时，请生成以下文件：
 > 1. `pyproject.toml`: 用于项目依赖管理，请在 `[project.dependencies]` 中加入 `httpx`, `pyyaml`, `python-json-logger`。
 > 2. `.gitignore`: 一个标准的 Python 项目 .gitignore 文件。
 > 3. `config/config.yaml.example`: 一个示例配置文件，包含文档中 `ConfigManager` 提到的所有配置项。

* **实现状态**: ✅ 已完成
* **说明**: 项目结构已按要求创建，包含所有必要的文件和目录。

---

#### **任务 0.2: 结构化日志记录器 (`Logger`)** ✅ 已完成

* **目标**: 建立一个全局可用的、输出 JSON 格式日志的记录器。
* **AI 编程提示词**:
 > 请创建一个 Python 模块 `mihomo_sync/logger.py`。
 >
 > **需求**:
 > 1. 该模块需要提供一个 `setup_logger` 函数，该函数接受 `log_level` (如 'INFO', 'DEBUG') 作为参数。
 > 2. 使用 `logging` 模块和 `python_json_logger.jsonlogger.JsonFormatter` 来配置根日志记录器 (root logger)。
 > 3. 日志格式 (JsonFormatter) 必须包含以下标准字段：`timestamp` (时间戳), `level` (级别), `name` (记录器名称), `message` (消息)。
 > 4. `setup_logger` 函数应确保所有通过 `logging.getLogger(__name__)` 获取的记录器都继承此 JSON 格式化配置。
 > 5. 日志输出到标准输出 (stdout)。

* **实现状态**: ✅ 已完成
* **说明**: [logger.py](file:///d:/Software/MMS2.0/mihomo_sync/logger.py) 模块已实现，支持结构化 JSON 日志输出，并添加了服务名称字段。

---

#### **任务 0.3: 配置管理器 (`ConfigManager`)** ✅ 已完成

* **目标**: 实现一个加载并提供应用配置的单例或模块。
* **AI 编程提示词**:
 > 请创建一个 Python 模块 `mihomo_sync/config.py`。
 >
 > **需求**:
 > 1. 创建一个名为 `ConfigManager` 的类。
 > 2. 该类应在初始化时接收一个 YAML 配置文件路径。
 > 3. 使用 `PyYAML` 库加载和解析该文件。
 > 4. 为开发文档中提到的每一项配置（如 `mihomo_api_url`, `polling_interval`, `api_retry_config` 等）提供一个 `get_...()` 方法。
 > 5. 如果配置文件中缺少必要的键，应在加载时抛出 `ValueError` 并给出清晰的错误提示。
 > 6. 这个模块应该能以单例模式工作，即在应用中只加载一次配置。

* **实现状态**: ✅ 已完成
* **说明**: [config.py](file:///d:/Software/MMS2.0/mihomo_sync/config.py) 模块已实现，支持配置加载、验证和单例模式。

---

### **阶段 1: 核心逻辑实现 (Core Logic Implementation)** ✅ 已完成

**目标**: 开发与 `mihomo` API 交互以及解析策略的核心模块，这两个模块是系统的"输入"和"大脑"。

---

#### **任务 1.1: Mihomo API 客户端 (`MihomoApiClient`)** ✅ 已完成

* **目标**: 创建一个健壮的、支持异步、超时和指数退避重试的 API 客户端。
* **AI 编程提示词**:
 > 请使用 Python 和 `httpx` 库，在 `mihomo_sync/modules/api_client.py` 中实现一个名为 `MihomoApiClient` 的异步类。
 >
 > **核心需求**:
 > 1. **初始化**: `__init__` 方法接收 `api_base_url`, `timeout` 和一个包含重试参数的字典 `retry_config`。
 > 2. **异步客户端**: 内部使用 `httpx.AsyncClient`。
 > 3. **指数退避重试**:
 > * 实现一个 `_request` 私有方法，封装所有的 GET 请求。
 > * 此方法需要实现一个重试循环，当请求遇到 `httpx.TimeoutException`, `httpx.ConnectError` 或返回 5xx 状态码时触发。
 > * 重试逻辑必须遵循**带抖动(Jitter)的指数退避算法**。公式为：`delay = min(max_backoff, initial_backoff * (2 ** (attempt - 1)))`，最终等待时间应在此基础上增加少量随机性。
 > * 在每次重试前，必须使用 `logging` 记录一条 `WARN` 级别的结构化日志，包含端点、尝试次数和等待时间。
 > 4. **公共方法**:
 > * 实现 `async def check_connectivity(self)`、`async def get_rules(self)`、`async def get_proxies(self)` 和 `async def get_rule_providers(self)` 这四个公共方法。
 > * 这些方法内部调用 `_request` 方法。成功时（状态码 2xx）返回 JSON 解析后的数据；失败时（如 4xx 错误或重试耗尽），记录 `ERROR` 级别的结构化日志并向上抛出自定义异常（如 `ApiClientError`）。

* **实现状态**: ✅ 已完成
* **说明**: [api_client.py](file:///d:/Software/MMS2.0/mihomo_sync/modules/api_client.py) 模块已实现，支持异步 HTTP 请求、超时控制和指数退避重试机制。

---

#### **任务 1.2: 策略解析器 (`PolicyResolver`)** ✅ 已完成

* **目标**: 实现一个能够解析策略链、找到最终出口并能检测循环依赖的模块。
* **AI 编程提示词**:
 > 请在 `mihomo_sync/modules/policy_resolver.py` 中实现一个名为 `PolicyResolver` 的类。
 >
 > **需求**:
 > 1. **初始化**: `__init__` 方法接收所有代理/策略组的数据 (`proxies_data`)，并将其处理成一个易于查找的字典或映射。
 > 2. **核心方法**: 实现一个 `resolve(self, policy_name)` 方法，输入策略名称，返回最终的出口节点名称（即非策略组的节点）。
 > 3. **递归解析**: `resolve` 方法需要能处理嵌套的策略组。例如，A -> B -> C，其中 B 是策略组，C 是最终节点。
 > 4. **备忘录/缓存**: 实现一个内部缓存（memoization），对于已经解析过的 `policy_name`，直接返回结果，避免重复计算。
 > 5. **循环依赖检测**:
 > * 在递归解析的过程中，必须检测循环依赖（例如 A -> B -> A）。
 > * 可以传递一个 `visited` 集合来跟踪当前的解析路径。如果发现一个策略名已在当前路径中，则判定为循环。
 > * 检测到循环时，必须立即停止解析，记录一条 `ERROR` 级别的结构化日志（包含循环路径信息），并返回一个预设的默认值（例如 `'DIRECT'`）。

* **实现状态**: ✅ 已完成
* **说明**: [policy_resolver.py](file:///d:/Software/MMS2.0/mihomo_sync/modules/policy_resolver.py) 模块已实现，支持策略链解析、循环依赖检测和结果缓存。

---

### **阶段 2: 工作流编排 (Workflow Orchestration)** ✅ 已完成

**目标**: 开发驱动整个同步流程的监控器、生成器和控制器，将核心逻辑串联起来。

---

#### **任务 2.1: 状态监视器 (`StateMonitor`)** ✅ 已完成

* **目标**: 实现一个能够精确检测状态变化并利用防抖机制触发任务的监控器。
* **AI 编程提示词**:
 > 请在 `mihomo_sync/modules/state_monitor.py` 中使用 `asyncio` 实现一个 `StateMonitor` 类。
 >
 > **需求**:
 > 1. **初始化**: 接收 `MihomoApiClient` 的实例、轮询间隔 `polling_interval`、防抖间隔 `debounce_interval` 和一个回调函数 `on_change_callback`。
 > 2. **深度状态比对**:
 > * 实现一个私有方法 `_get_state_hash(self)`，它调用 API 客户端获取 `/proxies` 和 `/providers/rules` 的数据。
 > * 根据这些数据构建一个简化的、仅包含关键信息的字典（状态快照），并按键排序。
 > * 使用 `hashlib` (如 SHA-256) 计算该状态快照的哈希摘要并返回。
 > 3. **监控循环**: 实现一个 `async def start(self)` 方法，该方法启动一个无限循环：
 > * 每隔 `polling_interval` 秒，调用 `_get_state_hash` 获取新哈希。
 > * 与上一次的哈希进行比对。如果哈希值发生变化，则触发防抖逻辑。
 > 4. **防抖机制 (Debounce)**:
 > * 当检测到变化时，如果存在一个正在等待的防抖计时器 (`asyncio.Task`)，则取消它。
 > * 创建一个新的 `asyncio.sleep(self.debounce_interval)` 任务，任务完成后调用 `on_change_callback`。

* **实现状态**: ✅ 已完成
* **说明**: [state_monitor.py](file:///d:/Software/MMS2.0/mihomo_sync/modules/state_monitor.py) 模块已实现，支持状态监控、深度比对和防抖机制。

---

#### **任务 2.2: Mosdns 规则生成器 (`MosdnsRuleGenerator`) 与 服务控制器 (`MosdnsServiceController`)** ✅ 已完成

* **目标**: 将两个功能紧密相关的模块合并开发，一个负责生成和写入文件，一个负责执行系统命令。
* **AI 编程提示词**:
 > **第一部分：`MosdnsServiceController`**
 > 请在 `mihomo_sync/modules/mosdns_controller.py` 中实现 `MosdnsServiceController` 类。
 > **需求**:
 > 1. 初始化时接收 `reload_command` 字符串。
 > 2. 实现一个 `async def reload(self)` 方法。
 > 3. 使用 `asyncio.create_subprocess_shell` 或 `asyncio.create_subprocess_exec` 来异步执行重载命令。
 > 4. 必须捕获命令的 `returncode`, `stdout`, 和 `stderr`。
 > 5. 如果 `returncode` 不为 0，记录包含所有捕获信息的 `ERROR` 结构化日志，并返回 `False`。成功则记录 `INFO` 日志并返回 `True`。
 >
 > **第二部分：`MosdnsRuleGenerator`**
 > 请在 `mihomo_sync/modules/rule_generator.py` 中实现 `MosdnsRuleGenerator` 类。
 > **需求**:
 > 1. 初始化时接收 `MihomoApiClient` 和 `MosdnsServiceController` 的实例，以及 `mosdns_config_path`。
 > 2. 实现一个核心的 `async def run(self)` 方法，该方法是**被 `StateMonitor` 回调的函数**。
 > 3. **`run` 方法的逻辑**:
 > * 调用 API 客户端获取所有需要的数据 (`/rules`, `/proxies`, `/providers/rules`)。
 > * 实例化 `PolicyResolver`。
 > * 循环处理所有规则，映射规则提供者，并使用 `PolicyResolver` 找出最终出口。
 > * 将结果格式化为 `mosdns` 的规则字符串列表。
 > * **执行原子化文件写入**: 将所有规则字符串写入一个临时文件（如 `config_path + ".tmp"`）。写入成功后，使用 `os.rename` 将其重命名为最终的 `config_path`。
 > * 如果在写入或重命名过程中发生异常，必须清理临时文件，并记录 `CRITICAL` 日志。
 > * 文件操作成功后，调用 `mosdns_controller.reload()`。

* **实现状态**: ✅ 已完成
* **说明**: [mosdns_controller.py](file:///d:/Software/MMS2.0/mihomo_sync/modules/mosdns_controller.py) 模块已实现，包含 [MosdnsServiceController](file:///d:/Software/MMS2.0/mihomo_sync/modules/mosdns_controller.py#L12-L55) 和 [MosdnsRuleGenerator](file:///d:/Software/MMS2.0/mihomo_sync/modules/mosdns_controller.py#L58-L197) 两个类，支持规则生成、原子化文件写入和 Mosdns 服务重载。

---

### **阶段 3: 整合与应用启动 (Integration & Application Entrypoint)** ✅ 已完成

**目标**: 将所有模块组装起来，创建应用主入口，并实现健康检查和优雅退出。

---

#### **任务 3.1: 应用主入口 (`main.py`)** ✅ 已完成

* **目标**: 编写应用的启动脚本，完成所有对象的初始化和工作流的启动。
* **AI 编程提示词**:
 > 请为项目编写 `main.py` 文件，实现应用的异步主入口。
 >
 > **需求**:
 > 1. 使用 `async def main():` 作为主协程。
 > 2. **初始化**:
 > * 首先调用 `setup_logger` 初始化结构化日志。
 > * 加载 `ConfigManager` 并获取所有配置。
 > * 实例化 `MihomoApiClient`, `MosdnsServiceController`, 和 `MosdnsRuleGenerator`。
 > 3. **启动前健康检查**:
 > * 调用 `api_client.check_connectivity()` 检查与 `mihomo` 的连通性。
 > * 检查 `mosdns_config_path` 所在的目录是否可写。
 > * 任何检查失败，都应记录 `CRITICAL` 日志并退出程序。
 > 4. **启动工作流**:
 > * 实例化 `StateMonitor`，并将 `rule_generator.run` 方法作为其回调。
 > * 调用 `state_monitor.start()` 启动监控循环。
 > 5. **程序运行**: 使用 `asyncio.run(main())` 启动程序。程序应能持续运行直到被中断。

* **实现状态**: ✅ 已完成
* **说明**: [main.py](file:///d:/Software/MMS2.0/main.py) 文件已按照要求实现，包含了所有必要的组件初始化、健康检查、工作流启动和优雅退出机制。

---

### **阶段 4: 部署与文档 (Deployment & Documentation)** ✅ 已完成

**目标**: 为项目提供容器化部署方案和清晰的使用文档。

---

#### **任务 4.1: Dockerfile** ✅ 已完成

* **目标**: 创建一个优化的、多阶段构建的 Dockerfile 以便容器化部署。
* **AI 编程提示词**:
 > 请为这个 Python `asyncio` 项目编写一个 `Dockerfile`。
 >
 > **要求**:
 > 1. **多阶段构建**:
 > * 第一阶段 (`builder`): 使用一个标准的 Python 镜像（如 `python:3.10-slim`），安装 `poetry` 或 `pip`，复制 `pyproject.toml` 并安装依赖到一个虚拟环境中。
 > * 第二阶段 (final): 使用一个更小的基础镜像（如 `python:3.10-slim`）。从 `builder` 阶段复制虚拟环境和应用代码。
 > 2. **非 Root 用户**: 创建并切换到一个非 root 用户（如 `appuser`）来运行应用，以增强安全性。
 > 3. **工作目录**: 设置合适的工作目录 (`WORKDIR`)。
 > 4. **入口点**: 设置 `CMD` 来执行 `python main.py`。
 > 5. 确保 `config` 目录可以作为卷（volume）挂载，以便用户自定义配置。

* **实现状态**: ✅ 已完成
* **说明**: Dockerfile 已按照要求实现，使用了多阶段构建、非 root 用户运行、合理的卷挂载配置。

---

#### **任务 4.2: README 文档** ✅ 已完成

* **目标**: 编写一份全面的 `README.md` 文件。
* **AI 编程提示词**:
 > 请为 `Mihomo-Mosdns 动态同步` 项目生成一份详细的 `README.md` 文件。
 >
 > **内容应包括**:
 > 1. **项目简介**: 简要说明项目是做什么的，解决了什么问题。
 > 2. **特性**: 列出项目的主要特性（如：自动同步、高健壮性、指数退避重试、结构化日志等）。
 > 3. **运行原理**: 简单描述一下 "轮询-比对-生成-重载" 的工作流程。
 > 4. **如何使用**:
 > * **配置**: 详细解释 `config.yaml` 文件中每一个配置项的含义。
 > * **Docker 运行**: 提供一个 `docker run` 命令示例，包括如何挂载配置文件。
 > * **Docker Compose**: 提供一个 `docker-compose.yaml` 示例，将本服务与 `mihomo` 和 `mosdns` (如果它们也在 docker 中) 链接起来。
 > 5. **日志查看**: 说明如何查看结构化的 JSON 日志。

* **实现状态**: ✅ 已完成
* **说明**: README.md 已按照要求实现，包含了项目简介、特性、工作原理、使用方法、配置说明、Docker 部署示例和日志查看方法。

---

### **阶段 5: 测试覆盖 (Test Coverage)** ✅ 已完成

**目标**: 为所有核心模块编写单元测试，确保代码质量和功能正确性。

---

#### **任务 5.1: 核心模块单元测试** ✅ 已完成

* **目标**: 为所有核心模块编写全面的单元测试。
* **AI 编程提示词**:
 > 请为项目的各个模块编写单元测试：
 > 1. `ConfigManager` - 测试配置加载、验证和单例模式
 > 2. `MihomoApiClient` - 测试 API 请求、重试机制和错误处理
 > 3. `PolicyResolver` - 测试策略解析、循环依赖检测和缓存
 > 4. `StateMonitor` - 测试状态哈希计算和变化检测
 > 5. `MosdnsServiceController` 和 `MosdnsRuleGenerator` - 测试规则生成和服务重载

* **实现状态**: ✅ 已完成
* **说明**: 为所有核心模块编写了全面的单元测试，确保了代码质量和功能正确性。所有测试均已通过。