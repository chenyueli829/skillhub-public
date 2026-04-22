---
name: cyl-openclaw multiagent配置
description: "帮助新手快速规划和配置 OpenClaw 多 Agent 系统。通过交互式问答收集需求，自动生成 openclaw.json 的 agents.list + bindings 配置片段，以及标准的 Agent 工作区目录结构（包含 AGENTS.md / SOUL.md）。适用于需要构建多角色协作 Bot 的用户。"
version: 1.0.0
---

# OpenClaw 多 Agent 配置助手

帮助用户快速理解和配置 OpenClaw 多 Agent 系统，从需求分析到生成配置片段和标准 Agent 工作区目录结构。

## 何时使用此技能

当用户需要：
- 构建多个 Agent 协作的系统
- 在已有的 OpenClaw 中添加子 Agent
- 配置 `agents.list` 和 `bindings` 路由
- 设计 Agent 分工和角色
- 创建标准的 Agent 工作区目录结构（AGENTS.md / SOUL.md）
- 理解 `sessions_spawn`、`sessions_send` 等调度方法
- 把不同频道/账号路由到不同 Agent

## 核心能力

1. **需求分析** - 通过结构化问答理解业务场景
2. **架构设计** - 推荐合适的 Agent 分工方案
3. **配置生成** - 生成追加配置片段（而非完整文件！）
4. **目录结构生成** - 生成标准 Agent 工作区、AGENTS.md 和 SOUL.md
5. **路由设计** - 生成 bindings 路由规则，将频道/账号/DM 路由到对应 Agent
6. **激活说明** - 重启 Gateway 即可生效

## ⚠️ 极度重要：追加模式，绝不覆盖！

**你的 openclaw.json 中已有主 Agent 和其他配置，本次操作仅添加新内容，绝不删除或修改已有内容！**

---

## OpenClaw 多 Agent 核心概念

在开始之前，先理解 OpenClaw 的多 Agent 架构：

| 概念 | 说明 |
|------|------|
| **agentId** | Agent 的唯一标识（如 `main`、`writer`、`coding`） |
| **workspace** | Agent 的工作区目录，包含 AGENTS.md / SOUL.md / USER.md 等 |
| **agentDir** | Agent 的状态目录（auth、model registry），位于 `~/.openclaw/agents/<agentId>/agent` |
| **sessions** | Agent 的会话存储，位于 `~/.openclaw/agents/<agentId>/sessions` |
| **bindings** | 路由规则，将入站消息路由到指定 Agent |
| **accountId** | 频道账号实例（如 WhatsApp 的 `personal` vs `biz`） |

**每个 Agent 是一个完全隔离的"大脑"**：独立的工作区、独立的认证、独立的会话存储。

---

## 工作流程

### 步骤 0：备份已有配置

**备份文件**：

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
```

> Windows (WSL2)：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup`
> 配置文件路径也可通过 `OPENCLAW_CONFIG_PATH` 环境变量自定义。

---

### 步骤 1：理解业务场景

主动询问用户：
- "你想用多 Agent 解决什么问题？"
- "主要应用场景是什么？"（内容创作 / 技术支持 / 团队协作 / 个人助手 / 多人共享等）
- "预计需要几个 Agent 角色？"（推荐 2-5 个）
- "需要哪些频道？"（WhatsApp / Telegram / Discord / Slack / 微信等）
- "是否需要不同 Agent 使用不同的 AI 模型？"

---

### 步骤 2：设计 Agent 分工

**必问问题：**
1. "你想新增哪些 Agent 角色？"
2. "每个角色分别处理什么业务？"
3. "需要通过什么方式路由消息到不同 Agent？"（按频道 / 按账号 / 按 DM 发送者 / 按群组）

**典型方案推荐：**

**方案 A：内容创作团队（新增 2 个 Agent）**
- writer：负责内容创作
- editor：负责润色和审校

**方案 B：技术支持团队（新增 3 个 Agent）**
- triage：初步诊断问题类型
- tech-expert：解决技术问题
- escalation：处理复杂/紧急问题

