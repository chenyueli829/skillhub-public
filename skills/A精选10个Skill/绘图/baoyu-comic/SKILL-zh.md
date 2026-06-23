---
name: baoyu-comic
description: 知识漫画创作器，支持多种画风与基调。可创作原创教育漫画，含详细分镜布局与可批量执行的图像生成。当用户要求创建「知识漫画」「教育漫画」「传记漫画」「教程漫画」或「Logicomix 风格漫画」时使用。
version: 1.57.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-comic
    requires:
      anyBins:
        - bun
        - npx
---

# 知识漫画创作器

创作原创知识漫画，支持灵活的画风 × 基调组合。

## 用户输入工具

当本 skill 需要向用户提问时，按以下工具选择规则（优先级顺序）：

1. **优先使用**当前 Agent 运行时暴露的内置用户输入工具 — 例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等价工具。
2. **回退方案**：若不存在上述工具，则发出带编号的纯文本消息，请用户以编号/答案回复每个问题。
3. **批量提问**：若工具支持单次调用多个问题，将所有适用问题合并为一次调用；若仅支持单问，则按优先级顺序逐一提问。

下文中的 `AskUserQuestion` 示例仅供参考 — 在其他运行时请替换为本地等价工具。

## 图像生成工具

当本 skill 需要渲染图像时，按以下顺序解析后端：

1. **当前请求覆盖** — 若用户在当前消息中指定了特定后端，则使用该后端。
2. **已保存偏好** — 若 `EXTEND.md` 将 `preferred_image_backend` 设为当前可用的后端，则使用该后端。
3. **自动选择**（当偏好为 `auto`、未设置，或固定后端不可用时）：
   - **Codex（`imagegen`）** — 首先检查可用 skill / 工具清单。若列出名为 `imagegen` 的 skill，说明运行在 Codex 内，**必须**使用它：通过 `Skill` 工具调用 `skill: "imagegen"`，传入已保存 prompt 文件的内容（以及 Codex `imagegen` 自身参数要求的输出路径与宽高比）。Codex `imagegen` 是该运行时的官方栅格后端，优先级高于任何非原生 skill（如 `baoyu-imagine`），除非用户已通过 `preferred_image_backend` 显式固定其他后端。
   - **其他运行时原生工具** — 若运行时暴露不同的原生图像工具（如 Hermes `image_generate`），以同样方式使用。
   - 否则，若恰好安装了一个非原生后端（如 `baoyu-imagine`），则使用它。
   - 否则（多个非原生后端且无运行时原生工具），向用户询问一次 — 可与其它初始问题合并批量提问。
4. **若均不可用**，告知用户并询问如何继续。

**⛔ 禁止用 SVG、HTML、canvas 或其他基于代码的渲染替代栅格图像生成。** Codex `imagegen` 的说明指出，当输出应为位图资源而非仓库原生代码或矢量时应使用它。若无法通过步骤 3 解析栅格后端，则进入步骤 4 询问用户 — **不要**静默输出 SVG、内联 `<svg>` 标记，或 HTML/CSS 艺术作为替代。即使文章/章节看起来「像图表」，调用本规则的上游 skill 已决定需要栅格图像。

**⛔ 禁止通过覆盖已生成位图来修复渲染文字。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加来覆盖、重写、擦除、描边或替换已生成漫画页内的对话、音效、分镜标签或任何其他文字。若文字错误或不清，应从修正后的 prompt 重新生成、用更少或无页内文字重绘该页，或询问用户保留哪个不完美的候选图。

设置 `preferred_image_backend: ask` 会无论可用后端如何，每次运行都强制执行步骤 3 的询问。用户可通过下文 `## 修改偏好` 一节更改固定后端。

**Prompt 文件要求（硬性）**：在调用任何后端**之前**，将每张图像的完整、最终 prompt 写入 `prompts/` 下的独立文件（命名：`NN-{type}-[slug].md`）。后端接收 prompt 文件（或其内容）；该文件是可复现性记录，便于切换后端而无需重新生成 prompt。

上文的具体工具名（`imagegen`、`image_generate`、`baoyu-imagine`）仅为示例 — 在相同规则下替换为本地等价物。

