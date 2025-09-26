# RuleMerger 模板文档

## 功能介绍

RuleMerger（规则合并器）是 Mihomo-Mosdns 同步系统中两阶段生成架构的第二阶段模块。它负责读取 RuleGenerationOrchestrator 生成的结构化中间文件，高效地将它们合并、去重，并生成 Mosdns 使用的最终规则文件。该模块实现了跨文件的规则去重，确保最终生成的规则文件中没有重复项。

## 工作流程

1. **准备工作**：
   - 彻底清理或删除旧的最终输出目录
   - 创建新的输出目录结构

2. **遍历中间目录**：
   - 使用 os.walk 遍历中间目录下的所有策略和内容类型子目录
   - 识别目录结构中的策略和内容类型信息

3. **合并与去重**：
   - 对于每一个策略和内容类型的子目录：
     - 初始化一个空的规则集合（set）
     - 遍历该目录下的所有 .list 文件
     - 读取每个文件的所有行，并使用集合的 update 方法将它们全部添加到规则集合中
     - 集合会自动处理所有跨文件的重复规则

4. **写入最终文件**：
   - 当一个子目录下的所有文件都处理完毕后，如果规则集合不为空：
     - 在最终输出目录下创建对应的策略目录
     - 将规则集合的内容排序后，一次性写入到最终的文件中
     - 文件命名格式：`{content_type}.list`

5. **错误处理**：
   - 在读取单个文件失败时记录警告日志并继续处理其他文件
   - 在写入文件失败时记录错误日志并抛出异常

## 输入参数

### merge_from_intermediate 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| intermediate_path | str | 是 | 包含中间文件的目录路径 |
| final_output_path | str | 是 | 生成最终规则文件的输出目录路径 |

### _prepare_workspace 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| final_output_path | str | 是 | 最终输出目录路径 |

### _process_intermediate_directory 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| intermediate_path | str | 是 | 中间文件目录路径 |
| final_output_path | str | 是 | 最终输出目录路径 |

### _merge_directory_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| directory_path | str | 是 | 包含规则文件的目录路径 |
| policy | str | 是 | 策略名称（PROXY、DIRECT、REJECT等） |
| content_type | str | 是 | 内容类型（domain、ipv4、ipv6） |
| final_output_path | str | 是 | 最终输出目录路径 |

## 输出参数

### merge_from_intermediate 方法

该方法没有返回值，但会产生以下副作用：

1. **输出目录清理**：删除输出目录中的所有现有文件。

2. **最终文件生成**：在输出目录中创建以下文件结构：
   ```
   final_output_path/
   ├── PROXY/
   │   ├── domain.list
   │   ├── ipv4.list
   │   └── ipv6.list
   ├── DIRECT/
   │   ├── domain.list
   │   ├── ipv4.list
   │   └── ipv6.list
   └── REJECT/
       ├── domain.list
       ├── ipv4.list
       └── ipv6.list
   ```

3. **日志记录**：记录规则合并过程中的关键信息和错误。

### _merge_directory_rules 方法

该方法没有返回值，但会产生以下副作用：

1. **单个规则文件生成**：在输出目录中创建特定策略和内容类型的规则文件。

2. **日志记录**：记录目录规则合并的详细信息。