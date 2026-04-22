# Usage Examples

Complete examples of using the iwiki Knowledge Organizer skill.

**Important:** All workflows start with user providing an iwiki URL.

**Supported URL Formats:**
- Space URL: `https://iwiki.woa.com/space/{spaceKey}` (e.g., `https://iwiki.woa.com/space/~username`)
- Document URL: `https://iwiki.woa.com/p/{docid}` (e.g., `https://iwiki.woa.com/p/1234567890`)

---

## Example 1: Incremental Sync/Update ⭐ **New Feature**

**User Request:**
```
同步更新 @产品组/FiT-资金中台/
```

**Agent Actions:**

1. Scan local directory:
```javascript
// Find all .md files in specified folder
const mdFiles = glob("产品组/FiT-资金中台/**/*.md");
// Found: 50 files

// Extract metadata from each file
for (const file of mdFiles) {
  const frontmatter = parseFrontmatter(file);
  localDocs.push({
    path: file,
    iwiki_id: frontmatter.iwiki_id,
    updated: frontmatter.updated
  });
}
```

2. Check remote updates:
```javascript
// For each local document, check remote timestamp
for (const doc of localDocs) {
  const remote = await user-iWiki-metadata(docid: doc.iwiki_id);
  
  if (remote.lastModified > doc.updated) {
    needsUpdate.push({
      ...doc,
      remoteTime: remote.lastModified
    });
  }
}

// Result: 12 documents need update
```

3. Ask user for confirmation:
```
Agent: "扫描完成：
        总文档: 50 个
        需要更新: 12 个
        跳过: 38 个 (无变化)
        
        是否继续更新？"
        
User: "是"
```

4. Perform incremental update:
```javascript
for (const doc of needsUpdate) {
  // Download latest content
  const content = await user-iWiki-getDocument(docid: doc.iwiki_id);
  
  // Check for image changes
  const remoteImages = await user-iWiki-listImages(docid: doc.iwiki_id);
  const localImages = getLocalImages(doc.path);
  
  const newImages = remoteImages.filter(img => 
    !localImages.includes(img.filename)
  );
  
  // Download only new images
  for (const img of newImages) {
    const url = await user-iWiki-getAttachmentDownloadUrl(
      attachmentid: img.attachmentId
    );
    downloadImage(url, img.filename);
  }
  
  // Update document
  updateDocument(doc.path, {
    content: content.body,
    updated: content.metadata.lastModified,
    newImages: newImages
  });
}
```

5. Generate sync report:
```
Agent: "同步完成！
        
        ✅ 已更新: 12 个文档
        ✅ 新增图片: 8 个
        ⏭️ 跳过: 38 个 (无变化)
        
        详细更新列表:
        - 技术文档/API设计.md: 内容更新 + 3张新图片
        - 技术文档/系统架构.md: 内容更新
        - 产品文档/需求分析.md: 内容更新 + 2张新图片
        ... (还有9个)
        
        ⏱️ 总耗时: 2分35秒"
```

**Key Benefits:**
- ⚡ Fast: Only updates changed documents (12/50 = 24%)
- 💾 Efficient: Saves bandwidth by downloading only new images
- 🎯 Accurate: Ensures local copy matches iwiki exactly
- 📊 Transparent: Detailed report of what was updated

---

## Example 2: Pull from Space URL

**User Request:**
```
拉取 https://iwiki.woa.com/space/~lylianchen 到 产品组/
```

**Agent Actions:**

1. Parse URL and identify type:
```javascript
const url = "https://iwiki.woa.com/space/~lylianchen";
// Detected: type = 'space', spaceKey = '~lylianchen'
```

2. Get space information:
```javascript
user-iWiki-getSpaceInfoByKey(spaceKey: "~lylianchen")
// Returns: {
//   spaceName: "陈跃理的个人空间",
//   homepageId: "4016687569",
//   description: "...",
//   ...
// }
```

3. Extract homepage docid and continue with standard workflow:
```javascript
const homepageDocid = "4016687569";
user-iWiki-metadata(docid: homepageDocid)
user-iWiki-getSpacePageTree(parentid: homepageDocid)
// Detected: 25 documents in total
```

4. Ask user for confirmation:
```
Agent: "检测到这是一个空间，包含 25 个文档。
        保存到: 产品组/
        是否继续？"
User: "是"
```

5. Pull all documents recursively:
```javascript
// Download entire document tree
for (const doc of documentTree) {
  await user-iWiki-getDocument(doc.id);
  await user-iWiki-listImages(doc.id);
  // ... download images and save
}
```

**Result:**
```
## Processing Summary

✅ Successfully processed: 25 documents
✅ Images downloaded: 48 files (total 12.3MB)
❌ Failed downloads: 0 files

### Structure created:
产品组/
├── 陈跃理的个人空间/
│   ├── 项目文档/
│   │   ├── 需求分析.md (3 images)
│   │   └── 技术方案.md (5 images)
│   ├── 产品设计/
│   │   ├── 产品PRD.md (8 images)
│   │   └── 交互设计.md (6 images)
│   └── 会议记录/
│       ├── 2024-01-15会议.md (2 images)
│       └── 2024-01-20会议.md (1 image)

All images saved under each document folder's sibling `_images/` directory.
```

