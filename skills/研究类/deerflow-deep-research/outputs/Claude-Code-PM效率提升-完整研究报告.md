# Claude Code 提升产品经理工作效率 — 深度研究报告

> 研究日期：2026-04-09 | 方法论：Deep Research Skill（四阶段系统化研究）

---

## Executive Summary

Claude Code 已从一个面向开发者的终端 AI 工具，演变为产品经理（PM）最具生产力的 Agentic 平台。其核心优势不在于「更好的聊天机器人」，而在于**构建可复用的自动化工作流系统**。

**核心发现：**
- PM 使用 Claude Code 可将竞品调研时间缩短 **85%**（从 3 小时→25 分钟）
- PRD 首稿可在 **2 分钟内**生成，深度图表分析从 3 小时降至 **90 秒**
- 通过 Skills + MCP + Hooks + Subagents 四层架构，PM 可将重复性工作流完全自动化
- **关键局限**：深度研究仍不如 ChatGPT/Perplexity；PRD 自动生成的内容质量需要人工迭代；使用成本和 Rate Limit 需关注

**核心判断**：Claude Code 的价值不在替代 PM 的策略思考，而在将 PM 从信息搬运和文档格式化中解放出来，使其聚焦于高杠杆的判断和决策工作。

---

## 一、Claude Code 核心能力全景

### 1.1 与 PM 工作相关的六大差异化能力

| 能力 | 说明 | PM 场景价值 |
|------|------|-------------|
| **Artifact 生成** | 擅长创建、改进和修改文档产物 | PRD、策略文档、竞品报告、Release Notes |
| **富本地上下文** | 直接读取本地 Markdown 文件，比 API 调用更快更可靠 | 产品数据、历史文档、模板库一站式加载 |
| **工作流自动化** | Skills / Commands / Agents / Hooks 四类自动化原语 | 从「每次手动提问」升级为「一键触发复杂流程」 |
| **命令行工具调用** | 可运行任何本地命令（Whisper / MySQL / GitHub CLI 等） | 音频转录、数据查询、代码分析 |
| **代码即工具** | 自动编写代码完成任务，PM 无需会编程 | 调用第三方 API、数据可视化、自动化脚本 |
| **极致可移植性** | 所有内容存储为本地 Markdown，无供应商锁定 | 随时迁移到新工具，技能资产不丢失 |

> **来源**：Sachin Rekhi, "Claude Code for Product Managers", 2026-03-11

### 1.2 六大扩展机制详解

#### Skills（可复用工作流包）
- **本质**：包含 `SKILL.md` 的文件夹，定义可重复的工作流指令
- **触发方式**：Slash Command 或自动检测激活
- **分类**：Capability Uplift（新增能力，如网页抓取）和 Encoded Preference（标准化团队流程）
- **PM 价值**：将「长 Prompt」封装为可维护、可共享的工作流包

#### MCP（模型上下文协议）
- **本质**：连接外部数据源的开放标准（"AI 的 USB-C"）
- **集成工具**：Notion / Linear / Jira / GitHub / Slack / Google Drive / MySQL
- **PM 价值**：让 Claude 直接操作 PM 日常工具，消除手动数据搬运

#### Hooks（确定性守护脚本）
- **本质**：在 Claude 生命周期特定事件自动触发的脚本
- **关键事件**：`PreToolUse`（执行前拦截）、`PostToolUse`（执行后自动操作）、`Stop`（任务完成通知）、`Notification`（消息推送）
- **PM 价值**：自动格式化输出、发送 Slack 通知、阻止危险操作

#### Subagents（并行子任务代理）
- **本质**：独立的 AI 实例，拥有自己的上下文窗口和工具权限
- **模式**：Hub-and-Spoke 编排，主代理分发→子代理并行执行→主代理综合
- **PM 价值**：同时研究 5 个竞品、同时分析 20 份客户访谈

#### Agent Teams（多代理协作）
- **本质**：多个独立 Claude 会话相互通信协作
- **与 Subagents 区别**：Teammates 之间可以互相通信，由 Lead Agent 协调
- **PM 价值**：复杂项目的「工程师视角」+「PM 视角」+「设计师视角」并行审查

