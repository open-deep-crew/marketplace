#!/usr/bin/env python3
"""
Skill 初始化器 - 从模板创建新的 Skill

用法：
    init_skill.py <skill-name>

在当前工作目录下创建 Skill 目录。创建完成后，使用 `opendeepcrew atom add` 注册到 marketplace。

示例：
    init_skill.py my-new-skill
    init_skill.py my-api-helper
    init_skill.py custom-skill
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: 完整且信息丰富的说明，描述 Skill 的功能和使用时机。包含何时使用此 Skill 的信息——具体的场景、文件类型或触发任务。]
---

# {skill_title}

## 概述

[TODO: 1-2 句话说明此 Skill 能做什么]

## 组织此 Skill 的结构

[TODO: 选择最适合此 Skill 用途的结构。常见模式：

**1. 基于工作流程**（最适合顺序流程）
- 当有清晰的分步流程时效果最好
- 示例：DOCX Skill 的"工作流程决策树" → "读取" → "创建" → "编辑"
- 结构：## 概述 → ## 工作流程决策树 → ## 步骤 1 → ## 步骤 2...

**2. 基于任务**（最适合工具集合）
- 当 Skill 提供不同的操作/能力时效果最好
- 示例：PDF Skill 的"快速开始" → "合并 PDF" → "拆分 PDF" → "提取文本"
- 结构：## 概述 → ## 快速开始 → ## 任务类别 1 → ## 任务类别 2...

**3. 参考/指南**（最适合标准或规范）
- 当用于品牌指南、编码标准或需求时效果最好
- 示例：品牌样式的"品牌指南" → "颜色" → "字体" → "功能"
- 结构：## 概述 → ## 指南 → ## 规范 → ## 用法...

**4. 基于能力**（最适合集成系统）
- 当 Skill 提供多个相互关联的功能时效果最好
- 示例：产品管理的"核心能力" → 编号能力列表
- 结构：## 概述 → ## 核心能力 → ### 1. 功能 → ### 2. 功能...

模式可以根据需要混合搭配。大多数 Skill 会组合模式（例如，以基于任务开始，为复杂操作添加工作流程）。

完成后删除整个"组织此 Skill 的结构"部分——这只是指导。]

## [TODO: 根据选择的结构替换为第一个主要章节]

[TODO: 在此添加内容。参见现有 Skill 中的示例：
- 技术 Skill 的代码示例
- 复杂工作流程的决策树
- 包含真实用户请求的具体示例
- 根据需要引用脚本/模板/参考资料]

## 资源

此 Skill 包含示例资源目录，演示如何组织不同类型的捆绑资源：

### scripts/
可直接运行以执行特定操作的可执行代码（Python/Bash 等）。

**其他 Skill 的示例：**
- PDF Skill：`fill_fillable_fields.py`、`extract_form_field_info.py` - PDF 操作工具
- DOCX Skill：`document.py`、`utilities.py` - 文档处理 Python 模块

**适用于：** Python 脚本、Shell 脚本或任何执行自动化、数据处理或特定操作的可执行代码。

**注意：** 脚本可以不加载到上下文中直接执行，但 Claude 仍可能需要读取以进行修补或环境调整。

### references/
文档和参考材料，需要时加载到上下文中以指导 Claude 的流程和思考。

**其他 Skill 的示例：**
- 产品管理：`communication.md`、`context_building.md` - 详细工作流程指南
- BigQuery：API 参考文档和查询示例
- 财务：Schema 文档、公司政策

**适用于：** 深入文档、API 参考、数据库 Schema、综合指南，或 Claude 在工作时应参考的任何详细信息。

### assets/
不用于加载到上下文中的文件，而是用于 Claude 产出的输出中。

**其他 Skill 的示例：**
- 品牌样式：PowerPoint 模板文件（.pptx）、Logo 文件
- 前端构建器：HTML/React 样板项目目录
- 字体：字体文件（.ttf、.woff2）

**适用于：** 模板、样板代码、文档模板、图片、图标、字体，或任何用于复制或在最终输出中使用的文件。

---

**不需要的目录可以删除。** 并非每个 Skill 都需要所有三种类型的资源。
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的示例辅助脚本

这是一个可以直接执行的占位脚本。
根据需要替换为实际实现或删除。

其他 Skill 的真实脚本示例：
- pdf/scripts/fill_fillable_fields.py - 填写 PDF 表单字段
- pdf/scripts/convert_pdf_to_images.py - 将 PDF 页面转换为图片
"""

def main():
    print("这是 {skill_name} 的示例脚本")
    # TODO: 在此添加实际脚本逻辑
    # 可以是数据处理、文件转换、API 调用等

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 参考文档

这是详细参考文档的占位符。
根据需要替换为实际参考内容或删除。

