---
name: algorithmic-art
description: 使用 p5.js 创建算法艺术，支持种子随机数与交互式参数探索。当用户请求用代码创作艺术、生成艺术、算法艺术、流场或粒子系统时使用。应创作原创算法艺术，而非复制现有艺术家作品，以避免版权侵权。
license: 完整条款见 LICENSE.txt
---

算法哲学（algorithmic philosophies）是一种计算美学运动，随后通过代码加以表达。产出包括：`.md` 文件（哲学阐述）、`.html` 文件（交互式查看器）、`.js` 文件（生成式算法）。

流程分为两步：
1. 算法哲学创作（`.md` 文件）
2. 通过 p5.js 生成艺术进行表达（`.html` + `.js` 文件）

首先，执行以下任务：

## 算法哲学创作

开始时，创建一种**算法哲学**（不是静态图像或模板），它将通过以下方式被诠释：
- 计算过程、涌现行为、数学之美
- 种子随机数、噪声场、有机系统
- 粒子、流动、场、力
- 参数化变化与受控混沌

### 关键理解
- **接收到的**：用户提供的细微输入或指示，作为基础参考，但不应限制创作自由。
- **创建的**：一种算法哲学 / 生成式美学运动。
- **接下来发生的**：同一版本接收该哲学，并**用代码表达**——创建 90% 为算法生成、10% 为必要参数的 p5.js 草图。

可参考这一思路：
- 为一场生成艺术运动撰写宣言
- 下一阶段编写让其实现的算法

哲学必须强调：**算法表达**、**涌现行为**、**计算之美**、**种子变化**。

### 如何生成算法哲学

**为运动命名**（1–2 个词）：如「Organic Turbulence（有机湍流）」/「Quantum Harmonics（量子谐波）」/「Emergent Stillness（涌现静止）」

**阐述哲学**（4–6 段——简洁但完整）：

为捕捉**算法本质**，说明该哲学如何通过以下方式体现：
- 计算过程与数学关系？
- 噪声函数与随机模式？
- 粒子行为与场动力学？
- 时间演化与系统状态？
- 参数变化与涌现复杂性？

**关键准则：**
- **避免冗余**：每个算法方面只提一次。除非增加新深度，否则不要重复噪声理论、粒子动力学或数学原理等概念。
- **反复强调工艺水准**：哲学**必须多次强调**最终算法应看起来像是经过无数小时开发、精心打磨、出自该领域顶尖高手之手。这一 framing 至关重要——重复使用如「meticulously crafted algorithm（精心打磨的算法）」「the product of deep computational expertise（深厚计算 expertise 的产物）」「painstaking optimization（ painstaking 优化）」「master-level implementation（大师级实现）」等表述。
- **保留创作空间**：对算法方向要具体，但要足够简洁，让下一版 Claude 有空间在极高工艺水准下做诠释性实现选择。

哲学必须引导下一版本**以算法方式**表达思想，而非通过静态图像。美存在于过程之中，而非最终帧。

### 哲学示例

**「Organic Turbulence（有机湍流）」**
哲学：受自然法则约束的混沌，从无序中涌现秩序。
算法表达：由多层 Perlin 噪声驱动的流场。数千粒子沿向量力运动，轨迹累积成有机密度图。多倍噪声 octave 形成湍流区与平静区。颜色由速度与密度涌现——快粒子明亮，慢粒子沉入阴影。算法运行至平衡——一种 meticulously tuned 的平衡，每个参数都经过无数迭代由计算美学大师 refine。

**「Quantum Harmonics（量子谐波）」**
哲学：离散实体呈现波状干涉图样。
算法表达：粒子在网格上初始化，各携带随正弦波演化的相位值。粒子靠近时相位干涉——相长干涉形成亮节点，相消形成 void。简谐运动生成复杂涌现曼陀罗。 painstaking 频率校准的结果，每个比率都 carefully chosen 以产生 resonant beauty。

**「Recursive Whispers（递归低语）」**
哲学：跨尺度的自相似，有限空间中的无限深度。
算法表达：递归细分的 branching 结构。每根 branch 略随机但受 golden ratio 约束。L-system 或递归细分生成既数学又有机的树状形态。 subtle 噪声扰动打破完美对称。线宽随递归层级递减。每个 branching 角都是 deep mathematical exploration 的产物。

