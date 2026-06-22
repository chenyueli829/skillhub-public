---
name: ai-painpoint-kb
description: 每小时从 HN 挖掘 AI 产品用户痛点，持续迭代「AI产品机会知识库」Markdown 文件。知识库路径固定，包含方向评级、用户原声、更新日志。
---

# AI 产品痛点挖掘 & 知识库维护

## 触发场景

- Cron job 每小时自动运行（维护 AI 产品机会知识库）
- 用户说「抓一下 HN 最新讨论」「更新痛点知识库」

---

## 知识库路径

```
/Users/chenyueli/obsidian-lylian/workspace-lylian/06-AI产品痛点挖掘/痛点汇总/AI产品机会知识库.md
```

---

## 数据源

### Hacker News（主要来源，稳定可用）

⚠️ **HN Firebase API (`hacker-news.firebaseio.com`) 在本机有 SSL 握手失败问题（`UNEXPECTED_EOF_WHILE_READING` / `handshake timed out`），Python urllib + 禁用 SSL 验证也无效。请改用 Algolia HN Search API。**

**正确做法：使用 Algolia HN Search API（`hn.algolia.com`）**，支持关键词搜索 + 时间过滤，`curl` 可直接访问，无 SSL 问题：

```
# 按时间排序，只取最近 48 小时的故事
https://hn.algolia.com/api/v1/search_by_date?tags=story&query={关键词}&hitsPerPage=20&numericFilters=created_at_i>{unix_timestamp_48h_ago}
```

多个关键词查询后合并去重（按 `objectID`）：
- `llm`、`AI agent`、`chatgpt`、`openai`、`claude anthropic`
- `AI startup`、`automation workflow`、`coding assistant`、`AI productivity`
- `machine learning`

返回字段：`objectID`（故事 ID）、`title`、`url`、`points`、`num_comments`、`created_at_i`、`story_text`（摘要，如有）

### Reddit（**已确认永久 403 封锁**）

⚠️ **Reddit 对本机 IP 返回 403，所有 User-Agent 均无效，不要尝试。**  
上次确认时间：2026-04-25。每次运行直接跳过，记录「Reddit 因 403 封锁获取 0 条」。

---

## 批量抓取 HN 详情（关键技巧）

**⚠️ HN Firebase API 在本机有 SSL 握手失败问题（Python urllib + 禁用 SSL 验证也无效）。必须改用 Algolia HN Search API。**

**⚠️ execute_code 沙盒无法可靠运行多步骤脚本（heredoc 也不行）。正确做法：用 `write_file` 写脚本到 `/tmp/`，再用 `terminal()` 直接执行。**

### 正确抓取模式（Algolia API）

```python
# 1. 用 write_file 写脚本到 /tmp/fetch_hn.py
# 2. terminal("python3 /tmp/fetch_hn.py", timeout=120)
# 3. 结果写入 /tmp/hn_items.json，再用 read_file 读取
```

### fetch_hn.py 模板（Algolia 版）

```python
import urllib.request, urllib.parse, json, ssl, time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read().decode()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

cutoff = int(time.time()) - 48 * 3600  # 48 hours ago

queries = [
    "llm", "AI agent", "chatgpt", "openai", "claude anthropic",
    "AI startup", "automation workflow", "coding assistant",
    "AI productivity", "machine learning"
]

stories = {}
for query in queries:
    encoded = urllib.parse.quote(query)
    url = (
        f"https://hn.algolia.com/api/v1/search_by_date"
        f"?tags=story&query={encoded}&hitsPerPage=20"
        f"&numericFilters=created_at_i>{cutoff}"
    )
    raw = fetch_url(url)
    if not raw:
        continue
    try:
        data = json.loads(raw)
        for hit in data.get("hits", []):
            sid = hit.get("objectID")
            if sid and sid not in stories:
                stories[sid] = {
                    "id": sid,
                    "title": hit.get("title", ""),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                    "score": hit.get("points", 0),
                    "descendants": hit.get("num_comments", 0),
                    "time": hit.get("created_at_i", 0),
                    "text": (hit.get("story_text") or "")[:300],
                }
    except Exception as e:
        print(f"Parse error for query '{query}': {e}")
    time.sleep(0.2)

result = list(stories.values())
with open("/tmp/hn_items.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"DONE: {len(result)} unique AI stories from last 48h")
```

---

## 关键词过滤

筛选标题包含以下关键词的帖子（全部小写匹配）：

