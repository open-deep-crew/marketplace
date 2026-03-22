---
name: skill-creator
description: 创建高效 Skill 的指南。当用户想要创建新的 Skill（或更新现有 Skill）以扩展 Claude 的能力时使用此 Skill，包括专业知识、工作流程或工具集成。
license: 完整条款见 LICENSE.txt
---

# Skill 创建器

本 Skill 提供创建高效 Skill 的指导。

## 关于 Skill

Skill 是模块化、自包含的包，通过提供专业知识、工作流程和工具来扩展 Claude 的能力。可以将它们理解为特定领域或任务的"入职指南"——它们将 Claude 从通用 Agent 转变为配备了模型本身无法完全具备的程序性知识的专业 Agent。

### Skill 提供的能力

1. 专业工作流程 - 特定领域的多步骤流程
2. 工具集成 - 处理特定文件格式或 API 的指令
3. 领域专业知识 - 公司特定的知识、Schema、业务逻辑
4. 捆绑资源 - 用于复杂和重复任务的脚本、参考资料和素材

## 核心原则

### 简洁至上

上下文窗口是公共资源。Skill 与 Claude 所需的其他一切共享上下文窗口：系统提示词、对话历史、其他 Skill 的元数据以及实际的用户请求。

**默认假设：Claude 已经非常聪明。** 只添加 Claude 尚不具备的上下文。对每条信息进行审视："Claude 真的需要这个解释吗？"以及"这段内容值得消耗这些 token 吗？"

优先使用简洁的示例，而非冗长的解释。

### 设置适当的自由度

根据任务的脆弱性和可变性匹配具体程度：

**高自由度（文本指令）**：当多种方法都有效、决策取决于上下文、或启发式方法指导方向时使用。

**中等自由度（伪代码或带参数的脚本）**：当存在首选模式、允许一定变化、或配置影响行为时使用。

**低自由度（特定脚本，少量参数）**：当操作脆弱且容易出错、一致性至关重要、或必须遵循特定顺序时使用。

可以将 Claude 想象为在探索一条路径：悬崖边的窄桥需要具体的护栏（低自由度），而开阔的田野允许多条路线（高自由度）。

### Skill 的结构

每个 Skill 由一个必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name:（必需）
│   │   └── description:（必需）
│   └── Markdown 指令（必需）
└── 捆绑资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 需要时加载到上下文中的文档
    └── assets/           - 用于输出的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

每个 SKILL.md 包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。这是 Claude 用来判断何时使用该 Skill 的唯一字段，因此清晰全面地描述 Skill 是什么以及何时使用非常重要。
- **正文**（Markdown）：使用 Skill 的指令和指导。仅在 Skill 触发后（如果触发的话）才会加载。

#### 捆绑资源（可选）

##### 脚本（`scripts/`）

可执行代码（Python/Bash 等），用于需要确定性可靠性或反复重写的任务。

- **何时包含**：当相同的代码被反复重写或需要确定性可靠性时
- **示例**：`scripts/rotate_pdf.py` 用于 PDF 旋转任务
- **优势**：节省 token、确定性强、可以不加载到上下文中直接执行
- **注意**：脚本可能仍需要被 Claude 读取以进行修补或环境特定调整

##### 参考资料（`references/`）

文档和参考材料，需要时加载到上下文中以指导 Claude 的流程和思考。

- **何时包含**：Claude 在工作时需要参考的文档
- **示例**：`references/finance.md` 用于财务 Schema，`references/mnda.md` 用于公司保密协议模板，`references/policies.md` 用于公司政策，`references/api_docs.md` 用于 API 规范
- **使用场景**：数据库 Schema、API 文档、领域知识、公司政策、详细工作流程指南
- **优势**：保持 SKILL.md 精简，仅在 Claude 判断需要时加载
- **最佳实践**：如果文件较大（>10k 字），在 SKILL.md 中包含 grep 搜索模式
- **避免重复**：信息应只存在于 SKILL.md 或参考文件中，不要两处都有。除非信息确实是 Skill 的核心内容，否则优先将详细信息放在参考文件中——这样可以保持 SKILL.md 精简，同时使信息可被发现而不占用上下文窗口。仅在 SKILL.md 中保留核心流程指令和工作流程指导；将详细的参考材料、Schema 和示例移至参考文件。

