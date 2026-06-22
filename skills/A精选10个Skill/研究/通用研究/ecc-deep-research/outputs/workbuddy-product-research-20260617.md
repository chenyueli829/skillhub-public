# WorkBuddy 产品功能：研究报告

*生成日期：2026-06-17 | 来源数：12 | 置信度：高*

> **方法说明**：按 `ecc-deep-research` skill 工作流执行。当前环境未配置 firecrawl / exa MCP，已改用 WebSearch 多源检索 + 官方文档页面抓取，共分析 12 个来源。子问题：产品定位、核心能力、Agent 架构、企业版、集成生态。

## Executive Summary

WorkBuddy 是腾讯推出的**全场景 AI Agent 桌面工作台**，面向日常办公专业人士。用户用一句自然语言描述任务，产品即可自主规划、拆解并执行多步骤工作流，产出**可验证的交付物**（文档、报表、PPT、代码、分析结果等），而非仅聊天建议 ([WorkBuddy Overview](https://www.workbuddy.ai/docs/workbuddy/Overview))。

产品差异化在于：**本地文件操作**、**MCP 连接器生态**、**100+ 内置专家角色**、**专家团多 Agent 并行编排**，以及通过 Slack/Telegram/Discord/企微等实现的**远程助手（Assistant）** ([TechNode](https://technode.com/2026/05/29/tencent-launches-workbuddy-productivity-ai-agent-for-global-users/))。2026 年 6 月推出 **Enterprise Edition**，强化 OneID、积分计量、腾讯文档/云盘/乐享集成，从「超级个体」走向「超级团队」 ([abit.ee](https://abit.ee/en/artificial-intelligence/tencent-workbuddy-enterprise-ai-agent-agent-suite-enterprise-ai-mcp-en))。

## 1. 产品定位与核心价值

WorkBuddy 定位为「像同事一样干活的 AI 工作站」，与传统 AI 聊天工具对比：

| 维度 | 传统 AI 聊天 | WorkBuddy |
|------|-------------|-----------|
| 执行能力 | 仅建议 | 实际执行任务 |
| 文件操作 | 需人工处理 | 自动读写本地授权目录 |
| 任务复杂度 | 单步简单任务 | 多步复杂任务 |
| 输出形态 | 文本回复 | 可交付、可验证成果 |

来源：[WorkBuddy Overview](https://www.workbuddy.ai/docs/workbuddy/Overview)

支持平台：macOS（Apple Silicon / Intel）、Windows（x64 / ARM64）；需联网调用模型服务，支持 Google OAuth / GitHub OAuth 登录 ([FAQ](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/FQA))。

## 2. 核心产品功能模块

### 2.1 任务创建与执行

- **自然语言任务**：一句话描述需求，自动规划步骤 ([Create Task](https://www.workbuddy.ai/docs/workbuddy/Create-Task))
- **工作目录**：可选择文件夹作为任务上下文，批量处理本地文件
- **上下文补充**：`@` 引用文件/规则、粘贴截图、上传附件、明确目标/约束/输出格式
- **并行任务**：左侧任务列表，可同时创建多个任务；右侧结果面板展示 artifacts、文件变更与预览

### 2.2 典型办公场景

官方列举场景包括 ([Overview](https://www.workbuddy.ai/docs/workbuddy/Overview))：

- 文档生成：工作报告、技术文档、会议纪要
- 数据分析：上传数据文件自动分析与可视化
- 演示与报告：从需求描述生成 PPT / 报告
- 深度研究：复杂主题调研并输出报告
- 邮件起草、周报等日常办公
- 批量文件处理：整理、重命名、格式转换

### 2.3 专家中心（Expert / Expert Teams）

三层能力递进 ([专家中心文档](https://www.codebuddy.cn/docs/workbuddymini/features/Expert))：

| 层级 | 说明 |
|------|------|
| **Skill** | 工具能力 — 让 AI 能做某件事 |
| **专家（Agent 型）** | 领域 AI 顾问 — 独立人设、方法论、工具链 |
| **专家团（Team 型）** | 多 Agent 团队 — 团长拆解、分配、并行执行、整合交付 |

内置 **100+ 预配置专家角色**，覆盖运营、设计、数据、开发、营销、财务等 ([Tencent Cloud 产品页](https://www.tencentcloud.com/act/pro/workbuddy))。

### 2.4 远程助手（Assistant）

通过手机端 IM 远程操控电脑上的 WorkBuddy ([Assistant 文档](https://www.workbuddy.ai/docs/workbuddy/Claw))：

- 支持：Slack、Telegram、Discord、企业微信、飞书、钉钉、QQ、元宝派、微信助手
- 流程：手机发消息 → 电脑端 WorkBuddy 执行 → 结果回传手机
- 前提：电脑需开机且 WorkBuddy 在运行

### 2.5 安全与执行模式

- **本地优先**：授权文件在设备沙箱内处理，强调数据隐私 ([Futunn 报道](https://news.futunn.com/en/post/68528244/tencent-officially-enters-the-desktop-agent-market-with-workbuddy-launching))
- **高风险命令拦截**
- **人机协同**：AI 执行流程，人负责审核与最终质量把关 ([abit.ee Enterprise 报道](https://abit.ee/en/artificial-intelligence/tencent-workbuddy-enterprise-ai-agent-agent-suite-enterprise-ai-mcp-en))

## 3. 技术架构与扩展能力

### 3.1 MCP 连接器生态

通过 Connectors 扩展外部服务 ([Connector 文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector))：

| 连接器 | 典型用途 |
|--------|----------|
| GitHub / GitLab | 代码审查、PR、CI/CD |
| Jira | 工单、Sprint、报告 |
| Confluence | 文档与知识库 |
| Google Drive / Gmail | 文件协作、邮件 |
| Notion | 笔记与项目管理 |
| Slack | 消息与通知 |

Agent 向连接器发送结构化请求，获取数据后交由 LLM 处理 — 类似 function calling，但以统一 SDK 封装 ([LavX News 分析](https://news.lavx.hu/article/tencent-rolls-out-workbuddy-and-expands-its-ai-agent-lineup))。

### 3.2 多模型与 Skills

- 通过 API Key 灵活接入多模型；企业版可对接 Tencent Cloud TokenHub 统一 token 管理 ([Tencent Cloud 产品页](https://www.tencentcloud.com/act/pro/workbuddy))
- **Skills 技能库 / Skills Marketplace**：可扩展、可更新、部分社区技能免费
- 身份上下文：工作区注入 SOUL.md、IDENTITY.md、USER.md 等身份文件（产品运行时行为）

### 3.3 Expert Teams 编排机制

专家团内部为**任务图（task-graph）**：各节点在独立沙箱运行，通过共享状态存储通信；团长 Agent 拆解子任务、分配给角色专家、聚合结果 ([LavX News](https://news.lavx.hu/article/tencent-rolls-out-workbuddy-and-expands-its-ai-agent-lineup))。

## 4. 企业版（Enterprise Edition，2026-06）

三层企业能力模型 ([BestHub 分析](https://www.besthub.dev/articles/how-tencent-s-workbuddy-enterprise-aims-to-become-the-unified-ai-office-hub-33301d3250e9))：

| 层级 | 能力 |
|------|------|
| **Expert** | 封装角色知识、流程、工具、标准与输出要求 |
| **Assistant** | 云端 24/7 数字员工，跨设备记忆习惯与企业策略 |
| **Team** | 多专家/助手共享项目空间，沉淀集体智能 |

四大支柱：**Skills（怎么做）**、**MCP（在哪做）**、**数据与知识连接器（懂业务）**、**Harness（运行时基础）**。

企业版首批集成：腾讯文档、腾讯云盘、腾讯乐享；统一 **OneID** 与积分计量 ([abit.ee](https://abit.ee/en/artificial-intelligence/tencent-workbuddy-enterprise-ai-agent-agent-suite-enterprise-ai-mcp-en))。

## Key Takeaways

1. WorkBuddy 的核心卖点是**执行型 Agent**，不是聊天机器人 — 从自然语言到可交付成果的全链路自动化。
2. 产品能力呈三层递进：**Skill（能力）→ 专家（角色）→ 专家团（协作）**，适合从单点任务到复杂项目。
3. **MCP + 远程 Assistant + 本地沙箱** 构成「随时随地、安全可控」的办公 Agent 体验。
4. 企业版正将个人效率增益转化为**组织级知识资产与可管理数字员工**。

## Sources

1. [WorkBuddy Overview](https://www.workbuddy.ai/docs/workbuddy/Overview) — 产品定位与核心能力
2. [Create Task](https://www.workbuddy.ai/docs/workbuddy/Create-Task) — 任务创建流程
3. [Connectors](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector) — MCP 连接器列表
4. [Assistant Remote Control](https://www.workbuddy.ai/docs/workbuddy/Claw) — 远程助手与 IM 集成
5. [FAQ](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/FQA) — 平台、登录、网络要求
6. [专家中心](https://www.codebuddy.cn/docs/workbuddymini/features/Expert) — 专家/专家团/Skill 对比
7. [TechNode - Global Launch](https://technode.com/2026/05/29/tencent-launches-workbuddy-productivity-ai-agent-for-global-users/) — 全球化发布与 MCP
8. [PR Newswire - SEA Launch](https://www.prnewswire.com/apac/news-releases/tencent-cloud-unveils-new-ai-agents-workbuddy-and-miora-driving-innovation-and-real-business-outcomes-across-southeast-asia-302797910.html) — 企业场景与多 Agent 并行
9. [Tencent Cloud WorkBuddy 产品页](https://www.tencentcloud.com/act/pro/workbuddy) — 云服务、TokenHub、COS
10. [LavX News - Agent Lineup](https://news.lavx.hu/article/tencent-rolls-out-workbuddy-and-expands-its-ai-agent-lineup) — MCP 与 Expert Teams 技术解读
11. [BestHub - Enterprise Hub](https://www.besthub.dev/articles/how-tencent-s-workbuddy-enterprise-aims-to-become-the-unified-ai-office-hub-33301d3250e9) — 企业版三层模型
12. [abit.ee - Enterprise Edition](https://abit.ee/en/artificial-intelligence/tencent-workbuddy-enterprise-ai-agent-agent-suite-enterprise-ai-mcp-en) — 2026-06 企业版发布

## Methodology

检索 8 组关键词（WorkBuddy features、Enterprise、MCP、Expert Teams、官方文档等），筛选 12 个来源（官方文档优先，辅以 2025–2026 新闻报道与行业分析）。未使用 firecrawl/exa MCP（环境未配置）。
