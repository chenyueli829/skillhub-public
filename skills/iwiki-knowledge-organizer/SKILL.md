---
name: iwiki-knowledge-organizer
description: Pulls documentation from iwiki (Tencent internal wiki) and organizes it into a local knowledge base. Use when the user mentions iwiki, knowledge base organization, document pulling, or wants to download/organize iwiki documentation with images and external file tracking.
---

# iWiki Knowledge Organizer

Automates the process of pulling iwiki documentation to local storage, including recursive document fetching, image downloading with index prefixes, external file dependency tracking, and reference updating.

## Quick Start

When the user asks to organize iwiki documentation, follow this workflow:

1. **Get iwiki URL from user** - User can provide:
   - Space URL: `https://iwiki.woa.com/space/{spaceKey}` (e.g., `https://iwiki.woa.com/space/~username`)
   - Document URL: `https://iwiki.woa.com/p/{docid}` (can be folder or single document)
2. **Parse URL and identify type** - Extract spaceKey or docid
3. **Fetch metadata** - Get space/document information using appropriate MCP tools
4. **关联 iWiki** - 默认将正文中的 iwiki.woa.com/p/* 关联文档一并拉取（空文档检查 + 确认）；用户明确说「不拉关联」「只拉当前」时不拉关联
5. **空文档与确认** - 拉取正文/树后先判断是否为空；仅展示「内容非空」的文档列表，等待用户确认后再执行下载（空文档不下载，见下方「空文档与确认」规范）
6. **Ask user for save location** (default: `~/Desktop/21-Secret-内网知识库/iwikis/` or custom path)
7. **Fetch content** - 仅对「内容非空」且用户已确认的文档执行下载（含默认加入的关联文档）
8. **Download images** - 图片命名**仅**使用 **编号-图片名称.后缀**（如 `1-image.png`），不得使用「文件名称-编号.后缀」或「文档名-编号-图片名」
9. **Download document attachments** - 对每个文档调用 getAttachmentList(docid)，将**文档下方挂载的非图片类附件**（PPT/Excel/Word/PDF 等）下载到 files 目录（必做，见「文档下方附件必须拉取」）
10. **Extract external dependencies** - Detect Tencent Docs and other external file references
11. **Create dependencies manifest** if external files found
12. **Update references** - 图片与本地路径；正文中的 iWiki 内链替换为本地相对路径（仅对本次已下载的文档）
13. **Generate log** of all operations including dependency count

---

## Core Workflows

### 空文档与确认（必遵）

- **空文档不下载**：若 iWiki 文档正文为空（`getDocument` 返回内容 strip 后无实质文字，且无图片、无附件、无外链），则**不**写入本地，不创建目录。
- **先展示非空部分**：在真正执行下载前，先拉取正文/树，区分「内容非空」与「内容为空」的文档，**仅向用户展示内容非空的部分**（列表：标题、路径、可选简要说明如是否有图/外链）。
- **等待用户确认后再下载**：展示非空列表后，明确询问用户「是否确认下载以上文档？」；用户确认后，再询问保存位置并执行下载。未确认前不创建本地文件、不下载图片/附件。

**空文档判定**：`getDocument(docid)` 返回的 body 去掉首尾空白后长度为 0，且 `listImages(docid)` 为空、无附件、无外链引用时，视为空文档。仅正文为空但有图/附件/外链时视为非空（会展示并等待确认后下载）。

### 已存在则跳过与结束前输出（必遵）

- **下载前检查本地是否已存在**：在执行任一文档下载前，先在本地 iwikis 目录下检查是否已有该文档（通过检索「文档来源: https://iwiki.woa.com/p/{docid}」是否存在）。若已存在，则**跳过**该文档的下载与覆盖，并将该文档（docid、本地路径或标题）加入「已存在故未下载」列表。
- **结束前输出已存在未下载列表**：整次拉取/补拉流程结束前，必须输出「已存在故未下载」的文章列表（可含 docid、标题、本地路径），便于用户核对哪些文章因已存在而被跳过。

### 文档下方附件必须拉取（必遵）

- **不得只拉正文和图片**：iWiki 文档除正文和图片外，常在该文档**下方挂载附件**（PPT、Excel、Word、PDF、ZIP 等）。拉取任一文档时，**必须**同时拉取这些「文档下方挂载的文件」，不得遗漏。
- **操作要求**：对每个要保存的文档，调用 `user-iWiki-getAttachmentList(docid)` 获取该文档下全部附件；已通过 listImages 处理的图片类附件可跳过，对其余**非图片类附件**（如 .pptx/.xlsx/.docx/.pdf/.zip 等）逐一调用 `user-iWiki-getAttachmentDownloadUrl(attachmentid)` 下载，保存到**该层级共用的 `_files/{文档名}/`**（见「图片与文件：同级共用 _images、_files」），路径各段去空格。
- **与「本文引用」的关系**：若正文或正文底部需引用这些附件，可在该文档的「本文引用」小节中列出指向同层级 `_files/{文档名}/` 下文件的相对路径链接（可选，按需添加）。

### 文档若同时为文件夹则必须拉取子文档（必遵）

- **先判断是否为文件夹**：iWiki 中某页面可以既有正文内容，又在该页面下挂有子页面（即该节点既是文档也是文件夹）。拉取任意 `https://iwiki.woa.com/p/{docid}` 时，**必须先**调用 `user-iWiki-getSpacePageTree(docid)` 判断该 docid 下是否有子节点。
- **有子页面则按文件夹拉取**：若 getSpacePageTree 返回的树中该节点下存在子页面，则视为**文件夹**，必须按「递归拉取」（Workflow 2）处理：拉取该节点本身（当前页正文、图片、附件）**并**递归拉取其下所有子文档，保持层级结构。**不得**仅按单文档拉取当前页而遗漏其下子文档。
- **无子页面才按单文档拉取**：仅当 getSpacePageTree 显示该节点无子节点时，才按单文档（Workflow 3）只拉取该页。

### 关联 iWiki 默认一并拉取（必遵）

- **默认行为**：拉取某篇文档或空间/文件夹时，扫描正文中的 iWiki 内链（`https://iwiki.woa.com/p/{docid}`），将**未下载的关联文档**一并加入本次拉取范围；对关联文档同样做空文档检查与确认；拉取完成后将正文中的这些链接替换为本地相对路径。
- **用户明确不拉关联时除外**：若用户明确说「不拉取关联的 iwiki」「只拉当前文档」「关联的不用拉」「不要拉链接里的文档」等，则**不**把正文中的 iwiki 链接加入拉取范围，仅拉用户指定的文档/树，链接保持为原 iWiki URL。
- **执行顺序**：先确定「本次要拉取的文档集合」（当前文档/树 + 默认包含的关联文档），再做空文档检查 → 展示非空列表 → 用户确认 → 再执行下载与链接替换。

### 文档 frontmatter 与正文格式（必遵）

- **顶部 frontmatter 仅保留 4 项**（简化，不写多余元数据）：
  ```yaml
  ---
  title: {文档标题}
  文档来源: https://iwiki.woa.com/p/{docid}
  createtime: "{YYYY-MM-DD HH:mm:ss}"
  updatetime: "{YYYY-MM-DD HH:mm:ss}"
  ---
  ```
  不写入：docid、space、spacekey、path、creator、last_modifier、content_changetime、external_dependencies 等。

- **本文引用放在文章底部**：若有腾讯文档等外部依赖，**不要**在 frontmatter 中写 `external_dependencies`；在正文末尾（`---` 之后）追加「本文引用」小节，列出依赖文件链接。示例：
  ```markdown
  ---
  title: xxx
  文档来源: https://iwiki.woa.com/p/4015651258
  createtime: "2025-07-22 09:32:04"
  updatetime: "2025-10-27 17:49:48"
  ---

  （正文与图片、内链等）

  ---
  **本文引用**
  - [1-腾讯文档-资金账务业务发展规划](_files/资金账务领域架构/1-腾讯文档-资金账务业务发展规划.md)
  ```

- 扫描/更新时从 frontmatter 的 `文档来源` URL 中解析 docid（或从正文中的「文档来源」行解析），不依赖 docid 字段。

### Workflow 1: Detect and Pull from iwiki URL

```markdown
Task: User provides iwiki URL, detect type and pull accordingly

Steps:
1. Get iwiki URL from user (required input)

2. Parse URL and extract identifier:
   a) If URL matches `https://iwiki.woa.com/space/{spaceKey}`:
      - Extract spaceKey (e.g., "~username", "woa", "fit")
      - Call user-iWiki-getSpaceInfoByKey(spaceKey) to get space info
      - Extract homepage docid from space info
      - Use homepage docid as starting point
   
   b) If URL matches `https://iwiki.woa.com/p/{docid}`:
      - Extract docid directly from URL
      - Use docid as starting point

3. Get document metadata:
   - Call user-iWiki-metadata(docid) to get document info

4. **必做：检查是否为文件夹（是否有子页面）**
   - Call user-iWiki-getSpacePageTree(docid) to get tree for this docid
   - 若该节点下存在子节点（子页面），则该文档**同时为文件夹**，必须按文件夹处理

5. Determine type（必遵「文档若同时为文件夹则必须拉取子文档」）:
   - **If has children**: SPACE or FOLDER → 按 Workflow 2 **递归拉取**该节点及整棵子树（含当前页与所有子文档）；不得只拉当前页
   - **If no children**: SINGLE DOCUMENT → pull one file（Workflow 3）

6. **关联 iWiki 与空文档检查、确认（必做）：**
   - **是否拉取关联**：若用户明确说「不拉取关联的 iwiki」「只拉当前」「关联不用拉」等，则 skip_linked_iwiki = true；否则默认一并拉取正文中出现的 iwiki.woa.com/p/{docid} 所指文档。
   - **单文档**：Call user-iWiki-getDocument(docid)。若为空则直接回复「该文档内容为空，已跳过下载」，结束。若非空，且未 skip_linked_iwiki：从正文中提取所有 iwiki.woa.com/p/{docid}，去重，对每个关联 docid 拉取 content 并做空检查；列出「将下载：当前文档 + 关联文档（仅列非空）」及「将跳过：空文档」；询问「是否确认下载以上文档？」。若 skip_linked_iwiki 则只列当前文档并确认。
   - **空间/文件夹**（含「既是文档又有子页面」的节点）：预扫 getSpacePageTree + 对树中每个页面 getDocument 做空检查；若未 skip_linked_iwiki，再从这些文档正文中提取所有 iwiki.woa.com/p/{docid}，去掉已在树内的，得到「关联 docid 集合」，对每个关联 docid 做空检查；输出「内容非空（将下载）：树内文档 + 关联文档」「内容为空（将跳过）：…」；询问「是否确认下载以上非空文档？」。若 skip_linked_iwiki 则只列树内文档。
   - **批量处理优化（新增）**：
     - 当关联文档数量较多（>5个）时，采用批量处理策略
     - 先批量获取所有关联文档的metadata，过滤出有权限且非空的
     - 对于无权限或空文档，直接在确认列表中标注状态，不重复询问
     - 批量下载时使用并行策略，减少总耗时
     - 每完成一组（如3-5个）文档后输出进度提示
   - 未确认前不询问保存路径、不执行下载。

7. Ask user for save location (default: `~/Desktop/21-Secret-内网知识库/iwikis/`)（图片与文件保存在各层级共用的 _images、_files，按文档名分子目录，无需单独询问）

8. Execute appropriate workflow based on type（仅处理已确认且内容非空的文档）

9. Report completion with statistics
```

### Workflow 2: Recursive Pull (Space/Folder)

```markdown
Task: Pull entire document tree with hierarchy（仅下载内容非空且用户已确认的文档；默认包含正文中关联的 iWiki）

Steps:
0. **预扫与确认（必做）：**
   - 若用户未明确说「不拉关联」：在预扫树内文档时，从每个文档正文中提取 iwiki.woa.com/p/{docid}，去重，去掉已在树内的，得到「关联 docid 集合」；对每个关联 docid 拉取 content 并做空检查。
   - Call user-iWiki-getSpacePageTree(parentid) 得到完整树；对树中每个「页面」节点 getDocument，判断是否为空。
   - 输出：「内容非空（将下载）：树内文档 + 关联文档（若有）」「内容为空（将跳过）：…」。询问用户「是否确认下载以上非空文档？」；未确认则不执行后续下载。

1. 仅对「内容非空」且用户已确认的文档执行以下步骤（包含树内节点 + 默认加入的关联文档；关联文档按 metadata 建层级路径）。

2. For each non-empty document (tree + linked, if any):
   - **若本地已存在**：在 iwikis 下检索是否已有「文档来源」含该 docid 的 .md；若有则跳过下载，并将该文档加入「已存在故未下载」列表，继续下一篇。
   - Download content using user-iWiki-getDocument(docid)
   - Save as Markdown with simplified frontmatter（仅 title、文档来源、createtime、updatetime）；若有外部依赖则在正文底部写「本文引用」小节
   - Preserve folder hierarchy from iwiki
   - Download all images using user-iWiki-listImages(docid)
   - **图片命名：** 仅用「编号-图片名称.后缀」（如 `1-image.png`），不得使用文档名-编号-xxx
   - Save to: `{save_location}/{space}/{父路径}/_images/{doc}/{编号}-{图片名称}.{ext}`（与同级 .md 共用一个 _images，按文档名分子目录；禁止每文档一层 _images）
   - **拉取文档下方附件（必做）：** Call user-iWiki-getAttachmentList(docid)，对非图片类附件（PPT/Excel/Word/PDF/ZIP 等）逐一 getAttachmentDownloadUrl 并下载到 `{save_location}/{space}/{父路径}/_files/{doc}/{原文件名}.{ext}`（路径各段去空格；同级共用 _files，按文档名分子目录）
   - Extract external file dependencies (Tencent Docs, etc.)
3. Update all image references to local paths with index prefix
4. Create dependencies manifests for documents with external references
5. **Update cross-document links**：将正文中的 iwiki.woa.com/p/{docid} 替换为本地相对路径（仅替换本次已下载的 docid），格式 [标题](相对路径/to/doc.md)
6. **生成/更新 space.md**：在各空间根目录下生成或更新 space.md（空间名、spacekey、空间 URL、已下载文档列表/树）；若已有「Generate index file with tree structure」则合并为同一 space.md
7. **结束前输出**：Report 含 total documents (downloaded / skipped empty)、其中关联文档数、images、external dependencies、success/failures；并输出「已存在故未下载」的文章列表（docid、标题、本地路径）
   - **报告格式示例**：
     ```markdown
     ## ✅ 批量下载完成！
     
     ### 📊 下载统计
     **总计**: {N}个关联文档
     - ✅ **成功下载**: {X}个文档
     - ❌ **无权限**: {Y}个文档
     - ⏭️ **已存在跳过**: {Z}个文档
     
     ### 📁 成功下载的文档
     1. **文档标题**
        - 路径: {相对路径}
        - 图片: {N}张（{M}张无权限）
        - 附件: {K}个
     
     ### ❌ 无权限文档（已标记）
     - {docid} - {标题}
     
     ### 🔗 链接更新
     ✅ 已自动将已下载文档的链接替换为本地相对路径
     ✅ 已创建/更新 {N} 个空间索引文件（space.md）
     ```
```

### Workflow 3: Single Document Pull

```markdown
Task: Pull one document with its images（仅当内容非空且用户确认后执行）

IMPORTANT: Single documents MUST follow the same hierarchical structure as space/folder pulls.

Steps:
1. Call user-iWiki-getDocument(docid) to get content.
2. **空文档检查：** 若正文 strip 后为空且 listImages 为空、无附件/外链，则直接回复「该文档内容为空，已跳过下载」，结束；不创建任何本地文件。
3. **确认后再下载：** 若内容非空，先向用户展示：文档标题、是否有图片/附件/外链。**若用户未明确说不拉关联**：从正文提取所有 iwiki.woa.com/p/{docid}，去重，对每个关联 docid 拉取 content 并做空检查，展示「关联文档（非空）：[标题 / docid]」；询问「是否确认下载（含上述关联文档）？」。若用户明确说不拉关联则只确认当前文档。
4. **若本地已存在**：在 iwikis 下检索是否已有「文档来源」含本 docid 的 .md；若有则跳过下载，将该文档加入「已存在故未下载」列表，结束并在 Report 中输出该列表。
5. Call user-iWiki-metadata(docid) to get metadata
6. **Extract full path hierarchy from metadata:**
   - Get **space name** (spacename) from metadata 或 getSpaceInfoByKey(metadata.spacekey).name，不得用 spacekey 作为目录名
   - Get parent document chain by recursively calling user-iWiki-metadata(parentid)
   - Build full path: {space-name}/{parent-folders}/{doc-name}（各段去空格；spacename 若含 `/` 则替换为 `-`）
7. **Create hierarchical directory structure（不按文档建子目录）：**
   - Create: {save_location}/{space-name}/{parent-folders}/（同级文档的 .md 均在此目录，如 文档A.md、文档B.md）
   - 在该目录下建一个 _images、一个 _files；各文档图片/附件在 _images/{文档名}/、_files/{文档名}/。Even for single document, preserve iwiki folder structure.
8. Call user-iWiki-listImages(docid) to list all images
9. **For each image (in document order):**
   - Call user-iWiki-getAttachmentDownloadUrl(attachmentid)
   - Download using curl 到该层级**共用的** _images 下、以文档名命名的子目录
   - **图片命名：** 仅用「编号-图片名称.后缀」（如 `1-image.png`），不得使用文档名-编号-xxx
   - Save to: `{save_location}/{space}/{父路径}/_images/{doc}/{编号}-{图片名称}.{ext}`（多个同级文档共用一个 _images，按文档名分子目录）
   - Index starts from 1, increments for each image
10. **拉取文档下方附件（必做）：** Call user-iWiki-getAttachmentList(docid) 获取该文档下全部附件；对**非图片类**附件（PPT、Excel、Word、PDF、ZIP 等）逐一 Call user-iWiki-getAttachmentDownloadUrl(attachmentid)，下载到 `{save_location}/{space}/{父路径}/_files/{doc}/{原文件名}.{ext}`（路径各段去空格；同级共用 _files，按文档名分子目录）。不得只拉正文和图片而遗漏文档下方挂载的文件。
11. **Extract external link references from document content:**
   - Scan for iwiki internal links (iwiki.woa.com/p/*)：若本次已拉取该 doc（含关联文档），在**全部文档保存完成后**统一替换为本地相对路径（见步骤 16）。
   - Scan for Tencent Doc links (docs.qq.com, doc.weixin.qq.com) …
   - If found, create Tencent doc reference file(s) with naming `{序号}-腾讯文档-{文档名称}.md` (see Workflow 5)
12. Create .md file in proper hierarchical location：frontmatter 仅 4 项；若有外部依赖则在正文末尾追加「本文引用」小节
13. Update image references to 同级相对路径：`_images/{文档名}/{编号}-{图片名称}.{ext}`（与 .md 同目录，多文档共用一个 _images）
14. 不在 frontmatter 中写 attachment 列表；若有附件可在正文底部「本文引用」前补充说明（可选）
15. **若本次包含关联文档**：对每个已确认且非空的关联 docid，按同结构执行（metadata → 路径 → 目录 → getDocument/listImages/附件/外链 → 保存 .md）；关联文档也做空检查、本文引用等
16. **统一替换 iWiki 内链**：在所有已保存的 .md 中，将正文里的 iwiki.woa.com/p/{本次已下载的 docid} 替换为本地相对路径，格式 [标题](相对路径/to/doc.md)；已下载的关联文档之间也做同样替换
17. **生成/更新 space.md**：在本次涉及的各空间根目录下生成或更新 space.md（见「空间根目录下生成 space.md」）
18. **结束前输出**：Report 含 document name, full path, 关联文档数（若有）, image count, attachment count, external links count, save location；若有因已存在而跳过的文档，输出「已存在故未下载」的文章列表（docid、标题、本地路径）
```

### Workflow 4: Internal iwiki Links Management 🔗

```markdown
Task: 事后处理正文中的 iWiki 内链（拉取时未一并拉取关联文档时使用）

说明：拉取时默认已一并拉取关联文档并替换为本地路径（见「关联 iWiki 默认一并拉取」）。本流程用于：用户当时选择了「不拉关联」、或事后希望补拉/补链。

Steps:
1. **Scan for iwiki internal links:**
   - Pattern 1: https://iwiki.woa.com/p/{docid} (文档链接)
   - Pattern 2: https://iwiki.woa.com/space/{spaceKey} (空间链接)
   - Extract all docid and spaceKey from document content
   - Get list of already downloaded documents（从 frontmatter 的 文档来源 URL 解析）
   
2. **处理空间链接（新增）:**
   - 对于 `https://iwiki.woa.com/space/{spaceKey}` 链接：
   - 在本地 iwikis/ 目录下查找是否有对应的 space.md 文件
   - 查找方式：检查 space.md 中是否包含该 spaceKey
   - If found: 替换为本地相对路径 `[空间名称](../../空间目录/space.md)`
   - If not found: 保留原链接（该空间未下载）
   
3. **Check if referenced doc exists locally:**
   - Search in local iwikis/ for docid
   - If found: calculate relative path and replace link
   - If not found: add to download queue（可选：按 Workflow 3 拉取并维持层级）
   
4. **Download missing referenced docs (optional):**
   - For each missing docid: get metadata, download to iwikis/{space}/{folder}/{title}.md, process recursively if needed
   
5. **Update all internal links:**
   - Replace iwiki.woa.com URLs with local relative paths
   - 文档链接格式: [文档标题](../../../path/to/doc.md)
   - 空间链接格式: [空间名称](../../../空间目录/space.md)
   - Preserve link text if exists
```

### Workflow 5: File Attachments and External References Management 📎

```markdown
Task: Download file attachments and track external references

IMPORTANT: Handle both downloadable attachments and non-downloadable external links.

Steps:
1. **Check for iwiki attachments:**
   - Call user-iWiki-getAttachmentList(docid) to list all attachments
   - Filter out images (already handled)
   - Identify file types: PPT, Excel, Word, PDF, ZIP, etc.
   
2. **Download file attachments:**
   - For each non-image attachment:
     - Call user-iWiki-getAttachmentDownloadUrl(attachmentid)
     - Download file using curl
     - Save to: `{save_location}/{space}/{父路径}/_files/{doc}/{filename}.{ext}`（与同级 .md 共用一个 _files，按文档名分子目录）
     - Keep original filename
   
3. **Scan document content for external links:**
   - Tencent Doc patterns:
     - https://docs.qq.com/doc/*
     - https://docs.qq.com/sheet/*
     - https://docs.qq.com/slide/*
     - https://doc.weixin.qq.com/*
   - Excel Online patterns
   - Other cloud storage links
   
4. **Create Tencent docs reference file(s) (if found):**
   - **File naming:** `{编号}-腾讯文档-{文档名称}.md`，例如 `1-腾讯文档-资金账务业务发展规划.md`
   - One file per external link: `1-腾讯文档-名称1.md`, `2-腾讯文档-名称2.md`, ...
   - Location: `{save_location}/{space}/{父路径}/_files/{doc}/` (path 各段已去除空格；同级共用一个 _files，按文档名分子目录)
   - **Content (simplified):** 仅保留「来源文档」和「链接」两要素
   
   **Simplified manifest format (简化格式):**
   ```markdown
   # {编号}-腾讯文档-{文档名称}
   
   来源文档：[{来源 iwiki 文档标题}]({相对路径到该 .md})
   
   **链接**：[点击打开/下载]({腾讯文档完整 URL})
   ```
   - **链接** 必须写成 Markdown 链接形式 `[点击打开/下载](URL)`，方便用户点击快速跳转。
   - 若有多个链接，同一文件内可依次列出多个「**链接**」；或为每个链接单独一个文件（文件名用对应文档名称）。
   - 不在文件中写长说明、注意事项、类型枚举等，保持极简。

5. **Update main document:**
   - **不要**在 frontmatter 中写 external_dependencies。
   - 在正文末尾追加「本文引用」小节：先 `---` 分隔，再写 `**本文引用**`，然后列出依赖文件为 Markdown 链接，例如：
     `- [1-腾讯文档-{文档名称}](相对路径到该 .md)`

6. **Report:**
   - Number of external references found
   - Dependencies manifest file location
   
**Benefits:**
- Track all external dependencies in one place
- Easy to review what external files are referenced
- Maintain links even if original document changes
- Audit trail for file access requirements
```

### Workflow 6: Update Existing Documents (Scan Mode)

```markdown
Task: Scan local folder and download missing iwiki images

Steps:
1. User specifies folder to scan
2. Find all .md files recursively
3. For each file:
   - Look for "文档来源: https://iwiki.woa.com/p/{docid}" in content
   - Extract docid
   - Parse existing image references
   - Check which images are missing locally
4. Download missing images only
5. Update image references in .md files
6. Report: files scanned, images downloaded, skipped
```

### Workflow 7: Incremental Sync/Update ⭐

```markdown
Task: Check for updates and synchronize local knowledge base with iwiki

Trigger Phrases:
- "同步更新 {folder}"
- "检查更新 {space_url}"
- "增量更新知识库"
- "同步iwiki文档"

Steps:
1. Scan Target Directory:
   - User specifies folder path (e.g., "产品组/FiT-资金中台/")
   - Find all .md files recursively
   - Extract metadata from frontmatter（从 文档来源 解析 docid；updatetime 用于判断是否更新）

2. Check Each Document for Updates:
   For each local document:
   a) Extract docid from frontmatter（从 文档来源 URL 解析）
   b) Call user-iWiki-metadata(iwiki_id) to get remote metadata
   c) Compare timestamps:
      - Local: frontmatter.updatetime
      - Remote: metadata.lastModified
   d) If remote.lastModified > local.updated:
      - Mark document as "needs update"
      - Add to update queue
   
3. Analyze Update Scope:
   - Count documents needing update
   - Estimate total images to check
   - Ask user for confirmation:
     "找到 X 个文档需要更新，是否继续？"

4. Perform Incremental Update:
   For each document in update queue:
   a) Download latest content: user-iWiki-getDocument(docid)
   b) Compare with local content:
      - If content changed: update document body
      - Preserve local customizations (if marked)
   c) Check images:
      - List remote images: user-iWiki-listImages(docid)
      - Compare with local images
      - Download only NEW or CHANGED images
   d) Update frontmatter:
      - Update "updatetime"
      - Preserve title、文档来源、createtime
   e) Update image references if needed

5. Generate Sync Report:
   ```
   同步完成报告
   ==================
   扫描文档: 50 个
   需要更新: 12 个
   已更新文档: 12 个
   新增图片: 8 个
   删除图片: 2 个
   跳过: 38 个 (无变化)
   
   详细更新列表:
   - 技术文档/API设计.md: 内容更新 + 3张新图片
   - 产品文档/需求分析.md: 内容更新
   - 系统架构/架构图.md: 2张新图片
   ...
   ```

6. Optional: Cleanup Orphaned Images:
   - Ask user: "是否删除不再使用的图片？"
   - If yes, remove images not referenced by any document
   - Report: "清理了 X 个孤立图片"

Update Strategies:
- **Minimal Update**: Only update changed documents
- **Force Update**: Re-download all documents (user specified)
- **Image Only**: Only check and update images
- **Metadata Only**: Only update metadata, skip content

Error Handling:
- If document deleted on iwiki: Ask user "文档已删除，是否保留本地副本？"
- If permission denied: Skip and report
- If download fails: Retry once, then report
```

### Workflow 7: Batch Operations

```markdown
Task: Perform batch operations on multiple documents

Operations:
1. Batch Re-download:
   - User provides list of docids or folder
   - Re-download all documents (force update)
   - Useful for fixing corrupted downloads

2. Batch Convert Images:
   - Convert existing flat structure to hierarchical
   - Update all references
   - Use convert_to_hierarchical.py script

3. Batch Metadata Update:
   - Refresh metadata for all documents
   - Don't update content, only frontmatter
   - Useful for tracking who last modified

4. Batch Validation:
   - Check all image references are valid
   - Report broken links
   - Suggest fixes
```

### Workflow 8: 下载后检查（Post-Download Check）✅

```markdown
Task: 拉取完成后检查 iwikis 目录内文档，是否存在正文中引用但未下载的远程 iwiki 链接；若有则执行下载，无法下载的列举并说明原因。**全部处理完毕（已下载或已列举无法下载原因）后，工作流才可结束。**

Trigger Phrases:
- "iwiki下载后检查"
- "检查 iwikis 中是否还有未下载的 iwiki 链接"
- "补拉未下载的关联文档"

Steps:
1. **扫描正文中的 iwiki 文档链接：**
   - 在 ~/Desktop/21-Secret-内网知识库/iwikis/ 下递归查找所有 .md
   - 从正文（不含 frontmatter 的「文档来源」）中提取：
     - 格式一：https://iwiki.woa.com/p/{docid}
     - 格式二：https://iwiki.woa.com/pages/viewpage.action?pageId={docid}（pageId 视为 docid）
   - 去重得到「被引用 docid 集合」

2. **已下载集合：**
   - 从各 .md 的 frontmatter「文档来源: https://iwiki.woa.com/p/{docid}」解析 docid
   - 得到「已下载 docid 集合」

3. **待下载队列：**
   - 待下载 = 被引用 docid 集合 − 已下载 docid 集合

4. **执行下载：**
   - 对「待下载」中每个 docid：**先检查本地是否已存在**（iwikis 下是否有「文档来源」含该 docid 的 .md）；若已存在则跳过，并将该文档加入「已存在故未下载」列表。
   - 对未存在的 docid：按 Workflow 3（单文档拉取）执行拉取（含空文档检查、用户确认策略可简化：批量补拉时可默认确认）
   - 拉取成功后：更新引用该 docid 的 .md，将对应 iwiki URL 替换为本地相对路径

5. **无法下载的列举：**
   - 对拉取失败或跳过（如无权限、已删除、空文档等）的 docid，记录原因
   - 全部下载尝试结束后，输出「无法下载列表」：docid、出现位置（文件名/简要上下文）、原因

6. **结束条件（必遵）：**
   - 仅当「待下载队列」中每一项均已：要么已成功下载并更新链接，要么已存在故跳过，要么已列入「无法下载」并给出原因后，工作流才可结束。
   - **结束前输出**：摘要含「已补拉 X 个」「已存在故未下载 Z 个」（附列表：docid、标题、本地路径）「无法下载 Y 个」（附列表与原因）。
```

### 结束条件（工作流完成标准）

- **拉取/下载后检查场景**：执行 Workflow 8 时，必须满足以下条件才能结束：
  - 正文中出现的所有 iwiki 文档链接（`/p/{docid}` 与 `pageId=`）均已处理完毕；
  - 能下载的已执行下载并已将链接替换为本地路径；
  - 不能下载的已简要列举并写明原因（如无权限、文档已删除、空文档等）。
- 未完成上述步骤前，不得视为工作流结束。

---

## URL Parsing Logic

**CRITICAL: Always parse and validate the iwiki URL first.**

### Step 1: Identify URL Type

```javascript
function parseIwikiUrl(url) {
  // Pattern 1: Space URL
  // Examples:
  //   https://iwiki.woa.com/space/~lylianchen
  //   https://iwiki.woa.com/space/~lylianchen?from=collection
  //   https://iwiki.woa.com/space/woa
  const spaceMatch = url.match(/https:\/\/iwiki\.woa\.com\/space\/([^?&#]+)/);
  if (spaceMatch) {
    return {
      type: 'space',
      spaceKey: spaceMatch[1]  // e.g., "~lylianchen", "woa", "fit"
    };
  }
  
  // Pattern 2: Document URL
  // Examples:
  //   https://iwiki.woa.com/p/1234567890
  //   https://iwiki.woa.com/p/1234567890?tab=history
  const docMatch = url.match(/https:\/\/iwiki\.woa\.com\/p\/(\d+)/);
  if (docMatch) {
    return {
      type: 'document',
      docid: docMatch[1]  // e.g., "1234567890"
    };
  }
  
  // Invalid URL
  return { type: 'invalid' };
}
```

### Step 2: Process Based on Type

**If type = 'space':**
1. Extract `spaceKey` from URL
2. Call `user-iWiki-getSpaceInfoByKey(spaceKey)`
3. Extract homepage `docid` from space info response
4. Continue with document pulling workflow using homepage docid

**If type = 'document':**
1. Extract `docid` from URL
2. Continue with document pulling workflow directly

**If type = 'invalid':**
1. Show error message to user
2. Request valid iwiki URL

### Step 3: Continue with Standard Workflow

Once you have a valid `docid` (either from space homepage or direct document URL):
- Call `user-iWiki-metadata(docid)`
- Call `user-iWiki-getSpacePageTree(docid)`
- Determine if it's a space/folder/document
- Proceed with pulling content

---

## Configuration

**IMPORTANT: Always get configuration from user before starting.**

### Required Input from User:
1. **iwiki URL** (required): The iwiki link to pull
   
   **Format 1: Space URL** (pull entire space from homepage)
   - Format: `https://iwiki.woa.com/space/{spaceKey}`
   - Examples:
     - `https://iwiki.woa.com/space/~username` (personal space)
     - `https://iwiki.woa.com/space/woa` (team space)
     - `https://iwiki.woa.com/space/fit` (project space)
   - Agent will: Extract spaceKey → Get space info → Find homepage docid → Pull from homepage
   
   **Format 2: Document URL** (pull specific document/folder)
   - Format: `https://iwiki.woa.com/p/{docid}`
   - Examples:
     - `https://iwiki.woa.com/p/1234567890` (single document)
     - `https://iwiki.woa.com/p/9876543210` (folder with children)
   - Agent will: Extract docid → Detect if has children → Pull accordingly

2. **Save location** (optional):
   - Default: `~/Desktop/21-Secret-内网知识库/iwikis/`（桌面上的 `21-Secret-内网知识库` 目录内；与 Cursor 工作区无关）
   - Custom: User can specify any path
   - **All documents MUST follow hierarchical structure**: `{save_location}/{space-name}/{folders}/{doc.md}`
   - **This applies to ALL document types**: space, folder, and single document
   - Documents will be saved with **strict iwiki hierarchy** (preserve exact folder structure from iwiki)

3. **图片与文件：同级共用 _images、_files**（必遵）：
   - 图片与文件**不**再使用与 `iwikis/` 平级的独立 `images/`、`files/` 根目录（勿在 `21-Secret-内网知识库` 下与 `iwikis` 并列再建全局 images/、files/）。
   - **多个同级文档**（同一父节点下的多篇 .md）**共用一个 _images、一个 _files**：在该**同级目录**下新建 `_images`、`_files`，**禁止**为每个文档单独建一层目录再各自放 _images（如 文档A/_images/、文档B/_images/），避免层级过深。
   - 文档保存为 `{父路径}/{doc}.md`（如 `{space}/{父文件夹}/文档A.md`），**不得**为每篇文档再建子目录（如 `文档A/文档A.md`）。图片与附件放在该同级目录下的 `_images/{文档名}/`、`_files/{文档名}/`，多文档时按文档名分子目录避免重名。
   - 即：文档为 `~/Desktop/21-Secret-内网知识库/iwikis/{space}/{父路径}/{doc}.md` 时，该文档的图片目录为 `~/Desktop/21-Secret-内网知识库/iwikis/{space}/{父路径}/_images/{doc}/`，文件目录为 `~/Desktop/21-Secret-内网知识库/iwikis/{space}/{父路径}/_files/{doc}/`（与所有同级 .md 共用一个 _images、一个 _files）。
   - 图片命名：**编号-图片名称.后缀**（如 `1-image.png`）；禁止「文件名称-编号.后缀」或「文档名-编号-图片名」。
   - 正文中图片引用相对路径：`_images/{文档名}/{编号}-{图片名}.{ext}`（与 .md 同目录）。附件引用：`_files/{文档名}/{原文件名}.{ext}`。
   - 腾讯文档引用文件：放在 `_files/{文档名}/{编号}-腾讯文档-{文档名称}.md`（path 各段去空格）。

### Detection Logic:
- **判断方式**：对任意 docid 必须先 Call getSpacePageTree(docid)；根据是否有子节点决定类型。
- **Space / Folder**（含「既是文档又有子页面」的节点）：Has child documents → 按 Workflow 2 递归拉取整棵子树（含当前页与所有子文档），preserve hierarchy。
- **Single document**：仅当 getSpacePageTree 显示无子节点时，按单文档处理；extract full path from metadata, create hierarchical folder structure.

### Path Hierarchy Rules (CRITICAL):

**ALL documents (space/folder/single) MUST follow hierarchical structure：.md 与同级文档在同一目录，不按文档再建子目录。**

```
{save_location}/
└── {space-name}/
    └── {parent-folder-1}/
        └── {parent-folder-2}/
            ├── {doc-name-1}.md
            ├── {doc-name-2}.md
            ├── _images/
            │   ├── {doc-name-1}/
            │   └── {doc-name-2}/
            └── _files/
                ├── {doc-name-1}/
                └── {doc-name-2}/
```

**空间目录名（必遵）：**
- 路径第一段（`iwikis/` 下第一层）必须使用**空间名称**（spacename），不得使用 spacekey（空间 ID/英文键）。
- 获取方式：`metadata(docid)` 返回的 `spacename` 字段，或 `getSpaceInfoByKey(metadata.spacekey)` 的 `name`。取到后做与其它路径段相同的去空格处理；若 spacename 含 `/`，替换为 `-`，保证空间对应单层目录。
- 示例：spacekey 为 `~lylianchen` 时，目录名应为 `lylianchen(陈跃利)`（spacename），而非 `~lylianchen`。

**空间根目录下生成 space.md（必遵）：**
- 每次向某空间写入或更新文档后，须在该空间根目录下生成或更新 **space.md**。
- 格式示例：
  ```markdown
  # {空间名称}
  
  **空间标识**：{spacekey}  
  **空间链接**：https://iwiki.woa.com/space/{spacekey}  
  **最后更新**：YYYY-MM-DD
  
  ## 已下载文档
  
  - [文档标题](./路径/to/文档.md)
    - 路径：{层级路径描述}
    - 更新时间：{updatetime}
    - 图片：{数量}张
    - 附件：{数量}个
    - 外部引用：{数量}个
  ```
- **内容要求**：
  - 空间名称、spacekey、空间URL（`https://iwiki.woa.com/space/{spacekey}`）
  - 已下载文档列表（标题、相对路径、元数据摘要）
  - 可选：简要说明、最后更新时间
- **更新策略**：
  - 新建空间时创建
  - 每次向该空间添加文档后更新文档列表
  - 保持层级结构清晰，可使用二级列表展示子文档

**File and folder naming – remove spaces (CRITICAL):**
- All file and folder names in paths MUST have **every space removed**. Do not add hyphens, underscores, or any other symbols.
- Apply to: space name, every folder name, document name, and any path segment under `iwikis/`（含 `_images`、`_files` 内的文件名）.
- Example: `0 整体视图` → `0整体视图` (not `0-整体视图` or `0_整体视图`).
- When building paths from iwiki metadata, sanitize each segment: `segment.replace(/\s+/g, '')`.

**Algorithm to build path for single document:**
1. Get metadata for target document → extract parentid
2. Recursively get parent document metadata until root
3. Build path from root to target: space → folder1 → folder2 → ... → **父路径**；文档保存为 **{父路径}/{doc_name}.md**，**不得**再建 {doc_name}/ 子目录（即禁止 {父路径}/{doc_name}/{doc_name}.md）
4. **Remove all spaces from each path segment** (space name, folder names, doc name)
5. Create full directory structure（父路径目录 + 该目录下的一个 _images、一个 _files）
6. Save document as {父路径}/{doc_name}.md；图片/附件存 {父路径}/_images/{doc_name}/、{父路径}/_files/{doc_name}/

**Example:**
- Document URL: `https://iwiki.woa.com/p/1234567890`
- Metadata shows: parentid → 9999 → parentid → 8888 (root)
- Space name: "FiT-资金中台"
- Parent chain: "技术文档" → "系统设计"
- Final path: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/系统设计/API设计.md`
- Images path: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/系统设计/_images/API设计/1-diagram.png`（与同级 .md 共用一个 _images，按文档名分子目录；禁止 系统设计/API设计/_images/）
- Files path: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/系统设计/_files/API设计/需求文档.pptx`
- Tencent docs: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/系统设计/_files/API设计/1-腾讯文档-{文档名称}.md`

**Never assume paths - always confirm with user first.**

---

## Image Storage Strategy

**IMPORTANT: 多个同级文档共用一个 _images、一个 _files，且 .md 与 _images 同级，禁止「每个文档一个 _images」导致层级过深（见「图片与文件：同级共用 _images、_files」）。**

### 同级共用 _images、_files（必遵）

**原则：** 同一父路径下的多篇文档（同级文档）保存在**同一目录**，在该目录下**只建一个** `_images`、一个 `_files`；各文档的图片/附件分别放在 `_images/{文档名}/`、`_files/{文档名}/`。**禁止**为每篇文档单独建子目录并在其下再建 _images（如 `文档A/文档A.md` + `文档A/_images/`），否则层级过深。

**Structure:** 同级目录内：多篇 .md 平铺，一个 _images、一个 _files，按文档名分子目录

```
iwikis/{space}/{父路径}/
├── 文档A.md
├── 文档B.md
├── _images/          ← 多个同级文档共用一个 _images
│   ├── 文档A/
│   │   ├── 1-architecture-diagram.png
│   │   └── 2-flowchart.svg
│   └── 文档B/
│       └── 1-diagram.png
└── _files/
    ├── 文档A/
    │   └── 需求文档.pptx
    └── 文档B/
        └── 数据模型.xlsx
```

**图片命名规则（必遵）：编号-图片名称.后缀**
- **统一格式：** `{编号}-{图片名称}.{后缀}`，例如 `1-image.png`
- **禁止使用旧格式：** 不得使用「文件名称-编号.后缀」或「文档名-编号-图片名.后缀」（如 `文档名-1-image.png`），空间内图片**仅**使用「编号-图片名称.后缀」
- **编号：** 从 1 起的顺序号，按文档内出现顺序
- **图片名称：** 来自 iwiki 原文件名，可做清理（去特殊字符、空格等），不含扩展名
- **示例：** `1-image.png`、`2-系统架构图.png`、`3-drawio-flow.svg`

**Algorithm:**
1. Parse document's relative path from save location；**同级文档**的 .md 均落在同一目录（父路径），不按文档再建子目录。
2. Extract: space name, parent path (父路径), document name
3. Create directory: `{save_location}/{space}/{父路径}/_images/{doc}/`（该目录下只建一个 _images，多文档时按文档名分子目录）
4. **For each image in document order:**
   - 取 iwiki 原文件名，清理后作为「图片名称」
   - 命名：**编号-图片名称.后缀**（如 `1-image.png`），编号从 1 起
   - Call `user-iWiki-getAttachmentDownloadUrl(attachmentid)` 获取下载URL
   - **处理下载响应（必遵）：**
     - 若返回正常图片URL（以`.cos.ap-guangzhou.myqcloud.com`等开头）：使用curl下载
     - 若返回SVG内容（包含`<svg xmlns=...>`和权限提示文本）：
       - 说明该图片因权限限制无法下载
       - **保存SVG占位符**：将返回的SVG内容保存为`.svg`文件（命名：`{编号}-无原文档查看权限.svg`）
       - 在文档中创建指向该SVG的引用
       - 在报告中记录该图片无权限访问
     - 若下载失败：记录错误，继续处理下一张图片
   - Save image (or placeholder) with that filename
5. Generate markdown reference：与 .md 同目录，相对路径为 `_images/{文档名}/{编号}-{图片名称}.{ext}`

**Benefits:**
- 多个同级文档共用一个 _images、一个 _files，层级更浅；按文档名分子目录避免重名
- 禁止「每文档一个 _images」带来的深层目录
- 相对路径简短：`_images/{文档名}/...`、`_files/{文档名}/...`

**Example:**
- Document: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/API设计.md`
- Original image: `系统架构图.png` (first image in document)
- Image saved to: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/_images/API设计/1-系统架构图.png`（命名：编号-图片名称.后缀）
- MD reference: `_images/API设计/1-系统架构图.png`（与 .md 同目录）

**Benefits of Index Prefix:**
- ✅ Quick identification of image order in document
- ✅ Easy to locate specific images (e.g., "show me the first diagram")
- ✅ Maintains visual sequence when sorted alphabetically
- ✅ Prevents naming conflicts with similar filenames

---

### 批量图片下载实现要点（必遵）

**适用场景**：单文档/多文档拉取、补拉缺失图片、扫描模式下载图片时，均按此逻辑执行。

1. **获取图片列表与顺序**
   - 调用 `listImages(docid)` 得到文档内图片列表（含 attachmentid、文件名等），**顺序即文档内出现顺序**。
   - 按该顺序依次处理，编号从 1 起：`{编号}-{图片名称}.{后缀}`（图片名称取自原文件名，做清理）。

2. **获取临时下载 URL**
   - 对每个 attachmentid 调用 `getAttachmentDownloadUrl(attachmentid)` 获取临时下载 URL。
   - **临时 URL 有效期约 300 秒**，拿到 URL 后应尽快下载，避免批量取完再统一下载导致过期。

3. **下载方式：使用 curl**
   - **必须使用 curl 下载**（在终端执行 `curl -L -o <本地路径> "<临时URL>"`）。使用 Python 的 `urllib.request` 或 `requests` 直接请求 iWiki/COS 返回的 URL 时，可能收到 **HTTP 403**，导致下载失败；同一临时 URL 用 curl 可正常下载。
   - 建议流程：对每张图「取 URL → 立即 curl 下载到 _images/{文档名}/{编号}-{图片名}.{ext}」；或对少量图先批量取 URL，在有效期内尽快用 curl 逐条下载。

4. **保存路径与命名**
   - 保存到该层级共用的 `_images/{文档名}/` 下，文件名严格为 `{编号}-{图片名称}.{后缀}`，与文档内出现顺序一致。
   - 文档在子目录时，正文中相对路径为 `../../_images/{文档名}/...` 等，根据 .md 与 _images 的相对关系计算。

5. **正文链接替换**
   - 按文档内图片出现顺序，将每处 `![...](https://iwiki.woa.com/tencent/api/attachments/s3/url?attachmentid=...)` 依次替换为 `![{编号}-{图片名}.{后缀}](<相对路径>/_{编号}-{图片名}.{后缀})`。
   - 顺序必须与 listImages 及已下载的 `1-xxx`、`2-xxx` 一一对应，避免错位。

**小结**：listImages 定序 → getAttachmentDownloadUrl 取临时 URL → **curl 下载**（勿用 Python urllib/requests）→ 按序命名并存到 _images/{文档名}/ → 按序替换正文中的图片链接。

---

### Legacy / 已废弃的图片命名（请勿使用）

**以下格式已废弃，新拉取一律使用「编号-图片名称.后缀」：**
- 旧格式（禁止）：`{文档名}-{编号}-{图片名}.{ext}`、`{文件名称}-{编号}.{后缀}`、`{folder-hierarchy}-{doc-name}-{image-name}.{ext}`
- 正确格式：`{编号}-{图片名称}.{后缀}`，如 `1-image.png`

若本地已有用旧格式命名的图片，可用转换脚本迁移后再统一引用。

---

## iwiki MCP Tools Reference

| Tool | Purpose | Key Parameter |
|------|---------|---------------|
| `user-iWiki-getSpaceInfoByKey` | Get space info by space key | spaceKey |
| `user-iWiki-getDocument` | Fetch document content | docid |
| `user-iWiki-getSpacePageTree` | Get document tree | parentid |
| `user-iWiki-listImages` | List images in document | docid |
| `user-iWiki-getAttachmentList` | List all attachments in document（含文档下方挂载的文件；用于拉取非图片类附件） | docid |
| `user-iWiki-getAttachmentDownloadUrl` | Get attachment download URL（图片与文件附件均可用） | attachmentid |
| `user-iWiki-metadata` | Get document metadata | docid |
| `user-iWiki-aiSearchDocument` | Search document content | query |

### Tool Details:

**getSpaceInfoByKey**: Returns space information including homepage docid
- Input: `spaceKey` (e.g., "~username", "woa")
- Output: Space info with homepage document ID
- Usage: Convert space URL to document ID for pulling

---

## Path Extraction for Single Documents

**CRITICAL: For single documents, you MUST extract the full path hierarchy from iwiki metadata.**

### Algorithm: Build Full Path from Single Document

```javascript
async function buildDocumentPath(docid) {
  let path = [];
  let currentDocId = docid;
  
  // Step 1: Recursively collect parent chain
  while (currentDocId) {
    const metadata = await user-iWiki-metadata(currentDocId);
    
    // Add current document/folder to path (at beginning)
    path.unshift(metadata.title);
    
    // Move to parent
    currentDocId = metadata.parentid;
    
    // Stop at space root (when parentid is null or 0)
    if (!currentDocId || currentDocId === 0) break;
  }
  
  // Step 2: Get space name (use spacename, NOT spacekey)
  const spaceInfo = await user-iWiki-getSpaceInfoByKey(metadata.spaceKey);
  const spaceName = spaceInfo.name || metadata.spacename;
  
  // Step 3: Remove all spaces from every path segment (no other symbols). Space name only: also replace "/" with "-" so space is single folder.
  const sanitize = (s) => (s || '').replace(/\s+/g, '');
  const spaceNameClean = (spaceName || '').replace(/\s+/g, '').replace(/\//g, '-');
  const pathClean = path.map(sanitize);
  
  // Step 4: Build full path (all segments without spaces)
  const fullPath = [spaceNameClean, ...pathClean].join('/');
  
  return {
    spaceName: spaceNameClean,
    folderPath: pathClean.slice(0, -1).join('/'),
    docName: pathClean[pathClean.length - 1],
    fullPath: fullPath
  };
}
```

### Example:

**Input**: `https://iwiki.woa.com/p/1234567890`

**Metadata chain**:
1. Document (1234567890): title="API设计", parentid=9999
2. Parent (9999): title="系统设计", parentid=8888
3. Parent (8888): title="技术文档", parentid=7777
4. Root (7777): title="FiT-资金中台", parentid=null, spaceKey="fit"

**Result**:
- Space name: "FiT-资金中台"
- Folder path: "技术文档/系统设计"
- Doc name: "API设计"
- Full path: "FiT-资金中台/技术文档/系统设计/API设计"

**Final structure（同级多文档共用一个 _images、_files，不按文档再建子目录）：**
```
~/Desktop/21-Secret-内网知识库/
└── iwikis/                      ← Documents base path（默认 save_location）
    └── FiT-资金中台/            ← From space info
        └── 技术文档/            ← From parent chain
            └── 系统设计/        ← From parent chain（同级 .md 均在此目录）
                ├── API设计.md   ← 文档平铺，不建 API设计/ 子目录
                ├── 其他文档.md
                ├── _images/     ← 该层级只建一个 _images
                │   ├── API设计/
                │   │   ├── 1-diagram.png
                │   │   └── 2-flowchart.svg
                │   └── 其他文档/
                └── _files/      ← 该层级只建一个 _files
                    └── API设计/
                        ├── 需求文档.pptx
                        ├── 数据模型.xlsx
                        ├── 技术方案.pdf
                        └── 1-腾讯文档-文档名称.md   ← Tencent docs references
```

---

## Relative Path Calculation

**IMPORTANT: 同一级目录共用 _images、_files，相对路径无需 `../`。**

规则：
- 文档路径：`{save_path}/{space}/{folder}/{doc}.md`
- 该层级图片目录：`{save_path}/{space}/{folder}/_images/`，该文档的图片在 `_images/{doc}/`
- 该层级文件目录：`{save_path}/{space}/{folder}/_files/`，该文档的附件在 `_files/{doc}/`
- 正文中图片引用：`_images/{文档名}/{编号}-{图片名}.{ext}`（与 .md 同目录）
- 正文中附件引用：`_files/{文档名}/{原文件名}.{ext}`

Example:
- Document: `~/Desktop/21-Secret-内网知识库/iwikis/FiT-资金中台/技术文档/API设计.md`
- Image: 同层级 `_images/API设计/1-系统架构图.png`
- Relative path in .md: `_images/API设计/1-系统架构图.png`

**Always use relative paths in .md files for portability.**

---

## Common User Requests

### Request Pattern 1: Pull from Space URL
```
User: "拉取 https://iwiki.woa.com/space/~lylianchen"

Actions:
1. Parse URL → Extract spaceKey: "~lylianchen"
2. Call user-iWiki-getSpaceInfoByKey("~lylianchen")
3. Extract homepage docid from space info
4. Call user-iWiki-metadata(homepage_docid) and user-iWiki-getSpacePageTree(homepage_docid)
5. Ask: "保存到哪个文件夹？(默认: ~/Desktop/21-Secret-内网知识库/iwikis/)"
6. Pull entire space content recursively with strict iwiki hierarchy（图片与文件保存在各层级共用的 _images、_files，按文档名分子目录）
7. Report completion with statistics
```

### Request Pattern 2: Pull from Document URL
```
User: "拉取 https://iwiki.woa.com/p/1234567890"

Actions:
1. Parse URL → Extract docid: 1234567890
2. Detect type using user-iWiki-metadata and user-iWiki-getSpacePageTree
3. Ask: "保存到哪个文件夹？(默认: ~/Desktop/21-Secret-内网知识库/iwikis/)"
4. （图片与文件保存在该层级共用的 _images、_files，无需单独询问）
6. Pull content based on type (space/folder/document) with strict iwiki hierarchy
7. Report completion
```

### Request Pattern 3: Pull with Custom Path
```
User: "拉取 https://iwiki.woa.com/p/1234567890 到 FiT-资金中台/技术文档/"

Actions:
1. Extract docid and target path
2. Detect type
3. Confirm: "确认保存到 FiT-资金中台/技术文档/？"
4. Pull content
5. Report completion
```

### Request Pattern 4: Update Existing Documents
```
User: "扫描 @FiT-资金中台/ 下载缺失的 iwiki 图片"

Actions:
1. Scan all .md files in specified folder
2. Extract docids from "文档来源" field in each file
3. Check for missing images
4. Download missing images only
5. Update image references
6. Report completion
```

---

## Processing Rules

✅ **Do:**
- **Always ask user for iwiki URL first** (required input)
- **Parse and validate URL** before proceeding (space URL or document URL)
- **Handle space URLs**: Extract spaceKey → Get space info → Find homepage docid
- **Handle document URLs**: Extract docid directly
- **Confirm save location** before starting (default: `~/Desktop/21-Secret-内网知识库/iwikis/` or custom)
- **Detect document type** (space/folder/document) automatically
- **Preserve iwiki hierarchy strictly** - maintain exact folder structure from iwiki
- **Remove all spaces from file and folder names** - sanitize every path segment (space name, folder names, doc name): remove spaces only, do not add hyphens or other symbols (e.g. `0 整体视图` → `0整体视图`)
- **For ALL document types (including single documents)**:
  - Extract space name from metadata
  - Build parent folder chain by recursively querying parentid
  - Sanitize each segment (remove spaces) before creating directories
  - Create full hierarchical directory structure
  - Save document in proper folder location (not in root)
  - **Save images to `_images/{doc}/` and files to `_files/{doc}/`**（同一级目录共用 _images、_files 两个文件夹，按文档名分子目录；不再使用与 `iwikis/` 平级的独立 images/、files/ 根目录）
- Check if image exists before downloading (avoid duplicates)
- **Before downloading each document**: Check if it already exists locally（iwikis 下是否已有「文档来源」含该 docid 的 .md）；若已存在则跳过，并加入「已存在故未下载」列表
- **Before ending workflow**: Output the list of documents skipped because they already existed（已存在故未下载：docid、标题、本地路径）
- **For every document pulled**: Call getAttachmentList(docid) and download all **non-image attachments**（文档下方挂载的 PPT/Excel/Word/PDF 等）to files folder；不得只拉正文和图片而遗漏文档下方附件
- **When given a document URL (/p/{docid})**: Always call getSpacePageTree(docid) first；若该节点有子页面，则按文件夹递归拉取整棵子树，不得只拉当前页而遗漏子文档
- Create target folders if they don't exist
- Calculate relative paths dynamically based on actual locations
- Log all operations (success/failure)
- Use relative paths in .md files

❌ **Don't:**
- Hard-code file paths or folder names
- Assume user's folder structure
- Skip asking for required inputs (iwiki URL)
- Overwrite existing images without checking
- Use absolute paths in .md files
- Modify document content beyond image references and metadata
- **Save single documents directly in root folder** - MUST create hierarchical structure
- Skip metadata extraction for path building

---

## Token 节流（执行必遵）

- **同一会话内**：本 Skill 已加载后，拉第二篇、补拉时**不再重读** SKILL 全文，按已加载流程执行即可。
- **getDocument(docid)**：每文档**只调一次**；正文用于判空、写 .md、替换图片与内链，不因「再确认」等重复拉取。
- **metadata(docid)**：每文档**只调一次**；路径与父链解析时复用已有 parentid，避免同一 doc 的 metadata 调两次。
- **报告简短**：仅输出路径、文档数、图片数、附件数、是否跳过已存在（及「已存在故未下载」列表）；**不**把整篇正文或整段 MCP/JSON 贴回对话。
- **错误概括**：用「文件名 + 原因」一句话；**不**重复粘贴大段 MCP 原始错误。

---

## Error Handling

### Common Issues:

1. **Authentication Required**
   - MCP handles OA authentication automatically
   - Temporary URLs valid for 300 seconds

2. **Image Download Failed**
   - 若为 HTTP 403：改用 **curl** 下载（见「批量图片下载实现要点」），勿用 Python urllib/requests 直连 COS。
   - Retry once automatically
   - Log failure with attachment ID
   - Continue processing other images

3. **Invalid iwiki URL**
   - Prompt user: "请提供有效的 iwiki 链接"
   - Supported formats:
     - Space: `https://iwiki.woa.com/space/{spaceKey}`
     - Document: `https://iwiki.woa.com/p/{docid}`
   - Cannot proceed without valid iwiki URL

4. **Space Not Found**
   - Error when calling getSpaceInfoByKey
   - Possible reasons:
     - Space key is incorrect
     - Space doesn't exist or has been deleted
     - No permission to access the space
   - Ask user to verify the space URL in browser first

---

## Output Format

**保持简短**（见上方 Token 节流）：路径、文档数、图片数、附件数、跳过已存在列表；不贴正文或 JSON。

示例：
```markdown
## 拉取结果
- 文档：X 篇（路径：…）
- 图片：Y 张 | 附件：Z 个
- 已存在故未下载：N 篇（docid、标题、本地路径）
- 失败：文件名 + 原因（一句话）
```

---

## Supported Image Formats

`png`, `jpg`, `jpeg`, `gif`, `svg`, `webp`, `bmp`

---

## External File Dependency Detection

### Supported External File Patterns

**Tencent Documents:**
```regex
# Tencent Doc (Document)
https?://docs\.qq\.com/doc/[A-Za-z0-9_-]+

# Tencent Sheet (Spreadsheet)
https?://docs\.qq\.com/sheet/[A-Za-z0-9_-]+

# Tencent Slide (Presentation)
https?://docs\.qq\.com/slide/[A-Za-z0-9_-]+

# WeChat Work Doc
https?://doc\.weixin\.qq\.com/[A-Za-z0-9_/-]+
```

**Other Cloud Storage:**
```regex
# Excel Online
https?://[^/]*excel\.live\.com/[A-Za-z0-9_/-]+

# Google Docs (if accessible)
https?://docs\.google\.com/(document|spreadsheets|presentation)/[A-Za-z0-9_/-]+
```

### Detection Algorithm

```javascript
function extractExternalDependencies(documentContent) {
  const dependencies = [];
  
  // Patterns to detect
  const patterns = [
    { type: 'Tencent Doc', regex: /https?:\/\/docs\.qq\.com\/doc\/[A-Za-z0-9_-]+/g },
    { type: 'Tencent Sheet', regex: /https?:\/\/docs\.qq\.com\/sheet\/[A-Za-z0-9_-]+/g },
    { type: 'Tencent Slide', regex: /https?:\/\/docs\.qq\.com\/slide\/[A-Za-z0-9_-]+/g },
    { type: 'WeChat Doc', regex: /https?:\/\/doc\.weixin\.qq\.com\/[A-Za-z0-9_\/-]+/g },
    { type: 'Excel Online', regex: /https?:\/\/[^\/]*excel\.live\.com\/[A-Za-z0-9_\/-]+/g }
  ];
  
  patterns.forEach(({ type, regex }) => {
    const matches = documentContent.matchAll(regex);
    for (const match of matches) {
      const link = match[0];
      const context = extractContext(documentContent, match.index);
      
      dependencies.push({
        type: type,
        link: link,
        context: context,
        position: findSectionName(documentContent, match.index)
      });
    }
  });
  
  return dependencies;
}

function extractContext(content, index) {
  // Extract surrounding text (50 chars before/after)
  const start = Math.max(0, index - 50);
  const end = Math.min(content.length, index + 100);
  return content.substring(start, end).trim();
}
```

### Dependencies Manifest Format

Location: `{save_location}/{space}/{父路径}/_files/{doc-name}/` 下（同级共用一个 _files，按文档名分子目录；文件名 `{编号}-腾讯文档-{文档名称}.md`）

（见 Workflow 5：文件名 `{编号}-腾讯文档-{文档名称}.md`，内容仅保留来源文档、**链接**且链接须为可点击形式 `[点击打开/下载](URL)`。）

---

## Advanced: Document Metadata Extraction

When pulling documents, extract and preserve:

- Title (use as filename)
- Creator and modifier
- Create/update timestamps
- Parent document relationships
- Tags (if available)

Store metadata in frontmatter（仅 4 项；本文引用写在正文底部）：

```yaml
---
title: 系统架构设计
文档来源: https://iwiki.woa.com/p/1234567890
createtime: "2025-07-29 10:00:00"
updatetime: "2025-10-27 15:30:00"
---
```

---

## Tips for Efficiency

1. **Token 节流**：见上方「Token 节流（执行必遵）」— 同一会话不重读 Skill、getDocument/metadata 每文档只调一次、报告简短、错误一句话。
2. **Batch Operations**: Process multiple documents in parallel when possible
3. **Cache Check**: Skip existing images with matching file size
4. **Progress Updates**: Report progress every 5 documents for large batches
5. **权限处理**: 遇到无权限图片时保存SVG占位符，继续处理后续内容
6. **空间链接**: 自动将文档中的iwiki空间链接替换为本地space.md
7. **增量更新**: 检查已存在文档，避免重复下载

---

## 最佳实践（基于实际使用经验）

### 1. 批量下载关联文档

**场景**: 当文档中包含多个iwiki链接时

**建议做法**:
```markdown
✅ 好的做法：
- 先预扫所有关联文档，一次性展示给用户
- 标注每个文档的状态（有权限/无权限/已存在）
- 用户确认后批量下载，提供进度反馈

❌ 避免：
- 逐个询问用户是否下载每个关联文档
- 下载失败后中断整个流程
```

### 2. 图片权限问题处理

**场景**: 某些图片因权限限制无法下载

**建议做法**:
```markdown
✅ 好的做法：
- 检测getAttachmentDownloadUrl返回的内容类型
- 如果是SVG权限提示，保存为占位符文件
- 在文档中正常引用，保持结构完整
- 在报告中统计无权限图片数量

❌ 避免：
- 遇到权限问题就终止处理
- 忽略无权限图片，导致文档引用失效
```

**SVG占位符示例**:
```svg
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">
	<a xlink:href="https://iwiki.woa.com/p/{docid}" target="_blank">
	<text x="0" y="15" fill="gray">无原文档查看权限，点击进行跳转</text>
	</a>
</svg>
```

### 3. 空间索引管理

**场景**: 下载多个文档到同一空间

**建议做法**:
```markdown
✅ 好的做法：
- 每次下载后自动更新space.md
- 保持文档列表结构清晰
- 包含必要的元数据（更新时间、图片数、附件数）

❌ 避免：
- 只创建一次索引文件，后续不更新
- 索引信息过于简单或过于冗长
```

### 4. 链接替换策略

**场景**: 文档中包含多种类型的iwiki链接

**建议做法**:
```markdown
✅ 好的做法：
- 识别两种链接：文档链接(/p/{docid})和空间链接(/space/{key})
- 文档链接：已下载的替换为本地路径，未下载的保留原链接
- 空间链接：查找对应space.md，找到则替换，未找到保留原链接
- 保持链接文本不变

❌ 避免：
- 盲目替换所有链接
- 将空间链接替换为文档路径
```

### 5. 大规模下载优化

**场景**: 下载包含大量关联文档的空间

**建议做法**:
```markdown
✅ 好的做法：
- 分批处理（每批3-5个文档）
- 提供进度提示（已完成X/总数Y）
- 并行下载图片资源
- 出错继续，最后统一报告失败项

❌ 避免：
- 串行下载所有内容
- 没有进度反馈
- 一个错误导致全部失败
```

### 6. 文档结构保持

**场景**: 确保本地结构与iwiki一致

**建议做法**:
```markdown
✅ 好的做法：
- 使用metadata获取完整路径层级
- 保持文件夹嵌套关系
- 按文档名分子目录存储图片和附件
- 使用空间名而非spacekey作为目录名

❌ 避免：
- 将所有文档平铺在一个目录
- 使用spacekey作为目录名
- 图片和附件混在一起
```
5. **Validation**: Verify image downloads (check file size > 0)
6. **Index Naming**: Name images with sequential index for easy reference
7. **Dependency Tracking**: Always scan for external file references during download

---

## Key Principles

1. **User provides iwiki URL** - This is the starting point, always required
2. **Agent detects type** - Space, folder, or single document
3. **User confirms locations** - Where to save documents and images
4. **Agent does the work** - Downloads, organizes, and updates references
5. **Dynamic paths** - Everything calculated based on actual locations

## Quick Checklist

Before pulling from iwiki:
- [ ] Have iwiki URL ready
- [ ] Can access the URL in browser
- [ ] Know where you want to save (or use defaults)
- [ ] Have enough disk space for images

During pull:
- [ ] Agent shows document count
- [ ] User confirms save locations
- [ ] Agent reports progress
- [ ] Agent shows final summary

After pull:
- [ ] Check documents in save location
- [ ] Verify images downloaded
- [ ] Test image references work
- [ ] Review summary report

## Quick Reference

| 项 | 规则 |
|----|------|
| 默认路径 | 文档 `~/Desktop/21-Secret-内网知识库/iwikis/`；**多个同级文档**共用一个 `_images`、一个 `_files`（与 .md 同级），各文档资源在 `_images/{文档名}/`、`_files/{文档名}/`；禁止每文档一层目录+_images（层级过深） |
| 路径命名 | 所有文件/文件夹名**仅去空格**，不加其它符号（例：`0 整体视图` → `0整体视图`） |
| 空文档与确认 | 空文档不下载；先展示「内容非空」的文档列表，等待用户确认后再执行下载 |
| 关联 iWiki | 默认一并拉取正文中的 iwiki.woa.com/p/* 所指文档并替换为本地链接；用户明确说「不拉关联」「只拉当前」时不拉 |
| 文档 frontmatter | 仅 4 项：title、文档来源、createtime、updatetime；本文引用写在正文底部「本文引用」小节 |
| 图片命名 | **编号-图片名称.后缀**（如 `1-image.png`）；禁止「文件名称-编号.后缀」或「文档名-编号-xxx」 |
| 腾讯文档引用文件 | 文件名 `{编号}-腾讯文档-{文档名称}.md`；内容仅保留：来源文档（相对路径链接）、**链接**（Markdown 可点击链接 `[点击打开/下载](URL)`） |
| 用法示例 | 拉取 `https://iwiki.woa.com/p/{docid}` 或 `https://iwiki.woa.com/space/{spaceKey}` |
| 下载后检查 / 结束条件 | 检查 iwikis 正文中的 iwiki 链接是否均已下载；未下载的需执行拉取，无法下载的列举并说明原因；**全部处理完毕后方可结束工作流**（见 Workflow 8） |
| 已存在则跳过 | 下载前检查本地 iwikis 是否已有该 docid（文档来源）；若已存在则跳过下载；**结束前必须输出「已存在故未下载」的文章列表**（docid、标题、本地路径） |
| 文档下方附件 | 拉取文档时**必须**拉取该文档下方挂载的附件（getAttachmentList → 非图片类下载到 files）；不得只拉正文和图片而遗漏附件 |
| 文档即文件夹 | 拉取前**必须** getSpacePageTree(docid)；若该页有子页面，则按文件夹递归拉取整棵子树，不得只拉当前页而遗漏子文档 |