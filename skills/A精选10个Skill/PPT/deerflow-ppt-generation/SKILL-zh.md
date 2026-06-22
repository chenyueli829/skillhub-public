---
name: ppt-generation
description: 当用户请求生成、创建或制作演示文稿（PPT/PPTX）时使用此技能。通过为每张幻灯片生成图像并将它们组合成 PowerPoint 文件来创建视觉丰富的幻灯片。
---

# PPT 生成技能

## 概述

此技能通过为每张幻灯片创建 AI 生成的图像并将它们组合成 PPTX 文件来生成专业的 PowerPoint 演示文稿。工作流程包括规划具有一致视觉风格的演示文稿结构、按顺序生成幻灯片图像（使用上一张幻灯片作为风格一致性的参考），以及将它们组装成最终的演示文稿。

## 核心能力

- 规划和构建具有统一视觉风格的多幻灯片演示文稿
- 支持多种演示风格：商务、学术、极简、Apple Keynote、创意
- 使用 image-generation 技能为每张幻灯片生成独特的 AI 图像
- 通过使用上一张幻灯片作为参考图像来保持视觉一致性
- 将图像组合成专业的 PPTX 文件

## 演示风格

创建演示文稿计划时，选择以下风格之一：

| 风格 | 描述 | 最适用于 |
|------|------|----------|
| **glassmorphism** | 磨砂玻璃面板搭配模糊效果，浮动半透明卡片，鲜艳渐变背景，通过层叠产生深度 | 科技产品、AI/SaaS 演示、未来感推介 |
| **dark-premium** | 深黑色背景（#0a0a0a），发光的强调色，微妙的光晕效果，奢华品牌美学 | 高端产品、高管演示、高端品牌 |
| **gradient-modern** | 大胆的网格渐变，流畅的色彩过渡，现代排版，鲜艳而不失精致 | 初创公司、创意机构、品牌发布 |
| **neo-brutalist** | 粗犷大胆的排版，高对比度，刻意的"丑陋"美学，反设计即设计，孟菲斯风格启发 | 前卫品牌、Z 世代定位、颠覆性初创公司 |
| **3d-isometric** | 简洁的等距插图，浮动 3D 元素，柔和阴影，技术前沿美学 | 技术讲解、产品功能、SaaS 演示文稿 |
| **editorial** | 杂志级排版，精致的排版层次，戏剧性摄影，Vogue/Bloomberg 美学 | 年度报告、奢侈品牌、思想领导力 |
| **minimal-swiss** | 基于网格的精确排版，Helvetica 风格排版，大胆使用负空间，永恒的现代主义 | 建筑、设计公司、高端咨询 |
| **keynote** | Apple 风格美学，大胆排版，戏剧性画面，高对比度，电影感 | 主题演讲、产品发布、励志演讲 |

## 工作流程

### 步骤 1：理解需求

当用户请求生成演示文稿时，识别以下信息：

- 主题/内容：演示文稿是关于什么的
- 幻灯片数量：需要多少张幻灯片（默认：5-10）
- **风格**：business / academic / minimal / keynote / creative
- 宽高比：标准（16:9）或经典（4:3）
- 内容大纲：每张幻灯片的要点
- 你不需要检查 `/mnt/user-data` 下的文件夹

### 步骤 2：创建演示文稿计划

在 `/mnt/user-data/workspace/` 中创建一个包含演示文稿结构的 JSON 文件。**重要**：包含 `style` 字段以定义整体视觉一致性。

```json
{
  "title": "Presentation Title",
  "style": "keynote",
  "style_guidelines": {
    "color_palette": "Deep black backgrounds, white text, single accent color (blue or orange)",
    "typography": "Bold sans-serif headlines, clean body text, dramatic size contrast",
    "imagery": "High-quality photography, full-bleed images, cinematic composition",
    "layout": "Generous whitespace, centered focus, minimal elements per slide"
  },
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Main Title",
      "subtitle": "Subtitle or tagline",
      "visual_description": "Detailed description for image generation"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "Slide Title",
      "key_points": ["Point 1", "Point 2", "Point 3"],
      "visual_description": "Detailed description for image generation"
    }
  ]
}
```