## 批量生成策略

当前生成组的所有 prompt 文件保存并验证后，默认批量生成图像。

优先级顺序：

1. 若所选后端存在原生批量/多任务接口，则使用它。每个任务须保留各自的 prompt 文件、输出路径、宽高比、session ID 与直接参考图。
2. 若无原生批量接口但运行时可并行工具调用，则每次最多派发 `generation_batch_size` 张图像。默认：`4`。当前消息中的显式请求（如 `--batch-size 4` 或「并行4张一起生成」）覆盖 EXTEND.md。
3. 若既无原生批量也无并行工具调用，则顺序生成。

规则：

- 优先遵守工作流依赖：在使用角色表作为参考的页面之前，先生成 `characters/characters.png`。
- 在所有选定页面的 prompt 文件落盘之前，不要启动首批页面生成。
- 失败项重试一次，不重新生成已成功项。
- 不要仅为并行图像渲染而使用 subagent。Subagent 仅用于独立的 prompt 迭代或创意探索。

## 参考图像

用户可提供参考图像以指导画风、调色板、场景构图或主体。这与自动生成的角色表（步骤 7.1）**相互独立** — 两者可并存：用户参考图指导外观，角色表锚定 recurring 角色的身份一致性。

** intake**：通过 `--ref <files...>` 接受，或用户在对话中提供文件路径/粘贴图像。
- 文件路径 → 复制到漫画输出目录旁的 `refs/NN-ref-{slug}.{ext}`
- 粘贴图像但无路径 → 按上文用户输入工具规则询问路径，或口头提取风格特征作为文本回退
- 无参考 → 跳过本节

**使用模式**（每张参考图）：

| 用法 | 效果 |
|------|------|
| `direct` | 将文件作为参考图传给后端，用于每一页（或选定页面） |
| `style` | 提取风格特征（线条处理、纹理、氛围）并追加到每页 prompt 正文 |
| `palette` | 提取 hex 色值并追加到每页 prompt 正文 |

**若存在参考图，在每页 prompt frontmatter 中记录**：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-scene.png
    usage: direct
```

**生成时**：
- 验证每个引用的文件存在于磁盘
- 若 `usage: direct` **且**所选后端接受多张参考图 → 通过后端 ref 参数同时传递角色表（步骤 7.2）与用户参考图；先按步骤 7.1 指南压缩图像，避免 payload 失败
- 若后端仅接受一张 ref → 对有 recurring 角色的页面优先使用角色表；将用户参考特征嵌入 prompt 正文
- 对于 `style`/`palette` 用法 → 将提取的特征嵌入每页 prompt 文本（与后端能力无关）

## 选项

### 视觉维度

| 选项 | 取值 | 说明 |
|--------|--------|-------------|
| `--art` | ligne-claire（默认）、manga、realistic、ink-brush、chalk、minimalist | 画风 / 渲染技法 |
| `--tone` | neutral（默认）、warm、dramatic、romantic、energetic、vintage、action | 情绪 / 氛围 |
| `--layout` | standard（默认）、cinematic、dense、splash、mixed、webtoon、four-panel | 分镜排布 |
| `--aspect` | 3:4（默认，竖版）、4:3（横版）、16:9（宽屏） | 页面宽高比 |
| `--lang` | auto（默认）、zh、en、ja 等 | 输出语言 |
| `--ref <files...>` | 文件路径 | 应用于每页的参考图，用于风格/调色板/场景指导。见上文 [参考图像](#参考图像)。 |
| `--batch-size <n>` | 1-8 | 本次运行的临时页面生成批量大小。默认：EXTEND.md 中的 `generation_batch_size`，否则为 4。 |

### 部分工作流选项

| 选项 | 说明 |
|--------|-------------|
| `--storyboard-only` | 仅生成分镜，跳过 prompt 与图像 |
| `--prompts-only` | 生成分镜 + prompt，跳过图像 |
| `--images-only` | 从已有 prompts 目录生成图像 |
| `--regenerate N` | 仅重新生成指定页（如 `3` 或 `2,5,8`） |

详情：[references/partial-workflows.md](references/partial-workflows.md)

### 画风、基调与预设目录

- **画风**（6 种）：`ligne-claire`、`manga`、`realistic`、`ink-brush`、`chalk`、`minimalist`。完整定义见 `references/art-styles/<style>.md`。
- **基调**（7 种）：`neutral`、`warm`、`dramatic`、`romantic`、`energetic`、`vintage`、`action`。完整定义见 `references/tones/<tone>.md`。
- **预设**（5 种），除 plain art+tone 外有特殊规则：

  | 预设 | 等价组合 | 特色 |
  |--------|-----------|------|
  | `ohmsha` | manga + neutral | 视觉隐喻、避免 talking head、小道具揭示 |
  | `wuxia` | ink-brush + action | 气功特效、战斗视觉、氛围感 |
  | `shoujo` | manga + romantic | 装饰元素、眼部细节、浪漫节拍 |
  | `concept-story` | manga + warm | 视觉符号系统、成长弧线、对话+动作平衡 |
  | `four-panel` | minimalist + neutral + four-panel layout | 起承转合结构、黑白+点缀色、 stick figure 角色 |

  完整规则见 `references/presets/<preset>.md` — 选定预设时加载对应文件。

- **兼容矩阵**与**内容信号 → 预设**表见 [references/auto-selection.md](references/auto-selection.md)。在步骤 2 推荐组合前先阅读。

## 脚本目录

**重要**：所有脚本位于本 skill 的 `scripts/` 子目录。

**Agent 执行说明**：
1. 将本 SKILL.md 所在目录路径记为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/<script-name>.ts`
3. 将本文档中所有 `{baseDir}` 替换为实际路径
4. 解析 `${BUN_X}` 运行时：若已安装 `bun` → `bun`；若可用 `npx` → `npx -y bun`；否则建议安装 bun

