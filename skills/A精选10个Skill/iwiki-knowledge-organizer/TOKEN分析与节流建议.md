# iWiki 拉取：Token 消耗分析与节流现状

## 一、Token 消耗来源（估算）

| 消耗项 | 说明 | 量级估算 |
|--------|------|----------|
| **1. Skill 读取** | 统一读 SKILL 全文（约 1150 行） | 约 **12k～18k tokens** |
| **2. MCP 请求与响应** | 每次调用的入参 + 返回结果进入上下文 | 见下表 |
| **3. 文档正文** | `getDocument(docid)` 返回的 Markdown 全文 | 约 0.5k～5k+ tokens/篇 |
| **4. 图片 URL 响应** | `getAttachmentDownloadUrl(attachmentid)` 返回的长 COS URL | **单次约 400～600 tokens**，N 张图 ≈ N×500 |
| **5. 元数据** | `metadata(docid)`、`getSpacePageTree(parentid)` 的 JSON | 单次约 200～500 tokens |
| **6. Agent 推理与回复** | 多轮思考、总结、报错与最终回复 | 约 1k～3k+ tokens/轮 |

### 单文档拉取典型 MCP 响应量（示意）

| 调用 | 次数 | 单次响应大致 token | 小计 |
|------|------|--------------------|------|
| getSpacePageTree | 1 | ~50 | ~50 |
| getDocument | 1 | 0.5k～5k | 0.5k～5k |
| metadata | 1～2 | ~300 | ~600 |
| listImages | 1 | ~50 | ~50 |
| getAttachmentDownloadUrl | N（图片数） | ~500 | **N×~500** |
| **合计（MCP）** | — | — | **约 1.2k + N×500 + 正文** |

示例：单篇 + 8 张图：SKILL ~15k + MCP ~5k + 正文 ~2k + 对话 ~2k ≈ **约 24k tokens/篇**。

---

## 二、节流手段与当前状态

### 已落地（Skill 侧）

| 项 | 做法 | 位置 |
|----|------|------|
| **1. 减少重复读取与调用** | 同一会话内已加载则不再重读 SKILL 全文；getDocument(docid)、metadata(docid) 每文档各只调一次并复用 | SKILL「Token 节流」 |
| **2. 路径与命名固化** | 路径（去空格、iwikis/images/files 平级）、图片命名（编号-图片名.后缀）、frontmatter 仅 4 项，在 SKILL 中固化 | SKILL.md |
| **3. 输出侧节省** | 报告仅路径、文档数、图片数、附件数、跳过已存在列表；错误「文件名+原因」一句话，不贴正文或 MCP 原始输出 | SKILL「Token 节流」+ Output Format |

### 未采用（可选，不牺牲完整性）

| 项 | 说明 | 若采用可省 token |
|----|------|------------------|
| **4. 单篇场景简化流程** | 默认「只拉当前、不拉关联」、确认步骤可缩短、先查本地再调远程。当前 SKILL 仍为默认拉关联、先展示非空再确认、先查本地已存在则跳过（已做） | 不拉关联时每少一篇约 5k～15k；确认缩短可减一轮长回复 |

### 需 MCP/服务侧配合

| 项 | 说明 |
|----|------|
| **3. 控制 MCP 响应体积** | getAttachmentDownloadUrl 长 URL 占比较大；若支持批量（如 getAttachmentDownloadUrls(ids)）或响应仅含 url 字段，可减 token。getDocument 若支持仅返回 body 可略降，以内容完整优先可不改。 |
| **7. 附件列表** | 当前 MCP 已有 getAttachmentList(docid)，SKILL 已要求非图片附件必拉，无额外试错消耗。 |

---

## 三、当前是否已最优

**结论：在「不采用单篇简化流程」的前提下，Skill 侧已基本最优。**

- **所有场景**：统一读 SKILL 全文；同一会话不重读、每文档 getDocument/metadata 只调一次、输出简短已写入并执行。
- **进一步省 token 的余地**：  
  1）**MCP 侧**：图片 URL 批量或精简响应；  
  2）**策略可选**：若未来采纳「单篇默认不拉关联、确认可缩短」，可再降，但会改变当前产品语义。

---

## 四、维护建议

1. **统一流程**：单篇与复杂场景均走 SKILL 全文；新增规则写入 SKILL，注意控制篇幅与位置。
2. **与 MCP 协作**：若提供批量 getAttachmentDownloadUrls 或精简 URL 响应，可在 SKILL 中注明「优先用批量接口」以减 token。
