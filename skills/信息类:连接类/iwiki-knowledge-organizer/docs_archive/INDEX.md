# iWiki Knowledge Organizer - 文档索引

## 📚 文档结构

```
.cursor/skills/iwiki-knowledge-organizer/
├── SKILL.md              # AI使用的技术规范文档（英文）
├── README.md             # 英文简介
├── README_CN.md          # 📖 完整中文使用手册（推荐阅读）⭐
├── INDEX.md              # 本文件 - 文档索引
├── examples.md           # 使用示例
└── scripts/              # 辅助工具脚本
    ├── README.md         # 脚本详细说明
    ├── convert_to_hierarchical.py    # ⭐ 主要工具：图片重组
    ├── fix_md_refs_final.py          # 引用修复工具
    ├── update_md_refs.py             # 引用更新工具
    └── ... (其他脚本)
```

---

## 🎯 快速导航

### 对于普通用户

**👉 直接阅读**: [README_CN.md](README_CN.md) - 完整的中文使用手册

**包含内容**:
- ✅ 功能概述和核心能力
- ✅ 快速开始指南
- ✅ 详细使用场景
- ✅ 辅助工具说明
- ✅ 常见问题解答
- ✅ 最佳实践建议

---

### 对于开发者/高级用户

#### 1. 技术规范
- [SKILL.md](SKILL.md) - AI Agent使用的完整技术文档
  - URL解析逻辑
  - 工作流程详解
  - MCP工具调用规范
  - 路径计算算法

#### 2. 使用示例
- [examples.md](examples.md) - 实际使用案例
  - 不同场景的操作示例
  - 命令行操作演示

#### 3. 辅助脚本
- [scripts/README.md](scripts/README.md) - 脚本工具详细文档
  - 每个脚本的功能说明
  - 使用场景和示例
  - 故障排除指南

---

## 📖 推荐阅读顺序

### 新手入门
1. **[README_CN.md](README_CN.md)** - 从这里开始！
2. **[examples.md](examples.md)** - 看实际案例
3. 开始使用 - 直接对AI说："拉取 https://iwiki.woa.com/space/xxx"

### 进阶使用
1. **[README_CN.md](README_CN.md)** - 了解全部功能
2. **[scripts/README.md](scripts/README.md)** - 掌握辅助工具
3. 使用脚本优化已有内容

### 深度定制
1. **[SKILL.md](SKILL.md)** - 理解技术细节
2. **[scripts/](scripts/)** - 查看和修改脚本
3. 根据需要扩展功能

---

## 🔍 按需求查找

### 我想...

#### ...了解这个Skill能做什么
→ [README_CN.md - 功能概述](README_CN.md#功能概述)

#### ...快速开始下载iwiki文档
→ [README_CN.md - 快速开始](README_CN.md#快速开始)

#### ...优化已下载图片的存储结构
→ [README_CN.md - 辅助工具](README_CN.md#辅助工具)  
→ [scripts/README.md](scripts/README.md)

#### ...解决图片显示问题
→ [README_CN.md - 常见问题 Q1](README_CN.md#q1-图片显示不出来怎么办)

#### ...了解图片存储策略
→ [README_CN.md - 图片存储策略](README_CN.md#3️⃣-图片与文件管理)  
→ [DIRECTORY_STRUCTURE.md - 完整目录结构](DIRECTORY_STRUCTURE.md) 🆕  
**说明**: 统一采用层级化存储，默认路径为 `我的知识库/images/`

#### ...了解文件附件管理
→ [FILES_MANAGEMENT.md - 文件附件管理详解](FILES_MANAGEMENT.md) 🆕  
**说明**: 自动下载 PPT/Excel/Word/PDF 等附件，追踪外部链接（腾讯文档等）

#### ...了解 iwiki 内部链接管理
→ [IWIKI_INTERNAL_LINKS.md - iwiki 内部链接管理](IWIKI_INTERNAL_LINKS.md) 🆕  
**说明**: 自动处理文档间引用，已下载的替换为本地路径，未下载的自动下载

#### ...保持知识库与iwiki同步 ⭐
→ [README_CN.md - 增量同步功能](README_CN.md#增量同步功能详解-)  
→ [README_CN.md - 场景6: 增量同步更新](README_CN.md#场景6-增量同步更新--新功能)

#### ...查看具体的使用案例
→ [examples.md](examples.md)

#### ...理解技术实现细节
→ [SKILL.md](SKILL.md)

#### ...修改或扩展脚本
→ [scripts/](scripts/) 目录下的Python脚本

---

## 📊 功能清单

### 核心功能

- [x] 自动识别iWiki URL类型（空间/文档）
- [x] 递归下载文档树
- [x] 批量下载图片（序号前缀命名）
- [x] iwiki 内部链接管理（自动下载关联文档） 🆕
- [x] 下载文件附件（PPT/Excel/Word/PDF 等）
- [x] 外部链接追踪（腾讯文档等）
- [x] 保持iWiki层级结构
- [x] 自动计算相对路径
- [x] 元数据保存（创建者、时间等）
- [x] 层级化存储（文档/图片/附件）
- [x] 权限受限图片智能处理
- [x] 下载报告生成

### 辅助工具

- [x] 图片目录重组工具
- [x] Markdown引用修复工具
- [x] 引用更新工具
- [x] 自动备份功能

### 增量同步功能 ⭐ **新增**

- [x] 智能对比本地和远程时间戳
- [x] 最小化更新（只更新变化的文档）
- [x] 增量图片下载
- [x] 多种更新策略（最小化/强制/仅图片/仅元数据）
- [x] 孤立图片清理
- [x] 冲突智能处理
- [x] 详细同步报告

### 计划功能

- [ ] 本地修改保护标记
- [ ] 自动定期同步
- [ ] 版本对比工具
- [ ] 图片压缩优化
- [ ] 批量重命名工具
- [ ] 文档搜索索引

---

## 🆘 需要帮助？

### 常见问题
→ [README_CN.md - 常见问题](README_CN.md#常见问题)

### 脚本问题
→ [scripts/README.md - 故障排除](scripts/README.md#故障排除)

### 联系方式
- 提交Issue到项目仓库
- 查看文档中的解决方案

---

## 📈 版本信息

**当前版本**: v2.1  
**最后更新**: 2026-02-14

**主要变更**:
- v2.1: 默认目录优化 + 图片序号前缀命名 + **iwiki 内部链接管理** + 文件附件管理 + 外部链接追踪 + 单文档层级保存
- v2.0: 统一采用层级化图片存储，提供扁平转层级的重组工具
- v1.0: 基础文档下载（使用扁平图片存储，已废弃）

---

## 🔗 相关链接

- [iWiki官网](https://iwiki.woa.com)
- Skill主文档: [SKILL.md](SKILL.md)
- 中文手册: [README_CN.md](README_CN.md) ⭐
- 目录结构说明: [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) 🆕
- 文件附件管理: [FILES_MANAGEMENT.md](FILES_MANAGEMENT.md) 🆕
- 腾讯文档格式: [TENCENT_DOCS_FORMAT.md](TENCENT_DOCS_FORMAT.md) 🆕
- iwiki 内部链接: [IWIKI_INTERNAL_LINKS.md](IWIKI_INTERNAL_LINKS.md) 🆕
- 更新日志: [CHANGELOG.md](CHANGELOG.md)
- 快速参考: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 脚本工具: [scripts/README.md](scripts/README.md)
- 使用案例: [examples.md](examples.md)

---

**提示**: 如果您是第一次使用，强烈建议从 **[README_CN.md](README_CN.md)** 开始阅读！
