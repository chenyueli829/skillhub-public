---
name: design-taste-frontend
description: 面向落地页、作品集与改版的前端反套路（Anti-Slop）技能。Agent 阅读需求简报、推断正确设计方向，交付不显模板化的界面。适用时采用真实设计系统，改版优先审计，严格执行起飞前检查。
---

# tasteskill：反套路前端技能（Anti-Slop Frontend Skill）

> 落地页、作品集、改版。不是仪表盘，不是数据表，不是多步骤产品 UI。
> 下文每条规则都是**情境化的**。没有一条会自动触发。先读简报，再只取用契合的部分。

---

## 0. 简报推断（动手前先读懂场景）

在碰代码或调旋钮之前，**推断用户真正想要什么**。多数 LLM 设计产出糟糕，是因为模型跳到默认美学，而不是读懂场景。

### 0.A 先读这些信号
1. **页面类型** - 落地页（SaaS / 消费 / 代理 / 活动）、作品集（开发 / 设计师 / 创意工作室）、改版（保留 vs 大改）、编辑 / 博客。
2. 用户使用的**氛围词** - "minimalist"、"calm"、"Linear-style"、"Awwwards"、"brutalist"、"premium consumer"、"Apple-y"、"playful"、"serious B2B"、"editorial"、"agency-y"、"glassy"、"dark tech"。
3. **参考信号** - 他们贴的 URL、截图、点名的产品、对标的品牌。
4. **受众** - B2B 采购评审团 vs 有设计意识的消费者 vs 扫作品集招聘方。受众决定美学，不是你的个人品味。
5. **已有品牌资产** - logo、颜色、字体、摄影。改版时，这些是起点材料，不是可选输入（见第 11 节）。
6. **隐性约束** - 无障碍优先受众、公共部门、受监管行业、信任优先电商、儿童产品。这些约束**覆盖**美学偏好。

### 0.B 生成前先输出一行「设计解读」（Design Read）
在写任何代码之前，用一行说明：**「解读为：面向 \<受众> 的 \<页面类型>，采用 \<氛围> 语言，倾向 \<设计系统或美学家族>。」**

解读示例：
- *「解读为：面向技术买家的 B2B SaaS 落地页，采用 Linear 式极简语言，倾向 Tailwind 工具类 + Geist + 克制动效。」*
- *「解读为：面向招聘经理的独立设计师作品集，采用编辑 / 动感字体语言，倾向原生 CSS + 滚动驱动动画 + 定制字体。」*
- *「解读为：公共部门服务站点改版，采用信任优先语言，倾向 GOV.UK Frontend 或 USWDS。」*

### 0.C 简报模糊时，只问一个问题，不要猜
仅在设计解读确实分歧时，**恰好问一个**澄清问题——不要连环提问。示例：*「这更应该接近 Linear 式干净，还是 Awwwards 式实验？」*

若能从上下文自信推断，**不要问**。直接声明设计解读并继续。

### 0.D 反默认纪律（Anti-Default Discipline）
不要默认：AI 紫渐变、深色网格上的居中 Hero、三张等宽功能卡、到处泛用玻璃拟态、处处无限循环微动效、Inter + slate-900。这些是 LLM 默认。根据设计解读刻意越过它们。

---

## 1. 三个旋钮（核心配置）

设计解读之后，设定三个旋钮。下文布局、动效、密度决策都由它们门控。

* **`DESIGN_VARIANCE: 8`** - 1 = 完美对称，10 = 艺术混沌
* **`MOTION_INTENSITY: 6`** - 1 = 静态，10 = 电影感 / 物理感
* **`VISUAL_DENSITY: 4`** - 1 = 画廊 / 透气，10 = 驾驶舱 / 信息密集

**基线：** `8 / 6 / 4`。除非设计解读覆盖，否则使用这些值。不要要求用户改本文件——覆盖在对话中完成。

### 1.A 旋钮推断（设计解读 → 旋钮值）
| 信号 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B 用例预设
| 用例 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

### 1.C 旋钮如何驱动产出
将这些（或用户覆盖值）作为全局变量。全文交叉引用使用这些确切变量名——不要发明 `LAYOUT_VARIANCE` 或 `ANIM_LEVEL` 之类别名。

---

## 2. 简报 → 设计系统映射

有了设计解读（第 0 节）和旋钮（第 1 节）后，选对基础。有官方包的事不要手写 CSS。不要把美学趋势假装成官方系统。

### 2.A 何时采用真实设计系统（使用官方包）
| 简报解读为… | 选用 | 原因 |
|---|---|---|
| Microsoft / 企业 SaaS / 仪表盘 | `@fluentui/react-components` 或 `@fluentui/web-components` | 官方 Fluent UI，Microsoft token，无障碍已做好 |
| Google 风 UI、Material 味产品 | `@material/web` + Material 3 tokens | 官方，可通过 Material Theming 主题化 |
| IBM 风 B2B / 企业分析 | `@carbon/react` + `@carbon/styles` | 官方 Carbon，成熟数据密度模式 |
| Shopify 应用界面 | `polaris.js` web components / Polaris React | Shopify 管理后台 UI 必需 |
| Atlassian / Jira 风产品 | `@atlaskit/*` + `@atlaskit/tokens` | 官方 Atlassian DS |
| GitHub 风开发工具 / 社区页 | `@primer/css` 或 `@primer/react-brand` | 官方 Primer；营销用 Brand 变体 |
| 英国公共服务 | `govuk-frontend` | 法律 / 监管预期 |
| 美国公共部门 / 信任优先 | `uswds` | 同上 |
| 快速本地商户 / 代理 MVP | Bootstrap 5.3 | 朴实、快、能用 |
| 现代无障碍 React 基础 | `@radix-ui/themes` | 原语 + 打磨主题 |
| 自管组件的现代 SaaS | shadcn/ui (`npx shadcn@latest add ...`) | 代码归你，易定制；绝不交付默认态 |
| Tailwind 现代 SaaS / AI 营销 | Tailwind v4 utilities + `dark:` variant | 独立开发者与小团队默认 |

**诚实规则：** 若简报解读为上述系统之一，安装并使用**官方**包。不要手写复刻其 CSS。不要只导入系统 token 又覆盖 90%。

**每项目一个系统。** 不要在同一棵树混 Fluent React 与 Carbon。不要把 shadcn/ui 组件导入 Material 3 应用。

### 2.B 简报是美学而非系统时
这些方向**没有单一官方包**。用原生 CSS + Tailwind + 维护良好的组件库构建。在代码注释中诚实说明哪些是借鉴灵感、哪些是官方材料。

| 美学 | 诚实实现 |
|---|---|
| Glassmorphism / "frosted glass" | `backdrop-filter`、分层边框、高光叠加。为 `prefers-reduced-transparency` 提供实色填充回退。 |
| Bento（Apple 式瓦片网格） | CSS Grid 混合单元尺寸。无单一库独占。 |
| Brutalism | 原生 CSS、等宽字体、粗边框。无库。 |
| Editorial / magazine | 衬线字体、不对称网格、大量留白。无库。 |
| Dark tech / hacker | 等宽 + 霓虹强调、终端母题。无库。 |
| Aurora / mesh gradients | SVG 或分层径向渐变。无库。 |
| Kinetic typography | 原生 CSS 动画、滚动驱动动画、劫持用 GSAP。无库。 |
| **Apple Liquid Glass** | Apple 仅面向 Apple 平台文档化。**没有官方 `liquid-glass.css`。** Web 实现是用 `backdrop-filter` + 分层边框 + 高光的近似。明确标注为近似。 |

---

## 3. 默认架构与约定

除非设计解读选了真实设计系统（第 2.A 节），以下为默认：

### 3.A 技术栈
* **框架：** React 或 Next.js。默认 Server Components（RSC）。
  * **RSC 安全：** 全局状态**仅**在 Client Components 中有效。Next.js 中，在 `"use client"` 组件里包裹 providers。
  * **交互隔离：** 使用 Motion、滚动监听或指针物理的组件**必须**是独立叶子节点，顶部 `'use client'`。Server Components 只渲染静态布局。
* **样式：** **Tailwind v4**（默认）。仅当现有项目要求时用 v3。
  * v4：不要在 `postcss.config.js` 用 `tailwindcss` 插件。用 `@tailwindcss/postcss` 或 Vite 插件。
* **动画：** **Motion**（原 Framer Motion）。从 `motion/react` 导入（`import { motion } from "motion/react"`）。`framer-motion` 仍可作为遗留别名——新代码优先 `motion/react`。
* **字体：** 始终用 `next/font`（Next.js）或 `@font-face` 自托管 + `font-display: swap`。生产环境不要用 `<link>` 链 Google Fonts。

### 3.B 状态
* 局部 UI 用 `useState` / `useReducer`。
* 全局状态**仅**为避免深层 prop 钻取——Zustand、Jotai 或 React context。
* **绝不**用 `useState` 跟踪用户输入驱动的连续值（鼠标位置、滚动进度、指针物理、磁性悬停）。用 Motion 的 `useMotionValue` / `useTransform` / `useScroll`。`useState` 每次变化重渲染整棵 React 树，移动端会崩。

