---
name: wecom-group
description: 使用企业微信自建应用创建群聊并向群聊发送消息。适用于需要自动拉群、发送群通知、创建群后发送首条消息、或通过脚本/agent 调用企业微信群聊接口的场景。
---

# wecom-group

使用这个 skill 来完成企业微信（WeCom）群聊相关操作，当前聚焦两类能力：

1. 创建企业微信群聊
2. 向已有群聊发送文本消息

## 使用前提

在执行前，先确认以下条件：

- 已有企业微信自建应用
- 自建应用具备创建应用会话和发送消息的权限
- 已拿到 `CorpID` 和应用 `Secret`
- 已明确群主 `owner` 的企业微信 `UserID`
- 已明确要拉入群聊的成员 `UserID` 列表

优先使用环境变量，避免把敏感信息直接写进命令行历史：

```bash
export WECOM_CORPID='your-corpid'
export WECOM_GROUP_HELPER_SECRET='your-secret'
```

也可以在命令中显式传入 `--id` 和 `--secret`。

## 脚本位置

使用下面的脚本执行实际操作：

```bash
python3 atoms/skills/wecom-group/scripts/wecom_group_operation.py --help
```

## 常用操作

### 1. 创建群聊

```bash
python3 atoms/skills/wecom-group/scripts/wecom_group_operation.py \
  create \
  --name '项目同步群' \
  --owner 'zhangsan' \
  --users 'zhangsan,lisi,wangwu'
```

如果希望指定群 ID：

```bash
python3 atoms/skills/wecom-group/scripts/wecom_group_operation.py \
  create \
  --name '项目同步群' \
  --owner 'zhangsan' \
  --users 'zhangsan,lisi,wangwu' \
  --chatid 'project-sync-group'
```

如果希望创建后立刻发首条消息：

```bash
python3 atoms/skills/wecom-group/scripts/wecom_group_operation.py \
  create \
  --name '项目同步群' \
  --owner 'zhangsan' \
  --users 'zhangsan,lisi,wangwu' \
  --msg '大家好，这是新建的项目同步群。'
```

### 2. 向已有群聊发消息

```bash
python3 atoms/skills/wecom-group/scripts/wecom_group_operation.py \
  send \
  --chatid 'project-sync-group' \
  --msg '今天下午 3 点进行项目例会。'
```

## 适合 agent 的调用方式

为了便于自动化处理，建议加上 `--json-output`：

```bash
python3 atoms/skills/wecom-group/scripts/wecom_group_operation.py \
  --json-output \
  create \
  --name '项目同步群' \
  --owner 'zhangsan' \
  --users 'zhangsan,lisi,wangwu'
```

返回结果会包含：

- `ok`: 是否成功
- `action`: 执行的动作
- `chatid`: 创建出的群聊 ID（如有）
- `response`: 企业微信接口原始返回

## 建议执行流程

处理用户请求时，按下面顺序执行：

1. 明确当前目标是“创建群”还是“发消息”
2. 收集必要参数
   - 创建群：`name`、`owner`、`users`
   - 发消息：`chatid`、`msg`
3. 优先通过环境变量注入 `WECOM_CORPID` 和 `WECOM_GROUP_HELPER_SECRET`
4. 执行脚本
5. 检查返回结果中的 `ok`、`chatid`、`response.errcode`
6. 向用户返回简明结果

## 参数约定

- `owner`：企业微信内部通讯录中的 `UserID`
- `users`：逗号分隔的 `UserID` 列表，脚本会自动去除空格
- `chatid`：可选；如果不传则由企业微信生成
- `msg`：当前脚本发送的是文本消息

## 错误处理

如果失败，优先检查：

- `CorpID` / `Secret` 是否正确
- 应用权限是否足够
- `owner` 是否存在
- `users` 中的成员 `UserID` 是否有效
- 机器人/应用是否有权限给该群发消息

如果开启了 `--json-output`，失败时脚本会返回非 0 退出码，并输出结构化错误信息。

## 注意事项

- 不要在最终回复中泄露 `Secret`
- 不要把敏感凭据写入仓库文件
- 如果用户没有提供 `UserID`，先让用户确认企业微信内部账号标识，再执行创建群聊
