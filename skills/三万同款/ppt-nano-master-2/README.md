# Super PPT — 多风格 PPT 生成 Skill

AI 驱动的多风格 PPT 生成工具，通过参考图 + 提示词实现 image-to-image 风格化出图，支持 14 种视觉风格。

---

## 支持风格（14 种）

| 风格 | 视觉特点 | 适用场景 |
|------|---------|---------|
| 白板板书 | 真实白板 + 马克笔手写 + 手绘插图 | 培训/教学/头脑风暴 |
| 光辉 | 光效质感/科技感/未来感 | 科技发布/创新主题 |
| 黑胶风 | 复古唱片质感/暖色调/怀旧氛围 | 音乐/文艺/复古 |
| 画架 | 油画画布质感/艺术手绘感 | 艺术展示/创意汇报 |
| 立体 | 3D立体效果/空间层次感 | 产品展示/科技汇报 |
| 黑板报风格 | 粉笔手绘/彩色粉笔字 | 教育/校园/培训 |
| 旧画报风格 | 复古画报/怀旧印刷风 | 文艺/复古/历史 |
| 毛毡风 | 毛毡手工质感/缝线装饰 | 儿童/手工/温馨 |
| 拟物毛玻璃 | 毛玻璃透明模糊/现代UI风 | 科技/产品/现代商务 |
| 医疗行业 | 蓝白色调/专业简洁 | 医疗报告/健康科普 |
| 年度工作总结 | 商务蓝金/数据可视化 | 年终汇报/商务报告 |
| 开学第一课 | 活泼校园风/彩色插图 | 教学课件/教育培训 |
| 林地 | 绿色系/自然元素/清新 | 环保主题/自然教育 |
| 湿壁画 | 古典艺术质感/复古纹理 | 文化/艺术/历史 |

默认风格：白板板书

---

## 工作流程

```
1. 确认风格 → 用户选择或使用默认白板板书
2. 接收文案 → 整理页面确认表（页码/类型/参考图/内容摘要）
3. 依赖检查 → openai / pillow / python-pptx
4. 逐页生成 → generate_image.py + 参考图(image-to-image)
5. 合成输出 → build_pptx.py → .pptx 文件
```

---

## 文件结构

```
ppt-nano-master/
├── SKILL.md                      # Skill 执行规范（AI 读取）
├── README.md                     # 本文件
├── scripts/
│   ├── generate_image.py         # 单页图片生成脚本
│   ├── build_pptx.py             # 图片合成 .pptx 脚本
│   └── test_generate_image.py    # 生成脚本测试
└── styles/
    ├── styles.json               # 所有风格的配置（提示词/参考图路径）
    ├── whiteboard/               # 白板板书（jpg, content 用 content_new.jpg）
    ├── 光辉/                     # 光辉风格（jpg）
    ├── 黑胶风/                   # 黑胶风（jpg）
    ├── 画架/                     # 画架风格（jpg）
    ├── 立体/                     # 立体风格（jpg）
    ├── 黑板报风格/               # 黑板报风格（png）
    ├── 旧画报风格/               # 旧画报风格（png）
    ├── 毛毡风/                   # 毛毡风（jpg）
    ├── 拟物毛玻璃/               # 拟物毛玻璃（jpg）
    ├── 医疗行业/                 # 医疗行业（jpg）
    ├── 年度工作总结/             # 年度工作总结（jpg）
    ├── 开学第一课/               # 开学第一课（jpg）
    ├── 林地/                     # 林地风格（jpg）
    └── 湿壁画/                   # 湿壁画风格（jpg）
```

每个风格文件夹包含三张参考图：`cover` / `content` / `closing`（白板板书的 content 页使用 `content_new.jpg`）。

---

## 核心脚本

### generate_image.py — 单页生成

```bash
python scripts/generate_image.py \
  --prompt "提示词前缀 + 页面文案" \
  --filename "output.jpg" \
  --resolution 2K \
  --aspect-ratio 16:9 \
  -i "styles/风格名/cover.jpg"
```

| 参数 | 说明 |
|------|------|
| `--prompt` | 风格提示词 + 页面文案内容 |
| `--filename` | 输出文件名（.jpg） |
| `--resolution` | `2K` 或 `3K` |
| `--aspect-ratio` | `16:9` |
| `-i` | 参考图路径（必须带，image-to-image 模式） |

输出：`MEDIA:/path/to/generated.jpg`

### build_pptx.py — 合成 PPT

```bash
python scripts/build_pptx.py \
  -i slide1.jpg slide2.jpg slide3.jpg \
  -o output.pptx
```

| 参数 | 说明 |
|------|------|
| `-i` | 图片路径列表，按页序排列 |
| `--dir` | 或指定目录，扫描所有 jpg |
| `-o` | 输出路径，默认 `output.pptx` |
| `--width` / `--height` | 幻灯片尺寸（英寸），默认 13.33 x 7.5 |

输出：`PPTX:/path/to/file.pptx`

---

## 风格配置

所有风格定义在 `styles/styles.json` 中，每个风格包含：

- `name` — 显示名称
- `description` — 风格描述
- `refs` — 参考图路径映射（cover / content / closing）
- `style_prompts` — 各页面类型的提示词
- `page_type_rules` — 页面类型自动分配规则

---

## 环境依赖

```bash
python -m pip install openai pillow python-pptx
```

跨平台支持（Windows / macOS / Linux），中文路径已在脚本内部处理。