**「Field Dynamics（场动力学）」**
哲学：通过物质上的效应使 invisible forces 可见。
算法表达：由数学函数或噪声构造的 vector field。粒子在边缘诞生，沿 field line 流动，到达平衡或边界时消亡。多个场可吸引、排斥或旋转粒子。可视化只显示轨迹—— invisible forces 的 ghost-like 证据。通过 force balance meticulously choreographed 的计算之舞。

**「Stochastic Crystallization（随机结晶）」**
哲学：随机过程结晶为有序结构。
算法表达：随机 circle packing 或 Voronoi tessellation。从随机点出发，经 relaxation 算法演化。细胞相互推开直至平衡。颜色基于 cell size、neighbor count 或距中心距离。涌现的有机 tiling 既 random 又 inevitable。每个 seed 产生 unique crystalline beauty——master-level generative algorithm 的 mark。

*以上为 condensed 示例。实际算法哲学应为 4–6 段 substantial 段落。*

### 核心原则
- **算法哲学**：创建一种将通过代码表达的计算世界观
- **过程重于产物**：始终强调美从算法执行中涌现——每次运行都 unique
- **参数化表达**：思想通过数学关系、力、行为传达——而非静态构图
- **艺术自由**：下一版 Claude 以算法方式诠释哲学——提供创作实现空间
- **纯生成艺术**：这是创造**活算法**，而非带随机性的静态图像
- **专家工艺**：反复强调最终算法须 feel meticulously crafted、经 countless iterations refine、出自 computational aesthetics 领域 absolute top 者之手

**算法哲学应为 4–6 段。** 用诗意的计算哲学填满，汇聚 intended vision。避免重复同一点。将此算法哲学输出为 `.md` 文件。

---

## 推导概念种子

**关键步骤**：在实现算法之前，从原始请求中识别 subtle conceptual thread。

**核心原则**：
概念是**嵌入算法本身的 subtle、niche reference**——不总是 literal，始终 sophisticated。熟悉该主题者应 intuitively feel it，其他人则 simply experience masterful generative composition。算法哲学提供计算语言。推导出的概念提供 soul——quiet conceptual DNA，invisibly woven 进 parameters、behaviors 与 emergence patterns。

这**非常重要**：reference 须足够 refined，enhance 作品深度而不 announce itself。像 jazz musician 通过 algorithmic harmony quote 另一首歌——知情者会 catch，人人欣赏 generative beauty。

---

## P5.JS 实现

在哲学与 conceptual framework 确立后，用代码表达。继续前 pause 整理思路。仅使用已创建的算法哲学与下列说明。

### ⚠️ 步骤 0：先读模板 ⚠️

**关键：写任何 HTML 之前：**

1. 用 Read 工具**阅读** `templates/viewer.html`
2. **研究**其 exact structure、styling 与 Anthropic branding
3. **以该文件为 LITERAL STARTING POINT**——不仅是 inspiration
4. **完全保留**所有 FIXED 部分（header、sidebar structure、Anthropic colors/fonts、seed controls、action buttons）
5. **仅替换**文件中注释标记的 VARIABLE 部分（algorithm、parameters、参数的 UI controls）

**避免：**
- ❌ 从零写 HTML
- ❌ 发明 custom styling 或 color schemes
- ❌ 使用 system fonts 或 dark themes
- ❌ 改变 sidebar structure

**遵循：**
- ✅ 复制模板的 exact HTML structure
- ✅ 保留 Anthropic branding（Poppins/Lora fonts、light colors、gradient backdrop）
- ✅ 维持 sidebar layout（Seed → Parameters → Colors? → Actions）
- ✅ 仅替换 p5.js algorithm 与 parameter controls

模板是 foundation。在其上 build，不要 rebuild。

---

为创造 gallery-quality、living and breathing 的计算艺术，以算法哲学为 foundation。

### 技术要求

**种子随机数（Art Blocks 模式）**：
```javascript
// ALWAYS use a seed for reproducibility
let seed = 12345; // or hash from user input
randomSeed(seed);
noiseSeed(seed);
```

**参数结构——遵循哲学**：

为建立从算法哲学自然涌现的参数，考虑：「该系统的哪些 qualities 可调？」

```javascript
let params = {
  seed: 12345,  // Always include seed for reproducibility
  // colors
  // Add parameters that control YOUR algorithm:
  // - Quantities (how many?)
  // - Scales (how big? how fast?)
  // - Probabilities (how likely?)
  // - Ratios (what proportions?)
  // - Angles (what direction?)
  // - Thresholds (when does behavior change?)
};
```