### 3.C 图标
* **允许库（优先级）：** `@phosphor-icons/react`、`hugeicons-react`、`@radix-ui/react-icons`、`@tabler/icons-react`。
* **不推荐：** `lucide-react`。仅当用户明确要求或项目已依赖时可接受。
* **绝不手写 SVG 图标。** 缺字形就装第二库或组合原语——不要从零画路径。
* **每项目一个图标族。** 不要在同一组件树混 Phosphor 与 Lucide。
* **全局统一 `strokeWidth`**（如 `1.5` 或 `2.0`）。

### 3.D Emoji 政策
默认在代码、标记、可见文本中不推荐。用图标库字形替代符号。**例外：** 仅当用户明确要求 playful / chat-style / social-native 氛围——即便如此也要有意、克制使用。

### 3.E 响应式与布局机制
* 统一断点（`sm 640`、`md 768`、`lg 1024`、`xl 1280`、`2xl 1536`）。
* 页面布局用 `max-w-[1400px] mx-auto` 或 `max-w-7xl` 约束。
* **视口稳定：** Hero 全高**绝不**用 `h-screen`。**始终**用 `min-h-[100dvh]`，避免移动端（iOS Safari 地址栏）布局跳动。
* **Grid 优于 Flex 算式：** **绝不**用复杂 flex 百分比（`w-[calc(33%-1rem)]`）。**始终**用 CSS Grid（`grid grid-cols-1 md:grid-cols-3 gap-6`）。

### 3.F 依赖校验（强制）
导入任何第三方库前，检查 `package.json`。缺包则先输出安装命令。**绝不**假设库已存在。

---

## 4. 设计工程指令（偏差校正）

LLM 默认走向陈词滥调。主动覆盖这些默认。每条规则都有情境化覆盖路径。

### 4.1 字体排印
* **展示 / 标题：** 默认 `text-4xl md:text-6xl tracking-tighter leading-none`。
* **正文 / 段落：** 默认 `text-base text-gray-600 leading-relaxed max-w-[65ch]`。
* **无衬线选择：**
  * **默认不推荐：** `Inter`。优先 `Geist`、`Outfit`、`Cabinet Grotesk`、`Satoshi` 或品牌合适的衬线。
  * **覆盖：** 用户明确要求中性 / 标准 / Linear 风，或简报为公共部门 / 无障碍优先时，Inter 可接受。
* **已知配对：** `Geist` + `Geist Mono`、`Satoshi` + `JetBrains Mono`、`Cabinet Grotesk` + `Inter Tight`、`GT America` + `IBM Plex Mono`。

* **衬线纪律（默认强烈不推荐）：**
  * 衬线**极不推荐作为任何项目的默认字体。**「感觉创意 / 高级 / 编辑感」不是上衬线的理由。Agent 默认「创意简报 = 衬线」是生产测试中最常见的 AI 痕迹。
  * **衬线仅当以下之一明确成立时可接受：**
    - 品牌简报字面点名衬线字体，或
    - 美学家族确为 editorial / luxury / publication / manuscript / heritage / vintage，且能说明**为何该衬线契合该品牌**
  * 其余（创意代理、设计工作室、现代品牌、高端消费、作品集、生活方式），**默认无衬线展示字体**（Geist Display、ABC Diatype、Söhne Breit、Cabinet Grotesk Display、Migra Sans、GT Walsheim、Inter Display、PP Neue Montreal）。无衬线展示并不「无聊」——与时尚里黑色是默认同理。
  * **强调规则（相关）：** 标题内强调某词（动感「and `spatial` design」式），用**同字族的斜体或粗体**。不要为了趣味在 sans 标题里塞随机衬线词（反之亦然）。混族强调是业余。同族斜体/粗体才是正解。
  * **明确禁止作为默认：** `Fraunces` 与 `Instrument_Serif`（两个 LLM 最爱展示衬线）。
  * **若衬线有理有据**（罕见，见上），从此池轮换，**不要**连续项目复用同一衬线：PP Editorial New、GT Sectra Display、Cardinal Grotesque、Reckless Neue、Tiempos Headline、Recoleta、Cormorant Garamond、Playfair Display、EB Garamond、IvyPresto、Migra、Editorial Old、Saol Display、Söhne Breit Kursiv、Domaine Display、Canela、Schnyder、Tobias、NB Architekt、ITC Galliard。

* **斜体下伸部留白（强制）：** 展示字号用斜体且含下伸字母（`y g j p q`）时，`leading-[1]` 或 `leading-none` 会裁切下伸部。至少 `leading-[1.1]`，包裹元素加 `pb-1` 或 `mb-1` 预留。发货前审计每个展示标题中的斜体词。

### 4.2 色彩校准
* 最多 1 个强调色。默认饱和度 < 80%。
* **LILA 规则：** 默认不推荐「AI 紫 / 蓝发光」美学。不要自动紫按钮光晕、随机霓虹渐变。用中性底（Zinc / Slate / Stone）+ 高对比单一强调（Emerald、Electric Blue、Deep Rose、Burnt Orange 等）。
* **覆盖：** 品牌或简报明确要求紫 / 紫罗兰 / lila 时，大胆用。但有意执行：一致色板、协调中性色、克制渐变。不是泛用 AI 渐变 slop。
* **每项目一套色板。** 同一项目不要在暖灰与冷灰间摇摆。
* **色彩一致性锁定（强制）：** 页面选定强调色后，**整页**统一使用。暖灰站不会在第七区块突然蓝 CTA。玫瑰强调站不会在页脚突然青绿状态徽章。选一个强调色，锁定，发货前审计每个组件。

* **高端消费色板禁令（强制，第二大 recurring AI 痕迹）：**
  * 高端消费简报（厨具、 wellness、手工艺、奢侈品、传承工艺、DTC 家居等）时，LLM 默认是**暖米/奶油 + 黄铜/陶土/酒红/赭石 + 浓缩咖啡/墨色深字**。具体禁止作为默认背景与强调的 hex 族：
    - 背景：`#f5f1ea`、`#f7f5f1`、`#fbf8f1`、`#efeae0`、`#ece6db`、`#faf7f1`、`#e8dfcb`（皆「暖纸 / 奶油 / 粉笔 / 骨色」）
    - 强调：`#b08947`、`#b6553a`、`#9a2436`、`#9c6e2a`、`#bc7c3a`、`#7d5621`（皆「黄铜 / 陶土 / 酒红 / 赭石」）
    - 文字：`#1a1714`、`#1a1814`、`#1b1814`（皆「浓缩咖啡 / 暖近黑」）
  * 此色板**禁止**作为高端消费简报默认选择。你做过的高端消费站几乎都用这一套。品牌会消失。
  * **默认替代（轮换，勿复用）：**
    - **冷奢（Cold Luxury）：** 银灰 + 铬 + 烟（如 Tesla、Apple Watch Hermès 无皮革感）
    - **森林（Forest）：** 深绿 + 骨色 + 琥珀强调（如 Filson、Patagonia premium）
    - **黑与棕（Black and Tan）：** 真 off-black + 暖棕，强对比，无米色
    - **钴蓝 + 奶油（Cobalt + Cream）：** 饱和蓝对单一中性，无黄铜
    - **陶土 + 石板（Terracotta + Slate）：** 暖锈对冷灰，无黄铜
    - **橄榄 + 砖红 + 纸（Olive + Brick + Paper）：**  muted 橄榄 + 砖红强调
    - **纯单色 + 单一饱和点缀：** off-white + off-black + 一个亮色（电蓝、翡翠、热粉等）
  * **色板轮换规则：** 若上一高端消费项目用了米+黄铜族，本项目**必须**换族。不要连续两次暖工艺色板。
  * **覆盖：** 仅当品牌简报明确点名这些色，或品牌身份确为 vintage / artisan / warm-craft 且能说明**为何此色板契合此品牌**时，米+黄铜+浓缩咖啡可接受。因「这是厨具简报」就默认伸手，禁止。

### 4.3 布局多样化
* **反居中偏见：** `DESIGN_VARIANCE > 4` 时避免居中 Hero / H1。强制「分屏」（50/50）、「左内容右素材」、「不对称留白」或滚动钉住结构。
* **覆盖：** 编辑 / 宣言 / 发布宣告类简报，信息即设计时，居中 hero 可接受。

### 4.4 材质、阴影、卡片
* **仅**当 elevation 表达真实层级时用卡片。否则用 `border-t`、`divide-y` 或负空间分组。
* 用阴影时，向背景色相染色。浅色背景不要纯黑 drop shadow。
* `VISUAL_DENSITY > 7`：禁止泛用卡片容器。数据指标在朴素布局中呼吸。
* **形状一致性锁定（强制）：** 整页选**一套**圆角尺度并坚持。选项：全锐角（radius 0）、全软（12-16px）、全药丸（交互元素 full radius）。混用系统仅当有文档化规则（如「按钮全药丸、卡片 16px、输入 8px」）且处处遵守。圆按钮配方布局，或方卡片配药丸按钮页，都是坏设计。