### 步骤 3：按顺序生成幻灯片图像

**重要**：**严格按顺序逐张**生成幻灯片。不要并行化或批量生成图像。每张幻灯片都依赖于上一张幻灯片的输出作为参考图像。并行生成幻灯片会破坏视觉一致性，这是不允许的。

1. 阅读 image-generation 技能：`/mnt/skills/public/image-generation/SKILL.md`

2. **对于第一张幻灯片（幻灯片 1）**，创建一个建立视觉风格的提示词：

```json
{
  "prompt": "Professional presentation slide. [style_guidelines from plan]. Title: 'Your Title'. [visual_description]. This slide establishes the visual language for the entire presentation.",
  "style": "[Based on chosen style - e.g., Apple Keynote aesthetic, dramatic lighting, cinematic]",
  "composition": "Clean layout with clear text hierarchy, [style-specific composition]",
  "color_palette": "[From style_guidelines]",
  "typography": "[From style_guidelines]"
}
```

```bash
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/slide-01-prompt.json \
  --output-file /mnt/user-data/outputs/slide-01.jpg \
  --aspect-ratio 16:9
```

3. **对于后续幻灯片（幻灯片 2+）**，使用上一张幻灯片作为参考图像：

```json
{
  "prompt": "Professional presentation slide continuing the visual style from the reference image. Maintain the same color palette, typography style, and overall aesthetic. Title: 'Slide Title'. [visual_description]. Keep visual consistency with the reference.",
  "style": "Match the style of the reference image exactly",
  "composition": "Similar layout principles as reference, adapted for this content",
  "color_palette": "Same as reference image",
  "consistency_note": "This slide must look like it belongs in the same presentation as the reference image"
}
```

```bash
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/slide-02-prompt.json \
  --reference-images /mnt/user-data/outputs/slide-01.jpg \
  --output-file /mnt/user-data/outputs/slide-02.jpg \
  --aspect-ratio 16:9
```

4. **继续为所有剩余幻灯片执行此操作**，始终引用上一张幻灯片：

```bash
# 幻灯片 3 引用幻灯片 2
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/slide-03-prompt.json \
  --reference-images /mnt/user-data/outputs/slide-02.jpg \
  --output-file /mnt/user-data/outputs/slide-03.jpg \
  --aspect-ratio 16:9

# 幻灯片 4 引用幻灯片 3
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/slide-04-prompt.json \
  --reference-images /mnt/user-data/outputs/slide-03.jpg \
  --output-file /mnt/user-data/outputs/slide-04.jpg \
  --aspect-ratio 16:9
```

### 步骤 4：组合 PPT

在所有幻灯片图像生成完成后，调用组合脚本：

```bash
python /mnt/skills/public/ppt-generation/scripts/generate.py \
  --plan-file /mnt/user-data/workspace/presentation-plan.json \
  --slide-images /mnt/user-data/outputs/slide-01.jpg /mnt/user-data/outputs/slide-02.jpg /mnt/user-data/outputs/slide-03.jpg \
  --output-file /mnt/user-data/outputs/presentation.pptx
```

参数说明：

- `--plan-file`：演示文稿计划 JSON 文件的绝对路径（必需）
- `--slide-images`：按顺序排列的幻灯片图像的绝对路径（必需，空格分隔）
- `--output-file`：输出 PPTX 文件的绝对路径（必需）

[!NOTE]
不要读取 python 文件，直接使用参数调用它。

## 完整示例：Glassmorphism 风格（最现代前卫）

用户请求："创建一个关于 AI 产品发布的演示文稿"

### 步骤 1：创建演示文稿计划

