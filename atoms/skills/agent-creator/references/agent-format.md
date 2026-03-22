# Agent 文件格式规范

## 文件结构

Agent 是一个 `.md` 文件，通过 `opendeepcrew atom add ./<agent-name>.md --type agent --force` 注册到 marketplace。

```
---
name: <显示名称>
description: <角色定位、核心能力和适用场景的完整描述>
---

# Role: <显示名称> — <角色副标题>

<1-2 句话描述身份和职责>

## 行为准则

- 交流语言和风格
- 流程控制规则（如：每步等待用户确认）
- 范围限定

## 工作流程

### 阶段一：<阶段名>
<具体步骤、使用的 skill、输出格式>

**⏸ 停下，等待用户确认。**

### 阶段二：<阶段名>
...
```

## 命名规范

- 文件名：小写字母、数字、连字符，如 `my-code-reviewer.md`
- `name` 字段：人类可读的显示名称，如 `Code Reviewer`
- `description` 字段：完整描述角色和使用场景，这是触发 Agent 的关键

## 设计要点

1. **引用 Skill**：Agent 通过 `/<skill-name>` 引用已有 Skill 来组合能力
2. **阶段化流程**：将工作拆分为多个阶段，每个阶段结束后等待用户确认
3. **明确范围**：在行为准则中限定 Agent 的工作边界
4. **输出格式**：为关键输出定义固定格式（如报告模板）

## 现有 Agent 示例

| 文件名 | 角色 | 特点 |
|--------|------|------|
| `opendeepcrew-product-dev.md` | 需求开发专家 | 5 阶段流程，引用多个 Skill |
| `opendeepcrew-bug-fixer.md` | Bug 修复专家 | 3 阶段流程，精简高效 |
| `matteo-collina.md` | 架构专家人设 | 无阶段流程，以技术信仰和工作方式为主 |
