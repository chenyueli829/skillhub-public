# 小红书爆款创作工具集 (xhs-utils)

从小红书爆款创作 skill 中提取的通用工具脚本，可独立使用。

## 📦 安装

```bash
cd xhs-utils
npm install
```

## 🛠️ 工具列表

| 脚本 | 用途 | 命令 |
|------|------|------|
| `char-counter.js` | 字数检查 (标题≤20/正文≤1000) | `node char-counter.js --demo` |
| `pattern-analyzer.js` | 爆款规律分析 | `node pattern-analyzer.js --demo` |
| `comment-sentiment.js` | 评论情感共鸣分析 | `node comment-sentiment.js --demo` |
| `ai-tone-detector.js` | AI 味检测 | `node ai-tone-detector.js --demo` |
| `image-finder.js` | 配图搜索建议 | `node image-finder.js --demo` |
| `workflow-demo.js` | 完整工作流演示 | `node workflow-demo.js "主题"` |

## 📖 使用示例

### 1️⃣ 字数检查

```bash
# 运行示例
node char-counter.js --demo

# 检查标题
node char-counter.js --title "打工人带饭｜5 天不重样 30 元/天"

# 检查正文文件
node char-counter.js --body-file body.txt
```

### 2️⃣ 爆款规律分析

```bash
# 运行示例
node pattern-analyzer.js --demo

# 分析自己的数据
node pattern-analyzer.js --input posts.json
```

输入格式 (`posts.json`):
```json
{
  "titles": ["标题 1", "标题 2"],
  "bodies": ["正文 1", "正文 2"]
}
```

### 3️⃣ 评论情感分析

```bash
# 运行示例
node comment-sentiment.js --demo

# 分析评论
node comment-sentiment.js --input comments.json
```

输入格式 (`comments.json`):
```json
["评论 1", "评论 2", "评论 3"]
```

### 4️⃣ AI 味检测

```bash
# 运行示例 (对比 AI 味 vs 真人感)
node ai-tone-detector.js --demo

# 检测文案
node ai-tone-detector.js --text "这是要检测的文案"

# 检测文件
node ai-tone-detector.js --file draft.txt
```

### 5️⃣ 配图搜索

```bash
# 运行示例
node image-finder.js --demo

# 生成搜索链接
node image-finder.js --topic "带饭" --links

# 模拟结果 (无需 API)
node image-finder.js --topic "化妆" --mock
```

### 6️⃣ 完整工作流演示

```bash
# 运行完整流程 (默认主题：打工人带饭)
node workflow-demo.js

# 指定主题
node workflow-demo.js "新手化妆"
```

## 🔧 集成到工作流

### 作为 write-xiaohongshu skill 的辅助工具

在 write-xiaohongshu skill 中，可以调用这些脚本：

```bash
# 步骤 4: 写完文案后自检
node char-counter.js --title "$TITLE" --body-file body.txt

# 步骤 4: 检测 AI 味
node ai-tone-detector.js --file body.txt

# 步骤 5: 找配图
node image-finder.js --topic "$TOPIC" --mock
```

### 输出处理

所有脚本都返回标准输出，可以重定向到文件：

```bash
node pattern-analyzer.js --input posts.json > analysis.txt
node ai-tone-detector.js --file draft.txt 2>&1 | grep "综合得分"
```

## 📝 注意事项

1. **Node.js 要求**: 需要 Node.js 16+ (使用 ES Modules)
2. **依赖安装**: 首次使用需运行 `npm install`
3. **图片生成**: 完整流程请使用 write-xiaohongshu skill 的 image-gen 生图功能
4. **图片搜索**: `image-finder.js` 仅生成搜索链接，作为 image-gen 不可用时的备选方案
5. **字数计算**: 按字符数计算 (包含空格、标点、emoji)

## 🚀 扩展建议

可以进一步扩展的功能:

- [ ] 接入 Pexels/Unsplash API 自动下载图片
- [ ] 批量处理多个文案
- [ ] 生成可视化报告 (HTML/PDF)
- [ ] 与小红书 MCP 深度集成
- [ ] 添加更多爆款模式识别

## 📄 License

MIT
