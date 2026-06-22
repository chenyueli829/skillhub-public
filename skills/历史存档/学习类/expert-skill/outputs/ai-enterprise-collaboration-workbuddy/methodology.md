# 专家成长方法论：AI + 企业办公协同

> 领域自适应框架，锚定 WorkBuddy 及企业 Agent 工作台赛道。  
> 适用目标：L5 资深（能判断、评审、带人）。

## 方法论总览：ACE 循环

```
Assess（场景评估）→ Compose（编排设计）→ Execute（试点验证）→ Evolve（治理演进）
         ↑___________________________________________|
```

### Phase A — Assess 场景评估（1–2 周）

**输入**：业务痛点、现有工具栈、合规约束  
**动作**：
1. 用 JTBD 写清「用户要完成的 Job」，而非「要一个 Chatbot」
2. 判定 AI 成熟度级别：L1 个人效率 / L2 流程嵌入 / L3 自主 Agent
3. 映射到 WorkBuddy 能力：单 Expert、Expert Team、自定义 Skill、MCP 外连

**产出**：场景卡片（用户、Job、成功标准、风险等级、建议 HITL 级别）

### Phase B — Compose 编排设计（2–3 周）

**动作**：
1. 画三层栈：推理层（Agent）→ 连接层（MCP）→ 治理层（审批/审计）
2. 定义工作流环：research → synthesis → critique → decision → log
3. 设计 Skill 契约：触发语、输入输出、禁止行为、外部依赖
4. 设计 Identity（若需要人格/角色）：SOUL 边界、不可越权事项

**产出**：编排蓝图 + Skill 规格草稿 + 治理规则表

### Phase C — Execute 试点验证（3–4 周）

**动作**：
1. 选 1 个高价值、中风险场景做 POC（建议：调研报告生成或知识库问答）
2. 埋点：任务成功率、人工介入率、平均轮次、用户满意度
3. 跑 3 次「红队」：权限越界、幻觉引用、级联失败

**产出**：试点报告 + 迭代清单

### Phase D — Evolve 治理演进（持续）

**动作**：
1. 从 HITL 逐步评估 HOTL 可行性（按风险分级）
2. 建立 Skill/Expert 评审门禁（可参考 skill-vetter 思路）
3. 季度复盘：ROI、采用率、团队 AI 协作规范更新

## 与 ai-learning-accelerator 的差异

| | ai-learning-accelerator | 本方法论 |
|--|-------------------------|----------|
| 目标 | 从零到能干活 | 到能评审、带人、定治理 |
| 调研 | 可选 | **强制**（见 research/） |
| 产出 | 学习路径 | 材料包 + 领域 Skill + 陪跑 |

## 推荐学习节奏（12 周冲刺资深入门）

| 周 | 主题 | 核心材料 |
|----|------|----------|
| 1–2 | 格局与 WorkBuddy 产品 | research-report §1–2 |
| 3–4 | 场景拆解与 JTBD | materials/01, 05 |
| 5–6 | MCP + Skill 编排 | materials/03, 05 |
| 7–8 | 治理与 HITL | materials/04 |
| 9–10 | 竞品与选型 | materials/02, 03 |
| 11–12 | 综合评审演练 | materials/06 + 模拟评审 |