创建 `/mnt/user-data/workspace/ai-product-plan.json`：
```json
{
  "title": "Introducing Nova AI",
  "style": "glassmorphism",
  "style_guidelines": {
    "color_palette": "Vibrant purple-to-cyan gradient background (#667eea→#00d4ff), frosted glass panels with 15-20% white opacity, electric accents",
    "typography": "SF Pro Display style, bold 700 weight white titles with subtle text-shadow, clean 400 weight body text, excellent contrast on glass",
    "imagery": "Abstract 3D glass spheres, floating translucent geometric shapes, soft luminous orbs, depth through layered transparency",
    "layout": "Centered frosted glass cards with 32px rounded corners, 48-64px padding, floating above gradient, layered depth with soft shadows",
    "effects": "Backdrop blur 20-40px on glass panels, subtle white border glow, soft colored shadows matching gradient, light refraction effects",
    "visual_language": "Apple Vision Pro / visionOS aesthetic, premium depth through transparency, futuristic yet approachable, 2024 design trends"
  },
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Introducing Nova AI",
      "subtitle": "Intelligence, Reimagined",
      "visual_description": "Stunning gradient background flowing from deep purple (#667eea) through magenta to cyan (#00d4ff). Center: large frosted glass panel with strong backdrop blur, containing bold white title 'Introducing Nova AI' and lighter subtitle. Floating 3D glass spheres and abstract shapes around the card creating depth. Soft glow emanating from behind the glass panel. Premium visionOS aesthetic. The glass card has subtle white border (1px rgba 255,255,255,0.3) and soft purple-tinted shadow."
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "Why Nova?",
      "key_points": ["10x faster processing", "Human-like understanding", "Enterprise-grade security"],
      "visual_description": "Same purple-cyan gradient background. Left side: floating frosted glass card with title 'Why Nova?' in bold white, three key points below with subtle glass pill badges. Right side: abstract 3D visualization of neural network as interconnected glass nodes with soft glow. Floating translucent geometric shapes (icosahedrons, tori) adding depth. Consistent glassmorphism aesthetic with previous slide."
    },
    {
      "slide_number": 3,
      "type": "content",
      "title": "How It Works",
      "key_points": ["Natural language input", "Multi-modal processing", "Instant insights"],
      "visual_description": "Gradient background consistent with previous slides. Central composition: three stacked frosted glass cards at slight angles showing the workflow steps, connected by soft glowing lines. Each card has an abstract icon. Floating glass orbs and light particles around the composition. Title 'How It Works' in bold white at top. Depth created through card layering and transparency."
    },
    {
      "slide_number": 4,
      "type": "content",
      "title": "Built for Scale",
      "key_points": ["1M+ concurrent users", "99.99% uptime", "Global infrastructure"],
      "visual_description": "Same gradient background. Asymmetric layout: right side features large frosted glass panel with metrics displayed in bold typography. Left side: abstract 3D globe made of glass panels and connection lines, representing global scale. Floating data visualization elements as small glass cards with numbers. Soft ambient glow throughout. Premium tech aesthetic."
    },
    {
      "slide_number": 5,
      "type": "conclusion",
      "title": "The Future Starts Now",
      "subtitle": "Join the waitlist",
      "visual_description": "Dramatic finale slide. Gradient background with slightly increased vibrancy. Central frosted glass card with bold title 'The Future Starts Now' and call-to-action subtitle. Behind the card: burst of soft light rays and floating glass particles creating celebration effect. Multiple layered glass shapes creating depth. The most visually impactful slide while maintaining style consistency."
    }
  ]
}
```

### 步骤 2：阅读 image-generation 技能

阅读 `/mnt/skills/public/image-generation/SKILL.md` 以了解如何生成图像。

### 步骤 3：使用参考链式方法按顺序生成幻灯片图像

**幻灯片 1 - 标题（建立视觉语言）：**

