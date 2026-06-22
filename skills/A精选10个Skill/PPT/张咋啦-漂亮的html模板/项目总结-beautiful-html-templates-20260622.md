# 项目总结：张咋啦-漂亮的html模板

> 整理日期：2026-06-22  
> 项目路径：`skills/精选10个Skill/设计/张咋啦-漂亮的html模板/beautiful-html-templates-main/`  
> 上游仓库：[zarazhangrui/beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates)

---

## 一句话概括

**一套给 AI 编程助手用的 HTML 幻灯片模板库**——让 Agent 根据你的场景和风格，自动选模板、填内容，生成可直接在浏览器里演示的精美 HTML 幻灯片。

---

## 核心用途

| 维度 | 说明 |
|------|------|
| **目标用户** | 主要是 **Coding Agent**（Cursor、Claude Code 等），不是给人手写 HTML 的 |
| **产出物** | 单文件或文件夹形式的 **HTML 幻灯片 Deck**（16:9，1920×1080 舞台缩放） |
| **模板数量** | **34 套**风格各异的视觉模板 |
| **许可证** | MIT，可自由使用、修改、分发 |

---

## 项目结构

```
beautiful-html-templates-main/
├── AGENTS.md          # Agent 操作手册（核心工作流）
├── index.json         # 34 套模板的元数据索引（mood、occasion、tone 等）
├── templates/         # 每套模板一个文件夹
│   └── <slug>/
│       ├── template.html   # 完整示例幻灯片
│       ├── template.json   # 模板元数据
│       ├── design.md       # 设计系统说明（配色、字体、组件语法）
│       └── deck-stage.js   # 翻页运行时（方向键、空格等）
├── runtime/           # 共享运行时
└── screenshots/       # 各模板预览截图
```

---

## Agent 工作流程（`AGENTS.md` 规定）

1. **先问用户**：场合（pitch、研究报告、品牌宣言等）+ 想要的氛围（沉稳、活泼、暗黑等）
2. **读 `index.json`**：按 mood / occasion / tone 匹配，选出 **3 个候选模板**
3. **生成封面预览**：用用户真实标题做 3 个标题页 HTML，在浏览器打开供对比
4. **用户选定后**：克隆整套模板，替换占位内容，按需增删幻灯片
5. **交付**：在浏览器打开最终 deck，把文件路径发给用户

---

## 模板风格举例

34 套覆盖多种审美，例如：

- **Soft Editorial** — 暖纸色 + 衬线，文艺杂志感
- **Blue Professional** — 奶油底 + 钴蓝，商务专业
- **8-Bit Orbit** — 像素霓虹，赛博/游戏风
- **Retro Windows** — Win95 怀旧界面
- **Bold Poster** — 大字报 + 鲜红强调色
- **Sakura Chroma** — 日式磁带包装美学
- **Scatterbrain** — 便利贴手写风

每套模板都带有 `design.md`，定义配色、字体、间距、装饰元素，方便 Agent 在缺布局时按同一设计系统扩展新幻灯片。

---

## 和「张咋啦PPT」的关系

同仓库里还有 `skills/精选10个Skill/PPT/张咋啦PPT/frontend-slides/`，是同一作者的另一套 **frontend-slides** 技能，侧重 PPT 生成流程。  
**beautiful-html-templates** 更偏「模板库 + 选版工作流」，两者视觉体系有重叠（如 bold-template-pack），但本项目的核心是 **34 套可克隆的 HTML 模板 + Agent 操作规范**。

---

## 典型使用方式

把下面这段话丢给 Coding Agent 即可：

```
Clone https://github.com/zarazhangrui/beautiful-html-templates 
and follow the instructions in AGENTS.md to build me a beautiful HTML slide deck.
```

Agent 会按 `AGENTS.md` 问场合、选模板、生成 deck。

---

## 总结

这不是普通 UI 组件库，而是 **「AI 做漂亮幻灯片」的设计资产包**——预置 34 种高审美 HTML 模板 + 结构化元数据 + Agent 标准流程，让 AI 能自动选风格、填内容、产出可演示的 HTML 幻灯片，避免千篇一律的「AI 味」页面。
