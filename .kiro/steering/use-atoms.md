---
inclusion: auto
description: 指导 Kiro 优先使用 atoms/ 目录中的 agents 和 skills 能力库
---

# 使用 atoms 能力库

这个工作区的 `atoms/` 目录是我的能力库，包含 agents 和 skills。

**核心原则：`atoms/` 里有的，优先用 `atoms/` 里的。**

每次对话前，判断当前任务是否有对应的 agent 或 skill：
- 有对应 agent（`atoms/agents/`）→ 读取该 agent 文件，按其工作流程和阶段执行
- 有对应 skill（`atoms/skills/`）→ 读取该 skill 文件，按其流程和输出格式执行
- 用户明确指定 agent/skill → 必须读取并遵循，不能凭直觉自由发挥

当前可用的 agents：`creative-architect`、`prompt-alchemist`
当前可用的 skills：`film-narrative`、`film-visual-language`、`film-directing`、`film-performance`、`film-art-direction`、`nano-banana-prompts`、`seedance-prompts`、`creative-workflow`、`film-narrative`