创建 `/mnt/user-data/workspace/nova-slide-01.json`：
```json
{
  "prompt": "Ultra-premium presentation title slide with glassmorphism design. Background: smooth flowing gradient from deep purple (#667eea) through magenta (#f093fb) to cyan (#00d4ff), soft and vibrant. Center: large frosted glass panel with strong backdrop blur effect, rounded corners 32px, containing bold white sans-serif title 'Introducing Nova AI' (72pt, SF Pro Display style, font-weight 700) with subtle text shadow, subtitle 'Intelligence, Reimagined' below in lighter weight. The glass panel has subtle white border (1px rgba 255,255,255,0.25) and soft purple-tinted drop shadow. Floating around the card: 3D glass spheres with refraction, translucent geometric shapes (icosahedrons, abstract blobs), creating depth and dimension. Soft luminous glow emanating from behind the glass panel. Small floating particles of light. Apple Vision Pro / visionOS UI aesthetic. Professional presentation slide, 16:9 aspect ratio. Hyper-modern, premium tech product launch feel.",
  "style": "Glassmorphism, visionOS aesthetic, Apple Vision Pro UI style, premium tech, 2024 design trends",
  "composition": "Centered glass card as focal point, floating 3D elements creating depth at edges, 40% negative space, clear visual hierarchy",
  "lighting": "Soft ambient glow from gradient, light refraction through glass elements, subtle rim lighting on 3D shapes",
  "color_palette": "Purple gradient #667eea, magenta #f093fb, cyan #00d4ff, frosted white rgba(255,255,255,0.15), pure white text #ffffff",
  "effects": "Backdrop blur on glass panels, soft drop shadows with color tint, light refraction, subtle noise texture on glass, floating particles"
}
```

```bash
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/nova-slide-01.json \
  --output-file /mnt/user-data/outputs/nova-slide-01.jpg \
  --aspect-ratio 16:9
```

**幻灯片 2 - 内容（必须引用幻灯片 1 以保持一致性）：**

创建 `/mnt/user-data/workspace/nova-slide-02.json`：
```json
{
  "prompt": "Presentation slide continuing EXACT visual style from reference image. SAME purple-to-cyan gradient background, SAME glassmorphism aesthetic, SAME typography style. Left side: frosted glass card with backdrop blur containing title 'Why Nova?' in bold white (matching reference font style), three feature points as subtle glass pill badges below. Right side: abstract 3D neural network visualization made of interconnected glass nodes with soft cyan glow, floating in space. Floating translucent geometric shapes (matching style from reference) adding depth. The frosted glass has identical treatment: white border, purple-tinted shadow, same blur intensity. CRITICAL: This slide must look like it belongs in the exact same presentation as the reference image - same colors, same glass treatment, same overall aesthetic.",
  "style": "MATCH REFERENCE EXACTLY - Glassmorphism, visionOS aesthetic, same visual language",
  "composition": "Asymmetric split: glass card left (40%), 3D visualization right (40%), breathing room between elements",
  "color_palette": "EXACTLY match reference: purple #667eea, cyan #00d4ff gradient, same frosted white treatment, same text white",
  "consistency_note": "CRITICAL: Must be visually identical in style to reference image. Same gradient colors, same glass blur intensity, same shadow treatment, same typography weight and style. Viewer should immediately recognize this as the same presentation."
}
```

```bash
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/nova-slide-02.json \
  --reference-images /mnt/user-data/outputs/nova-slide-01.jpg \
  --output-file /mnt/user-data/outputs/nova-slide-02.jpg \
  --aspect-ratio 16:9
```

**幻灯片 3-5：继续相同模式，每张引用上一张幻灯片**

后续幻灯片的关键一致性规则：
- 始终在提示词中包含"continuing EXACT visual style from reference image"
- 指定"SAME gradient background"、"SAME glass treatment"、"SAME typography"
- 包含强调风格匹配的 `consistency_note`
- 引用紧邻的上一张幻灯片图像

### 步骤 4：组合最终 PPT