#### Plugins（可分发工作流包）
- **本质**：将 Skills + Agents + Hooks + MCP 配置打包为可安装的团队标准化包
- **PM 价值**：团队统一工作流标准，新人一键安装即可上手

### 1.3 调度与执行方式

| 方式 | 基础设施 | 需本机在线 | 需打开会话 | 适用场景 |
|------|----------|-----------|-----------|---------|
| **Cloud Scheduled Tasks** | Anthropic 云端 | 否 | 否 | 每日 PR Review、定期依赖审计 |
| **Desktop Scheduled Tasks** | 本地机器 | 是 | 否 | 需要本地文件访问的定期任务 |
| **`/loop` (CLI)** | 本地终端 | 是 | 是 | 临时监控、轮询检查 |

---

## 二、场景一：方案产出加速

### 2.1 Sachin Rekhi 五步工作流构建法

这是目前 PM 社区最被广泛引用的 Claude Code 工作流构建框架：

#### Step 1: 拆解步骤（Detail the Steps）
用自然语言描述任务的离散步骤，无需编写代码。

> **示例**（数据问答 Skill）：
> 1. 分析数据库，理解表和列，总结 Schema
> 2. 告知用户已准备好回答数据问题
> 3. 对每个问题构造 SQL 查询并执行
> 4. 生成 HTML 报告（含原始问题、SQL、格式化结果表、可视化图表）

#### Step 2: 确定上下文策略（Context Strategy）
数据获取方式按可靠性排序：

| 优先级 | 方式 | 速度/可靠性 | 示例 |
|--------|------|------------|------|
| 1 | **本地文件** | ★★★★★ | Markdown 竞品文档、会议纪要 |
| 2 | **命令行工具** | ★★★★ | Whisper 音频转录、GitHub CLI |
| 3 | **MCP 服务器** | ★★★ | Notion / Linear / MySQL（Token 开销较大） |
| 4 | **第三方 API** | ★★★ | 让 Claude 写代码调用任意 API |
| 5 | **浏览器代理** | ★★ | 实时抓取竞品定价页（最慢但有时是唯一途径） |

#### Step 3: 选择工作流原语（Workflow Primitives）
**Sachin 的核心建议**：从 Skills 开始，它是其他原语的超集（可通过 Slash Command 调用、可 spawn Agents）。

#### Step 4: 塑造输出（Shape the Output）
三种提升输出质量的技术：
- **模板**：定义输出的精确结构（如客户访谈摘要的 7 个必填字段）
- **最佳实践**：投喂领域知识（如产品策略评估框架）
- **示例灵感**：提供 10-20 个优秀样例让 Claude 模仿风格

#### Step 5: 增量构建（Build Incrementally）
用自然语言描述需求，让 Claude Code 自己写 Skill 定义文件，然后迭代改进。

### 2.2 具体方案产出工作流

#### PRD 自动生成

**工作流**：
1. 用户调用 PRD Skill（如 `/pm-prd`）
2. Skill 引导用户回答 12+ 结构化问题（问题陈述、用户需求、指标、技术约束）
3. Claude 研究现有代码架构和项目文件
4. 应用预定义 PRD 模板生成文档
5. 自动验证（可测试性、清晰度、"shall" 语言规范）
6. 可选：自动在 Linear/Jira 创建分解任务

