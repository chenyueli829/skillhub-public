# 文件附件管理详解

## 📎 功能概述

iwiki 文档中通常包含两类文件引用：
1. **可下载的附件** - 如 PPT、Excel、Word、PDF 等
2. **外部链接** - 如腾讯文档、在线表格等（无法直接下载）

本 skill 会自动处理这两类文件，统一存储到 `我的知识库/files/` 目录。

---

## 🗂️ 目录结构

```
我的知识库/
└── files/
    └── {空间名}/
        └── {文件夹}/
            └── {文档名}/
                ├── 需求文档.pptx         ← PPT 附件
                ├── 数据模型.xlsx         ← Excel 附件
                ├── 技术方案.pdf          ← PDF 附件
                ├── 接口说明.docx         ← Word 附件
                ├── 代码包.zip            ← 压缩包附件
                └── external-links.txt   ← 外部链接清单
```

---

## 📥 可下载的附件

### 支持的文件类型

| 类型 | 扩展名 | 说明 |
|------|--------|------|
| **PowerPoint** | `.pptx`, `.ppt` | 演示文稿 |
| **Excel** | `.xlsx`, `.xls` | 电子表格 |
| **Word** | `.docx`, `.doc` | 文本文档 |
| **PDF** | `.pdf` | 便携文档 |
| **压缩包** | `.zip`, `.rar`, `.7z` | 压缩文件 |
| **文本** | `.txt`, `.csv` | 纯文本 |
| **其他** | 各种格式 | 其他可下载附件 |

### 下载流程

```
1. 获取文档附件列表
   └─ user-iWiki-getAttachmentList(docid)

2. 过滤掉图片类型
   └─ 排除: png, jpg, jpeg, gif, svg, webp, bmp

3. 下载文件附件
   └─ 对每个附件:
      ├─ 获取下载URL: user-iWiki-getAttachmentDownloadUrl(attachmentid)
      ├─ 使用 curl 下载
      └─ 保存到: files/{空间}/{文件夹}/{文档名}/{原始文件名}.{扩展名}

4. 记录到文档元数据
   └─ frontmatter 中添加 attachments 列表
```

### 示例

**iwiki 文档附件**：
- 需求文档 v1.0.pptx
- 数据字典.xlsx
- 技术规范.pdf

**下载后**：
```
我的知识库/
└── files/
    └── FiT-资金中台/
        └── 技术文档/
            └── API设计/
                ├── 需求文档v1.0.pptx
                ├── 数据字典.xlsx
                └── 技术规范.pdf
```

**文档 frontmatter**：
```yaml
---
attachments:
  - ../../../files/FiT-资金中台/技术文档/API设计/需求文档v1.0.pptx
  - ../../../files/FiT-资金中台/技术文档/API设计/数据字典.xlsx
  - ../../../files/FiT-资金中台/技术文档/API设计/技术规范.pdf
---
```

---

## 🔗 外部链接管理

### 支持的外部链接类型

| 类型 | URL 模式 | 示例 |
|------|----------|------|
| **腾讯文档** | `docs.qq.com/doc/*` | https://docs.qq.com/doc/DQVxxxxxx |
| **腾讯表格** | `docs.qq.com/sheet/*` | https://docs.qq.com/sheet/DQVxxxxxx |
| **腾讯幻灯片** | `docs.qq.com/slide/*` | https://docs.qq.com/slide/DQVxxxxxx |
| **微信文档** | `doc.weixin.qq.com/*` | https://doc.weixin.qq.com/doc/xxxxx |
| **Excel Online** | `excel.live.com/*` | https://excel.live.com/... |

### 识别流程

```
1. 扫描文档内容
   └─ 使用正则表达式匹配外部链接

2. 提取链接信息
   └─ 对每个匹配的链接:
      ├─ 提取完整 URL
      ├─ 提取上下文文本（链接前后50字符）
      └─ 确定链接类型（腾讯文档/表格/幻灯片等）

3. 创建 external-links.txt
   └─ 保存到: files/{空间}/{文件夹}/{文档名}/external-links.txt

4. 记录到文档元数据
   └─ frontmatter 中添加 external_links 路径
```

### external-links.txt 格式