```bash
python /mnt/skills/public/ppt-generation/scripts/generate.py \
  --plan-file /mnt/user-data/workspace/nova-plan.json \
  --slide-images /mnt/user-data/outputs/nova-slide-01.jpg /mnt/user-data/outputs/nova-slide-02.jpg /mnt/user-data/outputs/nova-slide-03.jpg /mnt/user-data/outputs/nova-slide-04.jpg /mnt/user-data/outputs/nova-slide-05.jpg \
  --output-file /mnt/user-data/outputs/nova-presentation.pptx
```

## 风格专属指南

### Glassmorphism 风格（推荐 - 最现代前卫）
```json
{
  "style": "glassmorphism",
  "style_guidelines": {
    "color_palette": "Vibrant gradient backgrounds (purple #667eea to pink #f093fb, or cyan #4facfe to blue #00f2fe), frosted white panels with 20% opacity, accent colors that pop against the gradient",
    "typography": "SF Pro Display or Inter font style, bold 600-700 weight titles, clean 400 weight body, white text with subtle drop shadow for readability on glass",
    "imagery": "Abstract 3D shapes floating in space, soft blurred orbs, geometric primitives with glass material, depth through overlapping translucent layers",
    "layout": "Floating card panels with backdrop-blur effect, generous padding (48-64px), rounded corners (24-32px radius), layered depth with subtle shadows",
    "effects": "Frosted glass blur (backdrop-filter: blur 20px), subtle white border (1px rgba 255,255,255,0.2), soft glow behind panels, floating elements with drop shadows",
    "visual_language": "Premium tech aesthetic like Apple Vision Pro UI, depth through transparency, light refracting through glass surfaces"
  }
}
```

### Dark Premium 风格
```json
{
  "style": "dark-premium",
  "style_guidelines": {
    "color_palette": "Deep black base (#0a0a0a to #121212), luminous accent color (electric blue #00d4ff, neon purple #bf5af2, or gold #ffd700), subtle gray gradients for depth (#1a1a1a to #0a0a0a)",
    "typography": "Elegant sans-serif (Neue Haas Grotesk or Suisse Int'l style), dramatic size contrast (72pt+ headlines, 18pt body), letter-spacing -0.02em for headlines, pure white (#ffffff) text",
    "imagery": "Dramatic studio lighting, rim lights and edge glow, cinematic product shots, abstract light trails, premium material textures (brushed metal, matte surfaces)",
    "layout": "Generous negative space (60%+), asymmetric balance, content anchored to grid but with breathing room, single focal point per slide",
    "effects": "Subtle ambient glow behind key elements, light bloom effects, grain texture overlay (2-3% opacity), vignette on edges",
    "visual_language": "Luxury tech brand aesthetic (Bang & Olufsen, Porsche Design), sophistication through restraint, every element intentional"
  }
}
```

### Gradient Modern 风格
```json
{
  "style": "gradient-modern",
  "style_guidelines": {
    "color_palette": "Bold mesh gradients (Stripe/Linear style: purple-pink-orange #7c3aed→#ec4899→#f97316, or cool tones: cyan-blue-purple #06b6d4→#3b82f6→#8b5cf6), white or dark text depending on background intensity",
    "typography": "Modern geometric sans-serif (Satoshi, General Sans, or Clash Display style), variable font weights, oversized bold headlines (80pt+), comfortable body text (20pt)",
    "imagery": "Abstract fluid shapes, morphing gradients, 3D rendered abstract objects, soft organic forms, floating geometric primitives",
    "layout": "Dynamic asymmetric compositions, overlapping elements with blend modes, text integrated with gradient flows, full-bleed backgrounds",
    "effects": "Smooth gradient transitions, subtle noise texture (3-5% for depth), soft shadows with color tint matching gradient, motion blur suggesting movement",
    "visual_language": "Contemporary SaaS aesthetic (Stripe, Linear, Vercel), energetic yet professional, forward-thinking tech vibes"
  }
}
```