**关键工具**：
- [PRD Template Skill](https://mcpmarket.com/tools/skills/prd-template-generator) — 强制 REQ-001~REQ-059 编号系统
- [ChatPRD.ai](https://chatprd.ai/learn/PRD-for-Claude-Code) — 2026 最佳实践指南
- [prd-taskmaster](https://github.com/anombyte93/prd-taskmaster) — 开源 PRD + 任务分解集成

**最佳实践**：
- 使用 `@` 引用相关文件（`@company-context.md`, `@user-research.md`）
- 生成多个策略方案并行对比，而非单一方案
- 用 Sub-agents 模拟不同角色审查（工程师视角看技术可行性、高管视角看商业价值）

#### 产品策略批判

Sachin Rekhi 的核心示例：
- 将产品策略课程内容（目标受众评估、价值主张、战略差异化框架）存为本地知识文件
- Skill 读取策略文档后，逐维度用框架批判
- **真实案例**：对个人理财产品策略的批判——指出「目标受众定义过宽，缺乏 bullseye narrowing」「问题陈述流于表面，未应用 outcome-motivation-gap 框架」

**核心洞察**：AI 不擅长从零生成产品策略，但极擅长**批判和检验**策略。

#### Release Notes 自动生成

**工作流**：
1. 输入 GitHub commit URL
2. Claude 通过 GitHub CLI 读取 commit 标题、描述、变更文件
3. 生成面向用户的 Release Note（标题 + 1-5 段描述）
4. 参考过去 20 条 Release Notes 保持风格一致

**效率提升**：从 commit message "web clipper added article summaries" 自动生成完整的、从用户视角描述功能价值的专业 Release Note。

#### 客户访谈综合分析

**工作流**：
1. 从本地文件夹读取 Zoom 录像
2. 用 Whisper CLI 转录为文字
3. 按定制模板摘要每次访谈（受访者信息、关键收获、痛点、当前工作流、替代工具、功能需求、原始引用）
4. 跨访谈模式分析（按出现频率排序痛点 + 支持引用）

**核心价值**：跨 10 份访谈的综合分析，AI 可以做到全面覆盖，而手工分析几乎不可能不遗漏。

#### 数据问答（Answer Data Curiosity）

**工作流**：
1. 用自然语言提问
2. Claude 自动写 SQL 查询
3. 在数据库执行查询
4. 生成 HTML 报告（含表格、可视化图表、可审计 SQL）

**核心价值**：PM 不再需要写 SQL，也不再需要排队等数据团队响应。"No data curiosity goes unanswered."

---

## 三、场景二：竞品调研自动化

### 3.1 竞品调研工作流架构

传统方式 vs Claude Code 自动化：

| 环节 | 传统方式 | Claude Code 方式 |
|------|---------|-----------------|
| 信息采集 | 手动浏览 5+ 竞品网站，复制粘贴 | 浏览器代理自动抓取 / Web Search 并行采集 |
| 数据结构化 | 手动填写 Excel 对比表 | 自动生成结构化 Markdown 文件 |
| 分析综合 | 人工逐项对比，容易遗漏 | 跨文件交叉分析，识别战略信号 |
| 输出格式 | PPT/Excel，格式化耗时 | 自动生成 Battle Card / 对比矩阵 / 执行摘要 |
| 更新维护 | 每季度重做，数据常过期 | 重新运行 Skill 即可刷新，数据实时 |

### 3.2 竞品分析 Skill 实操

**[Competitor Analysis Skill](https://mcpmarket.com/tools/skills/competitor-analysis-1) 核心功能**：
- 自动识别 5 个主要直接竞品
- 对每个竞品进行 SWOT 分析
- 分析竞品商业模式、定价结构、销售策略
- Gap 分析：识别未被满足的客户细分和市场机会
- 12-18 个月风险评估
- 可操作的定位建议

**执行步骤**：
1. **准备**：创建竞品列表（`competitors.md`）和自有产品信息（`product-info.md`）
2. **定义 Skill**：在 `SKILL.md` 中指定搜索模式、数据提取需求、输出模板
3. **执行**：调用 Slash Command（如 `/update-competitors`），Claude 自动执行多步采集
4. **综合**：从各竞品独立文件聚合为高层输出（定价对比表、功能矩阵、战略 Battle Card）

### 3.3 竞品定价实时追踪

**Sachin Rekhi 的关键洞察**：

> "每次我让 Deep Research 或 ChatGPT 获取竞品定价，结果都严重过期。唯一准确获取定价数据的方法是让 AI 实时导航到每个定价页面并直接提取信息。"

**工作流**：
- 使用浏览器代理（非 Web Search）实时访问每个竞品定价页
- 提取并编译为综合竞品分析
- 输出包含每个竞品计划和定价的执行摘要
- 附带战略评论（如"你的产品提供了最慷慨的免费方案"）

### 3.4 并行多竞品研究

利用 Subagents 并行研究多个竞品：

```
提示词示例：
"使用 5 个独立的 subagents 并行研究以下竞品：
[竞品A], [竞品B], [竞品C], [竞品D], [竞品E]。
每个 subagent 生成独立的竞品档案文件，
最后主代理综合为对比矩阵。"
```

**效率数据（来源：Reza Rezvani, Medium）**：
- 竞品分析：3 小时 → 25 分钟（**节省 85%**）
- 市场趋势综合：6 小时 → 1 小时（**节省 83%**）
- 数据可随时重新运行获取最新信息

### 3.5 用户评价采集与分析

**工作流**：
1. 用 Web Search 从 G2 / Capterra / Reddit / App Store 采集用户评价
2. 按产品分类存储
3. 情感分析 + 关键痛点提取
4. 跨竞品用户反馈对比
5. 输出：未被满足的用户需求清单 + 产品机会点

---

## 四、场景三：流程自动化体系

### 4.1 自动化架构总览

```
┌─────────────────────────────────────────────────┐
│                  PM 工作台                        │
│  ┌───────────┐  ┌───────────┐  ┌──────────────┐ │
│  │  Skills    │  │  Agents   │  │  Scheduled   │ │
│  │  (复用包)  │  │ (并行执行) │  │  Tasks (定时) │ │
│  └─────┬─────┘  └─────┬─────┘  └──────┬───────┘ │
│        │              │               │          │
│  ┌─────▼──────────────▼───────────────▼───────┐  │
│  │              Hooks (守护层)                  │  │
│  │  PreToolUse → 输入验证 / 危险操作拦截        │  │
│  │  PostToolUse → 自动格式化 / 测试             │  │
│  │  Stop → 任务完成通知 / 最终摘要              │  │
│  └─────────────────────┬──────────────────────┘  │
│                        │                          │
│  ┌─────────────────────▼──────────────────────┐  │
│  │           MCP (外部工具连接层)                │  │
│  │  Notion · Linear · Jira · GitHub · Slack    │  │
│  │  MySQL · Google Drive · Figma               │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │          CLAUDE.md (治理层)                  │  │
│  │  产品上下文 · 决策框架 · 术语表 · 偏好记忆   │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 4.2 Skill 编写规范与最佳实践

#### 文件夹结构

```
my-pm-skill/
├── SKILL.md              # 核心指令文件（必需）
├── templates/            # 输出模板
│   ├── prd-template.md
│   └── battle-card.md
├── best-practices/       # 领域知识
│   ├── strategy-frameworks.md
│   └── past-examples.md
├── scripts/              # 可执行脚本（可选）
│   └── fetch-data.sh
└── references/           # 补充文档（按需加载）
    └── api-guide.md
```

#### SKILL.md 编写要点

```yaml
---
name: competitive-analysis
description: >
  Conduct comprehensive competitive analysis for product positioning.
  Use when user asks to "analyze competitors", "update competitive landscape",
  "generate battle cards", or "compare our product with competitors".
---
```

**关键原则**：
1. **渐进式披露**：YAML frontmatter 始终加载（轻量级）→ SKILL.md body 按需加载 → references/ 仅在需要时读取
2. **可组合性**：Skill 应能与其他 Skill 协同工作
3. **可移植性**：在 Claude.ai / Claude Code / API 中均可工作
4. **描述包含触发短语**：明确列出用户可能使用的触发表达

### 4.3 Hooks 配置实操

#### 示例 1：文件编辑后自动格式化

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

#### 示例 2：任务完成后发送 Slack 通知

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"Claude Code task completed!\"}' $SLACK_WEBHOOK_URL"
          }
        ]
      }
    ]
  }
}
```

#### 示例 3：阻止危险操作

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Shell",
        "hooks": [
          {
            "type": "command",
            "command": "echo $TOOL_INPUT | grep -q 'rm -rf' && echo '{\"decision\":\"block\",\"reason\":\"Dangerous command blocked\"}' || echo '{\"decision\":\"allow\"}'"
          }
        ]
      }
    ]
  }
}
```

### 4.4 MCP 集成推荐清单

| MCP 服务器 | PM 用途 | 优先级 |
|-----------|---------|-------|
| **Notion** | 知识库读写、文档管理、任务追踪 | ★★★★★ |
| **Linear** | 需求管理、Sprint 规划、Issue 创建 | ★★★★★ |
| **GitHub** | PR Review、Release Notes、代码分析 | ★★★★ |
| **Slack** | 消息推送、频道摘要、团队沟通 | ★★★★ |
| **Google Drive** | 文档协作、数据导入 | ★★★ |
| **MySQL/Postgres** | 数据查询、指标分析 | ★★★ |
| **Figma** | 设计稿引用、UI 审查 | ★★ |

> **注意**：MCP 调用 Token 消耗较大。Sachin Rekhi 建议：能用命令行工具替代 MCP 的场景，优先用命令行工具。

### 4.5 CLAUDE.md 上下文工程

CLAUDE.md 是项目根目录的「治理层」文件，确保 Claude 的所有输出保持一致性。

**推荐内容结构**：

```markdown
# Product Context

