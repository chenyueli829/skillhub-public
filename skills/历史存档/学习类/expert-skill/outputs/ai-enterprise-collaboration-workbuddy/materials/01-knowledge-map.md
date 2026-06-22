# 01 知识图谱：AI + 企业办公协同

## 核心概念层（资深必掌握）

### 1. Agent 工作台 vs 聊天机器人
- **定义**：以任务闭环为中心，集成规划、工具调用、多步执行、交付物输出
- **WorkBuddy 体现**：自然语言 → 分解 → 并行执行 → 报告/表格/PPT
- **常见误区**：把「能对话」等同于「能交付」

### 2. Skill / Expert / Expert Team
- **Skill**：可复用工作流 + 触发条件 + 领域约束（本仓库即 Skill 范式）
- **Expert**：预置领域角色（方法论 + 模板 + 工具链）
- **Expert Team**：多子 Agent 分工，Lead 协调
- **关系**：Skill 偏「流程契约」，Expert 偏「角色人格」

### 3. MCP（Model Context Protocol）
- **作用**：标准化 Agent ↔ 工具/资源/提示词 的连接
- **企业意义**：避免 N×M 定制集成；治理层可统一审计
- **WorkBuddy**：连接 GitHub、Jira、Notion、Slack、iWiki 等

### 4. 治理三模式
| 模式 | 含义 | 典型场景 |
|------|------|----------|
| HITL | 人批准后才执行 | 对外发布、资金操作 |
| HOTL | 人监控，异常介入 | 内部报告生成 |
| 全自动 | 低风险重复任务 | 格式转换、摘要 |

### 5. 超级个体 vs 超级团队
- **超级个体**：单人 Agent 放大产出
- **超级团队**：组织级共享 Expert、统一身份、审计、知识接入
- **WorkBuddy Enterprise**：明确转向后者

## 概念关联图

```
用户 Job
  → 场景分级（风险/频率/价值）
    → 编排选择（单 Expert / Team / 自定义 Skill）
      → MCP 连接（数据源 + 执行面）
        → 治理层（HITL + 审计 + 权限）
          → 交付物 + 可追溯日志
```

## 与竞品的概念对齐

| 概念 | WorkBuddy | 钉钉悟空 | 飞书 Aily | Copilot Studio |
|------|-----------|----------|-----------|----------------|
| 执行入口 | AI 工作台 | 悟空/钉钉 CLI | Aily/飞书 CLI | Copilot / Power Platform |
| 开放连接 | MCP | 选择性 CLI | 飞书 CLI + OpenClaw | MCP（2026+） |
| 治理叙事 | 人审最终关 | 安全内建底层 | 分层（Aily 可控/OpenClaw 自建） | 租户内强治理 |

## 自测问题（资深层）

1. 什么情况下应该用 Expert Team 而不是单个 Expert？
2. MCP 解决的是集成问题还是推理问题？
3. WorkBuddy Enterprise 的 OneID 解决的是什么类问题？
