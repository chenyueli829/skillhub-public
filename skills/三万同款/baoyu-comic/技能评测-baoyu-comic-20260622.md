# 技能评测：baoyu-comic

> 生成日期：2026-06-22  
> 入口文件：skills/三万同款/baoyu-comic/SKILL.md  
> 版本：1.0.2（来自 `.easyclaw-metadata.json`）

## 1. 介绍

**baoyu-comic**（知识漫画创作器）是一套将文本内容转化为原创教育漫画的 Agent Skill。它面向「知识漫画」「教育漫画」「传记漫画」「教程漫画」等场景，支持多种画风（清线、日漫、写实、水墨、粉笔）与情绪基调（中性、温馨、戏剧、浪漫等）的自由组合，并内置 ohmsha、wuxia、shoujo 等带特殊分镜规则的预设。

工作流从内容分析开始，经用户确认风格与审阅选项后，依次产出分镜稿（`storyboard.md`）、角色定义与参考图、逐页图像生成提示词，再调用 Seedream 5.0 Lite 生成 JPEG 页面，最终合并为 PDF。输出统一落在项目下的 `comic/{topic-slug}/` 目录，包含分析、分镜、角色、提示词、图片与 PDF 等完整产物链。

Skill 强调**阻塞式首次配置**（`EXTEND.md` 偏好文件）与**步骤 2 风格确认**，并强制在生成各页之前先产出角色参考表（`characters/characters.jpg`），以保证跨页角色视觉一致。支持分阶段执行（仅分镜、仅提示词、仅图像）以及单页重生成与页面增删改。

## 2. 触发条件

Agent 应在用户明确要求创作漫画类内容，或 description 关键词匹配时启用本 skill。

- **description 关键词**：知识漫画、教育漫画、biography comic、tutorial comic、Logicomix-style comic、知识漫画创作器
- **显式触发语**：
  - 中文：「帮我做一版知识漫画」「把这篇文章做成教育漫画」「用日漫风格画教程漫画」「Logicomix 风格传记漫画」
  - 英文：「create a knowledge comic」「make an educational manga from this article」「biography comic in ligne-claire style」
  - 命令式：`/baoyu-comic <文件路径>` 或带 `--art`、`--tone`、`--style` 等参数
- **场景**：
  - 将 Markdown/文章/教程文本转为多页漫画
  - 需要指定画风、基调、布局或预设（ohmsha / wuxia / shoujo）
  - 仅需分镜或提示词、或从已有 prompts 补图
  - 修改/重生成已有漫画的某一页并更新 PDF
- **不适用**：
  - 单张插图、头像、海报（非分镜连载漫画）
  - 无需结构化工作流的一次性文生图
  - 用户未安装/配置 Easyclaw 且无法完成 `EXTEND.md` 首次设置的环境

## 3. 提问示例

### 示例 1：基础用法 — 从文章生成知识漫画

（复制以下内容提问）

> @baoyu-comic 请把下面这篇关于图灵生平的文章做成知识漫画，画风和基调你根据内容自动推荐即可：
>
> （在此粘贴 500–2000 字文章内容）

### 示例 2：带具体风格参数 — 教程漫画（Ohmsha 预设）

（复制以下内容提问）

> @skills/三万同款/baoyu-comic/SKILL.md 我有这份 Python 入门教程 `docs/python-basics.md`，请用 ohmsha 预设风格做成教育漫画，竖版 3:4，输出语言中文。生成分镜后先让我确认大纲再出图。

### 示例 3：部分工作流 — 仅生成分镜与提示词

（复制以下内容提问）

> @baoyu-comic 用 `articles/wuxia-legend.md` 的内容，武侠预设（wuxia），先只做到分镜和 prompts（`--prompts-only`），暂时不要调用图像生成。完成后告诉我输出目录路径。

### 示例 4：边界能力 — 重生成指定页并更新 PDF

（复制以下内容提问）

> @baoyu-comic 漫画项目在 `comic/alan-turing-bio/`，第 3 页分镜需要改：把实验室场景改成夜间。请先更新 `prompts/03-page-*.md`，再 `--regenerate 3` 重新出图，最后合并 PDF。

## 4. 外部依赖

### API / 在线服务

| 服务 | 用途 | 是否必需 | 备注 |
|------|------|----------|------|
| Easyclaw API（Seedream 5.0 Lite，`bytepluses.seedream-5.0-lite`） | 通过 `generate_image.py` 生成漫画页与角色参考图 | 是（完整出图流程） | 凭证从 `~/.easyclaw/` 自动读取，Skill 声明无需单独 API Key |
| `aibot-data-cdn.easyclaw.cn` | Skill 图标 CDN（`.easyclaw-metadata.json`） | 否 | 仅元数据展示，不影响执行 |

### MCP / CLI / 系统能力

| 依赖 | 用途 | 是否必需 |
|------|------|----------|
| Python 3 | 运行 `scripts/generate_image.py` | 是（出图） |
| `openai`（Python 包） | OpenAI 兼容客户端调用 Easyclaw 图像 API | 是（出图） |
| `pillow` / PIL（Python 包） | 输入图编码、尺寸处理 | 是（出图） |
| Bun | 运行 `scripts/merge-to-pdf.ts` | 是（合并 PDF） |
| `pdf-lib`（npm） | PDF 合成 | 是（合并 PDF，需 Bun 环境可解析） |
| Agent `AskUserQuestion` 能力 | 首次 `EXTEND.md` 设置、步骤 2 风格确认 | 是（按 Skill 设计） |

### 环境变量 / 凭证

| 变量/文件 | 用途 |
|--------|------|
| `~/.easyclaw/easyclaw.json` | Easyclaw `baseUrl` 等运行时配置 |
| `~/.easyclaw/identity/easyclaw-userinfo.json` | `uid` + `token` 认证（`X-Auth-Uid` / `X-Auth-Token` 请求头） |

> Skill 未要求单独的环境变量名；图像生成依赖上述 Easyclaw 本地配置文件。评测前需确认 Easyclaw 客户端已登录且 `~/.easyclaw/` 配置有效。

### skill 目录外的路径

| 路径 | 用途 |
|------|------|
| `.baoyu-skills/baoyu-comic/EXTEND.md` | 项目级偏好（水印、默认画风/基调/语言等） |
| `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 用户级偏好（项目未配置时的回退） |
| `~/.easyclaw/` | Easyclaw 认证与 API 配置 |
| `comic/{topic-slug}/`（工作区项目根下） | 漫画输出目录（分析、分镜、角色、图片、PDF） |
| 用户提供的源文件路径（如 `posts/turing-story/source.md`） | 输入内容 |

### 第三方包 / 运行时

- **Python**：`pip install openai pillow`（Skill 在步骤 7 前置检查中明确要求）
- **Node/Bun 生态**：`merge-to-pdf.ts` 依赖 `pdf-lib`，通过 `bun` 执行；仓库内未见 `package.json`，评测环境需自行确保 `bun` 与 `pdf-lib` 可用
- **无** pip/npm 锁定文件于 skill 根目录；图像脚本为自包含 Python，PDF 脚本为单文件 TypeScript