## Company & Product
- 公司名称、产品名称、一句话描述
- 目标客户画像
- 核心价值主张

## Voice & Tone
- 写作风格指南
- 术语表（产品专有名词）

## Technical Context
- 技术栈概述
- 架构模式

## Decision Frameworks
- 优先级评估框架
- 质量标准定义

## Memories & Preferences
- 历史决策记录
- 个人偏好（输出格式、语言风格）
```

### 4.6 推荐项目文件结构

```
product-hub/
├── CLAUDE.md                    # 全局上下文与治理
├── MEMORY.md                    # 自动记忆与纠错记录
├── .claude/
│   ├── settings.json            # Hooks 配置
│   ├── commands/                # Slash Commands
│   └── agents/                  # 自定义 Agent 定义
├── context/                     # 产品上下文文件
│   ├── product-context.md
│   ├── company-goals.md
│   └── domain-glossary.md
├── templates/                   # 输出模板
│   ├── prd-template.md
│   ├── battle-card-template.md
│   └── release-note-template.md
├── competitors/                 # 竞品数据
│   ├── competitors-list.md
│   ├── competitor-a.md
│   └── pricing-matrix.md
├── research/                    # 用户研究
│   ├── interviews/
│   ├── nps-analysis/
│   └── cross-interview-patterns.md
├── skills/                      # 自定义 Skills
│   ├── competitive-analysis/
│   ├── generate-prd/
│   ├── summarize-interviews/
│   └── generate-release-notes/
└── output/                      # 生成的产出物
    ├── prds/
    ├── reports/
    └── dashboards/
