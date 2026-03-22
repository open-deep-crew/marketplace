---
name: writing-plans
description: 当您有多步任务的规范或要求时，在生成代码之前使用
---

# 编写计划

## 概述

编写全面的实施计划，假设工程师对我们的代码库没有任何背景和可疑的品味。记录他们需要知道的一切：每个任务要接触哪些文件，代码，测试，他们可能需要检查的文档，如何测试。把整个计划作为小任务给他们。干。YAGNI。TDD。频繁提交。

假设他们是熟练的开发人员，但对我们的工具集或问题域几乎一无所知。假设他们不太了解好的测试设计。

**开始时宣布：“我将使用写作计划技能来制定实施计划。”**

**背景：** 这应在专用工作树（由头脑风暴技能创建）中运行。

**计划保存至：** `docs/plans/YYYY-MM-DD-<功能名称>.md`

## 细化任务粒度

**每个步骤为一个动作（2-5分钟）：**
- “编写失败的测试”——步骤
- “运行测试以确保其失败”——步骤
- “实施最少的代码以使测试通过”——步骤
- “运行测试并确保其通过”——步骤
- “提交”——步骤

## 计划文档标题

**每个计划必须以此标题开头：**

```markdown
# [功能名称] 实施计划

> **致Kiro：** 必需的子技能：使用超级能力：executing-plans，逐项执行此计划任务。

**目标：** [用一句话描述此计划要构建的内容]

**架构：** [用2-3句话说明实现方法]

**技术栈：** [关键技术/库]

---
```

## 任务结构

```markdown
### Task N: [组件名称]

**文件:**
- 创建: `exact/path/to/file.py`
- 修改: `exact/path/to/existing.py:123-145`
- 测试: `tests/exact/path/to/test.py`

**步骤1：编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤2：运行测试以验证其失败**

运行: `pytest tests/path/test.py::test_name -v`
预期：失败，提示“函数未定义”

**步骤3：编写最小化实现**

```python
def function(input):
    return expected
```

**步骤4：运行测试以验证其通过**

运行: `pytest tests/path/test.py::test_name -v`
预期: 通过

**步骤5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: 添加特定功能"
```

## 注意事项
- 始终使用准确的文件路径
- 计划中包含完整代码（而非“添加验证”之类的表述）
- 带有预期输出的准确命令
- 用@语法引用相关技能
- 遵循DRY（不要重复自己）、YAGNI（你不会需要它）、TDD（测试驱动开发）原则，频繁提交

## 执行交接

- 将计划保存到`docs/plans/YYYY-MM-DD-<功能名称>.md`后，将完整的设计方案展示给用户，展示格式为：
    ```
    <主题>-Implement

    --

    <计划内容>
    ```
- 询问：“是否开始实施，使用 /executing-plans skill 实施实现计划”