**方案 C：多人共享助手（新增 2 个 Agent）**
- home：个人日常助手
- work：工作专用助手

**方案 D：按频道分流（新增 2 个 Agent）**
- chat：日常快速回复（WhatsApp，使用快速模型）
- deepwork：深度工作（Telegram，使用强力模型）

---

### 步骤 3：工作区规划

**核心原则：**
- 每个 Agent 需要独立的工作区目录
- 每个 Agent 有独立的 agentDir 和 sessions 存储（自动创建）
- 工作区中放置 AGENTS.md（核心配置）和 SOUL.md（人格设定）

**工作区结构推荐：**

```
~/.openclaw/workspace/                    ← 主 Agent 工作区（已存在）
~/.openclaw/workspace-writer/             ← 新增：写手工作区
~/.openclaw/workspace-editor/             ← 新增：编辑工作区
~/.openclaw/shared/                       ← 共享文件目录（可选）
```

**自动管理的目录（无需手动创建）：**

```
~/.openclaw/agents/writer/agent/          ← 写手的认证和模型配置
~/.openclaw/agents/writer/sessions/       ← 写手的会话存储
~/.openclaw/agents/editor/agent/          ← 编辑的认证和模型配置
~/.openclaw/agents/editor/sessions/       ← 编辑的会话存储
```

---

## 创建 Agent（推荐使用 CLI 向导）

### 方法 1：使用 CLI 向导（推荐）

OpenClaw 提供交互式 CLI 命令，自动创建工作区和配置：

```bash
# 添加新 Agent
openclaw agents add writer
openclaw agents add editor

# 验证已创建的 Agent
openclaw agents list --bindings
```

### 方法 2：手动配置（完全控制）

如果需要精细控制，按以下步骤手动操作。

---

## 手动配置详解

### 步骤 1：创建工作区目录

```bash
# macOS / Linux
mkdir -p ~/.openclaw/workspace-writer
mkdir -p ~/.openclaw/workspace-editor

# Windows (WSL2)
mkdir -p ~/.openclaw/workspace-writer
mkdir -p ~/.openclaw/workspace-editor
```

**正确的目录命名格式：**

```
~/.openclaw/workspace-<agent名称>
```

**正确示例：**

```
~/.openclaw/workspace-writer             (写手)
~/.openclaw/workspace-editor             (编辑)
~/.openclaw/workspace-coding             (编程助手)
~/.openclaw/workspace-home               (个人助手)
~/.openclaw/workspace-work               (工作助手)
```

**❌ 错误示例：**

```
~/.openclaw/workspace/writer             (错误：子目录格式)
~/.openclaw/workspace/editor             (错误：子目录格式)
```

---

### 步骤 2：创建 AGENTS.md（核心配置文档）

**在每个工作区目录中创建 AGENTS.md 文件。这是 Agent 的核心配置文档，包含 Agent 的基本信息和职责。**

#### AGENTS.md 标准模板

**示例：写手 Agent 的 AGENTS.md**

```markdown
# 写手 Agent

## 基本信息

| 字段 | 值 |
|------|-----|
| Agent ID | writer |
| Agent 名称 | 写手 |
| 描述 | 负责内容创作、文案撰写 |

## 主要职责

1. **内容创作** - 撰写文章、博客、文案
2. **风格适配** - 根据需求调整写作风格和语气
3. **素材整理** - 组织和整理写作素材

## 业务范围

- 接收主 Agent 或用户的写作任务
- 根据要求完成各类文字创作
- 将成果保存到工作区

## 与其他 Agent 的协作

- 接受 **main** Agent 的调度（通过 sessions_spawn）
- 完成后结果自动返回调度者
- 使用共享目录传递大型文件（可选）

## 工具使用

### 文件操作
- 读取工作区中的素材和模板
- 将创作内容保存到工作区

### 限制
- 不能直接访问其他 Agent 的工作区（除非通过共享目录）
- 不能修改 openclaw.json 配置
```