```

---

## 五、工具对比与组合策略

### 5.1 Claude Code vs 其他工具对比矩阵

| 维度 | Claude Code | Cursor | ChatGPT / Perplexity | Replit |
|------|------------|--------|---------------------|--------|
| **交互模式** | 终端 CLI | VS Code GUI | 对话式网页 | 浏览器 IDE |
| **核心优势** | 自主执行多步工作流 | 快速自动补全、原型开发 | 深度研究、即时问答 | 零代码快速原型 |
| **上下文能力** | 200k+ token，读取本地文件系统 | VS Code 项目上下文 | 单次会话上下文 | 项目级上下文 |
| **自动化深度** | Skills / Hooks / Agents / Scheduled Tasks | Rules / Commands | 自定义 GPTs | — |
| **PM 场景适配** | ★★★★★ | ★★★ | ★★★★ | ★★ |
| **学习曲线** | 中等（需熟悉终端） | 低（VS Code 用户友好） | 极低 | 低 |
| **成本** | $20/月（Pro）| $20/月 | $20/月 | $25/月 |

### 5.2 推荐工具组合策略

**Sachin Rekhi 的核心建议**：

> "Claude Code 不擅长深度研究。ChatGPT、Claude.ai、Gemini 和 Perplexity 都提供更好的开箱即用的深度研究方案。每次需要做探索性研究时，我仍然使用这些工具，然后将输出保存为 Markdown 文件供 Claude Code 处理。"

**推荐组合**：

| 任务类型 | 首选工具 | 协同方式 |
|---------|---------|---------|
| 探索性研究 | Perplexity / ChatGPT Deep Research | 输出 → 保存为本地 Markdown → Claude Code 处理 |
| 方案撰写 & 文档生成 | Claude Code | 结合本地上下文 + 模板 + Skills |
| 竞品定价实时追踪 | Claude Code（浏览器代理） | 直接访问竞品页面，非搜索缓存 |
| 快速原型 | Cursor / Replit | 需要 GUI 实时预览时 |
| 数据分析 | Claude Code | SQL 自动生成 + 可视化报告 |
| 日常问答 | Claude.ai / ChatGPT | 无需启动工作流的快速问题 |

---

## 六、效率量化数据

| 任务 | 传统耗时 | Claude Code 耗时 | 节省比例 | 数据来源 |
|------|---------|-----------------|---------|---------|
| 竞品分析（5 家） | 3 小时 | 25 分钟 | **85%** | Reza Rezvani, Medium |
| 市场趋势综合 | 6 小时 | 1 小时 | **83%** | Reza Rezvani, Medium |
| PRD 首稿 | 2-4 小时 | < 2 分钟 | **>95%** | prodmgmt.world |
| 深度图表分析 | ~3 小时 | ~90 秒 | **>99%** | YouTube Analytics Masterclass |
| 客户访谈摘要（10 份） | 10+ 小时 | ~30 分钟 | **>95%** | Sachin Rekhi |
| Release Notes | 30-60 分钟 | < 5 分钟 | **>90%** | Sachin Rekhi |

> **注意**：以上数据基于用户自述，未经严格量化实验验证。实际效率提升取决于 Skill 质量、上下文准备和人工审核时间。

---

## 七、风险与局限

### 7.1 已知局限

| 局限 | 详情 | 应对策略 |
|------|------|---------|
| **深度研究能力不足** | 不如 ChatGPT/Perplexity 的 Deep Research | 用其他工具做研究，结果存入本地文件 |
| **内容质量需迭代** | PRD 自动生成的实质内容常不够好 | 模板 + 最佳实践 + 示例 + 迭代改进 |
| **Rate Limit / 成本** | 高频使用可能快速耗尽配额 | 监控用量、使用 Sonnet 做常规任务 |
| **幻觉风险** | 复杂推理中可能产生不准确信息 | 人工审核关键输出，交叉验证 |
| **上下文窗口退化** | 长会话后可靠性下降 | 定期使用 `/compact`，拆分为小任务 |
| **MCP Token 消耗大** | 每次 MCP 调用消耗大量 Token | 能用 CLI 替代的优先用 CLI |
| **学习曲线** | 需要熟悉终端操作 | 从简单任务开始，逐步构建 |

### 7.2 Sachin Rekhi 的关键警示

> "我分享了大约 12 个我现在经常使用的 Skill。但我尝试构建过大约另外 24 个 Skill，最终都丢弃了，因为输出质量不够好。我看到社交媒体上有人声称用 AI 自动化了整个 PM 角色，但我无法想象他们在这样做的过程中没有产出大量低质量内容（slop）。"

**核心判断**：产品判断力和品味仍然是不可替代的。评判输出是否达标、决定是否继续迭代——这是 AI 时代 PM 最核心的能力。

---

## 八、30 天上手路线图

### Week 1：基础搭建（Day 1-7）
- [ ] 安装 Claude Code（`curl -fsSL https://claude.ai/install.sh | bash`）
- [ ] 创建 `product-hub/` 项目文件夹
- [ ] 配置 `CLAUDE.md`（产品上下文、术语表、偏好）
- [ ] 尝试直接对话：竞品信息查询、简单文档生成
- [ ] 安装 prodmgmt.world 的 AI PM OS Plugin