**设计有效参数时，focus 系统需要 tunable 的 properties，而非「pattern types」。**

**核心算法——表达哲学**：

**关键**：算法哲学应 dictate 构建什么。

通过代码表达哲学时，避免想「用哪种 pattern？」而应想「如何用代码表达该哲学？」

若哲学关于 **organic emergence**，可考虑：
- 随时间累积或生长的 elements
- 受 natural rules 约束的 random processes
- Feedback loops 与 interactions

若哲学关于 **mathematical beauty**，可考虑：
- Geometric relationships 与 ratios
- Trigonometric functions 与 harmonics
- 产生 unexpected patterns 的 precise calculations

若哲学关于 **controlled chaos**，可考虑：
- Strict boundaries 内的 random variation
- Bifurcation 与 phase transitions
- 从无序涌现的 order

**算法从哲学 flow，而非从 options menu。**

实现时让 conceptual essence  inform creative and original choices。构建表达该 particular request vision 的作品。

**Canvas 设置**：标准 p5.js structure：
```javascript
function setup() {
  createCanvas(1200, 1200);
  // Initialize your system
}

function draw() {
  // Your generative algorithm
  // Can be static (noLoop) or animated
}
```

### 工艺要求

**关键**：为达 mastery，创造 feel 像 master generative artist 经 countless iterations 涌现的 algorithms。Carefully tune 每个 parameter。Ensure 每个 pattern 有 purpose 地涌现。这不是 random noise——是 deep expertise refine 的 **CONTROLLED CHAOS**。

- **平衡**：Complexity 而无 visual noise，order 而无 rigidity
- **色彩和谐**：Thoughtful palettes，非 random RGB
- **构图**：即使在 randomness 中维持 visual hierarchy 与 flow
- **性能**：Smooth execution，若 animated 则 optimize 为 real-time
- **可复现性**：Same seed **始终**产生 identical output

### 输出格式

输出：
1. **算法哲学**——以 markdown 或 text 解释 generative aesthetic
2. **单一 HTML Artifact**——基于 `templates/viewer.html` 的自包含交互式生成艺术（见步骤 0 与下一节）

HTML artifact 包含一切：p5.js（来自 CDN）、algorithm、parameter controls 与 UI——全部在一个文件中，在 claude.ai artifacts 或任意 browser 中立即可用。从 template 文件起步，非从零开始。

---

## 交互式 Artifact 创作

**提醒：`templates/viewer.html` 应已阅读（见步骤 0）。以该文件为 starting point。**

为允许探索 generative art，创建 single、self-contained HTML artifact。确保在 claude.ai 或任意 browser 中立即可用——无需 setup。Everything inline embed。

### 关键：FIXED vs VARIABLE

`templates/viewer.html` 是 foundation，包含所需 exact structure 与 styling。

**FIXED（始终 exactly as shown 包含）：**
- Layout structure（header、sidebar、main canvas area）
- Anthropic branding（UI colors、fonts、gradients）
- Sidebar 中的 Seed section：
  - Seed display
  - Previous/Next buttons
  - Random button
  - Jump to seed input + Go button
- Sidebar 中的 Actions section：
  - Regenerate button
  - Reset button

**VARIABLE（为每件作品 customize）：**
- 整个 p5.js algorithm（setup/draw/classes）
- Parameters object（定义 art 所需）
- Sidebar 中的 Parameters section：
  - Parameter controls 数量
  - Parameter names
  - Sliders 的 min/max/step
  - Control types（sliders、inputs 等）
- Colors section（可选）：
  - 部分 art 需要 color pickers
  - 部分 art 可能 fixed colors
  - 部分 art 可能 monochrome（无需 color controls）
  - 按 art 需求决定

**每件 artwork 应有 unique parameters 与 algorithm！** Fixed 部分提供 consistent UX——其余表达 unique vision。

### 必需特性

**1. 参数控件**
- 数值参数的 Sliders（particle count、noise scale、speed 等）
- Palette colors 的 Color pickers
- 参数变化时 real-time updates
- Reset button 恢复 defaults

**2. 种子导航**
- 显示 current seed number
- 「Previous」「Next」按钮循环 seeds
- 「Random」按钮 random seed
- Input field jump 到 specific seed
- 请求时生成 100 个 variations（seeds 1–100）