### Neo-Brutalist 风格
```json
{
  "style": "neo-brutalist",
  "style_guidelines": {
    "color_palette": "High contrast primaries: stark black, pure white, with bold accent (hot pink #ff0080, electric yellow #ffff00, or raw red #ff0000), optional: Memphis-inspired pastels as secondary",
    "typography": "Ultra-bold condensed type (Impact, Druk, or Bebas Neue style), UPPERCASE headlines, extreme size contrast, intentionally tight or overlapping letter-spacing",
    "imagery": "Raw unfiltered photography, intentional visual noise, halftone patterns, cut-out collage aesthetic, hand-drawn elements, stickers and stamps",
    "layout": "Broken grid, overlapping elements, thick black borders (4-8px), visible structure, anti-whitespace (dense but organized chaos)",
    "effects": "Hard shadows (no blur, offset 8-12px), pixelation accents, scan lines, CRT screen effects, intentional 'mistakes'",
    "visual_language": "Anti-corporate rebellion, DIY zine aesthetic meets digital, raw authenticity, memorable through boldness"
  }
}
```

### 3D Isometric 风格
```json
{
  "style": "3d-isometric",
  "style_guidelines": {
    "color_palette": "Soft contemporary palette: muted purples (#8b5cf6), teals (#14b8a6), warm corals (#fb7185), with cream or light gray backgrounds (#fafafa), consistent saturation across elements",
    "typography": "Friendly geometric sans-serif (Circular, Gilroy, or Quicksand style), medium weight headlines, excellent readability, comfortable 24pt body text",
    "imagery": "Clean isometric 3D illustrations, consistent 30° isometric angle, soft clay-render aesthetic, floating platforms and devices, cute simplified objects",
    "layout": "Central isometric scene as hero, text balanced around 3D elements, clear visual hierarchy, comfortable margins (64px+)",
    "effects": "Soft drop shadows (20px blur, 30% opacity), ambient occlusion on 3D objects, subtle gradients on surfaces, consistent light source (top-left)",
    "visual_language": "Friendly tech illustration (Slack, Notion, Asana style), approachable complexity, clarity through simplification"
  }
}
```

### Editorial 风格
```json
{
  "style": "editorial",
  "style_guidelines": {
    "color_palette": "Sophisticated neutrals: off-white (#f5f5f0), charcoal (#2d2d2d), with single accent color (burgundy #7c2d12, forest #14532d, or navy #1e3a5f), occasional full-color photography",
    "typography": "Refined serif for headlines (Playfair Display, Freight, or Editorial New style), clean sans-serif for body (Söhne, Graphik), dramatic size hierarchy (96pt headlines, 16pt body), generous line-height 1.6",
    "imagery": "Magazine-quality photography, dramatic crops, full-bleed images, portraits with intentional negative space, editorial lighting (Vogue, Bloomberg Businessweek style)",
    "layout": "Sophisticated grid system (12-column), intentional asymmetry, pull quotes as design elements, text wrapping around images, elegant margins",
    "effects": "Minimal effects - let photography and typography shine, subtle image treatments (slight desaturation, film grain), elegant borders and rules",
    "visual_language": "High-end magazine aesthetic, intellectual sophistication, content elevated through design restraint"
  }
}
```

### Minimal Swiss 风格
```json
{
  "style": "minimal-swiss",
  "style_guidelines": {
    "color_palette": "Pure white (#ffffff) or off-white (#fafaf9) backgrounds, true black (#000000) text, single bold accent (Swiss red #ff0000, Klein blue #002fa7, or signal yellow #ffcc00)",
    "typography": "Helvetica Neue or Aktiv Grotesk, strict type scale (12/16/24/48/96), medium weight for body, bold for emphasis only, flush-left ragged-right alignment",
    "imagery": "Objective photography, geometric shapes, clean iconography, mathematical precision, intentional empty space as compositional element",
    "layout": "Strict grid adherence (baseline grid visible in spirit), modular compositions, generous whitespace (40%+ of slide), content aligned to invisible grid lines",
    "effects": "None - purity of form, no shadows, no gradients, no decorative elements, occasional single hairline rules",
    "visual_language": "International Typographic Style, form follows function, timeless modernism, Dieter Rams-inspired restraint"
  }
}
```

