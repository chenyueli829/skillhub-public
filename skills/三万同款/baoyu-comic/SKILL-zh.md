---
name: baoyu-comic
description: 知识漫画创作器，支持多种画风与基调。可创作原创教育漫画，含详细分镜布局与逐页图像生成。当用户要求创建「知识漫画」「教育漫画」「传记漫画」「教程漫画」或「Logicomix 风格漫画」时使用。
---

# 知识漫画创作器

创作原创知识漫画，支持灵活的画风 × 基调组合。

## 用法

```bash
/baoyu-comic posts/turing-story/source.md
/baoyu-comic article.md --art manga --tone warm
/baoyu-comic  # 然后粘贴内容
```

## 选项

### 视觉维度

| 选项 | 取值 | 说明 |
|--------|--------|-------------|
| `--art` | ligne-claire（默认）、manga、realistic、ink-brush、chalk | 画风 / 渲染技法 |
| `--tone` | neutral（默认）、warm、dramatic、romantic、energetic、vintage、action | 情绪 / 氛围 |
| `--layout` | standard（默认）、cinematic、dense、splash、mixed、webtoon | 分镜排布 |
| `--aspect` | 3:4（默认，竖版）、4:3（横版）、16:9（宽屏） | 页面宽高比 |
| `--lang` | auto（默认）、zh、en、ja 等 | 输出语言 |

### 部分工作流选项

| 选项 | 说明 |
|--------|-------------|
| `--storyboard-only` | 仅生成分镜，跳过提示词与图像 |
| `--prompts-only` | 生成分镜 + 提示词，跳过图像 |
| `--images-only` | 从已有 prompts 目录生成图像 |
| `--regenerate N` | 仅重新生成指定页（如 `3` 或 `2,5,8`） |

详情：[references/partial-workflows.md](references/partial-workflows.md)

### 画风（Art Styles）

| 风格 | 中文 | 说明 |
|-------|------|-------------|
| `ligne-claire` | 清线 | 均匀线条、平涂色块，欧洲漫画传统（《丁丁》《Logicomix》） |
| `manga` | 日漫 | 大眼睛、日漫惯例、表情丰富 |
| `realistic` | 写实 | 数字绘画、写实比例、精致感 |
| `ink-brush` | 水墨 | 中国笔墨、水墨晕染效果 |
| `chalk` | 粉笔 | 黑板美学、手绘温暖感 |

### 基调（Tones）

| 基调 | 中文 | 说明 |
|------|------|-------------|
| `neutral` | 中性 | 平衡、理性、教育向 |
| `warm` | 温馨 | 怀旧、个人化、治愈 |
| `dramatic` | 戏剧 | 高对比、强烈、有力 |
| `romantic` | 浪漫 | 柔和、唯美、装饰元素 |
| `energetic` | 活力 | 明亮、动感、兴奋 |
| `vintage` | 复古 | 历史感、做旧、时代真实 |
| `action` | 动作 | 速度线、冲击效果、打斗 |

### 预设快捷方式

除 art+tone 外还有特殊规则的预设：

| 预设 | 等价于 | 特殊规则 |
|--------|-----------|---------------|
| `--style ohmsha` | `--art manga --tone neutral` | 视觉隐喻、禁止 talking heads、道具揭示 |
| `--style wuxia` | `--art ink-brush --tone action` | 气功效果、打斗画面、氛围元素 |
| `--style shoujo` | `--art manga --tone romantic` | 装饰元素、眼部细节、浪漫节拍 |

### 兼容性矩阵

| 画风 | ✓✓ 最佳 | ✓ 可用 | ✗ 避免 |
|-----------|---------|---------|---------|
| ligne-claire | neutral, warm | dramatic, vintage, energetic | romantic, action |
| manga | neutral, romantic, energetic, action | warm, dramatic | vintage |
| realistic | neutral, warm, dramatic, vintage | action | romantic, energetic |
| ink-brush | neutral, dramatic, action, vintage | warm | romantic, energetic |
| chalk | neutral, warm, energetic | vintage | dramatic, action, romantic |

详情：[references/auto-selection.md](references/auto-selection.md)

## 自动选择

根据内容信号决定默认画风 + 基调 + 布局（或预设）：

| 内容信号 | 推荐 |
|-----------------|-------------|
| 教程、how-to、编程、教育 | **ohmsha** 预设 |
| 1950 年前、古典、古代 | realistic + vintage |
| 个人故事、导师 | ligne-claire + warm |
| 武术、武侠 | **wuxia** 预设 |
| 恋爱、校园 | **shoujo** 预设 |
| 传记、平衡叙事 | ligne-claire + neutral |

**当推荐预设时**：加载 `references/presets/{preset}.md` 并应用全部特殊规则。