**3. 单一 Artifact 结构**
```html
<!DOCTYPE html>
<html>
<head>
  <!-- p5.js from CDN - always available -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
  <style>
    /* All styling inline - clean, minimal */
    /* Canvas on top, controls below */
  </style>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="controls">
    <!-- All parameter controls -->
  </div>
  <script>
    // ALL p5.js code inline here
    // Parameter objects, classes, functions
    // setup() and draw()
    // UI handlers
    // Everything self-contained
  </script>
</body>
</html>
```

**关键**：这是 single artifact。无 external files、无 imports（p5.js CDN 除外）。Everything inline。

**4. 实现细节——构建 SIDEBAR**

Sidebar structure：

**1. Seed（FIXED）**——始终 exactly as shown：
- Seed display
- Prev/Next/Random/Jump buttons

**2. Parameters（VARIABLE）**——为 art 创建 controls：
```html
<div class="control-group">
    <label>Parameter Name</label>
    <input type="range" id="param" min="..." max="..." step="..." value="..." oninput="updateParam('param', this.value)">
    <span class="value-display" id="param-value">...</span>
</div>
```
按 parameter 数量添加 control-group divs。

**3. Colors（OPTIONAL/VARIABLE）**——若 art 需要 adjustable colors 则包含：
- 若用户应 control palette 则加 color pickers
- 若 art 用 fixed colors 则跳过
- 若 monochrome 则跳过

**4. Actions（FIXED）**——始终 exactly as shown：
- Regenerate button
- Reset button
- Download PNG button

**要求**：
- Seed controls 须 work（prev/next/random/jump/display）
- 所有 parameters 须有 UI controls
- Regenerate、Reset、Download buttons 须 work
- 保留 Anthropic branding（UI styling，非 art colors）

### 使用 Artifact

HTML artifact 立即可用：
1. **在 claude.ai**：作为 interactive artifact 显示——instant run
2. **作为文件**：保存并在任意 browser 打开——无需 server
3. **分享**：发送 HTML 文件——完全 self-contained

---

## 变体与探索

Artifact 默认含 seed navigation（prev/next/random buttons），用户可探索 variations 而无需多文件。若用户希望 highlight specific variations：

- 含 seed presets（如「Variation 1: Seed 42」按钮）
- 加「Gallery Mode」并排显示多 seed thumbnails
- 均在同一 single artifact 内

如同从同一 plate 创作 print series——algorithm consistent，每个 seed 揭示不同 facet。Interactive 性质让用户在 seed space 中 discover 自己的 favorites。

---

## 创作流程

**用户请求** → **算法哲学** → **实现**

每个请求 unique。流程包括：

1. **Interpret 用户 intent**——寻求何种 aesthetic？
2. **创建算法哲学**（4–6 段）描述 computational approach
3. **用代码实现**——构建表达该哲学的 algorithm
4. **设计 appropriate parameters**——什么应 tunable？
5. **构建 matching UI controls**——sliders/inputs

**常量**：
- Anthropic branding（colors、fonts、layout）
- Seed navigation（始终 present）
- Self-contained HTML artifact

**其余皆 variable**：
- Algorithm 本身
- Parameters
- UI controls
- Visual outcome

为最佳结果，trust creativity，让 philosophy guide implementation。

---

## 资源

本 skill 含 helpful templates 与 documentation：

- **templates/viewer.html**：所有 HTML artifacts 的**必需 STARTING POINT**。
  - Foundation——含 exact structure 与 Anthropic branding
  - **保持不变**：Layout structure、sidebar organization、Anthropic colors/fonts、seed controls、action buttons
  - **替换**：p5.js algorithm、parameter definitions、Parameters section 中的 UI controls
  - 文件中 extensive comments 标记 exactly 保留 vs 替换

- **templates/generator_template.js**：p5.js best practices 与 code structure principles 参考。
  - 展示如何 organize parameters、use seeded randomness、structure classes
  - **不是** pattern menu——用这些 principles 构建 unique algorithms
  - 将 algorithms inline embed 于 HTML artifact（勿创建 separate `.js` 文件）

**关键提醒**：
- **Template 是 STARTING POINT**，非 inspiration
- **Algorithm 是创造 unique 之处**
- 勿复制 flow field example——构建 philosophy 所 demand 的
- **但须**保留 template 的 exact UI structure 与 Anthropic branding
