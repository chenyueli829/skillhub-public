---
name: laozhao-research
description: 老赵研究专家工作流。当用户要求研究某个产品、品牌、行业、技术或任何方向时触发。完整执行：多源信息采集 → 结构化分析 → 生成研究报告 → 本地保存 MD → 创建企微文档 → 更新研究目录智能表格 → 发送文档链接和表格链接给用户。触发词包括：研究、调研、分析、deep dive、研究一下、帮我研究。
---

# 老赵研究专家工作流

收到研究请求后，严格按以下步骤执行，不得跳过任何步骤。

## Step 1：信息采集

同时使用内网和外网多源搜索，不依赖单一来源。

**外网搜索**（优先使用 `web_search` scope=external，或 deep-research skill 的 firecrawl/exa）：
- 产品/官网信息、新闻报道、行业分析
- 竞品对比、用户评价、技术文档

**内网搜索**（`web_search` scope=intranet 或 isearch skill）：
- 公司内部 KM/iWiki 相关文章
- 同事研究过的相关经验

**目标**：15-30 个有效来源，多源交叉验证，识别低质量信息。

## Step 2：结构化分析

根据研究对象类型选择框架：

- **产品研究**：定位/核心功能/商业模式/目标用户/竞品/壁垒/风险
- **技术研究**：原理/适用场景/成熟度/局限性/主要玩家/趋势
- **市场/行业研究**：市场规模/格局/主要玩家/商业模式/趋势/机会

框架服务目的，不硬套。

## Step 3：生成报告 Markdown

报告格式参见 `references/report-template.md`。

**关键原则**：
- 结论先行，数据/事实支撑
- 观点标注为观点，引用标注来源
- 无数据时写"未找到可靠数据"，不编造

## Step 4：本地保存

保存路径：`/root/.openclaw/workspace/研究报告/<请求人>/`（请求人为当前用户的 sender_id）

文件名格式：`<研究主题>研究报告.md`

## Step 5：创建企微文档并写入完整内容

1. 调用 `wecom_mcp call doc create_doc` 创建普通文档（doc_type=3）
2. 文档名称：`<研究主题>研究报告`
3. **写入报告内容（核心步骤，必须走子代理流程）**：
   - ❗ **禁止直接通过 `wecom_mcp` tool call 传入长内容**——LLM tool call 参数传递存在字符截断限制，超过约3000字符的 content 会被截断，导致文档内容不完整。
   - ✅ **正确做法：用 `sessions_spawn` 起一个子代理**，让子代理读取本地 MD 文件并通过 HTTP 直接调用企微 MCP Server 接口写入完整内容。
   - 子代理 task 模板：
     ```
     任务：把本地 Markdown 文件的完整内容写入企微文档。
     1. 读取文件 `<本地MD路径>` 的完整内容
     2. 调用 wecom_mcp tool，category=doc, method=edit_doc_content
        - docid: `<docid>`
        - content: 文件的完整内容
        - content_type: 1
     3. 如果 wecom_mcp tool call 因参数截断导致内容不完整，则改用 Python 脚本直接调用企微 MCP Server 的 HTTP 接口：
        - 从 openclaw 日志中找到 MCP Server 的 HTTP 端点和 API Key
        - 用 Python urllib 直接 POST 完整 JSON payload
     完成后报告结果。
     ```
   - 等待子代理完成后再继续后续步骤。
4. **保存返回的 docid 和 url**，后续步骤需要用到

## Step 6：更新研究目录智能表格

### 6.1 查找用户目录表格

读取 `references/user-tables.md`，按当前用户的 sender_id 查找其目录表格信息。

**情况 A：找到记录** → 直接使用其 docid / sheet_id，跳到 6.2 写入数据。

**情况 B：未找到记录** → 自动执行以下步骤，无需询问用户：
1. 调用 `create_doc`（doc_type=10）创建智能表格，名称：`老赵研究报告目录`
2. 调用 `smartsheet_get_sheet` 获取默认 sheet_id
3. 将默认列重命名为"报告名称"（调用 `smartsheet_update_fields`）
4. 调用 `smartsheet_add_fields` 添加以下列（均为 FIELD_TYPE_TEXT）：研究方向、创建日期、企微文档链接、本地文件路径
5. **将新表格信息追加写入 `references/user-tables.md`**，格式如下：
```
## <sender_id>

- **表格链接**：<url>
- **docid**：`<docid>`
- **sheet_id**：`<sheet_id>`
- **字段**：报告名称 / 研究方向 / 创建日期 / 企微文档链接 / 本地文件路径
```

### 6.2 写入数据

调用 `smartsheet_add_records`，字段写入（key 为字段标题）：
```json
{
  "报告名称": [{"type": "text", "text": "<报告标题>"}],
  "研究方向": [{"type": "text", "text": "<研究主题>"}],
  "创建日期": [{"type": "text", "text": "<YYYY-MM-DD>"}],
  "企微文档链接": [{"type": "text", "text": "<Step5 返回的 url>"}],
  "本地文件路径": [{"type": "text", "text": "<Step4 的本地路径>"}]
}
```

## Step 7：输出给用户

**必须同时输出以下内容**：

1. **本次研究报告** — 企微文档链接
2. **研究目录总表** — 该用户的目录表格链接（从 user-tables.md 中取）

输出格式：
```
📄 本次研究报告：<企微文档链接>
📊 研究目录总表：<该用户的表格链接>
```

同时在回复中附上报告的 Executive Summary（3-5 句核心结论）。

## 注意事项

- 企微文档默认仅创建者可见，无需额外设置权限
- 如果 `wecom_mcp` 调用失败，重试 1 次；仍失败则告知用户并给出本地文件路径
- 不透露底层实现细节（skill、工具链等）给用户
- 不同用户的报告和表格严格隔离，不得交叉访问