### 4.5 交互 UI 状态
LLM 默认只做「静态成功态」。始终实现完整周期：
* **加载：** 骨架屏匹配最终布局形状。避免泛用圆形 spinner。
* **空状态：** 构图精美；说明如何填充。
* **错误：** 表单内联清晰，或情境化（toast 仅用于瞬态）。
* **触感反馈：** `:active` 用 `-translate-y-[1px]` 或 `scale-[0.98]` 模拟物理按压。
* **按钮对比检查（强制，a11y）：** 任何按钮发货前验证文字相对背景可读。白按钮+白字、`bg-white` CTA + `text-white`、透明按钮无描边贴在页面背景上，皆禁止。审计每个 CTA：对比度 WCAG AA 最低（正文 4.5:1，大号字 18px+ 3:1）。幽灵按钮在摄影背景上同理（用 backdrop、遮罩或描边）。
* **CTA 换行禁令（强制）：** 桌面端按钮文字**必须**单行。如 "VIEW SELECTED WORK" 折成 2-3 行，按钮即坏。修复：**要么**缩短文案（主 CTA 最多 3 词，理想 1-2）**要么**加宽按钮（不要人为 `max-width` 限制 CTA）。桌面 CTA 换行 = 起飞前失败。
* **禁止重复 CTA 意图（强制）：** 一页两个同意图 CTA = 起飞前失败。同意图示例："Get in touch" + "Contact us" + "Let's talk" + "Start a project" + "Start something" + "Reach out" = 皆「联系」→ 全页**一个**文案（nav、hero、footer）。同理 "Try free" + "Get started" + "Sign up free"（注册）、"View work" + "See selected work" + "Browse projects"（作品集）。一意图一文案。
* **表单对比检查（强制，a11y）：** 输入、placeholder、焦点环、辅助文、错误文相对区块背景均过 WCAG AA。近白表单浅 placeholder、白表单在白区块、标签灰度不足 4.5:1，皆禁止。发货前审计每个表单。

### 4.6 数据与表单模式
* 标签在输入**上方**。辅助文可选但标记里要有。错误文在输入**下方**。输入块标准 `gap-2`。
* 绝不用 placeholder 当标签。

### 4.7 布局纪律（硬规则。违反任一条即交付坏作品）

* **Hero 必须落在首屏视口内。** 桌面标题最多 2 行，副文最多 **20 词**且最多 3-4 行，CTA 无需滚动可见。文案过长：缩小字号**或**删文案。20 词副文说不清价值主张，是价值主张不清，不是规则太紧。绝不让 hero 溢出迫使用户滚动找 CTA。
* **Hero 字号纪律。** 字号与图片尺寸**一起**规划。Hero 素材大且标题超 6 词时，不要从 `text-7xl/text-8xl` 起。多数 hero 合理范围：`text-4xl md:text-5xl lg:text-6xl`；仅标题 3-5 词时用 `text-6xl md:text-7xl`。4 行 hero 标题永远是字号错误，不是文案长度错误。
* **HERO 顶部内边距上限（强制）：** 桌面 hero 顶部 padding 最多 `pt-24`（≈6rem）。再大则内容漂在视口中段，像布局 bug 而非有意留白。需要呼吸感就加大字号或素材，不要加 top padding。
* **HERO 栈纪律（最多 4 个文本元素）。** Hero 是单一瞬间，不是功能列表。允许文本元素合计最多 4 个：
  1. Eyebrow（小写全大标签）或品牌条或皆无——零或选一
  2. 标题（最多 2 行，见上）
  3. 副文（最多 20 词，最多 4 行）
  4. CTA（1 主 + 最多 1 次）
  - **Hero 禁止：** CTA 下小标语（"Works with GitHub, GitLab, and self-hosted Git"）、信任微条（"Used by engineering teams at..."）、定价 teaser（"Free for solo, $10/user for teams"）、功能 bullet、社交证明头像行。这些移到 hero 正下方独立区块。
  - 若 eyebrow 与 CTA 下标语同在 hero，删标语。若品牌条与标语同在，删标语。每 hero 最多一个小文本元素。
* **「Used by」/「Trusted by」logo 墙在 hero 下方，不在 hero 内。** Hero 放价值主张与主 CTA。Logo 墙是紧接其下的独立区块。不要把信任 logo 塞进 hero 文案同一 flex 行。
* **桌面导航必须单行。** `lg`（1024px）放不下则压缩标签、删次要项或汉堡菜单。桌面两行 nav 是坏设计。
* **导航高度上限：桌面最多 80px，默认 64-72px。** 不要巨大「代理」nav 吃掉 15% 视口。
* **Bento 网格要有节奏，不要单侧重复。** 不要堆 6 行左图右文。变化构图：交替全宽功能行、不对称瓦片、垂直断点。
* **BENTO 单元数规则（强制）：** Bento 单元数**恰好**等于内容项数。3 项 → 3 格（1+2、2+1 或不对称 trio）。5 项 → 5 格（2+3、3+2、hero+4 等）。网格中间或末尾有空格，是规划错误。重塑网格；不要贴空白瓦片。
* **区块布局重复禁令。** 某布局族用于一节后（如三列图卡、全宽引用、图文分屏），该族全页**最多出现一次**。「Selected commissions」不能长得像「What we do」。8 节落地页至少 4 种不同布局族。
* **Z 字交替上限（强制）。** 交替「左图右文」「左文右图」= 平庸。此图文分屏模式连续最多 2 节。第 3 个连续图文分屏 = 起飞前失败。用全宽节、垂直栈、bento、marquee 或其它布局族打破。
* **EYEBROW 克制（强制，生产测试违反 #1）。** 「Eyebrow」是节标题上方小写全大宽字距标签（如 `FOUR COLORWAYS`、`SELECTED WORK`）。典型 CSS：`text-[11px] uppercase tracking-[0.18em]`、`font-mono text-[10.5px] uppercase tracking-[0.22em]`。AI 站常在**每个**节标题上放 eyebrow，节奏模板化。硬规则：
  - **每 3 节最多 1 个 eyebrow。** Hero 计 1。9 节页最多 3 个 eyebrow。
  - A 节有 eyebrow，接下来 2 节不能有。
  - **起飞前检查可机械执行：** 统计所有节组件中标题上方的 `uppercase tracking`（或类似 small-caps mono 标签）。若数量 > ceil(sectionCount / 3)，产出失败。
  - **替代 eyebrow：** 直接删掉。仅标题就够。需分类时，页面位置已分类；不必标签。
* **分栏标题禁令（强制）。** 默认禁止「左大标题 + 右小说明段」作节头（左 col-span-7/8，右 col-span-4/5 漂浮小段）。节应**一条**聚焦信息。确需标题+说明段时，垂直堆叠（标题上、正文下，max-width 65ch）。仅当有真实构图理由（如右栏是视觉/交互元素，非填充文）才用分栏标题。
* **Bento 背景多样性（强制）。** Bento 与功能网格不能是 6 张白底白卡纯文字。任意多格网格至少 2-3 格需真实视觉变化：真实图、品牌合适渐变（非 AI 紫）、图案、着色背景。奶油底奶油 bento 仅排版，即使页面其它部分好，也像无聊 AI 默认。
* **移动端折叠每节显式声明。** 每个多列布局，在同一组件声明 `< 768px` 回退。不要「应该行，Tailwind 会处理」。

### 4.8 图像与视觉资产策略

落地页与作品集是**视觉产品**。纯文字页加假截图 div 是 slop。

**视觉资产优先级：**
1. **优先生图工具。** 环境中有任何生图工具（`generate_image`、MCP 生图、IDE 集成、OpenAI 生图等）**必须**用它做节级资产：hero 摄影、产品图、纹理背景、情绪图。按节宽高比生成。不要因手写 CSS 更快而跳过。
2. **其次真实网络图。** 无生图工具时用真实摄影源。可接受默认：
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` 占位摄影（seed 描述节，如 `marrow-cookware-kitchen`）
   * 简报提供的真实库存或品牌 URL
   * 明确允许时用开放许可源（Unsplash 直链、Pexels）
3. **最后告知用户。** 若皆不可，**不要**用手写 SVG 插画或 div 假截图填满页面。留清晰标注占位（`<!-- TODO: hero product photo, 1600x1200 -->`），回复末尾说：*「本页需在以下位置提供真实图片：\[位置列表\]。请生成或提供。」*

**极简站也需要真实图。** 纯文字页不是极简，是未完成。即使 Linear 风编辑站也至少 2-3 张真实图（hero、一张产品/生活、一张辅助）。简报克制可生成 B&W 极简摄影；不要因旋钮低而完全跳过图。

**社交证明用真实公司 logo。** 简报要「Trusted by / Used by / Customers」logo 墙时，**不要**默认纯文字 wordmark（`<span>Acme Co</span>` 排一行）。用真实 SVG logo：
* **来源：Simple Icons**（`https://cdn.simpleicons.org/{slug}/ffffff` 任意色，或 `simple-icons` npm）。覆盖多数知名品牌。
* **替代：devicon** 技术栈 logo（`@svgr/cli` 或 CDN）。
* **编造品牌名？也编造 SVG 标。** 生成简单字母标（圆内一字、双字连字、抽象 glyph）作 inline `<svg>`，匹配页面风格。编造品牌名的纯文字 wordmark 很泛。
* **始终**确保 logo 在明暗模式皆可渲染（深底白、浅底黑，或单色主题变量）。
* **仅 LOGO 规则（强制）：** logo 墙 = 只有 logo。不要在每个 logo 下印行业/类别标签（不要 `Vercel` + `hosting`、`Stripe` + `payments`、`Cloudflare` + `infra`）。Logo 即可信度，标签无增量信息。可选：品牌名作屏幕阅读器 alt；可选链到品牌站。仅此而已。