### Keynote 风格（Apple 风格）
```json
{
  "style": "keynote",
  "style_guidelines": {
    "color_palette": "Deep blacks (#000000 to #1d1d1f), pure white text, signature blue (#0071e3) or gradient accents (purple-pink for creative, blue-teal for tech)",
    "typography": "San Francisco Pro Display, extreme weight contrast (bold 80pt+ titles, light 24pt body), negative letter-spacing on headlines (-0.03em), optical alignment",
    "imagery": "Cinematic photography, shallow depth of field, dramatic lighting (rim lights, spot lighting), product hero shots with reflections, full-bleed imagery",
    "layout": "Maximum negative space, single powerful image or statement per slide, content centered or dramatically offset, no clutter",
    "effects": "Subtle gradient overlays, light bloom and glow on key elements, reflection on surfaces, smooth gradient backgrounds",
    "visual_language": "Apple WWDC keynote aesthetic, confidence through simplicity, every pixel considered, theatrical presentation"
  }
}
```

## 输出处理

生成完成后：

- PPTX 文件保存在 `/mnt/user-data/outputs/`
- 使用 `present_files` 工具将生成的演示文稿分享给用户
- 如有请求，也分享单独的幻灯片图像
- 提供演示文稿的简要描述
- 如需迭代或重新生成特定幻灯片，提供相应选项

## 注意事项

### 关键质量指南

**提示词工程以获得专业效果：**
- 无论用户使用什么语言，图像提示词始终使用英文
- 对视觉细节要**极其具体**——模糊的提示词会产生通用的结果
- 包含精确的十六进制颜色代码（例如 #667eea 而不是"紫色"）
- 指定排版细节：字重（400/700）、大小层次、字间距
- 精确描述效果："backdrop blur 20px"、"drop shadow 8px blur 30% opacity"
- 引用真实的设计系统："visionOS aesthetic"、"Stripe website style"、"Bloomberg Businessweek layout"

**视觉一致性（最重要）：**
- **按顺序生成幻灯片** — 每张幻灯片必须引用上一张
- 第一张幻灯片至关重要——它为整个演示文稿建立视觉语言
- 在每个后续幻灯片的提示词中，明确声明："continuing EXACT visual style from reference image"
- 在提示词中强调使用 SAME、EXACT、MATCH 关键词以强制一致性
- 在幻灯片 1 之后的每个 JSON 提示词中包含 `consistency_note` 字段
- 如果某张幻灯片看起来不一致，用更强的参考强调重新生成

**现代美学设计原则：**
- 拥抱负空间——40-60% 的空白营造高端感
- 限制每张幻灯片的元素数量——一个焦点，一条信息
- 通过层叠创造深度（阴影、透明度、z 轴深度）
- 排版层次：超大标题（72pt+），舒适的正文（18-24pt）
- 色彩克制：一个主色调，最多 1-2 个强调色

**常见错误避免：**
- ❌ 通用提示词如"professional slide"——要具体
- ❌ 每张幻灯片元素/文字过多——杂乱=不专业
- ❌ 幻灯片之间颜色不一致——始终引用上一张幻灯片
- ❌ 跳过参考图像参数——这会破坏视觉一致性
- ❌ 在一个演示文稿中使用不同的设计风格
- ❌ 并行生成幻灯片——幻灯片必须按顺序逐张生成（幻灯片 1 → 2 → 3...），绝不能同时进行

**不同场景的推荐风格：**
- 科技产品发布 → `glassmorphism` 或 `gradient-modern`
- 奢华/高端品牌 → `dark-premium` 或 `editorial`
- 初创公司路演 → `gradient-modern` 或 `minimal-swiss`
- 高管演示 → `dark-premium` 或 `keynote`
- 创意机构 → `neo-brutalist` 或 `gradient-modern`
- 数据/分析 → `minimal-swiss` 或 `3d-isometric`
