---
name: nano-banana-prompts
description: Nano Banana（nano-banana-pro 和 nano-banana-2）电影感图像提示词生成 skill。将分镜稿的单个镜头转化为可直接使用的图像生成提示词，包含摄影参数、角色一致性控制、风格标签。适用于 prompt-alchemist 的图像生成阶段。
---

# Nano Banana Prompts

将分镜稿的单个镜头转化为 Nano Banana 可执行的图像提示词。

## 参考资料位置

**个人知识库（最优先）：**
- `atoms/skills/nano-banana-prompts/references/my-best-practices.md`

**官方参考库（本地，按优先级）：**
1. `C:\Users\y2830\.opendeepcrew\references\awesome-nanobanana-pro\README.md` — 高质量提示词示例，搜索 `cinematic`、`film`、`portrait`
2. `C:\Users\y2830\.opendeepcrew\references\gpt4o-image-prompts\` — nanobanana 专项提示词，搜索电影感相关内容
3. `C:\Users\y2830\.opendeepcrew\references\awesome-nano-banana-images\` — 实际生成案例，搜索风格参考

查找顺序：个人知识库 → awesome-nanobanana-pro → gpt4o-image-prompts → awesome-nano-banana-images。

## 提示词结构

按以下顺序构建（Nano Banana 官方推荐）：

```
[Composition] [Subject] [Action] [Location] [Style] [Technical]
```

### Composition（构图/镜头）
来自分镜稿的景别和机位：
- 景别：`extreme close-up` / `close-up` / `medium shot` / `full body shot` / `wide shot` / `aerial view`
- 机位角度：`eye level` / `low angle` / `high angle` / `Dutch angle`
- 摄影机效果：`shallow depth of field` / `bokeh` / `motion blur`

### Subject（主体）
来自分镜稿的人物描述 + film-art-direction 的服装方案：
- 人物外貌：具体描述，越详细越好（用于一致性控制）
- 服装：颜色 + 材质 + 状态
- 情绪状态：来自 film-performance 的行动节拍

### Action（动作）
来自 film-performance 的人物行动节拍：
- 具体动作描述（动词 + 细节）
- 情绪与动作结合：`standing with tense posture` / `subtle grief expression`

### Location（场景）
来自 film-art-direction 的视觉元素清单：
- 场景陈设：具体物件描述
- 光源：来源 + 色温 + 方向
- 氛围：时代背景 + 环境细节

### Style（风格）
来自 film-visual-language 的视觉风格定调：
- 导演风格参考：`in the style of Wong Kar-wai` / `Hou Hsiao-hsien aesthetic`
- 胶片质感：`Kodak 5219 film stock` / `ARRI ALEXA` / `35mm film grain`
- 色彩风格：来自 film-visual-language 的色调描述转英文

### Technical（技术参数）
固定添加的电影感参数：
- 镜头焦段：`35mm lens`（广角叙事）/ `85mm lens`（人物情绪）/ `50mm lens`（自然视角）
- 光圈：`f/1.8`（浅景深）/ `f/2.8` / `f/8`（深焦）
- 质量标签：`cinematic`, `photorealistic`, `8K`, `professional cinematography`

## 一致性控制

**角色一致性（跨镜头）：**
1. 第一个镜头建立角色：用极详细的描述，包含独特标识（疤痕、特定饰品、发型）
2. 后续镜头：上传第一个镜头的图像作为参考，在提示词中写 `[Character Name] from the reference image`
3. Nano Banana 支持多图参考：`[Image1] [Image2]` 格式

**场景一致性（跨镜头）：**
- 建立场景参考图后，后续镜头上传参考图
- 提示词中明确：`same location as reference image, maintain consistent lighting and props`

## 输出格式

```
【镜号 X 图像提示词】

正向提示词：
[完整英文提示词，一段话叙述式，不是关键词列表]

负向提示词：
blurry, low quality, distorted face, extra limbs, watermark, text overlay

参考图：[是否需要上传参考图，上传哪张]
分辨率：[1K/2K/4K]
```

## 重要原则

- 用叙述式句子，不用关键词堆砌（Nano Banana 理解上下文，叙述式效果更好）
- 每个镜头单独输出，不混用
- 情绪描述要具体：不是 `sad`，而是 `eyes glistening with unshed tears, jaw slightly clenched`