---

## Example 2: Pull Single Document

**User Request:**
```
拉取 https://iwiki.woa.com/p/1234567890
```

**Agent Actions:**

1. Extract docid from URL: `1234567890`

2. Detect document type:
```javascript
user-iWiki-metadata(docid: "1234567890")
// Returns: { title: "系统架构设计", type: "document", ... }

user-iWiki-getSpacePageTree(docid: "1234567890")
// Returns: null or empty (no children) → Single document
```

3. Ask user for configuration:
```
Agent: "检测到这是单个文档。
        保存到哪里？(默认: 我的知识库/iwikis/)"
User: "用默认路径"
```

4. Pull document:
```javascript
user-iWiki-getDocument(docid: "1234567890")
user-iWiki-listImages(docid: "1234567890")
```

5. Download images:
```javascript
// For each image
user-iWiki-getAttachmentDownloadUrl(attachmentid: "34242155")
// Download to: .../_images/系统架构设计/1-xxx.png (sibling folder, indexed)
```

6. Create document with metadata:
```markdown
---
iwiki_id: 1234567890
title: 系统架构设计
source: https://iwiki.woa.com/p/1234567890
---

# 系统架构设计

![架构图](_images/系统架构设计/1-架构图.png)
```

**Result:**
- 1 document downloaded → `我的知识库/iwikis/.../系统架构设计.md`
- 1 image downloaded → `我的知识库/iwikis/.../_images/系统架构设计/1-架构图.png`
- Image reference updated to sibling relative path

---

## Example 3: Pull Document Space with Hierarchy

**User Request:**
```
拉取 https://iwiki.woa.com/p/9876543210
```

**Agent Actions:**

1. Extract docid: `9876543210`

2. Detect type:
```javascript
user-iWiki-metadata(docid: "9876543210")
// Returns: { title: "技术文档中心", type: "space", ... }

user-iWiki-getSpacePageTree(docid: "9876543210")
// Returns: Full tree with multiple children → SPACE
```

3. Ask user:
```
Agent: "检测到这是一个文档空间，包含 15 个文档。
        保存到哪里？(默认: Documents/)
        图片保存到哪里？(默认: Images/)"
User: "保存到 tech-docs/"
```

4. Get full document tree:
```javascript
const tree = user-iWiki-getSpacePageTree("9876543210")
// Returns hierarchical structure:
// 技术文档中心/
// ├── 架构设计/
// │   ├── 系统架构.md
// │   └── 技术方案.md
// └── 接口文档/
//     ├── API设计.md
//     └── 接口规范.md
```

5. Download all documents recursively:
```javascript
for (const doc of tree) {
  // Download content
  const content = await user-iWiki-getDocument(doc.id);
  
  // Save with hierarchy preserved
  await saveFile(`tech-docs/${doc.path}`, content);
  
  // Download images
  const images = await user-iWiki-listImages(doc.id);
  for (const img of images) {
    const url = await user-iWiki-getAttachmentDownloadUrl(img.id);
    await downloadImage(url, `Images/${doc.path}-${img.name}`);
  }
}
```

6. Update all image references to relative paths

**Result:**
```
## Processing Summary

✅ Successfully processed: 15 documents
✅ Images downloaded: 32 files (total 8.5MB)
❌ Failed downloads: 0 files

### Structure created:
tech-docs/
├── 技术文档中心/
│   ├── 架构设计/
│   │   ├── 系统架构.md (3 images)
│   │   └── 技术方案.md (5 images)
│   └── 接口文档/
│       ├── API设计.md (2 images)
│       └── 接口规范.md (1 image)

All images saved to: Images/
```

---

## Example 4: Pull with Custom Paths

**User Request:**
```
拉取 https://iwiki.woa.com/p/5555555555 到 my-project/documentation/
图片保存到 my-project/assets/images/
```

**Agent Actions:**

1. Extract docid: `5555555555`
2. Parse custom paths from user input:
   - Documents: `my-project/documentation/`
   - Images: `my-project/assets/images/`