详情：[references/auto-selection.md](references/auto-selection.md)

## 脚本目录

**重要**：所有脚本位于本 skill 的 `scripts/` 子目录。

**Agent 执行说明**：
1. 将本 `SKILL.md` 所在目录路径记为 `SKILL_DIR`
2. 脚本路径 = `${SKILL_DIR}/scripts/<script-name>.ts`
3. 将本文档中所有 `${SKILL_DIR}` 替换为实际路径

**脚本参考**：
| 脚本 | 用途 |
|--------|---------|
| `scripts/generate_image.py` | 通过 Seedream 5.0 Lite 生成图像（无需外部 API Key） |
| `scripts/merge-to-pdf.ts` | 将漫画页合并为 PDF |

## 文件结构

输出目录：`comic/{topic-slug}/`
- Slug：主题 2–4 个词的 kebab-case（如 `alan-turing-bio`）
- 冲突：追加时间戳（如 `turing-story-20260118-143052`）

**内容**：
| 文件 | 说明 |
|------|-------------|
| `source-{slug}.{ext}` | 源文件 |
| `analysis.md` | 内容分析 |
| `storyboard.md` | 含分镜拆解的分镜稿 |
| `characters/characters.md` | 角色定义 |
| `characters/characters.jpg` | 角色参考图 |
| `prompts/NN-{cover\|page}-[slug].md` | 生成提示词 |
| `NN-{cover\|page}-[slug].jpg` | 生成图像（JPEG，由 generate_image.py 输出） |
| `{topic-slug}.pdf` | 最终合并 PDF |

## 语言处理

**检测优先级**：
1. `--lang` 参数（显式）
2. EXTEND.md 中的 `language` 设置
3. 用户对话语言
4. 源内容语言

**规则**：所有交互使用用户输入语言或已保存的语言偏好：
- 分镜大纲与场景描述
- 图像生成提示词
- 用户选项与确认
- 进度更新、提问、错误、总结

技术术语保留英文。

## 工作流

### 进度清单

```
Comic Progress:
- [ ] Step 1: 设置与分析
  - [ ] 1.1 偏好（EXTEND.md）⛔ 阻塞
    - [ ] 已找到 → 加载偏好 → 继续
    - [ ] 未找到 → 首次设置 → 必须先完成才能进行其他步骤
  - [ ] 1.2 分析、1.3 检查已有产物
- [ ] Step 2: 确认 - 风格与选项 ⚠️ 必需
- [ ] Step 3: 生成分镜 + 角色
- [ ] Step 4: 审阅大纲（条件性）
- [ ] Step 5: 生成提示词
- [ ] Step 6: 审阅提示词（条件性）
- [ ] Step 7: 生成图像 ⚠️ 需要角色参考图
  - [ ] 7.1 优先生成角色表 → characters/characters.jpg
  - [ ] 7.2 各页使用 --input-image characters/characters.jpg 生成
- [ ] Step 8: 合并为 PDF
- [ ] Step 9: 完成报告
```

### 流程图

```
输入 → [偏好] ─┬─ 已找到 → 继续
                       │
                       └─ 未找到 → 首次设置 ⛔ 阻塞
                                      │
                                      └─ 完成设置 → 保存 EXTEND.md → 继续
                                                                              │
        ┌─────────────────────────────────────────────────────────────────────┘
        ↓
分析 → [检查已有?] → [确认: 风格 + 审阅] → 分镜 → [审阅?] → 提示词 → [审阅?] → 图像 → PDF → 完成
```

### 步骤摘要

| 步骤 | 动作 | 关键输出 |
|------|--------|------------|
| 1.1 | 加载 EXTEND.md 偏好 ⛔ 未找到则阻塞 | 配置已加载 |
| 1.2 | 分析内容 | `analysis.md` |
| 1.3 | 检查已有目录 | 处理冲突 |
| 2 | 确认风格、焦点、受众、审阅选项 | 用户偏好 |
| 3 | 生成分镜 + 角色 | `storyboard.md`、`characters/` |
| 4 | 审阅大纲（若用户要求） | 用户批准 |
| 5 | 生成提示词 | `prompts/*.md` |
| 6 | 审阅提示词（若用户要求） | 用户批准 |
| **7.1** | **优先生成角色表** | `characters/characters.jpg` |
| **7.2** | **带角色参考生成各页** | `*.jpg` 文件 |
| 8 | 合并为 PDF | `{slug}.pdf` |
| 9 | 完成报告 | 总结 |

### 步骤 7：图像生成 ⚠️ 关键

**角色参考图对视觉一致性为强制要求。**

**图像生成引擎**：使用内置 `scripts/generate_image.py`（通过 Easyclaw API 调用 Seedream 5.0 Lite）。无需外部 API Key — 自动从 `~/.easyclaw/` 读取凭证。