**手写插画：**
* 库中 SVG 图标：可以（见 3.C）。
* 手写装饰 SVG（定制插画、logo、标记）：**强烈不推荐**，绝不当默认。仅当：
  - 简报明确要求（「画个 SVG logo」）
  - 单一简单几何标（方、圆、展示字体 wordmark）
  - 对产出质量有信心

**禁止 div 假截图。** 用 `<div>` 矩形手搭「产品预览」、假任务列表、假仪表盘、假终端窗口是 Tell。要展示产品：
* 用真实截图 URL（若有）
* 用生图工具生成
* 用真实组件预览（页内 UI 迷你版）
* 或跳过预览，用编辑摄影

**Hero 需要真实视觉。** 文字 + 渐变 blob 不是 hero，是占位。

### 4.9 内容密度

落地页靠**第一印象**，不靠全文阅读。无情删减。

* **每节默认内容形态：** 短标题（≤ 8 词）+ 短段（≤ 25 词）+ 一个视觉资产**或**一个 CTA。更多须由节职责 justify。
* **禁止数据倾倒节。** 营销页上 20 行出版表、30 行奖项表、巨大定价矩阵 = 错误布局。用：
  - Top 3-5 亮点 + 「View full list」链接
  - Marquee / 轮播展示广度
  - 数据即产品时换整页
* **长列表要用对 UI 组件，不是更长列表。** 默认 `<ul>` bullet / `divide-y` 行是懒选择。> 5 项时考虑：
  - 两列分组
  - 带图+标签的卡片网格
  - 可分类时用 Tabs / accordion
  - 横向 scroll-snap pills
  - 广度型列表用轮播（证言、logo、能力）
  - 「大量不需单独关注之物」用 Marquee
  10 行规格表 + 每行发丝线是最差默认。要么分成 2-3 块稀疏分隔，要么改为每规格一卡。
* **规格表特别（Marrow 厨具模式）。** 长产品规格表每行 `border-b` 是厨具/硬件/服装/手工艺简报的 AI 默认。**禁止。** 具体替代：
  - **两列卡片网格：** 每规格一卡：名、值（大号数字）、一行「为何重要」。桌面 2 列，移动 1 列。
  - **横向 scroll-snap pills：** 每规格一 pill，用户滑动浏览。
  - **分组块：** 10 规格分 3 逻辑簇（如「材料」「烹饪」「保修」），每簇一条软分隔 + 簇标题。
  - **重点 vs 其余：** 3-4 个 hero 规格大图块，其余折叠在「View full specifications」下。

* **文案自审（发货前强制）：** 宣布完成前，重读页上每条可见字符串（标题、副标题、eyebrow、按钮、正文、说明、alt、页脚、错误信息）。标记：
  - **语法破碎**（"free on its past"、"two plans but one is honest"、脱离语境的 "to put it on the table"）
  - **指代不清**（"we plan to stay that way" 无前置语境）
  - **像 AI 幻觉**（可爱但错的文字游戏、不跟进的隐喻、"elegant nothing" 短语）
  - **像 LLM 装深沉**（被动攻击式谦逊、假工匠标签、 mock 诗意微元）
  重写每条标记串。不确定是否通顺，换成朴素功能句。AI 可爱文案比无聊文案更糟。
* **假精确数字要标记。** 如 `92%`、`4.1×`、`48k`、`5.8 mm`、`13.4 lb` 要么：
  - 来自真实数据（简报、品牌指南、公开指标）——可以
  - 明确标为 mock（`<!-- mock -->`、"example"、"sample data"）——可以
  - AI 发明的规格美学——禁止。不要假工程精度品牌未声称的。
* **每页一套文案语域。** 不要在同一构图混技术 mono（"47 tasks · 0.6 ctx-switches/day"）、编辑散文、营销 punch，除非品牌声线明确要求。

### 4.10 引用与证言

* 引用正文**最多 3 行**。绝不 6 行。原文更长就裁。落地页引用是片段，不是全文评论。
* 极小字号（如页脚式证言）行数可略松。精神：「一眼能看完」。
* 引用正文内**不要**用 em dash 作设计点缀（长停顿、动感 em dash、em dash bullet）。见 9.G——em dash 完全禁止。
* 署名：姓名 + 职位 +（可选）公司。不要仅姓名（"- Sarah"）。
* 引号：用真正排版引号（ " " ）或不用。不用直 ASCII（ " ）。

### 4.11 页面主题锁定（明 / 暗模式一致性）

页面**一个**主题。区块不反转。

* 暗色页则**全页**暗色。不要在暗区块间夹亮色暖纸区块（反之亦然）。用户滚动中不应感觉进了另一个站。
* 例外：简报明确要求「色块叙事」或「滚动换主题」装置，且是**有意**构图（一次完整主题切换+强过渡，非随机交替），每页允许一次。
* 默认：页面级选 light、dark 或 auto（`prefers-color-scheme`）并锁定。同主题族内区块背景 tint 可以（`bg-zinc-950` 旁 `bg-zinc-900`）；`bg-zinc-950` 页中间跳到 `bg-amber-50` 是坏的。
* 用内置主题的 DS（Radix Themes、带 `<Theme>` 的 shadcn/ui）时，在 `layout.tsx` 或页面根**设一次**主题。不要让单节覆盖。

---

## 5. 情境化主动性

这些是工具，不是默认。设计解读需要时才用。**无一自动触发。**

* **Liquid Glass / Glassmorphism：** 适合高端消费、Apple 邻近、奢侈品牌、媒体叠加氛围。不适合仪表盘、公共部门、「无聊 B2B」。使用时超越 `backdrop-blur`：加 1px 内边框（`border-white/10`）与 subtle 内阴影（`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`）模拟物理边缘折射。在 `prefers-reduced-transparency` 下提供实色回退。
* **磁性微物理（Magnetic Micro-physics）：** `MOTION_INTENSITY > 5` 且简报偏 premium / playful / agency 时用。**仅**用 Motion 的 `useMotionValue` / `useTransform`，在 React 渲染周期外。绝不用 `useState`。见 3.B。
* **永续微交互**（Pulse、Typewriter、Float、Shimmer、Carousel）：`MOTION_INTENSITY > 5` 且该节确实受益于动效（状态指示、实时流、AI 感）时用。**不是每张卡都要无限循环。** 信息节就静止。用 Spring Physics（`type: "spring", stiffness: 100, damping: 20`）——不要 linear easing。
* **「声称有动效，就要看到动效。」** `MOTION_INTENSITY > 4` 时页面必须真的动：hero 入场、关键节滚动显现、CTA 悬停物理，至少这些。声称 `MOTION_INTENSITY: 7` 的静态页是坏的。反之，范围内做不出可靠动效，把旋钮降到 3，交静态干净页。不要半吊子动效（ScrollTrigger 截断、入场跳动、缺清理）。
* **动效必须有动机（强制）。** 加任何动画前问：「这动画传达什么？」有效答案：层级（引到正确元素）、叙事（按故事顺序揭示）、反馈（确认用户操作）、状态过渡（表明变化）。无效：「看起来酷」。有 GSAP 就到处 GSAP 是业余。每个 ScrollTrigger、marquee、钉住节都要理由。一句话说不清就删动画。
* **MARQUEE 每页最多一个（强制）。** 横向滚动文字 marquee（「logo 无尽滚动」「宣言横滚」「动感词带」）每页**最多一次**。同页两个以上像懒填充。选真正服务内容的节用 marquee；其它换布局。
* **GSAP Sticky-Stack 模式（用滚动栈时）。** 「滚动卡片栈」必须是**真** sticky-stack，不是顺序揭示列表。见 5.A 规范骨架。常见失败：触发在滚动中途而非视口顶钉住。修复：`start: "top top"` 而非 `start: "top center"` 或 `"top 80%"`。
* **GSAP Horizontal-Pan 模式（用横向滚动劫持时）。** 见 5.B 规范骨架。常见失败：节钉住前动画已开始，用户看到半张 slide。同样修复：`start: "top top"`，钉住 wrapper，scrub 内轨。

### 5.A Sticky-Stack - 规范骨架

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

要点：`start: "top top"`、`pin: true`、除最后一张外每张都 pin，scale/opacity 由**下一张**的 scroll trigger 驱动（前一张在下一张到达时缩小）。