3. Detect type and pull content (assume it's a folder with 5 documents)

4. Calculate relative paths for images:
```javascript
// Document at: my-project/documentation/guide.md
// Images at: my-project/assets/images/
// Relative path: ../assets/images/
```

5. Download and save:
```javascript
// Save documents to custom path
await saveFile("my-project/documentation/guide.md", content);

// Save images to custom path
await downloadImage(url, "my-project/assets/images/guide-image1.png");

// Update with calculated relative path
content = content.replace(
  iwikiImageUrl,
  "../assets/images/guide-image1.png"
);
```

**Result:**
```
my-project/
├── documentation/
│   ├── guide.md
│   ├── tutorial.md
│   └── reference.md
└── assets/
    └── images/
        ├── guide-image1.png
        ├── tutorial-diagram.jpg
        └── reference-chart.png
```

All image references use relative paths like `../assets/images/xxx.png`

---

## Example 5: Update Existing Documents (Scan Mode)

**User Request:**
```
扫描 @my-docs/ 文件夹，下载缺失的 iwiki 图片
```

**Agent Actions:**

1. Scan folder recursively:
```javascript
const files = findAllMarkdownFiles("my-docs/");
// Found: 12 .md files
```

2. For each file, check for iwiki source:
```javascript
for (const file of files) {
  const content = readFile(file);
  
  // Look for: 文档来源: https://iwiki.woa.com/p/xxxxx
  const match = content.match(/文档来源.*?iwiki\.woa\.com\/p\/(\d+)/);
  
  if (match) {
    const docid = match[1];
    // Check for missing images
    await checkAndDownloadMissingImages(file, docid);
  }
}
```

3. Download only missing images:
```javascript
async function checkAndDownloadMissingImages(file, docid) {
  const images = await user-iWiki-listImages(docid);
  
  for (const img of images) {
    const localPath = calculateImagePath(file, img.name);
    
    if (!fs.existsSync(localPath)) {
      // Image is missing, download it
      const url = await user-iWiki-getAttachmentDownloadUrl(img.id);
      await downloadImage(url, localPath);
      console.log(`Downloaded: ${localPath}`);
    } else {
      console.log(`Skipped (exists): ${localPath}`);
    }
  }
}
```

**Result:**
```
## Scan Summary

📁 Scanned: 12 documents
✅ Downloaded: 5 missing images (1.2MB)
⏭️  Skipped: 18 existing images

### Downloaded:
- Images/doc1-diagram.png (256KB)
- Images/doc3-chart.jpg (512KB)
- Images/doc5-flow.png (128KB)
- Images/doc7-arch.png (256KB)
- Images/doc9-screen.png (64KB)

All documents now have complete images.
```

---

## Example 6: Pull Folder (Not Entire Space)

**User Request:**
```
拉取 https://iwiki.woa.com/p/7777777777
```

**Agent Actions:**

1. Detect it's a folder (not a full space):
```javascript
user-iWiki-metadata(docid: "7777777777")
// Returns: { title: "API接口文档", type: "folder", ... }

user-iWiki-getSpacePageTree(docid: "7777777777")
// Returns: 3 child documents
```

2. Agent asks for path (user accepts default: `Documents/`)

3. Pull folder with its documents:
```javascript
// Folder structure from iwiki:
// API接口文档/
// ├── 支付接口.md
// ├── 查询接口.md
// └── 回调接口.md
```

4. Download with preserved structure

**Result:**
```
Documents/
└── API接口文档/
    ├── 支付接口.md
    ├── 查询接口.md
    └── 回调接口.md

_images/
├── 支付接口/
│   └── 1-flow.png
├── 查询接口/
│   └── 1-diagram.jpg
└── 回调接口/
    └── 1-sequence.png
```

Note: Folder name comes from iwiki, preserving original structure.

---

## Example 7: Error Handling

**User Request:**
```
拉取 https://iwiki.woa.com/p/invalid123
```

**Agent Actions:**

1. Try to fetch document:
```javascript
try {
  const metadata = await user-iWiki-metadata("invalid123");
} catch (error) {
  // Document not found or no access
}
```

2. Agent responds:
```
❌ Error: Cannot access document

Possible reasons:
1. Document ID is invalid
2. You don't have permission to access this document
3. Document has been deleted

Please verify:
- The iwiki URL is correct
- You can access the document in iwiki web interface
- Try logging in to iwiki again
```

**User provides correct URL:**
```
拉取 https://iwiki.woa.com/p/8888888888
```

**Agent retries and succeeds:**
```
✅ Success!

Downloaded: 1 document
Images: 3 files (856KB)
Saved to: Documents/correct-document.md
```

---

## Best Practices

### 1. Always Provide iwiki URL
```
✅ Good: "拉取 https://iwiki.woa.com/p/1234567890"
❌ Bad: "下载那个文档" (Agent doesn't know which one)
```

### 2. Verify iwiki Access First
- Make sure you can open the iwiki link in browser
- Check you have read permission
- Ensure you're logged in to iwiki

### 3. Use Default Paths First
```
拉取 https://iwiki.woa.com/p/xxxxx
```
Let agent use defaults (Documents/ and Images/), then organize later if needed.

### 4. For Large Spaces
```
拉取 https://iwiki.woa.com/p/xxxxx
```
Agent will:
- Show how many documents found
- Ask for confirmation
- Report progress during download
- Show final statistics

### 5. Update Mode for Maintenance
```
扫描 @my-docs/ 下载缺失图片
```
Use this periodically to:
- Keep images in sync with iwiki
- Fix broken image references
- Download new images from updated documents
