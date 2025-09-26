# RuleGenerationOrchestrator 模板文档

## 功能介绍

RuleGenerationOrchestrator（规则生成协调器）是 Mihomo-Mosdns 同步系统中两阶段生成架构的第一阶段模块。它负责从 Mihomo API 获取所有规则数据，将其转换为结构化的中间文件格式。该模块实现了完全透明和可调试的转换过程，为后续的规则合并阶段提供标准化的输入。

与之前版本不同，该模块现在生成固定结构的中间文件夹，确保与 RuleMerger 模块的期望输入格式一致。

## 工作流程

1. **准备工作**：
   - 彻底清理或删除旧的中间目录，确保每次运行都是一个全新的开始
   - 创建新的中间目录结构

2. **一次性数据获取**：
   - 调用 Mihomo API 获取所有规则列表
   - 调用 Mihomo API 获取所有 RULE-SET 提供者的详细信息（URL, behavior 等）
   - 调用 Mihomo API 获取所有代理和策略组的信息

3. **初始化内存聚合器**：
   - 创建一个三层嵌套的字典，用于在内存中对规则进行分类和聚合
   - 结构为：`{ policy: { content_type: { provider_name: set() } } }`
   - 初始化固定策略：DIRECT、PROXY、REJECT

4. **遍历API规则列表**：
   - 对获取的每条规则进行处理
   - **对于 RULE-SET 类型的规则**：
     - 获取其策略和提供者名称
     - 使用 PolicyResolver 解析策略链，确定最终的出口策略（DIRECT、PROXY 或 REJECT）
     - 从提供者信息中查找详细信息
     - 调用 RuleConverter.fetch_and_parse_ruleset 获取解析后的内容列表
     - 根据提供者行为确定内容类型（domain 或 ipcidr）
     - 将内容列表批量添加到内存聚合器中
   - **对于单条规则**：
     - 获取其策略
     - 使用 PolicyResolver 解析策略链，确定最终的出口策略（DIRECT、PROXY 或 REJECT）
     - 调用 RuleConverter.convert_single_rule 转换为 Mosdns 格式
     - 将转换后的规则添加到内存聚合器中，使用 "_inline" 作为特殊提供者名称

5. **写入中间文件**：
   - 遍历内存聚合器的所有层级
   - 对于每个非空的规则集合，将其内容写入对应的中间文件
   - 文件路径结构：`{intermediate_dir}/{policy}/{content_type}/provider_{provider_name}.list`
   - 对于内联规则，文件名为 `_inline_rules.list`
   - 确保固定策略文件夹（DIRECT、PROXY、REJECT）都存在

6. **返回结果**：
   - 成功执行后返回生成的中间目录路径

## 输入参数

### __init__ 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| api_client | MihomoApiClient | 是 | Mihomo API 客户端实例 |
| config | ConfigManager | 是 | 配置管理器实例 |

### run 方法

该方法不需要额外参数，使用构造函数中传入的依赖项。

## 输出参数

### run 方法

| 返回类型 | 描述 |
|----------|------|
| str | 生成的中间目录的路径 |

### 中间文件结构

该模块会产生以下副作用：

1. **中间目录清理**：删除旧的中间目录并创建新的目录。

2. **中间文件生成**：在中间目录中创建以下结构的文件：
   ```
   {mosdns_config_path}_intermediate/
   ├── DIRECT/
   │   ├── domain/
   │   │   ├── provider_{provider_name1}.list
   │   │   ├── provider_{provider_name2}.list
   │   │   └── _inline_rules.list
   │   └── ipcidr/
   │       ├── provider_{provider_name3}.list
   │       └── _inline_rules.list
   ├── PROXY/
   │   ├── domain/
   │   │   ├── provider_{provider_name4}.list
   │   │   └── _inline_rules.list
   │   └── ipcidr/
   │       └── _inline_rules.list
   └── REJECT/
       └── domain/
           └── _inline_rules.list
   ```
   其中：
   - `{mosdns_config_path}` 是配置文件中指定的 Mosdns 配置路径。例如，如果 `mosdns_config_path` 设置为 `D:\Software\MMS2.0\output`，则中间目录为 `D:\Software\MMS2.0\output_intermediate`。
   - DIRECT、PROXY、REJECT 是固定的策略文件夹名称，确保与 RuleMerger 模块的期望输入格式一致。
   - `domain` 和 `ipcidr` 是内容类型，根据 RULE-SET 提供者的 behavior 属性确定。
   - `provider_{provider_name}.list` 是从 RULE-SET 提供者获取的规则文件。
   - `_inline_rules.list` 是内联规则文件，包含直接在配置中定义的规则。

3. **日志记录**：记录规则生成过程中的关键信息和错误。