```
# 本文引用 - {文档名}
# 来源: https://iwiki.woa.com/p/{docid}
# 创建时间: {timestamp}

[1] {链接标题或描述} (链接类型)
{完整URL}
位置: {在文档中的位置}
说明: {简短说明或上下文}

[2] {另一个链接}
...

注意事项:
- 这些外部链接需要相应权限才能访问
- 链接可能过期或需要重新认证
- 建议定期检查链接有效性
```

### 示例

**文档内容包含**：
- 详细需求说明：https://docs.qq.com/doc/DQVxxxxxx
- 数据字典表格：https://docs.qq.com/sheet/DQVyyyyyy
- 技术方案 PPT：https://docs.qq.com/slide/DQVzzzzzz

**生成的 external-links.txt**：
```
# 本文引用 - API设计
# 来源: https://iwiki.woa.com/p/1234567890
# 创建时间: 2026-02-14 16:30:00

[1] 详细需求说明文档 (腾讯文档)
https://docs.qq.com/doc/DQVxxxxxx
位置: 第二章 - 需求分析
说明: 包含完整的产品需求说明和用例

[2] 系统数据字典 (腾讯表格)
https://docs.qq.com/sheet/DQVyyyyyy
位置: 附录A - 数据字典
说明: 系统所有数据表和字段定义

[3] 技术架构方案 (腾讯幻灯片)
https://docs.qq.com/slide/DQVzzzzzz
位置: 第三章 - 技术方案
说明: 技术架构设计演示文稿

注意事项:
- 这些外部链接需要相应权限才能访问
- 链接可能过期或需要重新认证
- 建议定期检查链接有效性
```

---

## 📊 完整示例

### 示例文档：资金账务业务发展规划

**iwiki 文档包含**：
- 📊 3 张图片（架构图、流程图、数据模型）
- 📎 2 个附件（规划.pptx, 数据分析.xlsx）
- 🔗 4 个外部链接（腾讯文档）

**下载后的结构**：

```
我的知识库/
├── iwikis/
│   └── FiT-资金中台/
│       └── 产品规划/
│           └── 资金账务业务发展规划.md
│
├── images/
│   └── FiT-资金中台/
│       └── 产品规划/
│           └── 资金账务业务发展规划/
│               ├── 1-业务架构图.png
│               ├── 2-发展路线图.svg
│               └── 3-数据模型.jpg
│
└── files/
    └── FiT-资金中台/
        └── 产品规划/
            └── 资金账务业务发展规划/
                ├── 2026年发展规划.pptx        ← PPT 附件
                ├── 业务数据分析.xlsx         ← Excel 附件
                └── external-links.txt       ← 外部链接清单
```

**external-links.txt 内容**：
```
# 本文引用 - 资金账务业务发展规划
# 来源: https://iwiki.woa.com/p/4007960476
# 创建时间: 2026-02-14 16:30:00

[1] 详细需求文档 (腾讯文档)
https://docs.qq.com/doc/DQVxxxxxx
位置: 第一章 - 业务需求
说明: 2026年资金账务详细需求

[2] 竞品分析表 (腾讯表格)
https://docs.qq.com/sheet/DQVyyyyyy
位置: 第二章 - 市场分析
说明: 主要竞品功能对比分析

[3] 技术选型方案 (腾讯文档)
https://docs.qq.com/doc/DQVzzzzzz
位置: 第四章 - 技术方案
说明: 技术栈选型和架构设计

[4] 项目排期表 (腾讯表格)
https://docs.qq.com/sheet/DQVaaaaaa
位置: 第五章 - 实施计划
说明: 2026年项目排期和里程碑

注意事项:
- 这些外部链接需要相应权限才能访问
- 链接可能过期或需要重新认证
- 建议定期检查链接有效性
```

**文档 frontmatter**：
```yaml
---
iwiki_id: 4007960476
title: 资金账务业务发展规划
source: https://iwiki.woa.com/p/4007960476
creator: chenyueli(陈越立)
created: 2025-11-20 14:30:00
updated: 2026-02-12 16:45:00
parentid: 3998765432
attachments:
  - ../../../files/FiT-资金中台/产品规划/资金账务业务发展规划/2026年发展规划.pptx
  - ../../../files/FiT-资金中台/产品规划/资金账务业务发展规划/业务数据分析.xlsx
external_links: ../../../files/FiT-资金中台/产品规划/资金账务业务发展规划/external-links.txt
---
```