### Week 2：首个 Skill（Day 8-14）
- [ ] 选择一个高频重复任务（如 Release Notes / 会议摘要）
- [ ] 按五步法构建第一个 Skill
- [ ] 准备模板 + 3-5 个示例
- [ ] 运行并迭代至少 3 轮

### Week 3：竞品自动化（Day 15-21）
- [ ] 安装 Competitor Analysis Skill
- [ ] 创建竞品列表和自有产品信息文件
- [ ] 运行首次全面竞品分析
- [ ] 尝试 Subagents 并行研究多个竞品
- [ ] 配置 MCP 连接 Notion（保存研究结果）

### Week 4：系统化提升（Day 22-30）
- [ ] 配置 Hooks（自动格式化 + 完成通知）
- [ ] 构建第二个核心 Skill（如 PRD 生成或数据问答）
- [ ] 设置 Scheduled Tasks（如每周竞品定价刷新）
- [ ] 整理经验为团队分享文档
- [ ] 评估：哪些 Skill 真正达到了质量标准？哪些需要淘汰？

---

## 九、关键资源索引

### 权威指南
| 资源 | 链接 | 说明 |
|------|------|------|
| Sachin Rekhi 完整指南 | [sachinrekhi.com](https://www.sachinrekhi.com/p/claude-code-for-product-managers) | PM 视角最权威的 Claude Code 指南 |
| Anthropic 官方 Skill 构建指南 | [resources.anthropic.com](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | 官方技术文档 |
| Claude Code 官方 Hooks 文档 | [code.claude.com/docs](https://code.claude.com/docs/en/hooks-guide) | Hooks 配置详解 |
| Claude Code Scheduled Tasks | [code.claude.com/docs](https://code.claude.com/docs/en/web-scheduled-tasks) | 定时任务配置 |

### PM 社区资源
| 资源 | 链接 | 说明 |
|------|------|------|
| prodmgmt.world | [prodmgmt.world](https://www.prodmgmt.world/resources/claude-code) | 190+ PM Skills 库、168+ 框架、7 个工作流 |
| MCP Market 竞品分析 Skill | [mcpmarket.com](https://mcpmarket.com/tools/skills/competitor-analysis-1) | 开箱即用的竞品分析 Skill |
| MCP Market PRD 模板 | [mcpmarket.com](https://mcpmarket.com/tools/skills/prd-template-generator) | 专业 PRD 生成 Skill |
| ccforpms.com | [ccforpms.com](https://ccforpms.com/advanced/write-prd) | PM 专属 Claude Code 教程 |

### 开源仓库
| 仓库 | 说明 |
|------|------|
| [prd-taskmaster](https://github.com/anombyte93/prd-taskmaster) | PRD + 任务分解集成 |
| [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | Hooks 高级用法 |

### 视频教程
| 视频 | 说明 |
|------|------|
| [Sachin Rekhi 演示](https://www.youtube.com/watch?v=zsAAaY8a63Q) | 5 个 PM 工作流实操 Demo |
| [Build AI Agent Teams for Market Research](https://www.youtube.com/watch?v=JCVLTb4NvYk) | 多代理竞品调研 |
| [Claude Code Subagents](https://www.youtube.com/watch?v=GMAoTeD9siU) | 并行子代理详解 |
| [How Claude Code Hooks Save Hours](https://www.youtube.com/watch?v=Q4gsvJvRjCU) | Hooks 实操节省时间 |

---

## 十、结论与核心建议

### 核心判断

1. **Claude Code 是 2026 年 PM 最值得投资的 Agentic 平台**：企业级采用率最高、功能最全面、生态最活跃
2. **价值在于「系统化自动化」而非「更好的聊天」**：从 Skills → Hooks → MCP → Agents 逐层构建
3. **深度研究仍需组合工具**：Claude Code 搭配 Perplexity/ChatGPT 做研究，结果存本地供 Claude Code 处理
4. **质量 = 模板 × 最佳实践 × 示例 × 迭代轮次**：投入在 Skill 质量上的时间会持续复利
5. **PM 判断力不可替代**：AI 做执行，PM 做判断——这是最佳分工

### 立即行动

- **Quick Win（今天就能用）**：安装 Claude Code → 配置 CLAUDE.md → 用竞品分析 Skill 做一次完整调研
- **中期建设（2 周内）**：构建 2-3 个核心 Skill（PRD / Release Notes / 数据问答）
- **长期架构（1 个月内）**：建立完整 product-hub 项目 → MCP 集成 → Scheduled Tasks → 团队推广

---

*本报告基于 Anthropic 官方文档、Sachin Rekhi 权威指南、prodmgmt.world 社区资源、Medium/Reddit 用户实操反馈等多源交叉验证编写。效率数据基于用户自述，具体效果因场景而异。*
