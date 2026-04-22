# iWiki Knowledge Organizer

把 iwiki（腾讯内部 wiki）文档拉取到本地知识库：下载正文、图片（序号命名）、附件，并记录腾讯文档等外部链接。

## 何时会用到

对 AI 说「拉取 iwiki」「下载 iwiki 文档」「整理 iwiki 知识库」或给出 iwiki 链接时，会使用本 skill。

## 怎么用

1. 给一个 iwiki 链接：
   - 空间：`https://iwiki.woa.com/space/{spaceKey}`  
   - 文档：`https://iwiki.woa.com/p/{docid}`
2. 按提示选择保存位置（可直接用默认）。
3. 等待拉取完成即可。

**示例**：`拉取 https://iwiki.woa.com/p/4015651258`

## 默认目录

- 文档：`我的知识库/iwikis/`（按空间/文件夹/文档层级）
- 图片：同一级共用的 `_images` 文件夹，各文档在 `_images/{文档名}/` 下
- 附件与腾讯文档引用：同一级共用的 `_files` 文件夹，各文档在 `_files/{文档名}/` 下

## 详细规则

完整流程、命名与格式规则见 **[SKILL.md](SKILL.md)**（AI 按该文件执行）。  
中文简要说明见 **[README_CN.md](README_CN.md)**。  
历史/补充文档在 **docs_archive/**，需要时再查。
