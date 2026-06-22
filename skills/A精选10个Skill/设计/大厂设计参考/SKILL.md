---
name: big-tech-design-reference
description: >-
  使用 awesome-design-md 大厂设计系统库生成风格一致的 UI。内置 70+ 品牌 DESIGN.md（Linear、Stripe、Apple、Notion 等），
  在用户 @ 本 skill、说「大厂设计参考」「按 XX 风格做页面」「用 DESIGN.md 生成 UI」时使用。
---

# 大厂设计参考（awesome-design-md）

基于 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的 70+ 大厂/知名产品 DESIGN.md 设计系统库。每个品牌包含从真实网站提取的颜色、字体、组件、布局规则，供 AI Agent 生成视觉一致的前端界面。

## 资源路径

```
skills/精选10个Skill/设计/大厂设计参考/awesome-design-md/
├── design-md/{品牌}/DESIGN.md      # 设计系统主文件（Agent 必读）
├── design-md/{品牌}/preview.html   # 浅色预览
├── design-md/{品牌}/preview-dark.html  # 深色预览
└── README.md                       # 完整品牌目录与说明
```

**本 skill 目录**：`skills/精选10个Skill/设计/大厂设计参考/`

## 何时使用

- 用户 @ 本 skill 或说「大厂设计参考」「按 XX 风格做页面」
- 需要模仿 Linear / Stripe / Apple / Notion / Vercel 等已知品牌视觉
- 用户提到 `DESIGN.md`、Google Stitch 设计系统、品牌 UI 复刻
- 落地页、营销站、Dashboard 需要明确设计方向而非通用 AI 模板

## 执行流程

### 1. 选定品牌

按用户指定品牌读取对应 `DESIGN.md`。未指定时，根据产品类型推荐 1–3 个候选并请用户确认。

| 场景 | 推荐品牌 |
|------|----------|
| 开发者工具 / SaaS | `linear.app`、`vercel`、`cursor`、`supabase` |
| 金融科技 | `stripe`、`wise`、`revolut`、`coinbase` |
| 消费科技 / 硬件 | `apple`、`nvidia`、`hp` |
| 协作 / 生产力 | `notion`、`figma`、`airtable`、`miro` |
| AI 平台 | `claude`、`cohere`、`mistral.ai`、`voltagent` |
| 电商 / 零售 | `shopify`、`airbnb`、`nike`、`starbucks` |
| 汽车 / 奢侈 | `tesla`、`bmw`、`ferrari`、`lamborghini` |
| 复古 / 趣味 | `dell-1996`、`nintendo-2001` |

完整列表见 `awesome-design-md/README.md` 或 `awesome-design-md/design-md/` 目录。

### 2. 读取设计系统

**必须完整阅读**目标品牌的 `DESIGN.md`，重点关注：

1. Visual Theme & Atmosphere — 氛围与密度
2. Color Palette & Roles — 语义色 + hex + 用途
3. Typography Rules — 字体层级表
4. Component Stylings — 按钮、卡片、输入框及状态
5. Layout Principles — 间距、网格、留白
6. Do's and Don'ts — 禁止项（必须遵守）
7. Agent Prompt Guide — 可直接引用的 prompt 片段

可选：打开同目录 `preview.html` / `preview-dark.html` 对照色板与组件。

### 3. 应用到项目

**方式 A（推荐）**：在当前任务上下文中直接遵循 DESIGN.md 规则写代码，无需复制文件。

**方式 B**：将 `DESIGN.md` 复制到目标项目根目录，后续所有 UI 工作以该文件为唯一设计真相源。

### 4. 实现约束

- **严格遵循** DESIGN.md 中的颜色 hex、字体、圆角、阴影、间距，不得自行「优化」成通用 AI 风格
- **遵守 Do's and Don'ts**，尤其禁止项（如 Linear 禁止装饰性使用 accent 色）
- 字体 fallback：DESIGN.md 中的专有字体用 Google Fonts 或系统近似字体替代，并在注释中说明映射
- 响应式按 DESIGN.md 的 Responsive Behavior 章节执行
- 交付前对照 `preview.html` 自检色值与组件形态

### 5. 多品牌 / 混搭

默认**只选一个** DESIGN.md。用户明确要求混搭时，以主品牌为准，仅从辅品牌借鉴单一元素（如 Stripe 渐变 CTA），并在回复中说明取舍。

## 品牌目录速查

`design-md/` 下 74 个品牌（文件夹名 = 路径）：

**AI & LLM**：`claude` `cohere` `elevenlabs` `minimax` `mistral.ai` `ollama` `opencode.ai` `replicate` `runwayml` `together.ai` `voltagent` `x.ai`

**开发者工具**：`cursor` `expo` `lovable` `raycast` `superhuman` `vercel` `warp`

**后端 / DevOps**：`clickhouse` `composio` `hashicorp` `mongodb` `posthog` `sanity` `sentry` `supabase`

**SaaS**：`cal` `intercom` `linear.app` `mintlify` `notion` `resend` `zapier`

**设计工具**：`airtable` `clay` `figma` `framer` `miro` `webflow`

**金融科技**：`binance` `coinbase` `kraken` `mastercard` `revolut` `stripe` `wise`

**电商零售**：`airbnb` `meta` `nike` `shopify` `starbucks`

**媒体消费**：`apple` `hp` `ibm` `nvidia` `pinterest` `playstation` `spacex` `spotify` `theverge` `uber` `vodafone` `wired`

**汽车**：`bmw` `bmw-m` `bugatti` `ferrari` `lamborghini` `renault` `tesla`

**复古**：`dell-1996` `nintendo-2001`

**其它**：`slack`

## 提问示例

```
@大厂设计参考 用 Linear 风格做一个项目管理 SaaS 落地页，含 Hero、功能、定价
```

```
@大厂设计参考 参考 Stripe 的设计系统，用 React + Tailwind 做支付 API 文档首页
```

```
@大厂设计参考 我要 Notion 那种温暖极简风，做一个笔记 App 营销页
```

```
@大厂设计参考 对比一下 vercel 和 cursor 的设计差异，推荐哪个更适合 AI 代码编辑器
```

## 更新上游

```bash
cd skills/精选10个Skill/设计/大厂设计参考/awesome-design-md
git pull origin main
```

## 外部依赖

| 类型 | 说明 |
|------|------|
| 必需 | 无运行时依赖；DESIGN.md 为纯 Markdown |
| 写代码时 | 按目标项目技术栈（React/Vue/HTML 等） |
| 可选 | Google Fonts 或本地字体以实现 DESIGN.md 字体栈 |
| 参考 | [Google Stitch DESIGN.md 规范](https://stitch.withgoogle.com/docs/design-md/overview/) |

## 许可

上游仓库 MIT License。DESIGN.md 从公开网站提取的设计 token 仅供 AI 生成 UI 参考，不主张任何品牌视觉识别所有权。