### 5.B Horizontal-Pan - 规范骨架

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${distance}`,                    // scroll distance = track width minus viewport
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

要点：`start: "top top"`、`pin: true`、`end: "+=${distance}"`（滚动长度 = 所需横向位移）、`scrub: 1`。wrapper 钉住，内轨随纵向滚动横向滑动。

### 5.C Scroll-Reveal Stagger - 规范骨架（更轻替代）

简单「进入视口时出现」（无 pin），优先 Motion `whileInView` 而非 GSAP——更轻，无需 ScrollTrigger：

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

用于：功能列表、证言网格、logo 墙，只需「滚动进入」。真 pin/scrub 工作留给 GSAP。

### 5.D 禁止的动画模式

* **`window.addEventListener("scroll", ...)` 禁止。** 每帧滚动都跑，易卡顿，无批处理。用 Motion `useScroll()`、GSAP `ScrollTrigger`、`IntersectionObserver` 或 CSS `scroll-driven animations`（`animation-timeline: view()`）。
* **用 `window.scrollY` 在 React state 里算滚动进度。** 同理。每帧重渲染。
* **碰 React state 的 `requestAnimationFrame` 循环。** 用 motion values（`useMotionValue` + `useTransform`）。
* **布局过渡：** 可见状态变化（列表重排、模态展开、路由间共享元素）用 Motion `layout` 与 `layoutId`。不要为「安全」给静态内容包 `layout`——有测量成本。
* **交错编排：** 顺序重要时用 `staggerChildren`（Motion）或 CSS 级联（`animation-delay: calc(var(--index) * 100ms)`）。`staggerChildren` 时父（`variants`）与子必须在同一 Client Component 树。

---

## 6. 性能与无障碍护栏

### 6.A 硬件加速
* **仅**动画 `transform` 与 `opacity`。不要动画 `top`、`left`、`width`、`height`。
* `will-change: transform`  sparingly——仅将动画的元素。

### 6.B 减少动效（强制）
* **`MOTION_INTENSITY > 3` 的任何动效必须尊重 `prefers-reduced-motion`。** 不可协商。
* Motion：用 `useReducedMotion()` 包裹并降级为静态。
* CSS：动画放在 `@media (prefers-reduced-motion: no-preference)` 后，或在 `@media (prefers-reduced-motion: reduce)` 下提供禁用块。
* 无限循环、视差、滚动劫持、磁性物理在减少动效下**必须**坍缩为静态/瞬时。

### 6.C 暗色模式（面向消费者的页面强制）
* **从一开始**设计双模式。无用户明确指令不要只交 light 或只交 dark。
* 用 Tailwind `dark:` **或** CSS 变量作 token。每项目选一种策略。
* **此处不规定具体暗色。** 简报决定。保持视觉层级、品牌识别、双模式 WCAG AA（正文目标 AAA）。
* 尊重 `prefers-color-scheme: dark`。品牌未坚持单模式时默认系统偏好。

### 6.D Core Web Vitals 目标
* **LCP** < 2.5s。Hero 图须 `next/image priority` 或预加载。
* **INP** < 200ms。重活离主线程。
* **CLS** < 0.1。为图、字体、嵌入预留空间。
* 宣布页面前跑 Lighthouse。

### 6.E DOM 成本
* grain / noise 滤镜**仅**用于 fixed、`pointer-events-none` 伪元素（如 `fixed inset-0 z-[60] pointer-events-none`）。**绝不**用在滚动容器——持续 GPU 重绘摧毁移动 FPS。
* 注意 bundle 体积。Motion 不小。Three.js 很大。首屏以上懒加载。

### 6.F Z-Index 克制
**不要**滥发任意 `z-50` 或 `z-10`。z-index 严格用于系统层（粘性 nav、模态、叠加、grain）。在项目常量文件文档 z-index 尺度。

---

## 7. 旋钮定义（技术参考）

### DESIGN_VARIANCE（1-10 级）
* **1-3（可预测）：** 对称 CSS Grid（12 列、等 fr）、等 padding、居中对齐。
* **4-7（偏移）：** `margin-top: -2rem` 重叠、 varied 图片宽高比（4:3 旁 16:9）、左对齐标题对居中数据。
* **8-10（不对称）：** Masonry、分数单位 CSS Grid（`grid-template-columns: 2fr 1fr 1fr`）、巨大空区（`padding-left: 20vw`）。
* **移动覆盖：** 4-10 级时，`md:` 以上不对称布局在 `< 768px` **必须**坍缩为严格单列（`w-full`、`px-4`、`py-8`）。

### MOTION_INTENSITY（1-10 级）
* **1-3（静态）：** 无自动动画。仅 CSS `:hover`、`:active`。`prefers-reduced-motion` 反正常是默认。
* **4-7（流体 CSS）：** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`。`animation-delay` 级联入场。聚焦 `transform`、`opacity`。
* **8-10（高级编排）：** 复杂滚动触发揭示、视差、滚动驱动动画（CSS `animation-timeline` 或 GSAP ScrollTrigger）。用 Motion hooks。**绝不** `window.addEventListener('scroll')`——硬禁，非「最好不用」。见 5.D 允许替代。

### VISUAL_DENSITY（1-10 级）
* **1-3（画廊）：** 大量留白。巨大节间距（`py-32` 到 `py-48`）。昂贵、干净。
* **4-7（日常应用）：** 标准 Web 间距（`py-16` 到 `py-24`）。
* **8-10（驾驶舱）：** 紧 padding。无卡片盒；1px 线分隔数据。强制：所有数字 `font-mono`。

---

## 8. 暗色模式协议

默认双模式。简报非仿印刷编辑时不要假设仅 light。

### 8.A Token 策略（选一个，坚持）
* **Tailwind `dark:` variant**（工具优先项目默认）：每个颜色工具配对暗色变体（`bg-white dark:bg-zinc-950`、`text-gray-900 dark:text-gray-100`）。
* **CSS 变量**（shadcn/ui、Radix Themes 或带主题的组件库）：定义语义 token（`--surface`、`--surface-elevated`、`--text-primary`、`--accent`），在 `[data-theme="dark"]` 或 `@media (prefers-color-scheme: dark)` 下换值。

### 8.B 此处不规定具体颜色
简报与品牌决定。本 skill 只强制：
* **对比度** - 正文 WCAG AA 最低，hero 文案目标 AAA。
* **层级对等** - light 成立的层级 dark 也要成立。CTA 在 light 跳，在 dark 也要跳。
* **品牌保真** - 主品牌色保持可识别。不要为暗色把品牌去饱和到认不出。
* **不要纯 `#000000` 和纯 `#ffffff`** - 用 off-black（zinc-950、暖近黑灰）和 off-white。纯色杀死深度。

### 8.C 默认模式
尊重 `prefers-color-scheme`，除非品牌坚持。任一模式会损失关键品牌表达时加手动切换。

### 8.D 完成前双模式测试
开发中两种模式都打开看。不要只看过一种就发货。

---

## 9. AI 痕迹（禁止模式）

除非简报明确要求，避免这些签名。

### 9.A 视觉与 CSS
* 默认**不要**霓虹 / 外发光。用内边框或 subtle 着色阴影。
* **不要**纯黑（`#000000`）。Off-black、zinc-950 或炭灰。
* **不要**过饱和强调色。降饱和以融入中性色。
* **不要**大标题过度渐变字。
* **不要**自定义鼠标光标。过时、碍无障碍、碍性能。

### 9.B 字体排印
* **避免 Inter 作默认。** 见 4.1。有覆盖路径。
* **不要** oversized H1 纯靠吼。用字重+颜色控层级，不靠 raw scale。
* **衬线约束：** 编辑 / 奢侈 / 出版用衬线。仪表盘不用。

### 9.C 布局与间距
* **数学完美**的 padding 与 margin。不要有尴尬间隙的漂浮元素。
* **不要**三列等宽功能卡。泛用「三张横排相同卡」功能行禁止。用 2 列 zig-zag、不对称网格、滚动钉住或横向滚动替代。

### 9.D 内容与数据（「Jane Doe」效应）
* **不要**泛用名。「John Doe」、「Sarah Chan」、「Jack Su」→ 用创意、真实、符合地域的名字。
* **不要**泛用头像。不要 SVG「蛋」或 Lucide 用户图标 → 用可信照片占位或特定样式。
* **不要**假完美数字。避免 `99.99%`、`50%`、`1234567`。用有机、凌乱数据（`47.2%`、`+1 (312) 847-1928`）。
* **不要**创业 slop 品牌名。「Acme」、「Nexus」、「SmartFlow」、「Cloudly」→ 发明语境化、听起来真的高级名。
* **不要**填充动词。「Elevate」、「Seamless」、「Unleash」、「Next-Gen」、「Revolutionize」→ 只用具体动词。

### 9.E 外部资源与组件
* **不要**手写 SVG 图标。用 Phosphor / HugeIcons / Radix / Tabler。Lucide 仅显式要求。
* 默认**强烈不推荐**手写装饰 SVG（见 4.8）。
* **不要** div 假截图。绝不用 `<div>` 矩形模拟截图搭假产品 UI。用真实图、生成图，或跳过预览。
* **不要**坏掉的 Unsplash 链。用 `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`、生成照片占位或真实资产。
* **shadcn/ui 定制：** 允许，但**绝不**默认态。按项目美学定制圆角、色、阴影、字体。
* **生产级整洁：** 代码视觉干净、难忘、精雕细琢。

### 9.F 生产测试痕迹（ outright 禁止）

这些模式来自真实 LLM 落地页测试。是模型试图「看起来有设计」时的默认签名。除非简报明确要，当作硬禁。

**Hero 与页顶**
* **Hero 不要版本标签。** `V0.6`、`v2.0`、`BETA`、`INVITE-ONLY PREVIEW`、`EARLY ACCESS`、`ALPHA`——默认 eyebrow 禁止。仅简报明确产品发布/预览状态时可用。
* **不要「Brand · No. 01」式子 eyebrow。** 「Marrow · No. 01 · The 6-quart」类微元行。跳过。