---

## 🛠️ 技术实现

### 附件检测正则

```javascript
// 检测附件类型（非图片）
const attachmentPatterns = {
  ppt: /\.(pptx?|pps[xm]?)$/i,
  excel: /\.(xlsx?|xls[xm]?|csv)$/i,
  word: /\.(docx?|dot[xm]?)$/i,
  pdf: /\.pdf$/i,
  archive: /\.(zip|rar|7z|tar|gz)$/i,
  text: /\.(txt|log|md|json|xml)$/i
};
```

### 外部链接检测正则

```javascript
const externalLinkPatterns = {
  tencentDoc: /https?:\/\/docs\.qq\.com\/doc\/[A-Za-z0-9_-]+/g,
  tencentSheet: /https?:\/\/docs\.qq\.com\/sheet\/[A-Za-z0-9_-]+/g,
  tencentSlide: /https?:\/\/docs\.qq\.com\/slide\/[A-Za-z0-9_-]+/g,
  wechatDoc: /https?:\/\/doc\.weixin\.qq\.com\/[A-Za-z0-9_\/-]+/g,
  excelOnline: /https?:\/\/[^\/]*excel\.live\.com\/[A-Za-z0-9_\/-]+/g
};
```

---

## 📋 文档元数据更新

### 新增字段

下载文件附件后，文档的 frontmatter 会自动添加：

```yaml
---
# ... 其他元数据 ...
attachments:
  - ../../../files/空间名/文件夹/文档名/附件1.pptx
  - ../../../files/空间名/文件夹/文档名/附件2.xlsx
external_links: ../../../files/空间名/文件夹/文档名/external-links.txt
---
```

### 字段说明

- **`attachments`** - 数组，包含所有可下载附件的相对路径
- **`tencent_docs`** - 字符串，指向腾讯文档引用清单文件的相对路径

---

## 🎯 使用场景

### 场景1：文档包含 PPT 附件

**iwiki 文档**：技术方案设计.md，包含 1 个 PPT 附件

**下载命令**：
```
拉取 https://iwiki.woa.com/p/1234567890
```

**结果**：
```
我的知识库/
├── iwikis/FiT-资金中台/技术文档/技术方案设计.md
└── files/FiT-资金中台/技术文档/技术方案设计/
    └── 系统架构设计方案.pptx  ← 自动下载的 PPT
```

---

### 场景2：文档包含多个附件

**iwiki 文档**：需求分析，包含 2 个 Excel + 1 个 Word

**结果**：
```
files/FiT-资金中台/产品文档/需求分析/
├── 用户调研数据.xlsx
├── 功能清单.xlsx
└── 需求说明.docx
```

---

### 场景3：文档包含外部链接

**iwiki 文档**：系统设计，引用 3 个腾讯文档链接

**结果**：
```
files/FiT-资金中台/技术文档/系统设计/
└── 关联的腾讯文档.md

内容（Markdown格式）:
# 关联的腾讯文档

## 详细设计文档

**文章信息**：
- 引用空间：FiT-资金中台
- 引用文件夹：技术文档/系统设计
- 引用文章：系统设计文档
- 引用位置：第二章 - 详细设计

**链接地址**：
https://docs.qq.com/doc/DQVxxxxxx

**文档类型**：腾讯文档 (Tencent Doc)

---

## 接口定义表

**文章信息**：
- 引用空间：FiT-资金中台
- 引用文件夹：技术文档/系统设计
- 引用文章：系统设计文档
- 引用位置：第三章 - 接口设计

**链接地址**：
https://docs.qq.com/sheet/DQVyyyyyy

**文档类型**：腾讯表格 (Tencent Sheet)
```

---

### 场景4：混合场景

**iwiki 文档**：包含附件 + 腾讯文档链接

**结果**：
```
files/FiT-资金中台/技术文档/API文档/
├── 接口说明.pptx                ← 可下载附件
├── 数据字典.xlsx                ← 可下载附件
├── 测试报告.pdf                 ← 可下载附件
└── 关联的腾讯文档.md            ← 腾讯文档引用清单
    包含:
    文章1: 在线协作文档 (腾讯文档)
    文章2: 测试用例表 (腾讯表格)
```

