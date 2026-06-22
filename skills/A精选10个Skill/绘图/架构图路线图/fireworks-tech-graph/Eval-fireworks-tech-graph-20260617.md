# Eval：fireworks-tech-graph

> 生成日期：2026-06-17  
> 入口文件：skills/精选10个Skill/fireworks-tech-graph-main/SKILL.md  
> 版本：1.0.4（package.json）

## 1. 介绍

`fireworks-tech-graph` 是一个**技术图生成** skill：将用户的自然语言系统/流程描述转化为可发布的 **SVG 技术图**，并导出高分辨率 **PNG**。覆盖架构图、数据流图、流程图、时序图、Agent/记忆架构、UML（类图、用例图、状态机、ER 图等）、网络拓扑、思维导图等 **14 种图类型**，内置 **8 种视觉风格**（7 种模板风格 + 1 种 Dark Luxury 手绘风）。

核心工作流为：识别图类型 → 从描述中提取节点/边/层级 → 按布局规则规划 → 加载 `references/style-N.md` 样式与 `references/icons.md` 图标 → 用 Python 列表法或 `generate-from-template.py` 生成 SVG → XML 校验 → 用 `cairosvg`（推荐）导出 PNG → 回报文件路径；可选对 PNG 做视觉自检并迭代修正箭头/标签/重叠问题。

同目录提供 4 个辅助脚本：`generate-diagram.sh`（校验 + 导出）、`generate-from-template.py`（JSON 驱动模板渲染）、`validate-svg.sh`（SVG 语法检查）、`test-all-styles.sh`（批量风格测试）。对 AI/Agent 场景有内置模式（RAG、Agentic RAG、Mem0、Multi-Agent、Tool Call 等）。

## 2. 触发条件

- **description 关键词**：画图、帮我画、生成图、做个图、架构图、流程图、可视化一下、出图、generate diagram、draw diagram、visualize，以及用户希望被图示化的系统/流程描述
- **显式触发语**：
  - 中文：「画一张…架构图」「帮我可视化这个流程」「出个时序图」「用暗黑风格画 Mem0 记忆架构」「优化箭头路由」
  - 英文：「draw an architecture diagram for…」「generate a sequence diagram」「visualize the data flow」「export as SVG and PNG」
- **场景**：
  - 需要博客/文档/演示用的技术插图
  - 描述微服务、RAG、Agent、API 调用链、UML 类图/ER 图等
  - 已有 SVG 需校验、导出 PNG，或仅优化箭头 JSON 后重渲染
- **不适用**：
  - 非技术类插画、照片、3D 渲染、交互式图表（D3 实时 dashboard）
  - 用户仅需 Mermaid/PlantUML 纯文本源码、不需 SVG/PNG 成品
  - 复杂 CJK/emoji 标签且必须用 PNG 高保真输出、但未安装 puppeteer 时（cairosvg 对中文支持有限）

## 3. 提问示例

### 示例 1：基础架构图（默认风格）

（复制以下内容提问）

> @skills/精选10个Skill/fireworks-tech-graph-main/SKILL.md 帮我画一张电商微服务架构图：用户 → API Gateway → 订单服务、库存服务、支付服务 → MySQL / Redis。输出 SVG 和 PNG，用默认扁平图标风格。

### 示例 2：Agent 领域 + 指定风格与输出路径

（复制以下内容提问）

> @fireworks-tech-graph 画一张 Mem0 风格的 Agent 记忆架构图，包含 Input、Memory Manager、VectorDB、GraphDB 的读写路径，用 Style 2 暗黑极客风。输出到 `./outputs/mem0-arch.svg` 并导出 PNG。

### 示例 3：时序图 + 箭头优化（边界能力）

（复制以下内容提问）

> @skills/精选10个Skill/fireworks-tech-graph-main/SKILL.md 根据下面交互画时序图（Client、API、DB）：登录请求 → 校验 token → 查库 → 返回。生成后如果箭头穿过组件内部，请按 skill 里的箭头优化流程只改 JSON 的 arrows 字段重渲染，不要动节点布局。

## 4. 外部依赖

### API / 在线服务

| 服务 | 用途 | 是否必需 | 备注 |
|------|------|----------|------|
| GitHub (`yizhiyanhua-ai/fireworks-tech-graph`) | `npx skills add` 安装来源 | 否 | 本仓库已内置 skill 目录，评测可不拉取 |
| npm (`@yizhiyanhua-ai/fireworks-tech-graph`) | 公开发布页与版本信息 | 否 | 仅安装/更新参考 |
| 无运行时 API | — | — | 生成过程为本地 SVG/脚本，不调用外部 SaaS |

### MCP / CLI / 系统能力

| 依赖 | 用途 | 是否必需 |
|------|------|----------|
| Python 3 | `generate-from-template.py`、XML 校验、cairosvg 调用 | 是 |
| Bash | `generate-diagram.sh`、`validate-svg.sh`、`test-all-styles.sh` | 是（走脚本流程时） |
| `cairosvg` | SVG → PNG（推荐，CSS 支持较好） | 否（强烈推荐；无则回退 rsvg） |
| `rsvg-convert` / librsvg | PNG 导出备选 | 否 |
| `puppeteer` + Node.js | 最高保真 PNG（浏览器引擎） | 否 |
| `xmllint` | `validate-svg.sh` 中 XML 语法检查 | 否（无则用 Python ET） |
| 图像读取能力 | 可选视觉自检（读 PNG 查重叠/穿框） | 否 |
| `npx` | 从 GitHub 安装/更新 skill | 否 |

### 环境变量 / 凭证

| 变量名 | 用途 |
|--------|------|
| 无 | skill 不要求 API Key、Token 或 OAuth |

### skill 目录外的路径

| 路径 | 用途 |
|------|------|
| `./[derived-name].svg` / `.png` | 默认输出（当前工作目录） |
| 用户指定路径（如 `--output` / 「输出到 /path/」） | 自定义输出目录 |
| `/tmp/test.png` | SKILL 中 cairosvg 渲染测试示例路径 |

### 第三方包 / 运行时

- **Python**：`pip install cairosvg`（推荐 PNG 导出）
- **系统包**：`brew install librsvg`（macOS）或 `apt install librsvg2-bin`（Debian），供 `rsvg-convert`
- **Node**：`npm install puppeteer`（可选，完整 CSS/CJK/emoji 保真）
- **Node 引擎**：`package.json` 要求 `node >= 14`（仅 puppeteer / npx 安装路径）

**评测注意：**

1. `generate-diagram.sh` **不负责生成 SVG 内容**，仅在校验已存在 SVG 后导出 PNG；实际绘图由 Agent 按 SKILL 工作流完成。
2. 含中文/emoji 的图：优先交付 **SVG**（浏览器可正确渲染）；若必须 PNG 且 `cairosvg` 出现方框，需改用 **puppeteer** 路径。
3. 样式 8（Dark Luxury）需手工参照 `references/style-8-dark-luxury.md` 绘制，不走模板脚本默认路径。
4. 本仓库路径为 `skills/精选10个Skill/fireworks-tech-graph-main/`，评测时 `@` 引用以实际目录为准。
