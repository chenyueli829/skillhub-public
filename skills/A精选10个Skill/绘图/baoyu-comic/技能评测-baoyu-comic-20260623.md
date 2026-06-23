# 技能评测：baoyu-comic

> 生成日期：2026-06-23  
> 入口文件：skills/A精选10个Skill/绘图/baoyu-comic/SKILL.md  
> 版本：1.57.0

## 1. 介绍

**baoyu-comic**（知识漫画创作器）是一套将文本内容转化为原创教育漫画的 Agent Skill，源自 [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills#baoyu-comic)。它面向「知识漫画」「教育漫画」「传记漫画」「教程漫画」等场景，支持 6 种画风 × 7 种基调的自由组合，并内置 ohmsha、wuxia、shoujo、concept-story、four-panel 等带特殊分镜规则的预设。

工作流从**阻塞式首次配置**（`EXTEND.md`）开始，经内容分析、用户确认风格与审阅选项后，依次产出分析稿（`analysis.md`）、分镜稿（`storyboard.md`）、角色定义与参考表、逐页图像 prompt 文件，再调用**运行时原生或已安装的图像后端**生成 PNG 页面，最后用 Bun 脚本合并 PDF。输出统一落在项目下的 `comic/{topic-slug}/` 目录。

与旧版 Easyclaw/Seedream 封装不同，本版（v1.57.0）强调**多后端适配**（Codex `imagegen`、Hermes `image_generate`、`baoyu-imagine`、Cursor `GenerateImage` 等）、**prompt 文件先行**（可复现、可换后端）、**批量并行生成**、**用户参考图**（style/palette/direct）以及**禁止用 SVG/HTML 或位图 overlay 替代/修复出图**。支持分阶段执行（`--storyboard-only` / `--prompts-only` / `--images-only`）与单页重生成（`--regenerate N`）。

## 2. 触发条件

Agent 应在用户明确要求创作漫画类内容，或 description 关键词匹配时启用本 skill。

- **description 关键词**：知识漫画、教育漫画、biography comic、tutorial comic、Logicomix-style comic、Knowledge comic creator
- **显式触发语**：
  - 中文：「帮我做一版知识漫画」「把这篇文章做成教育漫画」「用日漫风格画教程漫画」「Logicomix 风格传记漫画」「四格漫画讲 XX 概念」
  - 英文：「create a knowledge comic」「make an educational manga from this article」「biography comic in ligne-claire style」
- **场景**：
  - 将 Markdown/文章/教程文本转为多页漫画
  - 需要指定画风、基调、布局、宽高比或预设（ohmsha / wuxia / shoujo / four-panel 等）
  - 提供 `--ref` 参考图统一视觉风格
  - 仅需分镜或 prompt、或从已有 `prompts/` 目录补图
  - 修改/重生成已有漫画的某一页并更新 PDF
- **不适用**：
  - 单张插图、头像、海报（非分镜连载漫画工作流）
  - 无需结构化工作流的一次性文生图
  - 环境中无任何可用栅格图像后端且用户未指定替代方案
  - 用户拒绝完成 `EXTEND.md` 首次设置（步骤 1.1 阻塞）

## 3. 提问示例

### 示例 1：基础用法 — 从文章生成知识漫画

（复制以下内容提问）

> @skills/A精选10个Skill/绘图/baoyu-comic/SKILL.md 请把下面这篇关于图灵生平的文章做成知识漫画，画风和基调你根据内容自动推荐即可：
>
> （在此粘贴 500–2000 字文章内容）

### 示例 2：带具体风格与预设 — Ohmsha 教程漫画

（复制以下内容提问）

> @baoyu-comic 我有这份 Python 入门教程 `docs/python-basics.md`，请用 ohmsha 预设风格做成教育漫画，竖版 3:4，输出语言中文。生成分镜后先让我确认大纲再出图。

### 示例 3：部分工作流 — 仅分镜与 prompt

（复制以下内容提问）

> @baoyu-comic 用 `articles/wuxia-legend.md` 的内容，武侠预设（wuxia），先只做到分镜和 prompts（`--prompts-only`），暂时不要调用图像生成。完成后告诉我输出目录路径。

### 示例 4：带参考图与批量参数 — 四格漫画

（复制以下内容提问）

> @baoyu-comic 把下面这段「产品经理日常」梗概做成四格漫画（four-panel 预设），参考图 `--ref ./refs/my-style.png` 用法为 style，并行 `--batch-size 2` 出图，语言中文：
>
> （粘贴 200 字以内梗概）

### 示例 5：边界能力 — 重生成指定页并更新 PDF

（复制以下内容提问）

> @baoyu-comic 漫画项目在 `comic/alan-turing-bio/`，第 3 页分镜需要改：把实验室场景改成夜间。请先更新 `prompts/03-page-*.md`，再 `--regenerate 3` 重新出图，最后合并 PDF。

## 4. 外部依赖

### API / 在线服务

| 服务 | 用途 | 是否必需 | 备注 |
|------|------|----------|------|
| 图像生成 API（由运行时后端决定） | 生成漫画页与角色参考表 PNG | 是（完整出图流程） | 非 skill 内置单一 API；取决于 `preferred_image_backend` 与当前环境可用工具 |
| GitHub（元数据） | `metadata.openclaw.homepage` 文档链接 | 否 | 仅参考，不影响执行 |

**常见后端（按 SKILL 优先级，择环境可用者）**：

| 后端 ID / 工具 | 典型环境 | 备注 |
|----------------|----------|------|
| Codex `imagegen` | OpenAI Codex | 运行时原生，优先级最高 |
| Hermes `image_generate` | Hermes Agent | 运行时原生 |
| `baoyu-imagine` skill | 已安装该 skill 的 Cursor/Agent | 需单独安装并阅读其 SKILL.md |
| Cursor `GenerateImage` | Cursor IDE Agent | 本仓库 Cursor 评测时的实际出图工具 |

### MCP / CLI / 系统能力

| 依赖 | 用途 | 是否必需 |
|------|------|----------|
| `bun` 或 `npx` | 运行 `scripts/merge-to-pdf.ts`；frontmatter `requires.anyBins` | 是（合并 PDF） |
| `pdf-lib`（npm） | PDF 合成（`merge-to-pdf.ts` import） | 是（合并 PDF；需 Bun 可解析依赖） |
| Agent 用户输入工具 | 首次 `EXTEND.md` 设置、步骤 2 风格确认 | 是（按 Skill 设计；Cursor 可用对话回复） |
| 栅格图像生成工具 | 步骤 7 出图 | 是（完整漫画流程） |
| `sips`（macOS）或 `pngquant` | 角色表/参考图压缩，避免 ref payload 失败 | 否（失败时可回退 prompt-only） |

### 环境变量 / 凭证

| 变量名 | 用途 |
|--------|------|
| （无 skill 级固定变量） | 图像后端凭证由所选后端自身决定（如 Cursor 内置图生、第三方 API Key 等） |

> 本版 skill **不**绑定 Easyclaw / Seedream；评测前需确认当前 Agent 至少有一种可用栅格图像后端。

### skill 目录外的路径

| 路径 | 用途 |
|------|------|
| `.baoyu-skills/baoyu-comic/EXTEND.md` | 项目级偏好（水印、默认画风/基调/语言、图像后端、批量大小等） |
| `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 用户级偏好（项目未配置时的回退） |
| `comic/{topic-slug}/`（工作区项目根下） | 漫画输出目录（分析、分镜、角色、prompts、图片、PDF） |
| 用户提供的源文件路径（如 `docs/python-basics.md`） | 输入内容 |
| 用户 `--ref` 指定的参考图路径 | 复制至输出目录 `refs/` |

### 第三方包 / 运行时

- **Bun 生态**：`merge-to-pdf.ts` 依赖 `pdf-lib`，通过 `bun {baseDir}/scripts/merge-to-pdf.ts <comic-dir>` 执行；若无 bun 可用 `npx -y bun`
- **图像后端**：按环境安装/启用（如 `baoyu-imagine` skill）；skill 目录内**无**自带 Python 出图脚本
- **可选系统工具**：macOS `sips`、跨平台 `pngquant`（角色表 JPEG 压缩）