---

## 📈 下载报告

### 报告格式

```markdown
## 文件附件下载报告

✅ 附件文件: 18 个
   ├─ PPT: 8 个
   ├─ Excel: 6 个
   ├─ Word: 2 个
   └─ PDF: 2 个

🔗 外部链接: 8 个文档
   ├─ 腾讯文档: 12 个链接
   ├─ 腾讯表格: 5 个链接
   └─ 微信文档: 2 个链接

### 详细列表:

技术方案设计.md
├─ 附件: 系统架构.pptx (2.3 MB)
└─ 外部链接: 2个 (详细设计文档, 接口定义表)

需求分析.md
├─ 附件: 
│   ├─ 用户调研.xlsx (1.2 MB)
│   └─ 需求说明.docx (456 KB)
└─ 外部链接: 1个 (在线需求池)

API文档.md
├─ 附件: 
│   ├─ 接口说明.pptx (3.1 MB)
│   └─ 测试报告.pdf (890 KB)
└─ 外部链接: 3个 (接口测试用例, 性能报告, 上线检查表)
```

---

## 🔍 附件信息展示

### Markdown 文档中的展示

在下载的 Markdown 文档中，可以添加附件信息章节：

```markdown
# 系统架构设计

## 相关附件 📎

### 本地附件
- [系统架构方案.pptx](../../../files/FiT-资金中台/技术文档/系统架构设计/系统架构方案.pptx)
- [数据模型.xlsx](../../../files/FiT-资金中台/技术文档/系统架构设计/数据模型.xlsx)

### 在线文档 🔗
详见: [external-links.txt](../../../files/FiT-资金中台/技术文档/系统架构设计/external-links.txt)

主要包含:
1. 详细设计文档（腾讯文档）
2. 接口定义表（腾讯表格）
3. 评审记录（腾讯文档）

---

## 正文开始...
```

---

## ⚙️ 配置与选项

### 启用/禁用附件下载

**默认行为**：自动下载所有附件

**自定义**：
```
用户: "拉取文档，但跳过附件下载"
```

### 文件大小限制

**建议配置**：
- 单个文件: < 100 MB
- 总大小: < 1 GB

**如果超过限制**：
- 记录文件信息到 external-links.txt
- 提示用户手动下载

---

## 🧹 维护建议

### 定期清理

```bash
# 查找大文件
find 我的知识库/files -type f -size +50M

# 检查重复文件
find 我的知识库/files -type f -exec md5 {} \; | sort | uniq -d

# 统计文件类型
find 我的知识库/files -type f | sed 's/.*\.//' | sort | uniq -c
```

### 验证附件完整性

```bash
# 检查附件是否完整（文件大小 > 0）
find 我的知识库/files -type f -size 0

# 验证外部链接有效性（需要 curl）
grep -r "https://" 我的知识库/files/*/external-links.txt | \
  cut -d: -f2 | xargs -I {} curl -s -o /dev/null -w "%{http_code} {}\n" {}
```

---

## 📦 批量操作

### 批量下载附件

```
用户: "重新下载所有附件 @我的知识库/iwikis/FiT-资金中台/"
```

系统会：
1. 扫描所有文档
2. 检查已有附件
3. 下载缺失的附件
4. 更新 frontmatter

### 批量更新腾讯文档清单

```
用户: "更新所有腾讯文档清单 @我的知识库/iwikis/FiT-资金中台/"
```

系统会：
1. 重新扫描所有文档内容
2. 提取腾讯文档链接
3. 更新 关联的腾讯文档.md 文件，包含完整的文章信息

---

## 🎁 优势总结

### 附件本地化
- ✅ 离线可用，不依赖网络
- ✅ 保留原始文件，便于编辑
- ✅ 版本控制友好

### 外部链接管理
- ✅ 集中管理，一目了然
- ✅ 保留上下文信息
- ✅ 便于权限审计

### 组织结构
- ✅ 镜像文档结构，易于查找
- ✅ 每个文档独立文件夹
- ✅ 支持增量更新

---

**版本**: v2.1  
**最后更新**: 2026-02-14  
**相关文档**: [README_CN.md](README_CN.md) | [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)