**脚本参考**：
| 脚本 | 用途 |
|--------|------|
| `scripts/merge-to-pdf.ts` | 将漫画页合并为 PDF |

## 文件结构

输出目录：`comic/{topic-slug}/`
- Slug：由主题提取 2-4 个词的 kebab-case（如 `alan-turing-bio`）
- 冲突：追加时间戳（如 `turing-story-20260118-143052`）

**内容**：
| 文件 | 说明 |
|------|------|
| `source-{slug}.{ext}` | 源文件 |
| `analysis.md` | 内容分析 |
| `storyboard.md` | 带分镜拆解的分镜稿 |
| `characters/characters.md` | 角色定义 |
| `characters/characters.png` | 角色参考表 |
| `prompts/NN-{cover\|page}-[slug].md` | 生成 prompt |
| `NN-{cover\|page}-[slug].png` | 生成的图像 |
| `{topic-slug}.pdf` | 最终合并 PDF |

## 语言处理

**检测优先级**：
1. `--lang` 标志（显式）
2. EXTEND.md 的 `language` 设置
3. 用户对话语言
4. 源内容语言

**规则**：所有交互使用用户输入语言或已保存的语言偏好：
- 分镜大纲与场景描述
- 图像生成 prompt
- 用户选项与确认
- 进度更新、提问、错误、摘要

技术术语保持英文。

## 工作流

### 进度清单

```
Comic Progress:
- [ ] Step 1: Setup & Analyze
  - [ ] 1.1 Preferences (EXTEND.md) ⛔ BLOCKING
    - [ ] Found → load preferences → continue
    - [ ] Not found → run first-time setup → MUST complete before other steps
  - [ ] 1.2 Analyze, 1.3 Check existing
- [ ] Step 2: Confirmation - Style & options ⚠️ REQUIRED
- [ ] Step 3: Generate storyboard + characters
- [ ] Step 4: Review outline (conditional)
- [ ] Step 5: Generate prompts
- [ ] Step 6: Review prompts (conditional)
- [ ] Step 7: Generate images
  - [ ] 7.1 Generate character sheet (if needed) → characters/characters.png
  - [ ] 7.2 Generate pages (with --ref if character sheet exists)
- [ ] Step 8: Merge to PDF
- [ ] Step 9: Completion report
```

### 流程

