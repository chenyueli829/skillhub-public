# 技能评测：algorithmic-art

> 生成日期：2026-06-22  
> 入口文件：`skills/anthropics-skills官方/skills/algorithmic-art/SKILL.md`  
> 版本：未标注

## 1. 介绍

**algorithmic-art** 是 Anthropic 官方 skill，用于指导 Agent 创作**原创生成式算法艺术**。它不产出静态图片模板，而是先撰写一份 4–6 段的「算法哲学」（computational aesthetic manifesto），再基于该哲学用 **p5.js** 实现可交互的生成艺术。

核心流程为两阶段：**哲学创作**（`.md`）→ **代码表达**（自包含 `.html`，内联 p5.js 算法与 UI）。哲学强调涌现行为、种子随机数、粒子/流场/噪声等计算美学；实现阶段必须基于 skill 自带的 `templates/viewer.html` 模板，保留 Anthropic 品牌 UI（侧边栏、种子导航、参数滑块、Regenerate/Reset/Download），仅替换算法与参数区。

产出物包括：算法哲学 Markdown、可在浏览器直接打开的交互式 HTML（支持 seed 切换、参数调节、PNG 下载）。Skill 要求算法具备 Art Blocks 式可复现性（`randomSeed` / `noiseSeed`），并强调工艺水准与原创性，避免复制现有艺术家作品。

## 2. 触发条件

Agent 应在用户请求**用代码创作艺术**、**生成艺术/算法艺术**、**流场/粒子系统**等场景下启用本 skill。

- **description 关键词**：algorithmic art、generative art、p5.js、flow fields、particle systems、creating art using code、seeded randomness
- **显式触发语**：
  - 中文：「帮我用代码做生成艺术」「做一个粒子流场可视化」「用 p5.js 做算法艺术」「带种子切换的交互式生成画」
  - 英文：「Create generative art with p5.js」「Build a flow field particle system」「Make algorithmic art with seed exploration」
- **场景**：需要原创、可复现、可交互调参的生成艺术；需要哲学+代码两阶段交付；需要在浏览器中即时预览
- **不适用**：静态插画/照片处理、复制特定艺术家风格、无需交互的单张 PNG、非 p5.js 技术栈（如 Three.js 专属项目且用户未要求算法艺术流程）

## 3. 提问示例

### 示例 1：基础用法——主题化生成艺术

（复制以下内容提问）

> @algorithmic-art 帮我创作一件生成艺术：主题是「深海生物发光」，要有粒子在暗色背景中缓慢漂移、偶尔亮起的交互效果，输出哲学文档和可打开的 HTML。

### 示例 2：带具体美学约束

（复制以下内容提问）

> @skills/anthropics-skills官方/skills/algorithmic-art 用「受控混沌」风格做一幅 1200×1200 的流场艺术：多层 Perlin 噪声、轨迹累积、颜色随速度变化。请先生成算法哲学，再基于 templates/viewer.html 做完整交互页面，参数至少包含粒子数量、噪声尺度、速度。

### 示例 3：探索变体与种子空间

（复制以下内容提问）

> @algorithmic-art 我想探索同一算法的不同变体：请实现「随机结晶 / Voronoi 松弛」风格的生成艺术，侧边栏保留 seed 导航，并帮我预设 seed 42、127、999 三个推荐变体按钮；另外生成 seeds 1–100 的批量预览说明（Gallery Mode 可选）。

### 示例 4：边界场景——极简单色

（复制以下内容提问）

> @algorithmic-art 做一件极简黑白、只有线条与递归分支的生成艺术（L-system 或递归细分），不需要颜色选择器，但必须有 seed 切换和至少 3 个可调参数。

## 4. 外部依赖

本 skill **不依赖** API Key、MCP、数据库或本地 npm/pip 安装。Agent 执行时需能读取 skill 目录内模板；用户打开 HTML 时需网络加载 CDN 资源。

### API / 在线服务

| 服务 | 用途 | 是否必需 | 备注 |
|------|------|----------|------|
| cdnjs.cloudflare.com | 加载 p5.js 1.7.0 | 是（打开 HTML 时） | `https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js` |
| fonts.googleapis.com / fonts.gstatic.com | 加载 Poppins、Lora 字体（Anthropic UI 品牌） | 是（打开 HTML 时） | 离线环境 UI 字体可能回退系统字体 |
| claude.ai Artifacts | 可选展示环境 | 否 | Skill 提及 artifacts 可即时运行，Cursor 中通常保存为本地 HTML |

### MCP / CLI / 系统能力

| 依赖 | 用途 | 是否必需 |
|------|------|----------|
| Cursor Read 工具（或等价文件读取） | 实现前必须阅读 `templates/viewer.html` | 是（Agent 执行 skill 时） |
| 现代浏览器 | 打开并交互 HTML artifact | 是（用户验收时） |
| 网络连接 | 加载 p5.js CDN 与 Google Fonts | 是（默认模板；可改为本地 p5 以离线） |

### 环境变量 / 凭证

| 变量名 | 用途 |
|--------|------|
| 无 | 本 skill 不要求任何环境变量或凭证 |

### skill 目录外的路径

| 路径 | 用途 |
|------|------|
| 无 | 所有模板与参考均在 skill 目录内（`templates/viewer.html`、`templates/generator_template.js`） |

### 第三方包 / 运行时

- **p5.js 1.7.0**：通过 CDN 引入，无需本地 `npm install`
- **无** Python/Node 运行时要求（除非用户自行扩展脚本）
- **许可证**：skill 含 `LICENSE.txt`（Apache 2.0），商用或分发 HTML 产出时注意遵守

**评测时需人工准备的关键项**：确保评测环境可访问 cdnjs 与 Google Fonts；Agent 侧需能读取 skill 内 `templates/viewer.html`；验收时用浏览器打开生成的 HTML，验证 seed 切换、参数滑块、Regenerate/Reset/Download 是否可用。
