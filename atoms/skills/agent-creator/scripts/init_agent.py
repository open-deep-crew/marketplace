#!/usr/bin/env python3
"""
Agent 初始化器 - 创建新的 Agent 文件

用法：
    init_agent.py <agent-name>

输出路径通过执行 `opendeepcrew marketplace repodir` 命令自动获取。

示例：
    init_agent.py my-code-reviewer
    init_agent.py devops-expert
"""

import sys
import subprocess
from pathlib import Path


def get_agents_dir():
    """通过执行 opendeepcrew marketplace repodir 命令获取 agents 目录路径。"""
    try:
        result = subprocess.run(
            ['opendeepcrew', 'marketplace', 'repodir'],
            capture_output=True, text=True, check=True
        )
        repo_dir = result.stdout.strip()
        if not repo_dir:
            print("❌ 错误：opendeepcrew marketplace repodir 返回了空路径")
            sys.exit(1)
        return str(Path(repo_dir) / 'atoms' / 'agents')
    except FileNotFoundError:
        print("❌ 错误：未找到 opendeepcrew 命令，请确保已安装并在 PATH 中")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误：执行 opendeepcrew marketplace repodir 失败：{e.stderr.strip()}")
        sys.exit(1)


AGENT_TEMPLATE = """---
name: {agent_title}
description: [TODO: 描述此 Agent 的角色定位、核心能力和适用场景]
---

# Role: {agent_title}

[TODO: 1-2 句话描述此 Agent 的身份和职责]

## 行为准则

- 使用简体中文与用户交流
- 每一步完成后**必须停下来等待用户回复**，禁止在同一条消息中跳到下一步

## 工作流程

[TODO: 定义 Agent 的工作阶段和步骤]

### 阶段一：[TODO]

[TODO: 描述第一个阶段的具体步骤]

**⏸ 停下，等待用户确认。**
"""


def init_agent(agent_name, agents_dir):
    """初始化一个新的 Agent 文件。"""
    agents_path = Path(agents_dir)
    agents_path.mkdir(parents=True, exist_ok=True)

    agent_file = agents_path / f"{agent_name}.md"
    if agent_file.exists():
        print(f"❌ 错误：Agent 文件已存在：{agent_file}")
        return None

    title = ' '.join(word.capitalize() for word in agent_name.split('-'))
    agent_file.write_text(AGENT_TEMPLATE.format(agent_title=title))
    print(f"✅ 已创建 Agent 文件：{agent_file}")
    print("\n后续步骤：")
    print(f"1. 编辑 {agent_file} 完成 TODO 项")
    print("2. 运行 `opendeepcrew marketplace regenerate` 注册 Agent")
    return agent_file


def main():
    if len(sys.argv) < 2:
        print("用法：init_agent.py <agent-name>")
        print("\n示例：")
        print("  init_agent.py my-code-reviewer")
        print("  init_agent.py devops-expert")
        sys.exit(1)

    agent_name = sys.argv[1]
    agents_dir = get_agents_dir()

    print(f"🚀 正在初始化 Agent：{agent_name}")
    print(f"   位置：{agents_dir}")
    print()

    result = init_agent(agent_name, agents_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
