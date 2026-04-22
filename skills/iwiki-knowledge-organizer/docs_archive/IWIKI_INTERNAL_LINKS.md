# iwiki 内部链接管理

## 📋 功能概述

当 iwiki 文档中引用其他 iwiki 文档时，系统会自动检测并处理这些内部链接：

1. **已下载的文档** - 替换为本地相对路径
2. **未下载的文档** - 自动下载到对应的层级目录

这样可以建立完整的本地知识网络，实现文档间的无缝跳转。

---

## 🔍 链接检测

### iwiki 内部链接格式

```
https://iwiki.woa.com/p/{docid}
```

**示例**：
- `https://iwiki.woa.com/p/1234567890`
- `https://iwiki.woa.com/p/9876543210`

### 检测模式

```javascript
const iwikiLinkPattern = /https?:\/\/iwiki\.woa\.com\/p\/(\d+)/g;

// 提取所有内部链接
const matches = content.matchAll(iwikiLinkPattern);
for (const match of matches) {
  const docid = match[1];  // 提取文档 ID
  const fullUrl = match[0]; // 完整 URL
  // 处理链接...
}
```

---

## 🔄 处理流程

### 完整工作流

```
1. 下载 iwiki 文档 A
   ↓
2. 扫描文档 A 的内容
   ↓
3. 发现引用了文档 B (iwiki.woa.com/p/12345)
   ↓
4. 检查文档 B 是否已下载？
   ├─ 是 → 替换为本地相对路径
   └─ 否 → 下载文档 B（保持层级结构）
          ↓
          递归检查文档 B 中的引用
```

---

## 📂 场景 1：已下载的文档（替换为本地路径）

### 示例

**文档 A**：`我的知识库/iwikis/FiT-资金中台/技术文档/API设计.md`

**原始内容**：
```markdown
# API设计

## 参考文档

详细需求请查看：[需求文档](https://iwiki.woa.com/p/9876543210)

系统架构设计参考：https://iwiki.woa.com/p/1111111111
```

**文档 B** 已下载到：`我的知识库/iwikis/FiT-资金中台/产品文档/需求文档.md`

**文档 C** 已下载到：`我的知识库/iwikis/FiT-资金中台/技术文档/系统架构.md`

### 处理步骤

```javascript
1. 扫描文档 A，发现两个 iwiki 链接：
   - https://iwiki.woa.com/p/9876543210
   - https://iwiki.woa.com/p/1111111111

2. 搜索本地文档：
   - 在所有 .md 文件的 frontmatter 中搜索 iwiki_id
   - 找到 9876543210 → 需求文档.md
   - 找到 1111111111 → 系统架构.md

3. 计算相对路径：
   从: iwikis/FiT-资金中台/技术文档/API设计.md
   到: iwikis/FiT-资金中台/产品文档/需求文档.md
   相对路径: ../产品文档/需求文档.md

   从: iwikis/FiT-资金中台/技术文档/API设计.md
   到: iwikis/FiT-资金中台/技术文档/系统架构.md
   相对路径: ./系统架构.md

4. 替换链接
```

### 替换后的内容

```markdown
# API设计

## 参考文档

详细需求请查看：[需求文档](../产品文档/需求文档.md)

系统架构设计参考：[系统架构](./系统架构.md)
```

---

## 📥 场景 2：未下载的文档（自动下载）

### 示例

**文档 A**：`我的知识库/iwikis/FiT-资金中台/技术文档/API设计.md`

**原始内容**：
```markdown
# API设计

## 参考文档

数据库设计请查看：https://iwiki.woa.com/p/5555555555
```

**文档 D**（docid: 5555555555）**未下载**

### 处理步骤

```javascript
1. 扫描文档 A，发现 iwiki 链接：
   - https://iwiki.woa.com/p/5555555555

2. 搜索本地文档：
   - 未找到 docid 5555555555

3. 自动下载流程：
   a. 获取文档元数据：
      user-iWiki-metadata(5555555555)
      返回：
      {
        title: "数据库设计",
        space: "FiT-资金中台",
        parentid: 3333333333
      }
   
   b. 递归获取父级路径：
      user-iWiki-metadata(3333333333)
      返回：
      {
        title: "技术文档",
        parentid: 0  // 到根目录
      }
      
      完整路径：FiT-资金中台/技术文档/数据库设计
   
   c. 下载文档：
      保存到: 我的知识库/iwikis/FiT-资金中台/技术文档/数据库设计.md
   
   d. 递归处理新下载的文档：
      扫描"数据库设计.md"中的 iwiki 链接
      继续检查和下载...

4. 计算相对路径：
   从: iwikis/FiT-资金中台/技术文档/API设计.md
   到: iwikis/FiT-资金中台/技术文档/数据库设计.md
   相对路径: ./数据库设计.md

5. 替换链接
```