##### 素材（`assets/`）

不用于加载到上下文中的文件，而是用于 Claude 产出的输出中。

- **何时包含**：当 Skill 需要在最终输出中使用的文件时
- **示例**：`assets/logo.png` 用于品牌素材，`assets/slides.pptx` 用于 PowerPoint 模板，`assets/frontend-template/` 用于 HTML/React 样板代码，`assets/font.ttf` 用于字体
- **使用场景**：模板、图片、图标、样板代码、字体、需要复制或修改的示例文档
- **优势**：将输出资源与文档分离，使 Claude 能够使用文件而无需将其加载到上下文中

#### Skill 中不应包含的内容

Skill 应只包含直接支持其功能的必要文件。不要创建多余的文档或辅助文件，包括：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等等

Skill 应只包含 AI Agent 完成手头工作所需的信息。不应包含创建过程的辅助上下文、设置和测试流程、面向用户的文档等。创建额外的文档文件只会增加混乱。

### 渐进式披露设计原则

Skill 使用三级加载系统来高效管理上下文：

1. **元数据（name + description）** - 始终在上下文中（约 100 词）
2. **SKILL.md 正文** - 当 Skill 触发时（<5k 词）
3. **捆绑资源** - Claude 按需加载（无限制，因为脚本可以不读入上下文窗口直接执行）

#### 渐进式披露模式

保持 SKILL.md 正文精简，控制在 500 行以内以减少上下文膨胀。接近此限制时将内容拆分到单独的文件中。拆分内容到其他文件时，务必从 SKILL.md 中引用它们并清楚描述何时读取，以确保 Skill 的读者知道它们的存在和使用时机。

**关键原则：** 当 Skill 支持多种变体、框架或选项时，仅在 SKILL.md 中保留核心工作流程和选择指导。将变体特定的细节（模式、示例、配置）移至单独的参考文件。

**模式 1：高层指南 + 参考资料**

```markdown
# PDF 处理

## 快速开始

使用 pdfplumber 提取文本：
[代码示例]

## 高级功能

- **表单填写**：参见 [FORMS.md](FORMS.md) 获取完整指南
- **API 参考**：参见 [REFERENCE.md](REFERENCE.md) 获取所有方法
- **示例**：参见 [EXAMPLES.md](EXAMPLES.md) 获取常见模式
```

Claude 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

**模式 2：按领域组织**

对于包含多个领域的 Skill，按领域组织内容以避免加载无关上下文：

```
bigquery-skill/
├── SKILL.md（概览和导航）
└── reference/
    ├── finance.md（收入、计费指标）
    ├── sales.md（商机、管道）
    ├── product.md（API 使用、功能）
    └── marketing.md（营销活动、归因）
```

当用户询问销售指标时，Claude 只读取 sales.md。

类似地，对于支持多个框架或变体的 Skill，按变体组织：

```
cloud-deploy/
├── SKILL.md（工作流程 + 提供商选择）
└── references/
    ├── aws.md（AWS 部署模式）
    ├── gcp.md（GCP 部署模式）
    └── azure.md（Azure 部署模式）
```

当用户选择 AWS 时，Claude 只读取 aws.md。

**模式 3：条件性细节**

展示基础内容，链接到高级内容：

```markdown
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单编辑，直接修改 XML。

**修订追踪**：参见 [REDLINING.md](REDLINING.md)
**OOXML 详情**：参见 [OOXML.md](OOXML.md)
```

Claude 仅在用户需要这些功能时才读取 REDLINING.md 或 OOXML.md。