---

### 步骤 3：创建 SOUL.md（Agent 人格设定，可选）

**SOUL.md 定义 Agent 的人格、语气和行为风格。**

**示例：写手 Agent 的 SOUL.md**

```markdown
# 写手人格

你是一位经验丰富的内容创作专家。

## 性格特质

- 创意丰富：善于从不同角度切入话题
- 文笔优美：语言流畅自然，富有感染力
- 高效专注：快速理解需求并高质量完成

## 写作原则

1. 内容准确 - 确保事实正确
2. 风格适配 - 根据目标受众调整语气
3. 简洁有力 - 避免冗余，言之有物

## 行为规范

- 接到写作任务时，先确认需求和要求
- 完成后主动总结要点
- 遇到不确定的信息时如实说明
```

---

### 步骤 4：修改 openclaw.json（关键步骤）

**⚠️ 警告：只追加内容，不删除已有内容！**

**OpenClaw 使用 JSON5 格式**（支持注释和尾部逗号）。

#### 4.1 在 agents.list 中追加新 Agent

**在 `agents.list` 数组末尾追加新的 Agent 配置：**

```json5
{
  agents: {
    list: [
      // ... 已有的 Agent 配置（保留！）
      {
        id: "writer",
        name: "写手",
        workspace: "~/.openclaw/workspace-writer",
      },
      {
        id: "editor",
        name: "编辑",
        workspace: "~/.openclaw/workspace-editor",
      },
    ],
  },
}
```

#### 4.2 配置 subagents.allowAgents（允许调度）

**如果需要主 Agent 通过 sessions_spawn 调度子 Agent，需配置 allowAgents：**

```json5
{
  agents: {
    list: [
      {
        id: "main",
        // ... 已有配置
        subagents: {
          allowAgents: ["writer", "editor"],  // 新增允许调度的 Agent ID
        },
      },
      {
        id: "writer",
        name: "写手",
        workspace: "~/.openclaw/workspace-writer",
      },
      {
        id: "editor",
        name: "编辑",
        workspace: "~/.openclaw/workspace-editor",
      },
    ],
  },
}
```

**注意事项：**
- ✅ 保留 allowAgents 中所有已有的 agent ID
- ✅ 只新增新的 agent ID
- ❌ 不要删除任何已有的 agent ID！

#### 4.3 配置 bindings 路由（按需）

**bindings 决定入站消息如何路由到 Agent。路由规则是"最具体的优先"。**

**示例 A：按频道路由**

```json5
{
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "deepwork", match: { channel: "telegram" } },
  ],
}
```

**示例 B：按频道账号路由**

```json5
{
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

**示例 C：按 DM 发送者路由（同一 WhatsApp 号码）**

```json5
{
  bindings: [
    {
      agentId: "alex",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
      agentId: "mia",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
  ],
}
```

**示例 D：按 Discord 服务器路由**

```json5
{
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
}
```

**路由优先级（从高到低）：**

1. `peer` 匹配（精确 DM/群组/频道 ID）
2. `parentPeer` 匹配（话题继承）
3. `guildId + roles`（Discord 角色路由）
4. `guildId`（Discord）
5. `teamId`（Slack）
6. `accountId` 匹配
7. 频道级匹配（`accountId: "*"`）
8. 回退到默认 Agent

---

### 步骤 5：完整配置示例

**场景：内容创作团队，WhatsApp 为主频道**

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "主管",
        workspace: "~/.openclaw/workspace",
        subagents: {
          allowAgents: ["writer", "editor"],
        },
      },
      {
        id: "writer",
        name: "写手",
        workspace: "~/.openclaw/workspace-writer",
        model: "openai/gpt-4.1",  // 可选：指定模型
      },
      {
        id: "editor",
        name: "编辑",
        workspace: "~/.openclaw/workspace-editor",
        model: "anthropic/claude-sonnet-4-6",  // 可选：指定模型
      },
    ],
  },

  // 路由：WhatsApp 默认到主管 Agent
  bindings: [
    { agentId: "main", match: { channel: "whatsapp" } },
  ],
}
```

**场景：多人共享 + 按频道分流**

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "日常助手",
        default: true,
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-6",
      },
      {
        id: "deepwork",
        name: "深度工作",
        workspace: "~/.openclaw/workspace-deepwork",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "deepwork", match: { channel: "telegram" } },
  ],
}
```

---

### 步骤 6：重启 Gateway 使配置生效

```bash
# 重启 Gateway
openclaw gateway restart