其他 Skill 的真实参考文档示例：
- product-management/references/communication.md - 状态更新综合指南
- product-management/references/context_building.md - 收集上下文的深入指南
- bigquery/references/ - API 参考和查询示例

## 参考文档的适用场景

参考文档适用于：
- 全面的 API 文档
- 详细的工作流程指南
- 复杂的多步骤流程
- 对于主 SKILL.md 来说过长的信息
- 仅在特定使用场景下需要的内容

## 结构建议

### API 参考示例
- 概述
- 认证
- 端点及示例
- 错误码
- 速率限制

### 工作流程指南示例
- 前置条件
- 分步指令
- 常见模式
- 故障排除
- 最佳实践
"""

EXAMPLE_ASSET = """# 示例素材文件

此占位符表示素材文件的存储位置。
根据需要替换为实际素材文件（模板、图片、字体等）或删除。

素材文件不用于加载到上下文中，而是用于 Claude 产出的输出中。

其他 Skill 的素材文件示例：
- 品牌指南：logo.png、slides_template.pptx
- 前端构建器：hello-world/ 目录，包含 HTML/React 样板代码
- 字体：custom-font.ttf、font-family.woff2
- 数据：sample_data.csv、test_dataset.json

## 常见素材类型

- 模板：.pptx、.docx、样板目录
- 图片：.png、.jpg、.svg、.gif
- 字体：.ttf、.otf、.woff、.woff2
- 样板代码：项目目录、起始文件
- 图标：.ico、.svg
- 数据文件：.csv、.json、.xml、.yaml

注意：这是一个文本占位符。实际素材可以是任何文件类型。
"""


def title_case_skill_name(skill_name):
    """将连字符分隔的 Skill 名称转换为标题大小写以供显示。"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    初始化一个新的 Skill 目录，包含模板 SKILL.md。

    参数：
        skill_name: Skill 的名称
        path: Skill 目录应创建的路径

    返回：
        创建的 Skill 目录路径，如果出错则返回 None
    """
    # 确定 Skill 目录路径
    skill_dir = Path(path).resolve() / skill_name

    # 检查目录是否已存在
    if skill_dir.exists():
        print(f"❌ 错误：Skill 目录已存在：{skill_dir}")
        return None

    # 创建 Skill 目录
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 已创建 Skill 目录：{skill_dir}")
    except Exception as e:
        print(f"❌ 创建目录时出错：{e}")
        return None

    # 从模板创建 SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ 已创建 SKILL.md")
    except Exception as e:
        print(f"❌ 创建 SKILL.md 时出错：{e}")
        return None

    # 创建带有示例文件的资源目录
    try:
        # 创建 scripts/ 目录及示例脚本
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ 已创建 scripts/example.py")

        # 创建 references/ 目录及示例参考文档
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ 已创建 references/api_reference.md")

        # 创建 assets/ 目录及示例素材占位符
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ 已创建 assets/example_asset.txt")
    except Exception as e:
        print(f"❌ 创建资源目录时出错：{e}")
        return None

    # 打印后续步骤
    print(f"\n✅ Skill '{skill_name}' 已成功初始化于 {skill_dir}")
    print("\n后续步骤：")
    print("1. 编辑 SKILL.md 完成 TODO 项并更新描述")
    print("2. 自定义或删除 scripts/、references/ 和 assets/ 中的示例文件")
    print("3. 准备好后运行验证器检查 Skill 结构")

    return skill_dir


def main():
    if len(sys.argv) < 2:
        print("用法：init_skill.py <skill-name>")
        print("\nSkill 将在当前工作目录下创建。")
        print("\nSkill 名称要求：")
        print("  - 连字符分隔的标识符（例如 'data-analyzer'）")
        print("  - 仅限小写字母、数字和连字符")
        print("  - 最多 40 个字符")
        print("  - 必须与目录名完全匹配")
        print("\n示例：")
        print("  init_skill.py my-new-skill")
        print("  init_skill.py my-api-helper")
        print("  init_skill.py custom-skill")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = Path.cwd()

    print(f"🚀 正在初始化 Skill：{skill_name}")
    print(f"   位置：{path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        print(f"\n📋 注册到 marketplace：")
        print(f"   opendeepcrew atom add ./{skill_name} --type skill --force")
        print(f"\n📋 修改现有 skill 的工作流：")
        print(f"   1. opendeepcrew atom files skill <name>          # 列出文件")
        print(f"   2. opendeepcrew atom show skill <name>           # 读主文件")
        print(f"   3. opendeepcrew atom show skill <name> --file <path>  # 读子文件")
        print(f"   4. 保存到本地目录，编辑后：")
        print(f"      opendeepcrew atom add ./<name> --type skill --force  # 覆盖更新")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