**重要指导：**

- **避免深层嵌套引用** - 保持引用从 SKILL.md 出发只有一层深度。所有参考文件应直接从 SKILL.md 链接。
- **结构化较长的参考文件** - 对于超过 100 行的文件，在顶部包含目录，以便 Claude 在预览时能看到完整范围。

## Skill 创建流程

Skill 创建包含以下步骤：

1. 通过具体示例理解 Skill
2. 规划可复用的 Skill 内容（脚本、参考资料、素材）
3. 初始化 Skill（运行 init_skill.py）
4. 编辑 Skill（实现资源并编写 SKILL.md）
5. 验证 Skill（运行 quick_validate.py）
6. 注册 Skill（运行 opendeepcrew marketplace regenerate）
7. 基于实际使用进行迭代

按顺序执行这些步骤，仅在有明确理由时才跳过。

### 步骤 1：通过具体示例理解 Skill

仅当 Skill 的使用模式已经被清楚理解时才跳过此步骤。即使在处理现有 Skill 时，此步骤仍然有价值。

要创建有效的 Skill，需要清楚理解 Skill 将如何被使用的具体示例。这种理解可以来自用户直接提供的示例，也可以来自经过用户反馈验证的生成示例。

例如，在构建图像编辑器 Skill 时，相关问题包括：

- "图像编辑器 Skill 应该支持哪些功能？编辑、旋转，还有其他吗？"
- "能给一些这个 Skill 会如何使用的示例吗？"
- "我能想象用户会说'去除这张图片的红眼'或'旋转这张图片'。你还能想到其他使用方式吗？"
- "用户说什么应该触发这个 Skill？"

为避免让用户不堪重负，避免在单条消息中提出太多问题。从最重要的问题开始，根据需要跟进以获得更好的效果。

当对 Skill 应支持的功能有清晰认识时，结束此步骤。

### 步骤 2：规划可复用的 Skill 内容

要将具体示例转化为有效的 Skill，需要分析每个示例：

1. 考虑如何从零开始执行该示例
2. 识别在反复执行这些工作流程时哪些脚本、参考资料和素材会有帮助

示例：构建 `pdf-editor` Skill 来处理"帮我旋转这个 PDF"之类的查询时，分析显示：

1. 旋转 PDF 每次都需要重写相同的代码
2. 在 Skill 中存储 `scripts/rotate_pdf.py` 脚本会很有帮助

示例：设计 `frontend-webapp-builder` Skill 来处理"帮我构建一个待办应用"或"帮我构建一个步数追踪仪表板"之类的查询时，分析显示：

1. 编写前端 Web 应用每次都需要相同的 HTML/React 样板代码
2. 在 Skill 中存储包含样板 HTML/React 项目文件的 `assets/hello-world/` 模板会很有帮助

示例：构建 `big-query` Skill 来处理"今天有多少用户登录了？"之类的查询时，分析显示：

1. 查询 BigQuery 每次都需要重新发现表 Schema 和关系
2. 在 Skill 中存储记录表 Schema 的 `references/schema.md` 文件会很有帮助

要确定 Skill 的内容，分析每个具体示例以创建要包含的可复用资源列表：脚本、参考资料和素材。

### 步骤 3：初始化 Skill

此时，是时候实际创建 Skill 了。

仅当正在开发的 Skill 已经存在且需要迭代或打包时才跳过此步骤。在这种情况下，继续下一步。

从零创建新 Skill 时，始终运行 `init_skill.py` 脚本。该脚本方便地生成一个新的模板 Skill 目录，自动包含 Skill 所需的一切，使 Skill 创建过程更加高效和可靠。

用法：

```bash
scripts/init_skill.py <skill-name>
```

该脚本：

- 在当前工作目录下创建 Skill 目录
- 生成带有正确 frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 SKILL.md 和示例文件。

### 步骤 4：编辑 Skill