# 验证 Agent 列表和路由
openclaw agents list --bindings

# 检查频道连接状态
openclaw channels status --probe
```

---

## 调度方法说明

### 方法 1：sessions_spawn（最常用）

子 Agent 在独立会话中执行任务，完成后结果自动 announce 回调用者。

```python
# 让写手写文章
sessions_spawn(
  task="写一篇关于 AI 未来趋势的文章，800 字",
  agentId="writer"
)

# 指定模型和思考级别
sessions_spawn(
  task="深度分析这份报告的数据趋势",
  agentId="editor",
  model="anthropic/claude-opus-4-6",
  thinking="high"
)

# 设置超时
sessions_spawn(
  task="研究竞品的最新动态",
  agentId="researcher",
  runTimeoutSeconds=300
)
```

**sessions_spawn 参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `task` | ✅ | 任务描述 |
| `agentId` | 可选 | 目标 Agent ID（需在 allowAgents 中） |
| `label` | 可选 | 任务标签 |
| `model` | 可选 | 覆盖子 Agent 默认模型 |
| `thinking` | 可选 | 思考级别（off/minimal/low/medium/high/xhigh） |
| `runTimeoutSeconds` | 可选 | 超时秒数（0 = 无超时） |
| `thread` | 可选 | 是否绑定到频道话题（默认 false） |
| `mode` | 可选 | `run`（一次性）或 `session`（持续会话，需 thread=true） |
| `cleanup` | 可选 | `delete`（完成后归档）或 `keep`（保留，默认） |

### 方法 2：sessions_send

向现有会话发送消息，适用于持续对话场景。

```python
sessions_send(
  agentId="writer",
  message="请修改第二段，语气更正式一些"
)
```

### 方法 3：sessions_list + sessions_history

发现和检索其他 Agent 的会话信息。

```python
# 列出活跃会话
sessions_list()

# 获取某个会话的历史记录（安全过滤后的视图）
sessions_history(sessionId="agent:writer:subagent:abc123")
```

### 方法 4：agents_list（发现可用 Agent）

```python
# 查看当前允许调度的 Agent 列表
agents_list()
```

---

## 高级配置

### 为 Agent 配置独立模型

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        model: "anthropic/claude-sonnet-4-6",  // 快速模型
      },
      {
        id: "deepwork",
        model: "anthropic/claude-opus-4-6",     // 强力模型
      },
    ],
  },
}
```

### 为 Agent 配置沙箱和工具限制

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: ["exec", "read", "sessions_list", "sessions_history"],
          deny: ["write", "edit", "browser", "canvas", "cron"],
        },
      },
    ],
  },
}
```

### 子 Agent 全局默认配置

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2,           // 允许嵌套（默认 1）
        maxChildrenPerAgent: 5,     // 每个 Agent 最多活跃子任务
        maxConcurrent: 8,           // 全局并发上限
        runTimeoutSeconds: 900,     // 默认超时
        model: "anthropic/claude-sonnet-4-6",  // 子 Agent 默认模型
      },
    },
  },
}
```

### 跨 Agent 消息工具

```json5
{
  tools: {
    agentToAgent: {
      enabled: true,               // 默认关闭
      allow: ["home", "work"],     // 允许通信的 Agent 列表
    },
  },
}
```

---

## 重要提醒