```
Input → [Preferences] ─┬─ Found → Continue
                       │
                       └─ Not found → First-Time Setup ⛔ BLOCKING
                                      │
                                      └─ Complete setup → Save EXTEND.md → Continue
                                                                              │
        ┌─────────────────────────────────────────────────────────────────────┘
        ↓
Analyze → [Check Existing?] → [Confirm: Style + Reviews] → Storyboard → [Review?] → Prompts → [Review?] → Images → PDF → Complete
```

### 步骤摘要

| 步骤 | 动作 | 关键输出 |
|------|--------|------------|
| 1.1 | 加载 EXTEND.md 偏好 ⛔ 未找到则阻塞 | 配置已加载 |
| 1.2 | 分析内容 | `analysis.md` |
| 1.3 | 检查已有目录 | 处理冲突 |
| 2 | 确认风格、焦点、受众、审阅选项 | 用户偏好 |
| 3 | 生成分镜 + 角色 | `storyboard.md`、`characters/` |
| 4 | 审阅大纲（若请求） | 用户批准 |
| 5 | 生成 prompt | `prompts/*.md` |
| 6 | 审阅 prompt（若请求） | 用户批准 |
| 7.1 | 生成角色表（若需要） | `characters/characters.png` |
| 7.2 | 生成页面（若有角色 ref 则使用） | `*.png` 文件 |
| 8 | 合并 PDF | `{slug}.pdf` |
| 9 | 完成报告 | 摘要 |

### 步骤 7：图像生成

**每个 session 选择一次后端**，遵循文首 `## 图像生成工具` 规则。若后端是仓库 skill（如 `baoyu-imagine`），读取其 `SKILL.md` 并使用文档化接口，而非其脚本。

**7.1 角色表** — 当漫画为多页且角色 recurring 时生成（输出至 `characters/characters.png`，宽高比 `4:3`）。简单预设（如 four-panel minimalist）或单页漫画可跳过。用作 `--ref` 前先压缩为 JPEG（macOS 上 `sips -s format jpeg -s formatOptions 80 …`，其他平台 `pngquant --quality=65-80 …`）以避免 payload 失败。调用后端前须存在 `characters/characters.md` prompt 文件。

**7.2 页面** — 调用后端前，每页 prompt **必须**已存在于 `prompts/NN-{cover|page}-[slug].md`；该文件是可复现性记录。策略取决于角色表：

| 角色表 | 后端 `--ref` | 策略 |
|-----------------|-----------------|----------|
| 存在 | 支持 | 每页传递表作为 `--ref` |
| 存在 | 不支持 | 将角色描述 prepend 到每页 prompt 文件 |
| 跳过 | — | 所有描述 inline 在 prompt 中 |

**执行策略**：需要时先生成角色表。然后从已保存 prompt 文件构建选定页面任务列表，按 `## 批量生成策略` 批量派发：优先后端原生批量，其次运行时并行工具调用，最后才顺序生成。`--regenerate N` 与 `--images-only` 对选定已有 prompt 应用相同批量规则。

**备份规则**：已有 `prompts/…md` 与 `…png` 文件 → 重新生成前重命名为 `-backup-YYYYMMDD-HHMMSS` 后缀。宽高比来自分镜（默认 `3:4`；预设可能覆盖）。

**`--ref` 失败恢复**：压缩表 → 重试 → 仍失败 → 去掉 `--ref`，将角色描述嵌入 prompt 文本。

完整逐步工作流（分析、分镜、审阅关卡、重生成变体）：[references/workflow.md](references/workflow.md)。

### EXTEND.md 路径 ⛔ BLOCKING

若未找到 EXTEND.md，首次设置**阻塞** — 完成后再进行任何内容分析或风格/基调提问。

