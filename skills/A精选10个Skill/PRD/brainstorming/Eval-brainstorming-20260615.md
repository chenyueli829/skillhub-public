# Eval：brainstorming

> 生成日期：2026-06-15  
> 入口文件：skills/精选10个Skill/brainstorming/SKILL.md  
> 版本：未标注

## 1. 介绍

`brainstorming` 是一个**实现前设计门禁** skill：在任何创造性工作（新功能、组件、行为修改等）开始编码之前，Agent 必须先通过结构化对话把想法澄清为可执行的设计与规格说明。

核心流程为：探索项目上下文 →（可选）启用 Visual Companion 做视觉化讨论 → 逐题澄清需求 → 提出 2–3 种方案并推荐 → 分节呈现设计并逐节获批 → 将设计写入 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` 并提交 git → 规格自检 → 用户审阅书面规格 → 调用 `writing-plans` skill 生成实现计划。

skill 设有 **HARD-GATE**：在用户批准设计之前，禁止写代码、搭脚手架或调用实现类 skill。终态唯一允许的下游 skill 是 `writing-plans`，不是 `frontend-design`、`mcp-builder` 等。

可选能力 **Visual Companion** 通过本地 Node.js HTTP/WebSocket 服务，在浏览器中展示 mockup、线框图、架构图等 HTML 内容，用户点击选项后事件写入 `state/events`，Agent 在下一轮读取并与终端反馈合并。详见同目录 `visual-companion.md` 与 `scripts/`。

## 2. 触发条件

- **description 关键词**：creative work、creating features、building components、adding functionality、modifying behavior、before implementation、explores user intent、requirements and design
- **显式触发语**：
  - 中文：「帮我设计一下…」「先别写代码，我们先讨论方案」「头脑风暴」「做个功能前先对齐需求」「@brainstorming」
  - 英文：「brainstorm」「design before coding」「help me plan this feature」「explore approaches for…」「@brainstorming」
- **场景**：
  - 用户提出新功能、UI 改版、架构调整、在既有代码库中增加能力
  - 需求模糊、有多种实现路径、需要先对齐成功标准与范围
  - 项目较大需拆解为子项目，对第一个子项目做设计
- **不适用**：
  - 纯问答、代码审查、bug 修复（除非修复涉及较大行为/架构变更且用户明确要求先设计）
  - 用户已提供完整规格且明确要求直接实现
  - 仅文档翻译、格式化、一次性脚本等无设计歧义的任务

## 3. 提问示例

### 示例 1：新功能基础用法

（复制以下内容提问）

> @brainstorming 我想在这个项目里加一个「导出对话为 Markdown」的功能，先别写代码，帮我把需求和设计方案对齐清楚。

### 示例 2：带具体约束的 UI 改版

（复制以下内容提问）

> @brainstorming 请帮我把设置页重做成侧边栏 + 主内容区布局。目标用户是内部运营，要支持暗色模式，移动端可以只读。先用头脑风暴流程，我想看看 2–3 种布局方案再决定。

### 示例 3：大项目拆解 + Visual Companion（边界能力）

（复制以下内容提问）

> @brainstorming 我要做一个带实时聊天、文件上传和订阅计费的小型 SaaS，范围可能太大了。请先帮我拆成可独立实现的子项目，并对第一个子项目做设计；如果涉及首页布局对比，可以用 Visual Companion 在浏览器里给我看 wireframe。

## 4. 外部依赖

### API / 在线服务

| 服务 | 用途 | 是否必需 | 备注 |
|------|------|----------|------|
| Unsplash 等图床 | Visual Companion mockup 中可使用真实图片（visual-companion.md 设计建议） | 否 | 仅 HTML 中引用外部图片 URL，非 skill 硬依赖 |
| 无其他 SaaS/API | — | — | 核心流程为本地对话 + 本地文件 |

### MCP / CLI / 系统能力

| 依赖 | 用途 | 是否必需 |
|------|------|----------|
| Git | 设计文档撰写后需 commit（SKILL 明确要求） | 是（若走完整流程至写 spec） |
| Node.js | 运行 `scripts/server.cjs`（Visual Companion） | 否（仅启用 Visual Companion 时） |
| Bash | 执行 `scripts/start-server.sh`、`scripts/stop-server.sh` | 否（仅 Visual Companion） |
| 本地浏览器 | 用户打开 `http://localhost:<port>` 查看 mockup | 否（仅 Visual Companion） |
| `writing-plans` skill | 头脑风暴终态，生成实现计划 | 是（完整流程下游） |
| `elements-of-style:writing-clearly-and-concisely` skill | 撰写设计文档时可选使用 | 否 |
| Task 工具（general-purpose subagent） | `spec-document-reviewer-prompt.md` 中可选的规格审阅子代理 | 否 |

### 环境变量 / 凭证

| 变量名 | 用途 |
|--------|------|
| `BRAINSTORM_PORT` | Visual Companion 服务端口（默认随机高端口） |
| `BRAINSTORM_HOST` | 绑定地址（默认 `127.0.0.1`） |
| `BRAINSTORM_URL_HOST` | 返回 JSON 中显示的 URL 主机名 |
| `BRAINSTORM_DIR` | 会话目录（content/state 子目录） |
| `BRAINSTORM_OWNER_PID` | 父进程 PID，用于进程生命周期管理 |
| `CODEX_CI` | 由 start-server.sh 检测，影响前台/后台模式 |

无 API Key、Token、OAuth 要求。

### skill 目录外的路径

| 路径 | 用途 |
|------|------|
| `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | 默认设计文档输出位置（相对**当前项目根**） |
| `<project>/.superpowers/brainstorm/<session-id>/` | Visual Companion 持久化会话（`--project-dir` 时） |
| `/tmp/brainstorm-<session-id>/` | Visual Companion 无 project-dir 时的临时会话 |
| `skills/brainstorming/visual-companion.md` | SKILL 内引用的伴侣指南路径（本仓库中为 `skills/精选10个Skill/brainstorming/visual-companion.md`） |

### 第三方包 / 运行时

- **Node.js**（内置 `http`、`fs`、`crypto` 等，无额外 npm 依赖）
- 系统需支持 `bash`、`ps`、`kill`、`nohup`（start-server.sh）

**评测注意：** 本仓库内 skill 路径为 `skills/精选10个Skill/brainstorming/`，而 SKILL 正文引用 `skills/brainstorming/visual-companion.md`，评测时需以实际目录为准或做路径映射。下游 `writing-plans` skill 需在工作区或 Agent 环境中单独存在，本目录未捆绑。