- **只在 agents.list 中追加 Agent 配置，不要删除或覆盖已有配置！**
- **修改前务必备份 openclaw.json！**
- **subagents.allowAgents 必须保留所有已有的 agent ID，只新增！**
- **OpenClaw 使用 JSON5 格式**（支持注释 `//` 和尾部逗号）
- **认证是 per-agent 隔离的**，不要跨 Agent 复用 agentDir
- 每个 Agent 的 workspace 是默认 cwd，不是硬沙箱；启用 sandbox 可增强隔离
- 配置需要根据实际业务场景定制，不要直接套用示例
- 每个子 Agent 需要独立的工作区目录（格式：`workspace-<agent名称>`）
- 修改配置后需要 `openclaw gateway restart` 生效

---

## 故障排除

**问题 1：子 Agent 无法被 spawn**
- 检查主 Agent 的 `subagents.allowAgents` 是否包含子 Agent 的 ID
- 运行 `openclaw agents list --bindings` 确认 Agent 已注册
- 使用 `agents_list` 工具查看当前可用的 Agent

**问题 2：Agent 找不到 AGENTS.md / SOUL.md**
- 检查文件是否在正确的工作区目录中
- 确认文件名拼写正确（大写 AGENTS.md、SOUL.md）
- 检查文件编码是否为 UTF-8

**问题 3：原有的 Agent 无法 spawn**
- 检查 `subagents.allowAgents` 中是否不小心删除了已有的 agent ID
- 从备份文件中恢复：`cp ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json`

**问题 4：消息路由到了错误的 Agent**
- 检查 `bindings` 数组中的顺序（最具体的规则放在前面）
- 运行 `openclaw agents list --bindings` 查看当前路由表
- peer 匹配优先于 channel-wide 规则

**问题 5：Agent 没有独立人格**
- 检查工作区中的 SOUL.md 是否存在且内容完整
- 确认 AGENTS.md 中的职责描述清晰
- 重启 Gateway：`openclaw gateway restart`

**问题 6：spawn 后没有返回结果**
- 检查子 Agent 是否正常启动（查看 Gateway 日志）
- sessions_spawn 是非阻塞的，结果通过 announce 机制返回
- 使用 `/subagents list` 查看运行状态
- 使用 `/subagents log <runId>` 查看子 Agent 日志

**问题 7：认证/模型问题**
- 每个 Agent 的认证是独立的，存储在 `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- 如需共享认证，手动复制 `auth-profiles.json` 到目标 Agent 的 agentDir
- 运行 `openclaw doctor` 排查配置问题

**问题 8：JSON5 格式错误**
- OpenClaw 使用 JSON5，支持注释和尾部逗号
- 检查括号是否匹配
- 运行 `openclaw doctor` 检查配置语法

**问题 9：工作区配置错误**
- 确认工作区路径格式为 `workspace-<agent名称>`，而非 `workspace/<agent名称>`
- 路径可使用 `~` 代表 home 目录
- 确认目录已创建并存在

**问题 10：频道账号配置问题**
- 多账号需要为每个账号单独登录：`openclaw channels login --channel whatsapp --account <accountId>`
- 运行 `openclaw channels status --probe` 检查连接状态

---

## 常用 CLI 命令速查

| 命令 | 说明 |
|------|------|
| `openclaw agents add <name>` | 交互式添加新 Agent |
| `openclaw agents list --bindings` | 列出所有 Agent 和路由 |
| `openclaw gateway restart` | 重启 Gateway |
| `openclaw channels status --probe` | 检查频道连接状态 |
| `openclaw channels login --channel <ch> --account <id>` | 登录频道账号 |
| `openclaw doctor` | 诊断配置问题 |
| `/subagents list` | 查看当前子 Agent 运行状态 |
| `/subagents spawn <task>` | 手动 spawn 子 Agent |
| `/subagents kill <runId>` | 停止子 Agent |
| `/subagents log <runId>` | 查看子 Agent 日志 |

---

**完成以上步骤后，新 Agent 就可以正常使用了！**