编辑（新生成的或现有的）Skill 时，请记住 Skill 是为另一个 Claude 实例使用而创建的。包含对 Claude 有益且非显而易见的信息。考虑哪些程序性知识、领域特定细节或可复用素材能帮助另一个 Claude 实例更有效地执行这些任务。

#### 学习经过验证的设计模式

根据 Skill 的需求参考以下有用指南：

- **多步骤流程**：参见 references/workflows.md 了解顺序工作流程和条件逻辑
- **特定输出格式或质量标准**：参见 references/output-patterns.md 了解模板和示例模式

这些文件包含有效 Skill 设计的成熟最佳实践。

#### 从可复用的 Skill 内容开始

开始实现时，从上面识别的可复用资源开始：`scripts/`、`references/` 和 `assets/` 文件。注意此步骤可能需要用户输入。例如，在实现 `brand-guidelines` Skill 时，用户可能需要提供品牌素材或模板存储在 `assets/` 中，或文档存储在 `references/` 中。

添加的脚本必须通过实际运行来测试，确保没有 bug 且输出符合预期。如果有许多类似的脚本，只需测试有代表性的样本以确保它们都能工作，同时平衡完成时间。

Skill 不需要的任何示例文件和目录都应删除。初始化脚本在 `scripts/`、`references/` 和 `assets/` 中创建示例文件以演示结构，但大多数 Skill 不需要所有这些。

#### 更新 SKILL.md

**写作指南：** 始终使用祈使句/不定式形式。

##### Frontmatter

编写包含 `name` 和 `description` 的 YAML frontmatter：

- `name`：Skill 名称
- `description`：这是 Skill 的主要触发机制，帮助 Claude 理解何时使用该 Skill。
  - 包含 Skill 的功能和触发/使用场景。
  - 将所有"何时使用"信息放在这里——不要放在正文中。正文仅在触发后加载，因此正文中的"何时使用此 Skill"部分对 Claude 没有帮助。
  - `docx` Skill 的描述示例："全面的文档创建、编辑和分析，支持修订追踪、批注、格式保留和文本提取。当 Claude 需要处理专业文档（.docx 文件）时使用：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理修订追踪，(4) 添加批注，或任何其他文档任务"

不要在 YAML frontmatter 中包含其他字段。

##### 正文

编写使用 Skill 及其捆绑资源的指令。

### 步骤 5：验证 Skill

Skill 开发完成后，运行验证脚本检查 Skill 是否满足所有要求：

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

验证脚本将检查：

- YAML frontmatter 格式和必需字段
- Skill 命名规范（连字符格式、长度限制）
- 描述的完整性和质量（长度限制、禁止尖括号）
- 不允许的 frontmatter 属性

如果验证失败，脚本将报告错误。修复验证错误后重新运行验证命令。

### 步骤 6：注册 Skill

验证通过后，运行以下命令将 Skill 注册到 marketplace：

```bash
opendeepcrew atom add ./<skill-name> --type skill --force
```

该命令会自动完成 git commit 和 marketplace 注册，确保新创建或修改的 Skill 被正确注册和发现。

### 步骤 7：迭代

测试 Skill 后，用户可能会要求改进。这通常发生在使用 Skill 之后，对 Skill 的表现有新鲜的认识。

**迭代工作流程：**

1. 在实际任务中使用 Skill
2. 注意困难或低效之处
3. 确定 SKILL.md 或捆绑资源应如何更新
4. 实施更改并再次测试

**修改现有 Skill 的工作流：**

1. `opendeepcrew atom files skill <name>` — 列出 Skill 包含的所有文件
2. `opendeepcrew atom show skill <name>` — 读取主文件（SKILL.md）内容
3. `opendeepcrew atom show skill <name> --file <path>` — 读取子文件内容
4. 将内容保存到本地目录，进行编辑
5. `opendeepcrew atom add ./<name> --type skill --force` — 覆盖更新到 marketplace
