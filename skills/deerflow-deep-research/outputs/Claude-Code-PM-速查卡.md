# Claude Code × PM 效率提升 — 速查卡

> 一页纸核心要点，详情见[完整研究报告](./Claude-Code-PM效率提升-完整研究报告.md)

---

## 一句话结论

Claude Code 的 PM 价值不在「更好的聊天」，而在**构建可复用的自动化工作流系统**——把信息搬运和文档格式化交给 AI，PM 聚焦判断与决策。

---

## 核心效率数据

| 任务 | 节省时间 | 来源 |
|------|---------|------|
| 竞品分析（5 家） | **85%**（3h→25min） | Reza Rezvani |
| PRD 首稿 | **>95%**（<2min） | prodmgmt.world |
| 客户访谈综合（10 份） | **>95%**（~30min） | Sachin Rekhi |
| Release Notes | **>90%**（<5min） | Sachin Rekhi |
| 数据分析 | **>99%**（~90sec） | YouTube |

---

## 四层自动化架构

```
Skills（工作流包）→ Hooks（守护脚本）→ MCP（外部工具）→ CLAUDE.md（治理层）
```

## 五步工作流构建法（Sachin Rekhi）

1. **拆解步骤** — 用自然语言描述任务步骤
2. **上下文策略** — 本地文件 > CLI > MCP > API > 浏览器
3. **选择原语** — 从 Skills 开始（其他原语的超集）
4. **塑造输出** — 模板 + 最佳实践 + 示例
5. **增量构建** — 让 Claude Code 自己写 Skill，然后迭代

---

## 三大核心场景

### 方案产出
- PRD 自动生成（结构化问答 → 模板填充 → 质量验证）
- 产品策略批判（投喂框架知识 → 逐维度检验）
- Release Notes（GitHub commit → 用户视角文案）

### 竞品调研
- 浏览器代理实时抓取定价（非缓存搜索）
- Subagents 并行研究 5+ 竞品
- 自动生成 Battle Card / 对比矩阵

### 流程自动化
- Hooks：文件编辑后自动格式化 / 任务完成后通知
- Scheduled Tasks：每周定时刷新竞品数据
- MCP：直接操作 Notion / Linear / Slack

---

## 推荐工具组合

| 任务 | 用什么 |
|------|--------|
| 探索性研究 | Perplexity / ChatGPT → 存为 Markdown |
| 方案 & 文档 | Claude Code + Skills |
| 竞品定价追踪 | Claude Code 浏览器代理 |
| 快速原型 | Cursor / Replit |
| 日常问答 | Claude.ai / ChatGPT |

---

## 三大局限（必须知道）

1. **深度研究不如 ChatGPT/Perplexity** — 用其他工具做研究，结果喂给 Claude Code
2. **自动生成内容需迭代** — 首版质量常不达标，需要 3+ 轮优化
3. **PM 判断力不可替代** — AI 做执行，PM 做判断

---

## Quick Start

```bash
# 1. 安装
curl -fsSL https://claude.ai/install.sh | bash

# 2. 创建项目
mkdir product-hub && cd product-hub

# 3. 启动
claude

# 4. 配置上下文
# 创建 CLAUDE.md（产品信息 + 术语表 + 偏好）

# 5. 安装 PM Skills
# 访问 prodmgmt.world 或 mcpmarket.com
```