| 优先级 | 路径 | 范围 |
|----------|------|------|
| 1 | `.baoyu-skills/baoyu-comic/EXTEND.md` | 项目 |
| 2 | `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 用户主目录 |

| 结果 | 动作 |
|--------|------|
| 找到 | 读取、解析、显示摘要 → 继续 |
| 未找到 | ⛔ 运行首次设置（[references/config/first-time-setup.md](references/config/first-time-setup.md)）→ 保存 EXTEND.md → 继续 |

**EXTEND.md 支持**：水印、首选画风/基调/布局、自定义风格定义、角色预设、语言偏好、首选图像后端、生成批量大小。Schema：[references/config/preferences-schema.md](references/config/preferences-schema.md)。

## 参考文档

**核心模板**：
- [analysis-framework.md](references/analysis-framework.md) - 深度内容分析
- [character-template.md](references/character-template.md) - 角色定义格式
- [storyboard-template.md](references/storyboard-template.md) - 分镜结构
- [ohmsha-guide.md](references/ohmsha-guide.md) - Ohmsha 日漫 specifics

**风格定义**：
- `references/art-styles/` - 画风（ligne-claire、manga、realistic、ink-brush、chalk、minimalist）
- `references/tones/` - 基调（neutral、warm、dramatic、romantic、energetic、vintage、action）
- `references/presets/` - 带特殊规则的预设（ohmsha、wuxia、shoujo、concept-story、four-panel）
- `references/layouts/` - 布局（standard、cinematic、dense、splash、mixed、webtoon、four-panel）

**工作流**：
- [workflow.md](references/workflow.md) - 完整工作流详情
- [auto-selection.md](references/auto-selection.md) - 内容信号分析
- [partial-workflows.md](references/partial-workflows.md) - 部分工作流选项

**配置**：
- [config/preferences-schema.md](references/config/preferences-schema.md) - EXTEND.md schema
- [config/first-time-setup.md](references/config/first-time-setup.md) - 首次设置
- [config/watermark-guide.md](references/config/watermark-guide.md) - 水印配置

## 页面修改

| 动作 | 步骤 |
|--------|------|
| **编辑** | **先更新 prompt 文件** → `--regenerate N` → 重新生成 PDF |
| **添加** | 在指定位置创建 prompt → 用角色 ref 生成 → 重编号后续页 → 更新分镜 → 重新生成 PDF |
| **删除** | 删除文件 → 重编号后续页 → 更新分镜 → 重新生成 PDF |

**重要**：更新页面时，**始终先**更新 prompt 文件（`prompts/NN-{cover|page}-[slug].md`）再重新生成。确保变更有文档记录且可复现。

文字修正策略：

- 若对话、音效、分镜标签或任何渲染文字拼写错误、乱码、难读或视觉弱，不要用代码 patch 位图。
- 文字修正重生成时，写入新 prompt 文件与新输出路径，保留 flawed 候选以供对比。
- 后处理限于裁剪、缩放、压缩或格式转换，不得改变文字或主构图。

## 备注

- 图像生成：每页约 10-30 秒
- 生成失败自动重试一次
- 对敏感公众人物使用风格化替代
- 通过 session ID 保持风格一致
- **步骤 2 确认必填** - 不可跳过
- **步骤 4/6 条件性** - 仅当用户在步骤 2 请求时
- **步骤 7.1 角色表** - 多页漫画推荐，简单预设可选
- **步骤 7.2 角色参考** - 若有表则使用 `--ref`；失败时压缩/转换；回退到仅 prompt
- 水印/语言在 EXTEND.md 中一次性配置

## 修改偏好

EXTEND.md 位于 `.baoyu-skills/baoyu-comic/EXTEND.md`（项目）或 `~/.baoyu-skills/baoyu-comic/EXTEND.md`（用户）。三种修改方式：

- **直接编辑** — 打开 EXTEND.md 修改字段。完整 schema：`references/config/preferences-schema.md`。
- **交互式重新配置** — 删除 EXTEND.md（或说「reconfigure baoyu-comic preferences」/「重新配置」）。下次运行重新触发首次设置。
- **常见单行编辑**：
  - `preferred_image_backend: auto` — 默认；运行时原生工具优先，回退到唯一已安装后端，多个非原生时才询问。
  - `preferred_image_backend: codex-imagegen` — 固定 Codex 内置。
  - `preferred_image_backend: baoyu-imagine` — 固定 baoyu-imagine skill。
  - `preferred_image_backend: ask` — 每次运行确认后端。
  - `generation_batch_size: 4` — 后端/运行时支持批量或并行生成时的默认并发页数。
  - `watermark.enabled: true`、`preferred_art`、`preferred_tone`、`preferred_layout`、`language` — 调整自动选择默认值与外观选项。