```python
keywords = [
    'ai', 'llm', 'gpt', 'agent', 'automation', 'tool', 'productivity', 
    'workflow', 'chatgpt', 'claude', 'openai', 'anthropic', 'copilot', 
    'cursor', 'ml', 'model', 'inference', 'embeddings', 'rag', 'vector', 
    'neural', 'machine learning'
]
```

---

## 知识库文件格式

```markdown
# AI产品机会知识库

> 持续迭代 · 最后更新：{datetime}
> 累计追踪方向：{N}个 · 累计抓取来源：{N}条

---

## 方向一：{方向名称}

**机会评级**：🔥🔥🔥🔥🔥 / 🔥🔥🔥🔥 / 🔥🔥🔥（5-3分）
**首次发现**：{日期}
**最后更新**：{日期}

### 核心痛点
{1-2句话描述核心问题}

### 目标用户
{描述}

### 现有方案的不足
{描述}

### 产品机会
{具体的产品切入点}

### 用户原声（持续积累）
- [{日期}] "{原话}" — 来源：[{来源}]({链接})

### 更新日志
- {datetime}：{本次新增/更新了什么}

---

## 📊 本次运行摘要（{datetime}）

- 抓取来源：{N}条新内容
- 新增方向：{N}个
- 更新方向：{N}个
- 跳过重复：{N}条
```

方向按机会评级从高到低排序（🔥🔥🔥🔥🔥 在前）。

---

## 内容分析逻辑

对每条抓取到的内容：

| 情况 | 处理方式 |
|------|----------|
| 与已有方向高度相关 | 补充用户原声、更新证据、如有重大变化更新「最新判断」 |
| 全新方向/场景 | 新建方向条目，包含所有字段 |
| 重复内容且无新信息 | 跳过，不写入 |

### 评级标准
- 🔥🔥🔥🔥🔥：市场痛点明确、用户原声直接、已有验证案例、竞品空白明显
- 🔥🔥🔥🔥：痛点真实但竞争激烈，或市场规模待验证
- 🔥🔥🔥：趋势性机会，尚需更多验证

---

## 现有追踪方向（截至 2026-04-25）

1. AI 编码工作流碎片化（🔥🔥🔥🔥🔥）
2. LLM 品牌可见性监控 / GEO（🔥🔥🔥🔥🔥）
3. AI 代理成本压力与商业模式危机（🔥🔥🔥🔥🔥）
4. AI 辅助垂直行业文档生成（🔥🔥🔥🔥）
5. 个人知识管理 + AI（PKM）（🔥🔥🔥🔥）
6. AI 音频/语音内容生产工具（🔥🔥🔥🔥）
7. AI 内容可信度危机与溯源工具（🔥🔥🔥🔥）
8. AI Agent 持久记忆与跨会话知识沉淀（🔥🔥🔥🔥）
9. AI Agent 自主执行本地/设备任务（🔥🔥🔥🔥）
10. AI 虚拟穿搭与个人形象顾问（🔥🔥🔥）
11. AI 在高风险垂直场景的可信应用（🔥🔥🔥）
12. AI 改变传统游戏开发与创意产业（🔥🔥🔥）
13. AI 基础模型行业整合与企业市场竞争格局（🔥🔥🔥）
14. AI 使用中的完成障碍与注意力管理（🔥🔥🔥）

---

## 运行流程摘要

1. 读取当前知识库（如不存在则从零创建）
2. **用 `write_file` 写 Algolia 抓取脚本到 `/tmp/fetch_hn.py`**（不要用 execute_code 或 heredoc；不要用 HN Firebase API，SSL 握手会失败）
3. **用 `terminal("python3 /tmp/fetch_hn.py", timeout=120)` 执行**
4. 用 `read_file` 读取 `/tmp/hn_items.json` 获取结果（通常 60-120 条去重故事）
5. 逐条分析：匹配已有方向 or 新建方向
6. 构建完整新知识库文本（覆盖写入）
7. 回复摘要（新增/更新方向，总方向数，抓取条数）

---

## 注意事项

- **HN topstories 和 newstories 有重叠**，抓完后按 ID 去重再分析
- **每批 curl 并行最多 30 条**，超过 30 条 terminal 可能超时
- **JSON 解析用 raw_decode 循环**，不要用 `json.loads()` 直接解析拼接输出
- **方向更新时**：在「用户原声」中 append 新条目，在「更新日志」中追加记录，同时更新「最后更新」日期
- **覆盖写入整个文件**，不要只追加末尾（会破坏排序和格式）
- 如遇 HN API 不稳定（timeout），记录失败数量，不影响已解析的条目