### 下载后的结构

```
我的知识库/
└── iwikis/
    └── FiT-资金中台/
        └── 技术文档/
            ├── API设计.md          ← 原文档
            └── 数据库设计.md       ← 自动下载的关联文档
```

### 替换后的内容

```markdown
# API设计

## 参考文档

数据库设计请查看：[数据库设计](./数据库设计.md)
```

---

## 🎯 场景 3：跨空间引用

### 示例

**文档 A**：`我的知识库/iwikis/FiT-资金中台/技术文档/API设计.md`

**原始内容**：
```markdown
# API设计

## 参考文档

支付流程参考：https://iwiki.woa.com/p/7777777777
```

**文档 E**（docid: 7777777777）属于**不同空间**：微信支付

### 处理步骤

```javascript
1. 获取文档元数据：
   user-iWiki-metadata(7777777777)
   返回：
   {
     title: "支付流程设计",
     space: "微信支付",
     folder: "技术文档"
   }

2. 下载到对应的空间层级：
   保存到: 我的知识库/iwikis/微信支付/技术文档/支付流程设计.md

3. 计算相对路径：
   从: iwikis/FiT-资金中台/技术文档/API设计.md
   到: iwikis/微信支付/技术文档/支付流程设计.md
   相对路径: ../../微信支付/技术文档/支付流程设计.md
```

### 下载后的结构

```
我的知识库/
└── iwikis/
    ├── FiT-资金中台/
    │   └── 技术文档/
    │       └── API设计.md
    │
    └── 微信支付/                   ← 自动创建新空间目录
        └── 技术文档/
            └── 支付流程设计.md     ← 跨空间引用的文档
```

### 替换后的内容

```markdown
# API设计

## 参考文档

支付流程参考：[支付流程设计](../../微信支付/技术文档/支付流程设计.md)
```

---

## 🔄 递归处理

### 链式引用示例

```
文档 A 引用 文档 B
    ↓
文档 B 引用 文档 C
    ↓
文档 C 引用 文档 D
```

### 处理流程

```javascript
1. 下载文档 A
   - 发现引用文档 B（未下载）
   - 添加到下载队列

2. 下载文档 B
   - 处理完成后，扫描内容
   - 发现引用文档 C（未下载）
   - 添加到下载队列

3. 下载文档 C
   - 处理完成后，扫描内容
   - 发现引用文档 D（未下载）
   - 添加到下载队列

4. 下载文档 D
   - 处理完成后，扫描内容
   - 无更多引用
   - 队列为空，完成

5. 回溯更新所有链接
   - 文档 A 中的链接 → 更新为本地路径
   - 文档 B 中的链接 → 更新为本地路径
   - 文档 C 中的链接 → 更新为本地路径
```

---

## 📊 下载报告示例

```markdown
## 内部链接处理报告

✅ 原文档: API设计.md
   引用的 iwiki 文档: 5 个

### 已存在（替换为本地路径）

1. 需求文档 (docid: 9876543210)
   本地路径: ../产品文档/需求文档.md
   状态: ✓ 已替换

2. 系统架构 (docid: 1111111111)
   本地路径: ./系统架构.md
   状态: ✓ 已替换

### 自动下载（新增文档）

3. 数据库设计 (docid: 5555555555)
   保存位置: FiT-资金中台/技术文档/数据库设计.md
   状态: ✓ 已下载并替换
   递归引用: 发现 2 个新文档

4. 接口规范 (docid: 6666666666)
   保存位置: FiT-资金中台/技术文档/接口规范.md
   状态: ✓ 已下载并替换
   递归引用: 无

5. 支付流程设计 (docid: 7777777777)
   保存位置: 微信支付/技术文档/支付流程设计.md
   状态: ✓ 已下载并替换（跨空间）
   递归引用: 发现 1 个新文档

---

📈 统计:
- 总引用数: 5
- 本地已存在: 2
- 新下载文档: 3
- 跨空间引用: 1
- 递归下载文档: 3
- 总下载文档数: 6（原始 3 + 递归 3）
```

---

## ⚙️ 技术实现

