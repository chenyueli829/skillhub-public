# 技能评测：taste-skill-main

> 2026-06-22 · 入口 `skills/taste-skill/SKILL.md` · install name `design-taste-frontend` · v2 实验版

## 总结

**Taste Skill = 让 AI 做前端时别像 AI 做的。**

13 个子 skill 的技能包，专治模板感 UI（紫渐变、三等分卡片、Inter 字体）。默认从 brief 推断设计方向，调三个拨盘（版式 / 动效 / 密度），输出落地页、作品集或改版代码；也支持只出设计图。

| 你想… | 用哪个 |
|--------|--------|
| 通用建站（默认） | `taste-skill` |
| 先出图再写代码 | `image-to-code-skill` |
| 改现有项目 | `redesign-skill` |
| 只要设计稿 | `imagegen-frontend-web` 等 |
| 输出被截断 | 叠加 `output-skill` |

中文说明见 `skills/taste-skill/SKILL-zh.md`。

---

## 1. 介绍

面向 AI 编码 Agent 的**反 slop 前端设计**技能包，含 13 个可独立安装的子 skill。

**解决什么问题**：Agent 默认产出千篇一律的「AI 味」界面；本 skill 用设计解读、拨盘参数和硬规则（Pre-Flight Check）约束版式、字体、动效与留白。

**主 skill 流程**：读 brief → Design Read → 设拨盘 → 选设计系统/审美 → React/Next + Tailwind + Motion/GSAP 实现 → 交付前自检。

**主要输出**：前端代码，或设计参考图（imagegen 类）。

**子 skill 速查**：`image-to-code` 图先行；`redesign` 改版审计；`soft` / `minimalist` / `brutalist` 锁定风格；`gpt-taste` 更严格；`stitch` 兼容 Google Stitch。

## 2. 触发条件

**关键词**：Anti-slop、landing page、portfolio、redesign、frontend、GSAP、Tailwind、image-to-code、imagegen

**用户可能说**：
- 「做一个不像 AI 的落地页」「Linear 风格营销站」
- 「先出设计图再写代码」「改版现有网站」
- `build a landing page with taste-skill` / `anti-slop frontend`

**适用**：新建落地页/作品集、视觉改版、要高级动效、只要设计稿、输出被截断需叠加 output-skill

**不适用**：仪表盘、数据表、多步表单、代码编辑器、原生 App

## 3. 提问示例

### 示例 1：新建 SaaS 落地页

> @skills/精选10个Skill/设计/taste-skill-main/skills/taste-skill/SKILL.md 用 Next.js + Tailwind 做 B2B SaaS 落地页，Linear 极简风，含 Hero/功能/定价/FAQ。请先给 Design Read 和拨盘值再写代码。

### 示例 2：图先行流水线

> @skills/精选10个Skill/设计/taste-skill-main/skills/image-to-code-skill/SKILL.md 做高端厨具 DTC 官网，6 个区块。严格按 skill：每 section 一张参考图 → 分析 → 再写代码。

### 示例 3：改版现有项目

> @skills/精选10个Skill/设计/taste-skill-main/skills/redesign-skill/SKILL.md 审计并改版 `./src/app/page.tsx`，保留品牌紫色，不改 URL 和主导航。

### 示例 4：只出设计图

> @skills/精选10个Skill/设计/taste-skill-main/skills/imagegen-frontend-web/SKILL.md 为 AI 写作工具做 8 区块落地页视觉稿，每 section 单独一张横图，冷色 luxury，不要紫蓝光晕。

### 示例 5：防截断输出

> @skills/精选10个Skill/设计/taste-skill-main/skills/taste-skill/SKILL.md @skills/精选10个Skill/设计/taste-skill-main/skills/output-skill/SKILL.md 做设计师作品集单页，VARIANCE=9，完整可运行代码，禁止 TODO 和截断。

## 4. 外部依赖

### 必需（写代码时）

- Node.js + npm
- 目标项目 `package.json`（skill 会检查依赖是否已装）
- 常见包：`react`、`next`、`tailwindcss` v4、`motion`、`gsap`（按 brief 选用）

### 可选（按场景）

| 类型 | 举例 |
|------|------|
| 图生 | Cursor GenerateImage、ChatGPT Images（image-to-code / imagegen 强烈建议有） |
| 占位图 | picsum.photos、simpleicons.org（Logo 墙） |
| 设计系统 | shadcn、Radix、Carbon、Fluent 等（brief 决定，非全装） |
| 安装 CLI | `npx skills add`（装 skill 用，非运行时） |

### 凭证

- 图像 API Key：仅外部图生服务需要
- `SHOPIFY_API_KEY`：仅 Shopify 场景

### 验收前准备

1. 准备好 Node 项目环境
2. 图先行任务需图像生成能力
3. 无图生时 skill 会留占位并提示补图，不会用 div 假截图糊弄
