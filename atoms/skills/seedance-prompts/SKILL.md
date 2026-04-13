---
name: seedance-prompts
description: Seedance 2.0 视频提示词生成 skill。将已生成的参考图和分镜稿的镜头运动描述转化为 Seedance 2.0 可执行的视频提示词。适用于 prompt-alchemist 的视频生成阶段，输入为 nano-banana-prompts 生成的图像。
---

# Seedance Prompts

将参考图 + 分镜稿的镜头运动描述转化为 Seedance 2.0 视频提示词。

## 参考资料位置

**官方参考库（本地）：**
- `C:\Users\y2830\.opendeepcrew\references\awesome-seedance\`
- `C:\Users\y2830\.opendeepcrew\references\seedance-prompt-skill\`
- 搜索 `camera movement`、`cinematic`、`motion` 相关文件

**个人知识库（优先参考）：**
- `atoms/skills/seedance-prompts/references/my-best-practices.md`

查找顺序：先查个人知识库，再查官方参考库。

## 输入

- 参考图：nano-banana-prompts 生成的静态图
- 镜头运动：来自分镜稿的镜头运动描述（推/拉/摇/移/跟/静止）
- 时长：来自分镜稿的时长预估

## 提示词结构

Seedance 2.0 的提示词分两部分：

### 画面描述
基于参考图，简短描述画面内容（不需要重复图像里已有的细节，Seedance 会参考图像）：
- 主体状态：人物的动作和情绪
- 场景氛围：光线、环境

### 镜头运动描述
来自分镜稿，转化为 Seedance 可识别的运动指令：

| 分镜描述 | Seedance 提示词 |
|---------|----------------|
| 推镜头 | `slow push in toward subject` |
| 拉镜头 | `slow pull back, revealing the environment` |
| 摇镜头 | `pan left/right` |
| 移镜头 | `tracking shot, moving left/right` |
| 跟拍 | `follow shot, camera follows subject` |
| 静止 | `static shot, locked camera` |
| 手持 | `handheld camera, slight natural movement` |
| 升降 | `crane up/down` |

### 时间和节奏
- 时长：直接写秒数
- 节奏：`slow motion` / `normal speed` / `time lapse`

## 输出格式

```
【镜号 X 视频提示词】

提示词：
[画面描述] + [镜头运动] + [节奏/时长]

参考图：[使用哪张图作为首帧]
时长：[秒]
```

## 重要原则

- Seedance 以参考图为基础，提示词重点描述运动，不需要重复描述静态画面细节
- 镜头运动描述要具体：不是 `camera moves`，而是 `slow push in toward the character's face over 3 seconds`
- 每个镜头单独输出