**节编号与微标签**
* **不要节编号 eyebrow。** `00 / INDEX`、`001 · Capabilities`、`002 · Featured commission`、`06 · how it works`、`05 · The honest table`——禁止。Eyebrow 应用平实语言点名主题，不枚举。
* **不要图片或 bento 瓦片上 `01 / 4` 式分页。** 用户能数就不需要标签。
* **不要 `Scroll · 001 Capabilities` 式滚动提示。** 简单箭头或「Scroll」就够；不要节前缀编号。
* **不要「Index of Work, 2018 - 2026」式范围标签**作 eyebrow。直接说节是什么。

**分隔符与圆点**
* **中点（`·`）配给。** 元数据条每行最多 1 个。不要当默认分隔到处用（"foo · bar · baz · qux · quux"）。需要分隔族时优先换行、发丝线或列。
* **不要每个列表/nav/徽章装饰色状态点。** 「ONE Q4 SLOT OPEN」前、每条 nav、每行任务前的色点——默认禁止。仅当点传达真实语义状态（服务器状态、可用性标志）且 sparingly 时可用。

**Em dash 与字体花活**
* **禁止 em dash（`—`）作设计元素或任何其它用途。** 见 9.G 完整不可协商禁令。Em dash 禁止出现在标题、eyebrow、标签、pill、正文、引用、署名、说明、按钮、alt。用普通连字符（`-`）。
* **不要默认 `<br>` 断行+斜体标题**作「设计手法」。「for thirty\<br\>*years.*」类拆分。标题应先自然可读，仅简报要求时再耍花活。
* **不要竖排旋转文字**（「INDEX OF WORK, 2018 - 2026」转 90°）。代理作品集陈词。仅简报明确 agency / Awwwards / experimental 且服务真实构图时用。
* **不要十字/发丝网格线纯装饰。** 仅为让页「感觉有设计」画的纵横线——禁止。仅组织真实内容时用。

**假产品预览**
* **Hero 不要 div 假产品 UI**（假任务列表、假终端、假仪表盘）。#1 LLM 设计 Tell。用真实截图、生成图、真实组件预览，或不要。
* **假截图里不要假版本页脚**（"v0.6.2-rc.1"、"last sync 4s ago · main"）。无信息量，尖叫 AI。

**营销文案痕迹**
* **不要「Quietly in use at」/「Quietly trusted by」**社交证明标题。用自然语言："Trusted by"、"Used at"、"Customers include"，或 logo 够响就不要标题。
* **不要「From the field」/「Field notes」/「Currently on the bench」/「On our desks」/「Loose plates」**式诗意标签在引用、博客、侧栏。像表演工匠。用朴素功能标签（"Testimonials"、"Latest writing"、"Now working on"）或不要标签。
* **不要「We respect the French ones」**式 mock 谦逊行业引用在正文。可爱且 AI 味。
* **不要天气/地域条**（"LIS 14:23 · 18°C"）在头/脚，除非简报明确关于地点/跨时区工作室。
* **Eyebrow 下不要微元句。** 如 *"Each of these is a feature we ship today, not a roadmap promise. The list will stay short on purpose."* 在节标题下是 clutter。Eyebrow + 标题 + 正文就够。
* **不要泛用步骤标签。** "Stage 1 / Stage 2 / Stage 3"、"Step 1 / Step 2 / Step 3"、"Phase 01 / Phase 02 / Phase 03"、"Pass One / Pass Two / Pass Three"。禁止。步骤内容即标签。必须显示进度时用动宾直接（"Install"、"Configure"、"Ship"），不要 "Stage 1: Install"。

**Pill、标签与版本戳**
* **不要在图片上叠 pill/标签。** 照片上不要 `<span>` 叠 `Brand · 02`、`PLATE · BRAND`、`Field notes - journal`。让图说话，或在图外下方加说明。
* **不要把照片署名当装饰。** `Field study no. 12 · Ines Caetano`、`Plate 03 · House archive`、`Frame XII · 35mm` 在 stock/picsum 图下是装腔。仅真实摄影师、真实照片、有许可时允许署名。否则：跳过或一行功能说明（"The 6-quart, in Sage."）。
* **营销页不要版本页脚。** `v1.4.2`、`Build 0048`、`last sync 4s ago · main` 是 CLI/开发工具 fixture，不是落地页内容。营销/落地/作品集页禁止。
* **不要「Reservation 412 of 800」式 live 库存计数**作装饰。仅简报明确限量候补且有真实数据时。

**装饰文字条**
* **Hero 底不要装饰文字条。** `BRAND. MOTION. SPATIAL.`、`TYPE / FORM / MOTION`、`DESIGN · BUILD · SHIP`、`ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` 作 hero 底小 mono-caps 条是代理作品集陈词。默认禁止。仅当条带承载真实可导航链接（粘性底 nav）或真实状态（cookie 条、文档站构建信息）时可接受。
* **节标题不要漂浮右上副文。** 模式：节左侧巨大左对齐标题；同一节头右上角漂浮小段，与任何元素对齐不清。那是 Tell。副文放标题正下，或做干净两列头（左标题、右对齐正文），不要角落小段。

**列表、分隔与评分条**
* **长列表/规格表每行不要 `border-t` + `border-b`。** 选一种（行间底边**或**组顶边）且稀疏用。10 行规格表每行发丝线是最懒布局——见 4.9 替代 UI。
* **不要用带填充背景轨的评分/进度条**作对比视觉。要显示「X of Y」优先数字+小图标，或 tiny 内联条**无**背景轨。大 `bg-zinc-200` 轨+部分填充是仪表盘 clutter，不是落地页。

**地域、时间、滚动提示**
* **99% 简报禁止地域/城市/时间/天气条。** Hero 里 "Lisbon, working with founders"、页脚 "1200-690 Lisbon, Portugal"、nav "Lisbon 14:23 · 18°C"。代理作品集装饰 tell。仅当：简报明确全球分布式工作室且时区相关、旅行品牌、真实物理场所。页脚单一联系地址可以；氛围地域条不行。
* **禁止滚动提示。** `Scroll`、`↓ scroll`、`Scroll to explore`、`Scroll to walk through it`、动画滚轮图标。用户还没滚时在 hero。他们知道怎么滚。视口底不需要标签。
* **默认零装饰状态点。** Nav 项、列表行、徽章、状态标签前的色点是 Tell。仅传达真实语义状态（真实服务器 live 指示、真实可用性标志）且每节最多一个时可接受。

### 9.G EM-DASH 禁令（违反最多的单一 Tell）

**Em dash（`—`）完全禁止。** 它是 LLM 标志性文体拐杖，生产测试 #1 视觉 Tell。没有「有限使用」、没有「正文自然频率」、没有「正文可以」的例外。**零。**

* **标题禁止。** 用句号或逗号。
* **Eyebrow / 标签 / pill / 按钮 / 图说明 / nav 禁止。** 用换行、列或发丝线替代。
* **正文禁止。** 重组句子：两句用句号，或逗号，或括号，或冒号。
* **引用署名禁止。** 用普通连字符加空格（` - `）或换行+较小字重姓名。
* **作分隔的 en dash（`–`）也禁止。** 日期范围（`2018-2026`）用连字符。数字范围（`€40-80k`）用连字符。

页上**唯一**允许的 dash 字符：
* 普通连字符 `-`（复合词、范围、标记分隔）
* 数学减号（`-5°C`）

若产出 anywhere 对用户可见处有一个 `—` 或 `–`，起飞前检查失败，必须重写。

本规则不可协商。Agent 历史上在「少用」表述时会忽略 em dash 限制。此处表述是二元的：零 em dash。

---

## 10. 参考词汇（Agent 应知的模式名）

这是词汇表，不是库。Agent 应**知道**这些模式名以便沟通、设计时心中有数，设计解读需要时取用。**实现与代码草图在区块库（第 12 节），迭代填充。**

### Hero 范式
* **Asymmetric Split Hero** - 一侧文字一侧资产，大量留白。
* **Editorial Manifesto Hero** - 大字，无资产，近乎海报。
* **Video / Media Mask Hero** - 文字镂空作视频背景遮罩。
* **Kinetic-Type Hero** - 动画字体为主视觉。
* **Curtain-Reveal Hero** - 滚动时 hero 如幕布分开。
* **Scroll-Pinned Hero** - Hero 钉住，内容在后方滚动。

### 导航与菜单
* **Mac OS Dock Magnification** - 边缘 nav，悬停图标流体缩放。
* **Magnetic Button** - 向光标吸引。
* **Gooey Menu** - 子项如粘稠液体脱离。
* **Dynamic Island** - 变形 pill 显示状态/提醒。
* **Contextual Radial Menu** - 点击点展开圆形菜单。
* **Floating Speed Dial** - FAB 弹成弧形次级操作。
* **Mega Menu Reveal** - 全屏下拉，交错淡入内容。

### 布局与网格
* **Bento Grid** - 不对称瓦片分组（Apple 控制中心）。
* **Masonry Layout** - 错落网格，无固定行高。
* **Chroma Grid** - 边框/瓦片 subtle 动画渐变。
* **Split-Screen Scroll** - 两半反向滑动。
* **Sticky-Stack Sections** - 滚动时钉住并堆叠的节。

