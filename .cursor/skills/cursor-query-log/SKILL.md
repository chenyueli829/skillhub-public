---
name: cyl-cursor-query-log
description: >-
  Appends every user message from Cursor chat into queries-log.md (one entry per
  user turn, no skipping for brevity or small talk). Use when cursor-query-log.mdc
  applies, or when the user @-mentions this skill or asks to log questions.
---

# Cursor 提问存档

## 存储位置（当前项目内 skill）

本 skill 与日志在 **`产品工作台/.cursor/skills/cursor-query-log/`**：

- [`queries-log.md`](queries-log.md)（与 `SKILL.md` 同目录）

**按工作区根选路径：**

- 工作区为 **`产品工作台`**：`.cursor/skills/cursor-query-log/queries-log.md`
- 工作区为 **`knowlege` 仓库根**：`产品工作台/.cursor/skills/cursor-query-log/queries-log.md`

只向 `queries-log.md` 追加，勿整文件覆盖。

## 何时记录（必须全量）

- 已启用 `cursor-query-log.mdc` 时：**用户本轮发送的整段消息必须记一条**，答完后立即追加。
- **禁止**因「太短、寒暄、谢谢、好的、继续、补充一句」等理由跳过或合并到上一条；**每一轮用户消息各记一条**。
- 唯一例外：消息**完全为空**（零字符）可不写；用户若明确说 **「暂停 cursor 提问存档」** 则至其说 **「恢复」** 前可不记（用户未说暂停则一律记）。
- 用户 @ 本 skill 或说记下来、存档时，同样按上条全量执行。

## 追加格式

在 `queries-log.md` 末尾追加：

```markdown
### YYYY-MM-DD HH:mm:ss 本地时间

**问：**
（用户本轮问题的原文，多行保留）

---

```

时间标题**必须含秒**（`HH:mm:ss`），用用户本地时区；写入时以当前时刻为准。

## 其它仓库

其它仓库需各自复制本目录与对应规则。

## 检索与整理

在项目中搜索 `queries-log.md` 或打开上述路径；可加标签行如 `**标签：** #工作`。