**前置条件**（每会话检查一次）：
```bash
python -c "import openai, PIL; print('ok')"
# 若失败：
python -m pip install openai pillow
```

**7.1 优先生成角色表**：
- **备份规则**：若 `characters/characters.jpg` 已存在，重命名为 `characters/characters-backup-YYYYMMDD-HHMMSS.jpg`
- 读取 `characters/characters.md` 中的 Reference Sheet Prompt，作为 `--prompt`
```bash
# 生成角色参考表（4:3 横版）
python ${SKILL_DIR}/scripts/generate_image.py \
  --prompt "<来自 characters/characters.md 的 Reference Sheet Prompt>" \
  --filename "characters/characters.jpg" \
  --aspect-ratio 4:3
```

**7.2 带角色参考生成各页**：
- 读取各提示词文件（`prompts/NN-*.md`），将其内容作为 `--prompt`
- 将角色表作为 `--input-image` 传入以保持角色一致
- **页面生成备份规则**：
  - 若图像文件已存在：重命名为 `NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.jpg`

```bash
# 示例：带角色参考生成页面以保持一致性
python ${SKILL_DIR}/scripts/generate_image.py \
  --prompt "<来自 prompts/01-page-xxx.md 的完整提示词>" \
  --filename "01-page-xxx.jpg" \
  --aspect-ratio 3:4 \
  --input-image characters/characters.jpg
```

**宽高比映射**（baoyu-comic → generate_image.py）：
| 漫画选项 | `--aspect-ratio` 值 |
|---|---|
| `--aspect 3:4`（竖版，默认） | `3:4` |
| `--aspect 4:3`（横版） | `4:3` |
| `--aspect 16:9`（宽屏） | `16:9` |
| 角色表 | `4:3` |

**输出格式**：JPEG（`.jpg`）。相应更新分镜/提示词中的文件引用。

**完整工作流详情**：[references/workflow.md](references/workflow.md)

### EXTEND.md 路径 ⛔ 阻塞

**关键**：若未找到 EXTEND.md，必须在任何其他问题或步骤之前完成首次设置。不得进行内容分析，不得询问画风，不得询问基调 — 仅完成偏好设置。

| 路径 | 位置 |
|------|----------|
| `.baoyu-skills/baoyu-comic/EXTEND.md` | 项目目录 |
| `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 用户主目录 |

| 结果 | 动作 |
|--------|--------|
| 已找到 | 读取、解析、展示摘要 → 继续 |
| 未找到 | ⛔ **阻塞**：仅运行首次设置（[references/config/first-time-setup.md](references/config/first-time-setup.md)）→ 完成并保存 EXTEND.md → 再继续 |

**EXTEND.md 支持**：水印 | 偏好画风/基调/布局 | 自定义风格定义 | 角色预设 | 语言偏好

Schema：[references/config/preferences-schema.md](references/config/preferences-schema.md)

## 参考文档

**核心模板**：
- [analysis-framework.md](references/analysis-framework.md) - 深度内容分析
- [character-template.md](references/character-template.md) - 角色定义格式
- [storyboard-template.md](references/storyboard-template.md) - 分镜结构
- [ohmsha-guide.md](references/ohmsha-guide.md) - Ohmsha 日漫专项

**风格定义**：
- `references/art-styles/` - 画风（ligne-claire、manga、realistic、ink-brush、chalk）
- `references/tones/` - 基调（neutral、warm、dramatic、romantic、energetic、vintage、action）
- `references/presets/` - 带特殊规则的预设（ohmsha、wuxia、shoujo）
- `references/layouts/` - 布局（standard、cinematic、dense、splash、mixed、webtoon）

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
|--------|-------|
| **编辑** | **先更新提示词文件** → `--regenerate N` → 重新生成 PDF |
| **新增** | 在指定位置创建提示词 → 带角色参考生成 → 重排后续页码 → 更新分镜 → 重新生成 PDF |
| **删除** | 删除文件 → 重排后续页码 → 更新分镜 → 重新生成 PDF |

**重要**：更新页面时，务必在重新生成之前先更新提示词文件（`prompts/NN-{cover|page}-[slug].md`），以确保变更有记录且可复现。

## 备注

- 图像生成：每页约 10–30 秒
- 生成失败自动重试一次
- 敏感公众人物使用风格化替代表现
- 通过 session ID 保持风格一致
- **步骤 2 确认必需** — 不可跳过
- **步骤 4/6 为条件性** — 仅在步骤 2 中用户要求时执行
- **步骤 7.1 必须先于各页生成角色表** — 确保一致性
- **步骤 7.2 每一页必须引用角色** — 使用 `--ref` 或嵌入描述
- 水印/语言在 EXTEND.md 中一次性配置