### 卡片与容器
* **Parallax Tilt Card** - 3D 倾斜跟踪鼠标。
* **Spotlight Border Card** - 光标下边框点亮。
* **Glassmorphism Panel** - 磨砂玻璃内折射。
* **Holographic Foil Card** - 悬停彩虹全息偏移。
* **Tinder Swipe Stack** - 物理卡栈，滑走。
* **Morphing Modal** - 按钮展开成自身对话框。

### 滚动动画
* **Sticky Scroll Stack** - 卡片钉住物理堆叠。
* **Horizontal Scroll Hijack** - 纵向滚 → 横向平移。
* **Locomotive / Sequence Scroll** - 视频/3D 序列绑滚动条。
* **Zoom Parallax** - 中央背景图滚动缩放。
* **Scroll Progress Path** - SVG 线随滚动绘制。
* **Liquid Swipe Transition** - 页面过渡如粘稠液体。

### 画廊与媒体
* **Dome Gallery** - 3D 全景画廊。
* **Coverflow Carousel** - 3D 轮播斜边。
* **Drag-to-Pan Grid** - 无界可拖画布。
* **Accordion Image Slider** - 窄条悬停展开。
* **Hover Image Trail** - 鼠标留下弹出图轨迹。
* **Glitch Effect Image** - 悬停 RGB 通道偏移。

### 字体与文字
* **Kinetic Marquee** - 无尽文字带滚动反向。
* **Text Mask Reveal** - 巨字作视频透明窗。
* **Text Scramble Effect** - 加载/悬停 Matrix 解码。
* **Circular Text Path** - 文字沿旋转圆弯曲。
* **Gradient Stroke Animation** - 描边字流动渐变。
* **Kinetic Typography Grid** - 字母躲光标。

### 微交互与效果
* **Particle Explosion Button** - 成功时 CTA 碎成粒子。
* **Liquid Pull-to-Refresh** - 刷新指示如脱离液滴。
* **Skeleton Shimmer** - 占位上流动反光。
* **Directional Hover-Aware Button** - 填充从光标确切侧边进入。
* **Ripple Click Effect** - 点击坐标波纹。
* **Animated SVG Line Drawing** - 矢量实时自绘。
* **Mesh Gradient Background** - 有机熔岩灯 blob。
* **Lens Blur Depth** - 背景 UI 模糊聚焦前景。

### 动画库选择
* **Motion (`motion/react`)** - UI / Bento / 状态变化动效默认。
* **GSAP + ScrollTrigger** - 全页滚动叙事与滚动劫持。隔离在专用叶子组件，`useEffect` 清理。
* **Three.js / WebGL** - 画布背景与 3D 场景。同样隔离规则。
* **绝不在同一组件树混 GSAP / Three.js 与 Motion。** 它们抢同一帧。

---

## 11. 改版协议

本 skill 处理**绿地构建与改版**。误判模式是改版产出差的最大来源。

### 11.A 检测模式（首要动作）
* **Greenfield** - 无现有站，或批准全面大修。旋钮基线见第 1 节。
* **Redesign - Preserve** - 现代化但不破品牌。先审计，提取品牌 token，渐进演化。
* **Redesign - Overhaul** - 现有内容上新视觉语言。视觉当 greenfield；保留内容与 IA。

若模糊，**问一次**：*「这次改版应保留现有品牌，还是视觉上从零开始？」*

### 11.B 动手前先审计
提议变更前记录现状：
* **品牌 token** - 主色/强调色、字体栈、logo 处理、圆角。
* **信息架构** - 页面树、主导航、关键转化路径。
* **内容块** - 有什么、什么有用、什么是填充。
* **应保留模式** - 标志性交互、可识别 hero、文案声线。
* **应退役模式** - AI slop tell、坏布局、死链、泛用库存图、性能陷阱。
* **现有站旋钮解读** - 推断当前 `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`。那是起点，不是基线。
* **SEO 基线** - 当前排名页、meta 标题、结构化数据、OG 卡。**SEO 迁移是改版 #1 风险。**

### 11.C 保留规则
* **除非要求，不改信息架构。** 为 SEO 与肌肉记忆保持 slug、锚 ID、主导航标签稳定。
* **应用 4.2 前先提取品牌色。** 已是紫色的品牌保持紫——适用 LILA 规则覆盖。
* **除非要求重写，保留文案声线。** 视觉现代化 ≠ 内容重写。
* **尊重已有无障碍成果。** 不要倒退焦点态、alt、键盘导航、对比度。
* **尊重现有分析事件。** 不要重命名下游跟踪依赖的按钮、表单字段、节 ID。

### 11.D 现代化杠杆（优先级顺序）
按序应用——简报满足即停：
1. **字体刷新** - 单位风险最大视觉提升。
2. **间距与节奏** - 加大节 padding，修垂直节奏。
3. **色彩重校** - 降饱和、统一中性色、保留品牌强调。
4. **动效层** - 给现有组件加符合 `MOTION_INTENSITY` 的微交互。
5. **Hero 与关键节重组** - 用第 10 节词汇重构漏斗顶部。
6. **整块替换** - 仅当现有块不可救药。

### 11.E 决策树：定向演化 vs 全面改版
* IA、内容、SEO 健康 → **定向演化**（杠杆 1-4）。约 70% 价值、约 40% 风险。
* 视觉债结构性（坏 IA、无 DS、移动坏）→ **全面改版**，严格保留内容。
* 品牌本身在变 → **greenfield**。

### 11.F 绝不静默修改
无用户明确批准绝不改：
* URL 结构 / 路由 slug。
* 主导航标签。
* 表单字段名或顺序（破坏分析+自动填充）。
* 品牌 logo 或 wordmark。
* 现有法律/同意/cookie 文案。

---

## 12. 区块库（契约 - 实现迭代落地于此）

参考词汇（第 10 节）命名模式。区块库用真实 props、动效规格、代码草图实现它们。

**状态：** 此处定义 schema。区块将迭代添加。不要不按 schema 自造新区块。

### 12.A 文件位置
```
skills/taste-skill/blocks/
  hero/
    asymmetric-split.md
    editorial-manifesto.md
    kinetic-type.md
    ...
  feature/
    bento-grid.md
    sticky-scroll-stack.md
    zig-zag.md
    ...
  social-proof/
  pricing/
  cta/
  footer/
  navigation/
  portfolio/
  transition/
```

### 12.B 必需 Frontmatter
```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "Landing pages with one strong asset and one strong message. Default hero for SaaS, agency, premium consumer."
not_for: "Editorial / manifesto launches where the message IS the design."
stack: ["react", "next", "tailwind", "motion"]
---
```

### 12.C 必需正文节
1. **视觉草图** - 短 ASCII 或布局描述。
2. **Props API** - 组件接口。
3. **代码草图** - 最小可工作实现（默认 Server Component，动效用 Client 岛）。
4. **移动回退** - `< 768px` 显式折叠规则。
5. **动效变体** - 每个 `MOTION_INTENSITY` 带（1-3、4-7、8-10）一变体。减少动效回退显式。
6. **暗色模式说明** - 本块特定 token 策略。
7. **反模式** - 本块常见翻车方式。
8. **参考** - 生产环境真实示例链接。

### 12.D 区块库纪律
* 每文件一块。不要多区块文件。
* 每块须可独立工作（拖进页面即渲染）。
* 每块须过起飞前检查（第 14 节）。
* 依赖第 2.A 设计系统的块放在 `blocks/<category>/<name>--<system>.md`（如 `feature/bento-grid--material.md`）。

---

## 13. 范围外

本 skill **不**用于：
* 仪表盘 / 密集产品 UI / 管理面板（用第 2.A 的 Fluent、Carbon、Atlassian 或 Polaris）。
* 数据表（用 TanStack Table 或 AG Grid）。
* 多步表单 / 向导（用表单专用模式；本 skill 帮不上）。
* 代码编辑器（用 Monaco / CodeMirror 官方皮肤）。
* 原生移动（直接用 Apple HIG / Material）。
* 实时协作 UI（presence、光标、OT 感知——不同问题类）。

若简报是上述之一，**明确说明**，指向正确工具，仅把本 skill 的营销页/关于页/落地页部分用于适用表面。

---

## 14. 最终起飞前检查

输出代码前跑此矩阵。最后一道滤镜。

**非可选。每项都跑。任一项失败则产出未完成。**

