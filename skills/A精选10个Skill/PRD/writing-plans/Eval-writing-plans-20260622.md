# Eval：writing-plans

> 生成日期：2026-06-22  
> 入口文件：skills/精选10个Skill/writing-plans/SKILL.md  
> 版本：未标注

## 1. 介绍

`writing-plans` 是一个**实现前计划编写** skill：在已有规格说明（spec）或多步骤任务需求、且**尚未动手写代码**时，由 Agent 产出一份可供零上下文工程师（或子代理）逐步执行的实现计划。

计划强调 **TDD 小步快跑**：每个任务拆成约 2–5 分钟的一步（写失败测试 → 确认失败 → 最小实现 → 确认通过 → git commit），且每步须含**完整代码、精确路径、可运行命令与预期输出**，严禁 TBD、TODO 等占位。写计划前先做范围检查（多子系统应拆成多份计划）和文件结构映射（职责边界、接口、与既有代码库模式一致）。

计划文档有固定头部（Goal、Architecture、Tech Stack），并注明下游应使用 `superpowers:subagent-driven-development` 或 `superpowers:executing-plans` 执行。默认保存到 `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`（用户可覆盖路径）。写完计划后 Agent 须自检（规格覆盖、占位扫描、类型一致性），再向用户提供两种执行方式选择。

同目录 `plan-document-reviewer-prompt.md` 提供可选的**计划文档审阅**子代理模板（完整性、与 spec 对齐、可构建性），可在计划写完后派发 Task 工具审阅，但 SKILL 正文未将其列为硬性步骤。

## 2. 触发条件

- **description 关键词**：spec、requirements、multi-step task、before touching code、implementation plan
- **显式触发语**：
  - 中文：「根据这份规格写实现计划」「帮我拆成可执行任务」「先别写代码，写个开发计划」「@writing-plans」「生成 TDD 实现计划」
  - 英文：「write an implementation plan」「break this spec into tasks」「use writing-plans」「plan before coding」「create a bite-sized dev plan」
- **场景**：
  - 头脑风暴（`brainstorming`）结束后，已有书面 design/spec，需要进入实现阶段前的任务分解
  - 用户粘贴或引用 PRD、设计文档、功能需求，要求可执行的逐步计划
  - 多文件、多组件功能，需要明确 Create/Modify/Test 路径与 commit 粒度
- **不适用**：
  - 尚无规格、需求仍模糊（应先走 `brainstorming`）
  - 用户明确要求直接写代码、不修计划
  - 纯问答、文档润色、一次性脚本且无多步实现结构
  - 单步 trivial 修改（如改一行文案），无需完整 TDD 计划

## 3. 提问示例

### 示例 1：基于已有规格的基础用法

（复制以下内容提问）

> @writing-plans 我有一份功能规格在 `docs/superpowers/specs/2026-06-20-export-markdown-design.md`，请按 writing-plans 流程生成完整实现计划，保存到默认 plans 目录。先声明你在用这个 skill。

### 示例 2：带具体技术栈与仓库上下文

（复制以下内容提问）

> @writing-plans 请为「用户设置页增加暗色模式开关」写实现计划。技术栈：React + TypeScript + Vitest，相关文件大概在 `src/pages/Settings/` 和 `src/hooks/useTheme.ts`。要求 TDD 小步、每步有完整代码和 pytest/vitest 命令，不要任何 TODO 占位。

### 示例 3：多子系统范围检查 + 执行交接（边界能力）

（复制以下内容提问）

> @writing-plans 下面这份 spec 同时包含「实时聊天 WebSocket」和「Stripe 订阅计费」两个子系统，请先判断是否要拆成两份计划；若只需先做聊天部分，请只为聊天子系统写计划，并在保存后给我子代理驱动 vs 会话内联两种执行选项。

## 4. 外部依赖

### API / 在线服务

| 服务 | 用途 | 是否必需 | 备注 |
|------|------|----------|------|
| 无 | — | — | 本 skill 为本地文档编写流程，不调用外部 API |

### MCP / CLI / 系统能力

| 依赖 | 用途 | 是否必需 |
|------|------|----------|
| Git | 计划中每任务末尾含 `git add` / `git commit` 步骤 | 是（若按 skill 完整执行计划中的提交步骤） |
| 项目测试运行器 | 计划中示例为 `pytest`；实际须与目标项目一致（如 vitest、jest、cargo test） | 是（执行计划时，非写计划本身） |
| Task 工具（general-purpose subagent） | `plan-document-reviewer-prompt.md` 可选的计划审阅子代理 | 否 |
| `superpowers:using-git-worktrees` | 若在隔离 worktree 中工作，应先通过该 skill 创建 | 否（仅隔离开发场景） |
| `superpowers:subagent-driven-development` | 用户选择「子代理驱动」执行时的必需下游 skill | 否（写计划阶段不需要；执行阶段需要） |
| `superpowers:executing-plans` | 用户选择「会话内联执行」时的必需下游 skill | 否（同上） |
| `brainstorming` skill | 上游流程：头脑风暴终态常调用本 skill | 否（可直接提供 spec 触发本 skill） |

### 环境变量 / 凭证

| 变量名 | 用途 |
|--------|------|
| 无 | 本 skill 不要求 API Key、Token 或 OAuth |

### skill 目录外的路径

| 路径 | 用途 |
|------|------|
| `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` | 默认计划输出位置（相对**当前项目根**；用户偏好可覆盖） |
| `docs/superpowers/specs/` | 上游 brainstorming 默认 spec 目录；评测时常作为计划输入 |
| 用户提供的 spec / 设计文档路径 | 计划编写的输入来源 |

### 第三方包 / 运行时

- 无 skill 内 `scripts/` 或 `requirements.txt`；计划中出现的 `pytest` 等仅为**文档示例**，实际依赖目标项目栈。
- 执行计划时依赖目标仓库已安装的测试框架与运行时（Node、Python 等），由具体项目决定。

**评测注意：**

1. 本仓库路径为 `skills/精选10个Skill/writing-plans/`，而 SKILL 引用 `superpowers:*` 系列 skill 名称，评测环境需确认这些下游 skill 是否已安装或需路径映射。
2. 写计划前 Agent 应**口头声明**正在使用本 skill；评测时可检查是否出现该声明。
3. 验收重点：计划是否无占位、是否含精确路径与完整代码块、是否提供执行方式二选一、默认保存路径是否正确。
4. 可选加强：写完后用 `plan-document-reviewer-prompt.md` 派发审阅子代理，检查与 spec 对齐度。