### 本地文档搜索

```javascript
// 在所有已下载文档的 frontmatter 中搜索 iwiki_id
function searchLocalDoc(docid) {
  const allMdFiles = glob('我的知识库/iwikis/**/*.md');
  
  for (const file of allMdFiles) {
    const content = readFile(file);
    const frontmatter = parseFrontmatter(content);
    
    if (frontmatter.iwiki_id === docid) {
      return {
        path: file,
        title: frontmatter.title,
        space: extractSpaceFromPath(file),
        folder: extractFolderFromPath(file)
      };
    }
  }
  
  return null; // 未找到
}
```

### 相对路径计算

```javascript
function calculateRelativePath(fromPath, toPath) {
  // fromPath: iwikis/FiT-资金中台/技术文档/API设计.md
  // toPath:   iwikis/FiT-资金中台/产品文档/需求文档.md
  
  const fromParts = fromPath.split('/').slice(0, -1); // 去掉文件名
  const toParts = toPath.split('/');
  
  // 找到共同父目录
  let commonIndex = 0;
  while (fromParts[commonIndex] === toParts[commonIndex]) {
    commonIndex++;
  }
  
  // 计算需要返回的层数
  const upLevels = fromParts.length - commonIndex;
  const upPath = '../'.repeat(upLevels);
  
  // 计算目标路径
  const downPath = toParts.slice(commonIndex).join('/');
  
  return upPath + downPath;
  // 结果: ../产品文档/需求文档.md
}
```

### 链接替换

```javascript
function replaceInternalLinks(content, linkMapping) {
  // linkMapping: { 'https://iwiki.woa.com/p/12345': '../path/to/doc.md' }
  
  for (const [iwikiUrl, localPath] of Object.entries(linkMapping)) {
    // 替换 Markdown 链接格式: [text](url)
    content = content.replace(
      new RegExp(`\\[([^\\]]+)\\]\\(${escapeRegex(iwikiUrl)}\\)`, 'g'),
      `[$1](${localPath})`
    );
    
    // 替换纯 URL
    content = content.replace(
      new RegExp(`(?<!\\()${escapeRegex(iwikiUrl)}(?!\\))`, 'g'),
      `[引用文档](${localPath})`
    );
  }
  
  return content;
}
```

---

## 🎁 优势总结

| 优势 | 说明 |
|------|------|
| **自动化** | 无需手动下载关联文档，系统自动处理 |
| **完整性** | 确保所有引用的文档都在本地，离线可用 |
| **层级保持** | 自动下载的文档保持原有的空间/文件夹结构 |
| **跨空间支持** | 自动处理不同空间的文档引用 |
| **递归处理** | 自动处理多层引用关系，建立完整知识网络 |
| **智能替换** | 已下载的文档直接替换为本地路径 |
| **可追溯** | 下载报告清晰记录所有处理过程 |

---

## 🔧 配置选项

### 是否自动下载关联文档

**默认行为**：自动下载

**自定义选项**：
```
用户: "拉取文档，但不自动下载关联文档"

系统行为:
- 只替换已存在的本地文档链接
- 未下载的文档链接保持原样
- 在报告中列出所有未下载的引用
```

### 下载深度限制

**默认行为**：无限制递归

**自定义选项**：
```
用户: "拉取文档，关联文档只下载 1 层"

系统行为:
- 下载直接引用的文档
- 不再递归处理新下载文档中的引用
```

---

## 📝 使用示例

### 示例 1：下载单个文档并处理引用

```
用户: "拉取 https://iwiki.woa.com/p/1234567890"

AI 处理:
1. 下载目标文档
2. 扫描发现 3 个 iwiki 内部链接
3. 检查本地：1 个已存在，2 个未下载
4. 自动下载 2 个关联文档（保持层级）
5. 替换所有链接为本地路径
6. 生成完整报告
```

### 示例 2：下载整个空间并处理所有引用

```
用户: "拉取整个空间 https://iwiki.woa.com/space/fit"

AI 处理:
1. 递归下载空间内所有文档
2. 扫描所有文档的内部链接
3. 识别跨文档引用
4. 自动下载引用的外部空间文档
5. 批量替换所有内部链接
6. 建立完整的本地知识网络
```

---

**版本**: v2.1  
**最后更新**: 2026-02-14  
**相关文档**: [SKILL.md](SKILL.md) | [README_CN.md](README_CN.md) | [FILES_MANAGEMENT.md](FILES_MANAGEMENT.md)