- [ ] **简报推断**已声明（第 0.B 一行）？
- [ ] **旋钮值**显式且由简报推理，非静默用基线？
- [ ] **设计系统**按第 2 节选定（若适用），或美学诚实标注？
- [ ] **改版模式**已检测并审计（若适用，第 11 节）？
- [ ] **全页零 em dash（`—`）。** 标题、eyebrow、pill、正文、引用、署名、说明、按钮、alt。零。（第 9.G - 不可协商。）
- [ ] **页面主题锁定**：全页一个主题（light、dark 或 auto）。无节中途反转（第 4.11）？
- [ ] **色彩一致性锁定**：全节同一强调色（第 4.2）？
- [ ] **形状一致性锁定**：一致圆角系统（第 4.4）？
- [ ] **按钮对比检查**：每个 CTA 文字相对背景可读（无白上白，WCAG AA 4.5:1）？
- [ ] **CTA 按钮换行**：桌面无 CTA 标签折 2+ 行？
- [ ] **表单对比检查**：输入、placeholder、焦点环、标签相对区块背景过 WCAG AA？
- [ ] **衬线纪律**：若用衬线，不是 Fraunces 或 Instrument_Serif（或有明确品牌理由）？与上一项目不同衬线？
- [ ] **高端消费色板检查**：若简报为高端消费（厨具/wellness/手工艺/奢侈），色板不是 AI 默认米+黄铜+酒红+浓缩咖啡族？与上一高端消费项目不同族？
- [ ] **斜体下伸部留白**：含 `y g j p q` 的斜体词有 `leading-[1.1]` 最小 + `pb-1` 预留？
- [ ] **Hero 落在视口内**：标题 ≤ 2 行，副文 ≤ 20 词且 ≤ 4 行，CTA 无需滚动可见，字号与图一起规划？
- [ ] **Hero 顶部 padding**：桌面最多 `pt-24`，hero 内容不漂在半视口？
- [ ] **Hero 栈纪律**：hero 最多 4 文本元素（eyebrow 或品牌条、标题、副文、CTA）？CTA 下无小标语、hero 内无信任微条？
- [ ] **EYEBROW 计数（机械）**：统计所有组件中节标题上方 `uppercase tracking` 微标签。数量 ≤ ceil(sectionCount / 3)？Hero 计 1。
- [ ] **分栏标题禁令**：无「左大标题+右小说明」作节头（改垂直栈）？
- [ ] **Z 字交替上限**：无 3+ 连续相同图文分屏节？
- [ ] **无重复 CTA 意图**：无两个同意图 CTA（"Get in touch" + "Let's talk" 同页 = 失败）？
- [ ] **Logo 墙仅 logo**：logo 下无行业/类别标签？
- [ ] **Bento 背景多样性**：至少 2-3 bento 格有真实视觉变化（图、渐变、图案），非全白底白卡？
- [ ] **「Used by / Trusted by」logo 墙**在 hero **下**不在内，用**真实** SVG logo（Simple Icons / devicon）或生成 SVG 标，**非**纯文字 wordmark？
- [ ] **文案自审**：每条可见串重读，无语法破碎或 AI 幻觉短语（"free on its past" 类）？
- [ ] **动效有动机**：每个动画一句话可 justify（层级/叙事/反馈/状态过渡），无 GSAP 秀？
- [ ] **Marquee 每页最多一**：同页无两个横向 marquee？
- [ ] **导航桌面单行**，高度 ≤ 80px？
- [ ] **节布局重复检查**：无两节同布局族（8 节至少 4 族）？
- [ ] **Bento 有节奏且单元数精确**（N 项 → N 格，中间/末尾无空格）？
- [ ] **长列表用对 UI 组件**（> 5 项不用默认 `<ul>` + `divide-y`——见 4.9）？
- [ ] **使用真实图**（生图优先，其次 Picsum-seed，再显式占位）——无 div 假截图、无手写装饰 SVG、无纯文字假极简？
- [ ] **图片上无叠 pill/标签**（无 `Plate · Brand`、`Field notes - journal`）？
- [ ] **无装饰性照片署名**（`Field study no. 12 · Ines Caetano`）？
- [ ] **无版本页脚**（`v1.4.2`、`Build 0048`）在营销页？
- [ ] **Eyebrow 下无微元句**（"Each of these is a feature we ship today..."）？
- [ ] **Hero 底无装饰文字条**（`BRAND. MOTION. SPATIAL.`）？
- [ ] **节标题无漂浮右上副文**？
- [ ] **无带填充背景轨的评分/进度条**作对比视觉？
- [ ] **无地域/城市/时间/天气条**，除非简报真全球分布式或地点聚焦？
- [ ] **无滚动提示**（`Scroll`、`↓ scroll`、`Scroll to explore`）？
- [ ] **Hero 无版本标签**（V0.6、BETA、INVITE-ONLY），除非简报是发布？
- [ ] **无节编号 eyebrow**（`00 / INDEX`、`001 · Capabilities`、`06 · how it works`）？
- [ ] **无装饰点**（默认零，仅真实语义状态）？
- [ ] **长列表/规格表每行无 `border-t` + `border-b`**？
- [ ] **内容密度合理**：无 20 行数据表、无无依据假精确规格、默认副段 ≤ 25 词？
- [ ] **引用 ≤ 3 行**正文，署名干净（无 em dash）？
- [ ] **声称动效 = 看到动效**：`MOTION_INTENSITY > 4` 时页面真动，非只声称？
- [ ] **GSAP sticky-stack / horizontal-pan** 按 5.A / 5.B 规范骨架（`start: "top top"`、`pin: true`、正确 scrub）？
- [ ] **无 `window.addEventListener('scroll')`**——仅用 Motion `useScroll()` / ScrollTrigger / IntersectionObserver / CSS scroll-driven animations？
- [ ] **减少动效**：`MOTION_INTENSITY > 3` 的一切已包裹？
- [ ] **暗色模式** token 已定义且双模式测试？
- [ ] **移动折叠显式**（高 variance 布局 `w-full`、`px-4`、`max-w-7xl mx-auto`）？
- [ ] **视口稳定**：`min-h-[100dvh]`，绝不 `h-screen`？
- [ ] **`useEffect` 动画**有严格清理函数？
- [ ] **空/加载/错误**状态已提供？
- [ ] **能省略卡片处已用间距**？
- [ ] **图标**仅来自允许库（Phosphor / HugeIcons / Radix / Tabler），无手写 SVG 路径？
- [ ] **Motion** 隔离在 client 叶子组件，顶部 `'use client'`，已 memo？
- [ ] **无第 9 节 AI Tell**（Inter 默认、AI 紫、三等宽卡、Jane Doe、Acme、"Quietly in use at"）？
- [ ] **Core Web Vitals** 可信达标（LCP < 2.5s、INP < 200ms、CLS < 0.1）？
- [ ] **每项目一个设计系统**（不混 Material + shadcn）？

任一项无法诚实勾选，页面未完成。交付前修复。

---

# 附录 - 真实来源支撑的参考材料

以下节为 vendored 参考内容。为 Agent 提供第 2 节各设计系统的真实安装命令、规范文档链接、可工作起步片段。用于把决策锚在生产现实，而非训练数据虚构。

## 附录 A - 各设计系统安装命令

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product/devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
# Add this to your app HTML head:
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## 附录 B - 规范来源（再造轮子前先读）

### Material Web
- https://github.com/material-components/material-web
- https://material-web.dev/theming/material-theming/
- https://m3.material.io/develop/web

### Fluent UI
- https://fluent2.microsoft.design/get-started/develop
- https://fluent2.microsoft.design/components/web/react/
- https://github.com/microsoft/fluentui
- https://learn.microsoft.com/en-us/fluent-ui/web-components/

### Carbon
- https://carbondesignsystem.com/
- https://github.com/carbon-design-system/carbon
- https://carbondesignsystem.com/developing/react-tutorial/overview/
- https://carbondesignsystem.com/developing/web-components-tutorial/overview/

### Shopify Polaris
- https://shopify.dev/docs/api/app-home/web-components
- https://github.com/Shopify/polaris-react
- https://polaris-react.shopify.com/components

### Atlassian
- https://atlassian.design/get-started/develop
- https://atlassian.design/components/button/examples
- https://atlaskit.atlassian.com/packages/design-system/button/example/disabled
- https://atlassian.design/tokens/design-tokens

### Primer
- https://primer.style/
- https://github.com/primer/css
- https://github.com/primer/brand

### GOV.UK
- https://design-system.service.gov.uk/components/button/
- https://design-system.service.gov.uk/styles/layout/
- https://github.com/alphagov/govuk-frontend

### USWDS
- https://designsystem.digital.gov/documentation/developers/
- https://designsystem.digital.gov/components/button/
- https://designsystem.digital.gov/components/card/
- https://github.com/uswds/uswds

### Bootstrap
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/components/card/

### Tailwind
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

### Radix
- https://www.radix-ui.com/themes/docs/components/theme
- https://www.radix-ui.com/themes/docs/components/card
- https://github.com/radix-ui/themes

### shadcn/ui
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/components/card
- https://github.com/shadcn-ui/ui

### Native CSS / W3C standards
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass (Apple platforms only)
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## 附录 C - Apple Liquid Glass：诚实的 Web 近似

**不要**把随机 CSS 片段当官方 Apple Liquid Glass。

### 什么是官方的
Apple 在 **Apple 平台**的 HIG 与开发者文档中记录 Liquid Glass。它是跨 Apple 平台 UI 的动态材质。Apple 原生实现属于 Apple 平台 API 与系统组件，**不是**面向普通网站的公开 Web CSS 包。

相关官方文档：
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### 什么不是官方的
Apple 没有给普通网站提供 `liquid-glass.css`。

Web 近似可用：
- `backdrop-filter`
- 透明背景
- 分层边框
- 高光叠加
- 渐变
- 动效
- 强对比回退

但那是 **Web 玻璃拟态/磨砂玻璃近似**，不是官方 Apple Liquid Glass。注释中应如此标注。

### 更安全的 Web 近似骨架

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

**重要：** `prefers-reduced-transparency` 浏览器支持不均；要测试。无模糊时也要有足够对比。

---

**附录结束。** 上方安装命令是现实锚点。Apple Liquid Glass 骨架是标注近似，非 Apple 发行包。各设计系统规范文档见第 2 节与附录 B。

