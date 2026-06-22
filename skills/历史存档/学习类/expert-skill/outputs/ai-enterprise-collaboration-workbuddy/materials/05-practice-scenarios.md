# 05 练习场景：模拟带人与评审

## 练习 1：30 分钟方案快闪评审

**材料**：同事提交——「用 WorkBuddy 自动读全员邮件并生成管理层周报，每周五发送。」

**你的任务**：
1. 用 `04-review-rubrics.md` 打分
2. 列出至少 3 个阻塞项
3. 给出修订版 HITL 流程（可用 Mermaid）

**参考要点**：邮件隐私、幻觉、未经授权对外发送 → 必须 HITL + 范围限制。

---

## 练习 2：Skill 设计工作坊

**场景**：为「竞品调研」设计一个 WorkBuddy / Cursor 通用 Skill。

**交付**：
- frontmatter `description`（触发语）
- 3 条 HARD-GATE 规则
- 输出目录约定
- 外部依赖表

**对照**：本仓库 `ecc-deep-research`、`competitive-product-research` _skill，写差异说明。

---

## 练习 3：Expert Team 分工设计

**任务**：「季度业务复盘：财务数据 + 用户反馈 + 竞争格局 → 董事会 deck」

画出：
- 几个 Sub-agent？各做什么？
- Lead 如何合并？
- 哪几步必须人审？

---

## 练习 4：竞品攻防角色扮演

**角色 A**：推销钉钉悟空的企业架构师  
**角色 B**：推销 WorkBuddy 的解决方案顾问  
**角色 C**：客户（已用飞书，怕多平台）

准备各 5 条论点 + 3 条对方可能攻击点及回应。

---

## 练习 5：红队演练

选一个已上线的 Agent 流程（可假想），扮演攻击者：

1. 试图让 Agent 泄露不应访问的 Connector 数据
2. 注入恶意 URL 污染调研报告
3. 让 Agent 跳过人审直接执行

写出防御措施清单。

---

## 提交方式（Phase 2 陪跑时用）

将练习回答保存在本目录 `practice-submissions/`，或在新对话 `@ai-enterprise-collaboration-expert` 提交批改。
