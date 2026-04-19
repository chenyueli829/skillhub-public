---
name: screenshot
description: 对本地或远程 Web 页面进行高质量截图，无黑屏、无外部依赖。使用 puppeteer + Chrome for Testing（非系统 Chrome），Retina 分辨率（deviceScaleFactor=2）。触发词：「截图」、「screenshot」、「帮我截一张」、「截取页面」、「截取效果」。project-review skill 截图步骤应优先调用此 skill。
---

# Screenshot Skill

## 核心方案

**puppeteer + Chrome for Testing**（已预装于本机）

| 方案 | 黑屏率 | 速度 | 可靠性 | 说明 |
|------|--------|------|--------|------|
| **本方案（puppeteer）** | **0%** | **~3s** | **✅ 最高** | Chrome for Testing，专为自动化设计 |
| screencapture -x（全屏） | ~55%+ | 即时 | ❌ 依赖屏幕状态 | Retina 全屏，含桌面/其他窗口 |
| Chrome --headless --screenshot | ~35%+ | ~15s | ❌ GPU/渲染问题 | 经常黑屏 |
| Python playwright | N/A | N/A | ❌ chromium 下载失败 | 网络问题 |
| osascript + 指定窗口 | 低 | ~5s | ⚠️ 权限问题 | System Events 访问受限 |

## 关键路径

```
截图脚本：{SKILL_DIR}/scripts/screenshot.js
多截图脚本：{SKILL_DIR}/scripts/multi-screenshot.js
```

## 环境配置

### 环境变量

- `PUPPETEER_PATH`：自定义 puppeteer 模块路径（可选）
  ```bash
  # 示例：设置自定义 puppeteer 路径
  export PUPPETEER_PATH=/path/to/your/node_modules/puppeteer
  ```

- `PUPPETEER_SCALE`：默认设备缩放因子（可选）
  ```bash
  # 示例：设置默认缩放因子为 1（标准分辨率）
  export PUPPETEER_SCALE=1
  ```

### 依赖安装

Screenshot Skill 需要 puppeteer 依赖，可通过以下方式安装：

```bash
# 在项目根目录安装
npm install puppeteer

# 或全局安装
npm install -g puppeteer
```

脚本会自动按以下顺序查找 puppeteer：
1. 环境变量 `PUPPETEER_PATH` 指定的路径
2. 当前目录的 `./node_modules/puppeteer`
3. 上级目录的 `../node_modules/puppeteer`
4. 上上级目录的 `../../node_modules/puppeteer`
5. 全局安装的 `puppeteer`

## 使用方法

### 单张截图

```bash
node {SKILL_DIR}/scripts/screenshot.js <url> <output_path> [width] [height] [wait_ms] [full_page] [scale]
```

参数说明：
- `url`：目标页面地址（localhost 或 https）
- `output_path`：输出 PNG 路径（绝对路径）
- `width`：视口宽度，默认 1280
- `height`：视口高度，默认 800
- `wait_ms`：页面加载后额外等待毫秒数，默认 2000（动画/异步渲染用）
- `full_page`：是否截取完整页面，默认 false
- `scale`：设备缩放因子，默认 2（Retina 分辨率），范围 1-4

**常用示例：**

```bash
# 默认 1280x800
node {SKILL_DIR}/scripts/screenshot.js http://localhost:3000 /tmp/demo.png

# 宽屏 + 长等待（动画密集页面）
node {SKILL_DIR}/scripts/screenshot.js http://localhost:5173 /tmp/app.png 1440 900 3000

# 完整长页面
node {SKILL_DIR}/scripts/screenshot.js http://localhost:8888 /tmp/launchpad.png 1280 800 2000 true

# 高分辨率（3x）
node {SKILL_DIR}/scripts/screenshot.js http://localhost:3000 /tmp/highres.png 1440 900 2000 false 3

# 标准分辨率（1x，文件更小）
node {SKILL_DIR}/scripts/screenshot.js http://localhost:3000 /tmp/standard.png 1440 900 2000 false 1
```

### 多状态截图（推荐用于 project-review）

```bash
node {SKILL_DIR}/scripts/multi-screenshot.js '{
  "url": "http://localhost:3000",
  "outputDir": "/tmp",
  "prefix": "myapp",
  "viewport": {"width": 1280, "height": 800},
  "scale": 2,
  "shots": [
    {"name": "home",  "waitMs": 2000},
    {"name": "dark",  "waitMs": 500,  "js": "document.documentElement.classList.add(\"dark\")"},
    {"name": "full",  "waitMs": 500,  "fullPage": true}
  ]
}'
```

输出文件：`/tmp/myapp-home.png`、`/tmp/myapp-dark.png`、`/tmp/myapp-full.png`

## Agent 调用模板

在 `exec` 工具中直接调用：

```python
exec(command="""node {SKILL_DIR}/scripts/screenshot.js \
  "http://localhost:PORT" "/tmp/OUTPUT.png" 1280 800 2000""")
```

返回 JSON：
```json
{"ok": true, "path": "/tmp/OUTPUT.png", "size": 115000, "width": 1280, "height": 800, "url": "..."}
```

## 注意事项

1. **等待时间**：页面有动画/异步加载时，`wait_ms` 设 3000 以上
2. **SPA 应用**：`networkidle0` 已等待所有网络请求完成，一般 2000ms 足够
3. **暗色主题**：用 `js` 参数注入 `toggleDark()` 或 class 切换
4. **全页截图**：`full_page=true` 时 height 参数仍影响视口宽高，只是截取范围更长
5. **输出大小**：`deviceScaleFactor=2`（Retina），实际像素是视口的 2 倍，文件约 100-500KB

## 黑屏排查

如果截图仍然黑屏：
1. 增加 `wait_ms`（试 5000ms）
2. 检查页面是否有 `--background` 参数（CSS background 是否设置）
3. 检查页面 JS 报错：`page.on('console', ...)` 或加 `--disable-web-security`
4. 确认服务已启动且 URL 可访问（先 `curl` 验证）

## 依赖检查

```bash
# 验证 puppeteer 可用
node -e "require('puppeteer'); console.log('OK')"

# 或使用环境变量指定路径
# export PUPPETEER_PATH=/path/to/puppeteer
# node -e "require(process.env.PUPPETEER_PATH); console.log('OK')"
```
