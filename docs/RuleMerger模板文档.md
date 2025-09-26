# RuleMerger 模板文档

## 功能介绍

RuleMerger（规则合并器）是 Mihomo-Mosdns 同步系统中的文件处理模块，负责将 RuleConverter 生成的中间文件合并成最终的 Mosdns 规则文件。该模块处理临时目录中的所有策略和内容类型文件，生成可以直接被 Mosdns 使用的规则文件。

## 工作流程

1. **清理输出目录**：在开始合并之前，清空输出目录中的所有文件，确保生成的是最新规则。

2. **遍历策略目录**：扫描临时目录中的所有策略子目录（如 direct、proxy、reject）。

3. **处理每个策略**：对每个策略目录，处理其中的三种内容类型（domain、ipv4、ipv6）。

4. **合并内容类型规则**：
   - 收集指定内容类型目录中的所有 .txt 文件
   - 按文件名排序以确保输出一致性
   - 将所有文件内容合并写入到输出目录的对应文件中

5. **生成最终文件**：在输出目录中生成以下格式的文件：
   - policy_contenttype.txt（如 direct_domain.txt、proxy_ipv4.txt、reject_ipv6.txt）

6. **错误处理**：在读取单个文件失败时记录警告日志并继续处理其他文件。

## 输入参数

### merge_all_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| temp_dir | str | 是 | 包含中间文件的临时目录路径 |
| output_dir | str | 是 | 生成最终规则文件的输出目录路径 |

### _merge_policy_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| policy_temp_dir | str | 是 | 特定策略的临时目录路径 |
| policy | str | 是 | 策略名称（DIRECT、PROXY、REJECT） |
| output_dir | str | 是 | 输出目录路径 |

### _merge_content_type_rules 方法

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| content_type_dir | str | 是 | 特定内容类型的目录路径 |
| policy | str | 是 | 策略名称 |
| content_type | str | 是 | 内容类型（domain、ipv4、ipv6） |
| output_dir | str | 是 | 输出目录路径 |

## 输出参数

### merge_all_rules 方法

该方法没有返回值，但会产生以下副作用：

1. **输出目录清理**：删除输出目录中的所有现有文件。

2. **最终文件生成**：在输出目录中创建以下文件：
   ```
   output_dir/
   ├── direct_domain.txt
   ├── direct_ipv4.txt
   ├── direct_ipv6.txt
   ├── proxy_domain.txt
   ├── proxy_ipv4.txt
   ├── proxy_ipv6.txt
   ├── reject_domain.txt
   ├── reject_ipv4.txt
   └── reject_ipv6.txt
   ```

3. **日志记录**：记录规则合并过程中的关键信息和错误。

### _merge_content_type_rules 方法

该方法没有返回值，但会产生以下副作用：

1. **单个规则文件生成**：在输出目录中创建特定策略和内容类型的规则文件。

2. **日志记录**：记录内容类型规则合并的详细信息。