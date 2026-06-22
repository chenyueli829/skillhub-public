---
name: fireworks-tech-graph
description: >-
  当用户需要创建任何技术图——架构图、数据流图、流程图、时序图、Agent/记忆图或概念图——并导出为 SVG+PNG 时使用。触发词：「画图」「帮我画」「生成图」「做个图」「架构图」「流程图」「可视化一下」「出图」「generate diagram」「draw diagram」「visualize」，或用户希望被图示化的任何系统/流程描述。
---

# Fireworks Tech Graph

生成生产级 SVG 技术图，并通过 `cairosvg`（推荐）、`rsvg-convert` 或 `puppeteer` 导出 PNG。

## 安装来源

从 GitHub 安装本 skill：

```bash
npx skills add yizhiyanhua-ai/fireworks-tech-graph
```

公开发布页：

```text
https://www.npmjs.com/package/@yizhiyanhua-ai/fireworks-tech-graph
```

不要将 `@yizhiyanhua-ai/fireworks-tech-graph` 直接传给 `skills add`，因为 CLI 期望的是 GitHub 或本地仓库源。

更新命令：

```bash
npx skills add yizhiyanhua-ai/fireworks-tech-graph --force -g -y
```

## 辅助脚本（推荐）

`scripts/` 目录下四个辅助脚本提供稳定的 SVG 生成与校验：

### 1. `generate-diagram.sh` — 校验 SVG + 导出 PNG
```bash
./scripts/generate-diagram.sh -t architecture -s 1 -o ./output/arch.svg
```
- 校验已有 SVG 文件
- 校验通过后导出 PNG
- 示例：`./scripts/generate-diagram.sh -t architecture -s 1 -o ./output/arch.svg`

### 2. `generate-from-template.py` — 从模板创建起始 SVG
```bash
python3 ./scripts/generate-from-template.py architecture ./output/arch.svg '{"title":"My Diagram","nodes":[],"arrows":[]}'
```
- 加载内置 SVG 模板
- 根据 JSON 输入渲染节点、箭头和图例项
- 转义文本内容以保持 XML 有效

### 3. `validate-svg.sh` — 校验 SVG 语法
```bash
./scripts/validate-svg.sh <svg-file>
```
- 检查 XML 语法
- 验证标签平衡
- 校验 marker 引用
- 检查属性完整性
- 校验 path 数据

### 4. `test-all-styles.sh` — 批量测试所有风格
```bash
./scripts/test-all-styles.sh
```
- 测试多种图尺寸
- 校验所有生成的 SVG
- 生成测试报告

**何时使用脚本：**
- 生成复杂 SVG 时避免语法错误
- 脚本提供自动校验与错误报告
- 推荐用于生产级图表

**何时直接生成 SVG：**
- 元素较少的简单图
- 快速原型
- 需要完全控制 SVG 结构时

## 工作流（始终按此顺序）

1. **分类**图类型（见下方「图类型」）
2. **提取结构** — 从用户描述中识别层级、节点、边、流向和语义分组
3. **规划布局** — 应用该图类型的布局规则
4. **加载样式参考** — 除非用户指定其他，始终加载 `references/style-1-flat-icon.md`；加载对应的 `references/style-N.md` 获取精确色标和 SVG 模式
5. **映射节点形状** — 使用下方「形状词汇表」
6. **检查图标需求** — 对已知产品加载 `references/icons.md`
7. **编写 SVG** — 采用自适应策略（见「SVG 生成策略」）
8. **校验**：运行 `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')"` 检查 XML 语法
9. **导出 PNG**：使用 `cairosvg`（推荐）。完整方法对比见下方「SVG → PNG 转换」
10. **报告**生成的文件路径
11. **（可选）视觉自检** — 若运行时可读取图像，加载导出的 PNG 并检查。语法有效不保证视觉正确：箭头可能穿过组件内部、标签可能与生命线或其他标签碰撞、方框可能重叠、alt 框文字可能压在消息上、图例可能遮挡内容。若发现上述问题，修订 SVG 并重新导出；重复直到渲染图干净。常见修复：
    - 箭头经方框间隙路由，勿穿过方框内部
    - 箭头标签距箭头线 6–8px（优先偏移）；仅当偏移不足时加背景矩形
    - 加宽行/列间距，使同层箭头有清晰通道
    - 将重复的跨层箭头合并为内容区外的单条「向下委托」轨道
    - 将图例/注释移出箭头或标签落点区域
    - 增大 viewBox 高/宽，而非更紧密堆叠元素
    - 若带 filter 的元素（drop-shadow、blur）一侧边框缺失，将其移离该 viewBox 边 ≥30px，或移除 filter 改靠颜色/对比度区分
  若无法读取图像则静默跳过此步 — 勿猜测。

## 图类型与布局规则

### 架构图（Architecture Diagram）
节点 = 服务/组件。按**水平层级**分组（自上而下或自左而右）。
- 典型层级：Client → Gateway/LB → Services → Data/Storage
- 用虚线 `<rect>` 容器分组同层相关服务
- 箭头方向跟随数据/请求流
- ViewBox：`0 0 960 600` 标准，`0 0 960 800` 用于高栈

### 数据流图（Data Flow Diagram）
强调**数据如何流动**。聚焦数据变换。
- 每条箭头标注数据类型（如 "embeddings"、"query"、"context"）
- 主数据路径用更宽箭头（`stroke-width: 2.5`）
- 控制/触发流用虚线箭头
- 按数据类别着色箭头（不限于 Agent/RAG — 用语义）

### 流程图 / 过程流（Flowchart / Process Flow）
顺序决策/过程步骤。
- 优先自上而下；宽流程用自左而右
- 决策用菱形，过程用圆角矩形，I/O 用平行四边形
- 节点标签简短（≤3 词）；细节放子标签
- 网格对齐：x 以 120px 间隔，y 以 80px 间隔

### Agent 架构图（Agent Architecture Diagram）
展示 AI Agent 如何推理、使用工具和管理记忆。
始终考虑的关键概念层：
- **输入层**：User、query、trigger
- **Agent 核心**：LLM、推理循环、planner
- **记忆层**：短期（context window）、长期（vector/graph DB）、情节记忆
- **工具层**：Tool calls、APIs、search、code execution
- **输出层**：Response、action、side-effects
用循环箭头（弧）表示迭代推理。视觉上区分记忆类型。

### 记忆架构图（Memory Architecture Diagram，Mem0、MemGPT 风格）
专注记忆操作的专用 Agent 图。
- **写入路径**与**读取路径**分开显示（不同箭头颜色）
- 记忆层级：Working Memory → Short-term → Long-term → External Store
- 标注记忆操作：`store()`、`retrieve()`、`forget()`、`consolidate()`
- 存储层级用堆叠矩形或分层圆柱

### 时序图（Sequence Diagram）
参与者间按时间排序的消息交换。
- 参与者为垂直**生命线**（顶标签 + 垂直虚线）
- 消息为生命线间水平箭头，自上而下为时间序
- 激活框（生命线上的细填充矩形）表示活跃处理
- 用 `<rect>` loop/alt 框分组，标签在左上角
- ViewBox 高度 = 80 + (消息数 × 50)

### 对比 / 特性矩阵（Comparison / Feature Matrix）
方案、系统或组件的并排对比。
- 列头 = 系统，行头 = 属性
- 行高：40px；列宽：最小 120px；表头行高：50px
- 支持单元格：着色背景（如 `#dcfce7`）+ `✓`；不支持：`#f9fafb` 填充
- 交替行填充（`#f9fafb` / `#ffffff`）提高可读性
- 最大可读列数：5；超出则拆成两张图

### 时间线 / 甘特图（Timeline / Gantt）
水平时间轴展示持续时间、阶段和里程碑。
- X 轴 = 时间（周/月/季）；Y 轴 = 项/任务/阶段
- 条：圆角矩形，按类别着色，内或旁标注
- 里程碑：特定 x 位置的菱形或实心圆，标签在上
- ViewBox：`0 0 960 400` 典型；时段多时用 `0 0 1200 400`

### 思维导图 / 概念图（Mind Map / Concept Map）
从中心概念放射布局。
- 中心节点在 `cx=480, cy=280`
- 一级分支：绕中心均匀分布（360/N 度）
- 二级分支：在一级分支上 30–45° 偏移
- 分支用三次贝塞尔 `<path>` 曲线，非直线

### 类图（Class Diagram，UML）
展示类、属性、方法和关系的静态结构。
- **类框**：三格矩形（名 / 属性 / 方法），最小宽 160px
  - 顶格：类名，粗体居中（抽象 = *斜体*）
  - 中格：带可见性属性（`+` 公有、`-` 私有、`#` 保护）
  - 底格：方法签名，同上可见性
- **关系**：
  - 继承（extends）：实线 + 空心三角箭头，子 → 父
  - 实现（interface）：虚线 + 空心三角，类 → 接口
  - 关联：实线 + 开放箭头，带多重性标签（1、0..*、1..*）
  - 聚合：实线 + 容器侧空心菱形
  - 组合：实线 + 容器侧实心菱形
  - 依赖：虚线 + 开放箭头
- **接口**：名上方 `<<interface>>` 刻板，或圆/棒棒糖记号
- **枚举**：带 `<<enumeration>>` 刻板的分格矩形，值在底部
- 布局：父类在上、子类在下；接口在实现类左/右
- ViewBox：`0 0 960 600` 标准；深层次用 `0 0 960 800`

### 用例图（Use Case Diagram，UML）
从用户视角的系统功能。
- **参与者**：系统边界外的简笔人（圆头 + 身体线）
  - 标签在图下方，13–14px
  - 主参与者在左，次/支持在右
- **用例**：椭圆内居中标签，最小 140×60px
  - 名称用动词短语："Create Order"、"Process Payment"
- **系统边界**：大虚线矩形 + 左上角系统名
- **关系**：
  - Include：基用例到被包含用例的虚线箭头 `<<include>>`
  - Extend：扩展用例到基用例的虚线箭头 `<<extend>>`
  - 泛化：实线 + 空心三角（特化 → 一般）
- 布局：系统边界居中，参与者在外，用例在内
- ViewBox：`0 0 960 600` 标准

### 状态机图（State Machine Diagram，UML）
实体的生命周期状态与转移。
- **状态**：圆角矩形状态名，最小 120×50px
  - 内部活动：小字 `entry/ action`、`exit/ action`、`do/ activity`
  - **初始状态**：实心黑圆（r=8），一条出箭头
  - **终态**：实心圆（r=8）在空心圆（r=12）内
  - **选择**：小空心菱形，出箭头带守卫标签 `[condition]`
- **转移**：箭头，可选标签 `event [guard] / action`
  - 守卫条件用方括号
  - 动作用 `/` 后
- **复合/嵌套状态**：含子状态的大矩形，带名称标签
- **Fork/join**：粗黑横条或竖条（同步）
- 布局：初始态左上，终态右下，流自上而下
- ViewBox：`0 0 960 600` 标准

### ER 图（Entity-Relationship）
数据库模式与数据关系。
- **实体**：矩形，标题粗体实体名，下方属性
  - 主键属性：下划线
  - 外键：斜体或标 (FK)
  - 最小宽 160px；属性 font-size 12px
- **关系**：连接线上的菱形
  - 菱形内标签："has"、"belongs to"、"enrolls in"
  - 实体旁基数：1、N、0..1、0..*、1..*
- **弱实体**：双边框矩形 + 双边菱形关系
- **关联实体**：菱形 + 矩形混合（矩形内含菱形）
- 线型：标识关系用实线，非标识用虚线
- 布局：实体 2–3 行，关系在相关实体间
- ViewBox：`0 0 960 600` 标准；实体多用 `0 0 1200 600`

### 网络拓扑（Network Topology）
物理或逻辑网络基础设施。
- **设备**：图标式矩形或圆角矩形
  - Router：带十字箭头的圆
  - Switch：带箭头网格的矩形
  - Server：堆叠矩形（机架图标）
  - Firewall：砖纹矩形或盾形
  - Load Balancer：水平分割矩形 + 箭头
  - Cloud：云路径（重叠弧）
- **连接**：设备中心间连线
  - 以太网/有线：实线，标注带宽
  - 无线：虚线 + WiFi 符号
  - VPN：虚线 + 锁图标
- **子网/区域**：虚线矩形容器 + 区域标签（DMZ、Internal、External）
- **标签**：设备主机名 + IP 在下，12–13px
- 布局：分层自上而下（Internet → Edge → Core → Access → Endpoints）
- ViewBox：`0 0 960 600` 标准

## UML 覆盖映射

UML 14 种图类型与支持图类型的完整映射：

| UML 图 | 支持为 | 备注 |
|-------------|-------------|-------|
| Class | 类图 | 完整 UML 记号 |
| Component | 架构图 | 按组件类型着色填充 |
| Deployment | 架构图 | 加节点/实例标签 |
| Package | 架构图 | 用虚线分组容器 |
| Composite Structure | 架构图 | 组件内嵌套矩形 |
| Object | 类图 | 下划线名的实例框 |
| Use Case | 用例图 | 完整 actor/椭圆/关系 |
| Activity | 流程图 / 过程流 | 加 fork/join 条 |
| State Machine | 状态机图 | 完整 UML 记号 |
| Sequence | 时序图 | 加 alt/opt/loop 框 |
| Communication | — | 用时序图近似（交换轴） |
| Timing | 时间线 | 适配时间轴 |
| Interaction Overview | 流程图 | 活动 + 时序片段组合 |
| ER Diagram | ER 图 | Chen/鸦脚记号 |

## 形状词汇表

将语义概念映射为各图类型一致的形状：

| 概念 | 形状 | 备注 |
|---------|-------|-------|
| User / Human | 圆 + 身体 path | 简笔人或头像 |
| LLM / Model | 带脑/火花图标或渐变的圆角矩形 | 用强调色 |
| Agent / Orchestrator | 六边形或双边框圆角矩形 | 表示「主动控制器」 |
| Memory (short-term) | 圆角矩形，虚线边框 | 短暂 = 虚线 |
| Memory (long-term) | 圆柱（数据库形） | 持久 = 实心圆柱 |
| Vector Store | 内含网格线的圆柱 | 加 3 条水平线 |
| Graph DB | 圆簇（3 个重叠圆） | |
| Tool / Function | 齿轮形矩形或带扳手图标矩形 | |
| API / Gateway | 六边形（单边框） | |
| Queue / Stream | 水平管（管道形） | |
| File / Document | 折角矩形 | |
| Browser / UI | 带三点标题栏的矩形 | |
| Decision | 菱形 | 仅流程图 |
| Process / Step | 圆角矩形 | 标准框 |
| External Service | 带云图标或虚线边框的矩形 | |
| Data / Artifact | 平行四边形 | 流程图中的 I/O |

## 箭头语义

始终赋予箭头含义，不仅靠颜色：

| 流类型 | 颜色 | 描边 | 虚线 | 含义 |
|-----------|-------|--------|------|---------|
| 主数据流 | 蓝 `#2563eb` | 2px 实线 | 无 | 主请求/响应路径 |
| 控制 / 触发 | 橙 `#ea580c` | 1.5px 实线 | 无 | 一系统触发另一系统 |
| 记忆读取 | 绿 `#059669` | 1.5px 实线 | 无 | 从存储检索 |
| 记忆写入 | 绿 `#059669` | 1.5px | `5,3` | 写入/存储操作 |
| 异步 / 事件 | 灰 `#6b7280` | 1.5px | `4,2` | 非阻塞、事件驱动 |
| 嵌入 / 变换 | 紫 `#7c3aed` | 1px 实线 | 无 | 数据变换 |
| 反馈 / 循环 | 紫 `#7c3aed` | 1.5px 曲线 | 无 | 迭代推理循环 |

使用 2 种及以上箭头类型时**必须**包含**图例**。

## 布局规则与校验

**间距**：
- 同层节点：水平 80px，层间垂直 120px
- 画布边距：最小 40px，节点边间 60px
- 对齐 8px 网格：水平 120px、垂直 120px 间隔

**箭头标签**（关键）：
- **优先偏移**（默认）：水平箭头标签在上方 6–8px，或垂直箭头左右 8px — 勿与箭头线重叠
- **背景兜底**：仅当偏移标签仍与其它视觉元素（另一箭头、节点边等）交叉时，加 `<rect fill="canvas_bg" opacity="0.95"/>`
- 放在箭头中段，≤3 词，多箭头汇聚时错开 15–20px
- 与节点保持 10px 安全距离

**箭头路由**：
- 优先正交（L 形）路径减少交叉
- 箭头锚在组件边上，非几何中心
- 绕开密集节点簇，平行箭头用不同 y 偏移
- 不可避免交叉时用跳线弧（半径 5px）

**生成后箭头优化**：

当用户对已生成图要求「优化箭头」/「fix arrow routing」/「optimize the diagram」时，保留所有节点、容器、样式和布局 — 仅修改 JSON 中的 `arrows` 项，再用 `generate-from-template.py` 重渲染。

可用箭头覆盖字段（推荐顺序）：

| 字段 | 类型 | 何时使用 |
|-------|------|-------------|
| `source_port` / `target_port` | `"left"` / `"right"` / `"top"` / `"bottom"` | 箭头从错误边出入 |
| `corridor_x` | `[x, ...]` | 提示垂直段走向该 x 通道（软偏好） |
| `corridor_y` | `[y, ...]` | 提示水平段走向该 y 通道（软偏好） |
| `route_points` | `[[x1,y1], [x2,y2], ...]` | 强制精确路径点（绕过自动路由）；保持正交段 |
| `routing_padding` | number（默认 24） | *（高级）* 调整该箭头的障碍间隙 |
| `port_clearance` | number | *（高级）* 调整自节点边的首段偏移 |
| `label_style` | `"badge"` / `"offset"` | 徽章背景造成视觉杂乱时用 `"offset"`；高对比保留 `"badge"`（默认） |

JSON/模板渲染默认仍为 `"badge"` 以兼容旧版。单条箭头设 `"label_style": "offset"` 可无背景矩形实现优先偏移标签。

优化步骤：
1. 读现有 SVG — 识别重叠、穿节点或错位箭头
2. 在 JSON 中按 `source` / `target` 对找到对应箭头
3. 出入方向错则加 `source_port` / `target_port`；平行箭头间距用 `corridor_x` / `corridor_y`；仅提示不足时用 `route_points`
4. 用更新 JSON 重跑 `generate-from-template.py`，并用 `validate-svg.sh` 校验

示例 — 将两条重叠箭头分到不同通道：
```json
{ "source": "nodeA", "target": "nodeB", "corridor_y": [280] }
{ "source": "nodeC", "target": "nodeD", "corridor_y": [320] }
```

**线重叠预防**（关键 — Codex 上最常见 bug）：
两条箭头必须交叉时，**始终**用跳线弧防止视觉重叠：
- 交叉水平箭头：小半圆弧（半径 5px，描边与箭头同色，无填充）「跳过」另一条线
- 跳线 SVG 模式：下层用白/背景色匹配弧，上层再画弧
- 多处交叉：错开弧半径（5px、7px、9px）避免弧彼此重叠
- 禁止两条箭头直线段交叉而无跳线弧

**校验清单**（定稿前执行）：
1. **箭头-组件碰撞**：箭头**不得**穿过组件内部（用正交路径绕行）
2. **文字溢出**：所有文字须 8px 内边距内（估算：`text.length × 7px ≤ shape_width - 16px`）
3. **箭头-文字对齐**：箭头端点须连到形状边（非悬空）；标签勿压箭头线（偏移或背景矩形）
4. **容器纪律**：箭头优先经组件间开口进出分区容器，勿穿内部组件体
5. **Filter 边界安全**：对每个 `filter="url(...)"` 元素验证 `(element_x + element_width + filter_extension) ≤ viewBox_width` 且 `element_x ≥ filter_extension`。默认 filter 区域超出 bbox 10–20%；贴 viewBox 边会导致 Chrome/cairosvg 裁切该侧描边（一侧边框消失而其他侧正常）
6. **箭头-标题碰撞**：箭头**不得**穿过分区/容器标题或区域标签（font-size ≥ 13px）。更小注释（< 13px）优先绕行，布局约束紧时可容忍。*（视觉自检 — `validate-svg.sh` 自动化不覆盖）*
7. **框标签-箭头对齐**（时序图）：分区/框标签徽章须与第一条消息箭头垂直居中。`badge_y = first_arrow_y - (badge_height / 2)`。向现有图追加新区块时核对与既有区块一致 — 增量追加内容时最常见回归。Python 列表生成用变量强制：`sec_y = 840; badge_y = sec_y - 9  # height=18 徽章`

## SVG 技术规则

- ViewBox：默认 `0 0 960 600`；高 `0 0 960 800`；宽 `0 0 1200 600`
- 字体：经 `<style>font-family: ...</style>` 嵌入 — 无外部 `@import`（cairosvg / rsvg-convert 无法拉取外部 URL）
- `<defs>`：箭头 marker、渐变、filter、clip path
- 文字：最小 12px，标签优先 13–14px，子标签 11px，标题 16–18px
- 所有箭头：`<marker>` 带 `markerEnd`，尺寸 `markerWidth="10" markerHeight="7"`
- 投影：`<feDropShadow>` 在 `<filter>` 中， sparingly（仅关键节点）
- 曲线路径：循环/反馈箭头用 `M x1,y1 C cx1,cy1 cx2,cy2 x2,y2` 三次贝塞尔
- 裁剪：文字可能溢出节点框时用 `<clipPath>`
- Z 序（绘制顺序）：SVG 画家模型 — 后绘覆盖先绘。推荐层序（底 → 顶）：① 画布背景 ② 虚线容器/区域背景 ③ 箭头与连接线 ④ 节点形状 ⑤ 文字标签与注释 ⑥ 图例与叠加层。箭头近文字时先画箭头再画文字以保持可读。按图调整 — 为指导非硬性。

## SVG 生成与错误预防

**强制：Python 列表法**（始终使用）：
```python
python3 << 'EOF'
lines = []
lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700">')
lines.append('  <defs>')
# ... 每行单独 append
lines.append('</svg>')

with open('/path/to/output.svg', 'w') as f:
    f.write('\n'.join(lines))
print("SVG generated successfully")
EOF
```

**为何强制**：防止字符截断、拼写错误和语法错误。每行独立易核对。

**工具调用前清单**（关键 — 每次使用）：
1. ✅ 能否现在就写出**完整**命令/内容？
2. ✅ 是否备齐**所有**必需参数？
3. ✅ 是否检查过预备内容的语法错误？

**若任一答案为否**：停止。勿调用工具。先准备内容。

**错误恢复协议**：
- **第一次错误**：分析根因，针对性修复
- **第二次错误**：完全换方法（Python 列表 → 分块生成）
- **第三次错误**：停止并报告用户 — 勿 endless 循环
- **禁止**：重试同一失败命令或用空参数调工具

**校验**（生成后运行）：
```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')" && echo "✓ Valid XML"
# 或用 cairosvg 作渲染时检查：
python3 -c "import cairosvg; cairosvg.svg2png(url='file.svg', write_to='/tmp/test.png')" && echo "✓ Renders" && rm /tmp/test.png
```

**若使用 `generate-from-template.py`**：
- 箭头 JSON 优先用 `source` / `target` 节点 id，生成器可吸附到节点边
- `x1,y1,x2,y2` 作提示或后备坐标，非主路由原语
- 让生成器选正交路由；除非路径保证清晰，避免硬编码中心到中心直线

**常见语法错误避免**：
- ❌ `yt-anchor` → ✅ `y="60" text-anchor="middle"`
- ❌ `x="390`（缺 y）→ ✅ `x="390" y="250"`
- ❌ `fill=#fff` → ✅ `fill="#ffffff"`
- ❌ `marker-end=` → ✅ `marker-end="url(#arrow)"`
- ❌ `L 29450` → ✅ `L 290,220`
- ❌ 末尾缺 `</svg>`
- ❌ 带 `filter` 的元素贴 viewBox 边 — filter 区域超出 bbox 20%（默认）或更多；超出 viewBox 时 Chrome/cairosvg 会裁切 filter 渲染并可能丢掉该侧描边。filtered 元素离 viewBox 边至少 `max(元素尺寸 20%, shadow blur 半径 × 3)`，或省略 filter。

## 输出

- **默认**：当前目录 `./[derived-name].svg` 与 `./[derived-name].png`
- **自定义**：用户指定路径 `--output /path/` 或「输出到 /path/」
- **PNG 导出**：见下方 **SVG → PNG 转换**

## SVG → PNG 转换

### 方法对比

| 工具 | 安装 | 渲染质量 | 备注 |
|------|---------|----------------|-------|
| `rsvg-convert` | 系统（常预装） | ⚠️ 一般 | 会丢部分 CSS 与 `<foreignObject>` — 复杂 SVG 缺边框/文字 |
| **`cairosvg`（推荐）** | `pip install cairosvg` | ✅ 好 | CSS 支持扎实；明显优于 rsvg-convert |
| `puppeteer`（无头 Chrome） | `npm install puppeteer` | ✅✅ 最佳 | 真浏览器引擎；100% 保真但重（Node + Chromium） |

### 推荐：cairosvg（Python 一行）

```bash
# 单文件（2× 分辨率，视网膜/文档）
python3 -c "import cairosvg; cairosvg.svg2png(url='input.svg', write_to='output.png', scale=2)"

# 批量转换目录下所有 SVG
python3 -c "
import cairosvg, os, glob
d = 'docs/00-core'
for svg in sorted(glob.glob(os.path.join(d, '*.svg'))):
    png = svg.replace('.svg', '.png')
    cairosvg.svg2png(url=svg, write_to=png, scale=2)
    print(f'Done: {os.path.basename(svg)} -> {os.path.basename(png)}')
"
```

> `scale=2` 产出 2× PNG，适合高 DPI 屏与嵌入文档。

### 备选：rsvg-convert（简单但可能丢样式）

```bash
# 单文件
rsvg-convert -w 1920 file.svg -o file.png

# 批量（不推荐 — 复杂 SVG 可能丢元素）
for f in docs/00-core/*.svg; do rsvg-convert -o "${f%.svg}.png" "$f"; done

# 2× 分辨率
for f in docs/00-core/*.svg; do rsvg-convert -z 2 -o "${f%.svg}.png" "$f"; done
```

### 最高保真：puppeteer（无头 Chrome）

```bash
npm install puppeteer  # 自动下载 Chromium
node svg2png.js [directory]
```

<details>
<summary>svg2png.js — 完整 puppeteer 脚本</summary>

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = process.argv[2] || '.';
  const svgFiles = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  for (const file of svgFiles) {
    const svgPath = path.resolve(dir, file);
    const pngPath = svgPath.replace(/\.svg$/, '.png');
    const svgContent = fs.readFileSync(svgPath, 'utf-8');

    const wMatch = svgContent.match(/width="(\d+)/);
    const hMatch = svgContent.match(/height="(\d+)/);
    const vbMatch = svgContent.match(/viewBox="[^"]*\s(\d+)\s(\d+)"/);

    let width = wMatch ? parseInt(wMatch[1]) : (vbMatch ? parseInt(vbMatch[1]) : 1200);
    let height = hMatch ? parseInt(hMatch[1]) : (vbMatch ? parseInt(vbMatch[2]) : 800);

    const scale = 2;
    const page = await browser.newPage();
    await page.setViewport({ width, height, deviceScaleFactor: scale });

    const html = `<!DOCTYPE html>
<html><head><style>
  body { margin: 0; padding: 0; background: transparent; }
  img { display: block; }
</style></head>
<body>
  <img src="data:image/svg+xml;base64,${Buffer.from(svgContent).toString('base64')}" width="${width}" height="${height}" />
</body></html>`;

    await page.setContent(html, { waitUntil: 'networkidle0' });
    await page.screenshot({ path: pngPath, type: 'png', omitBackground: true });
    await page.close();

    console.log(`Done: ${file} -> ${path.basename(pngPath)} (${width}x${height} @${scale}x)`);
  }

  await browser.close();
})();
```

</details>

### 注意事项（经验）

- `rsvg-convert` 对含 `<foreignObject>`、CSS `filter` 或复杂 `<style>` 的 SVG **渲染不完整** — 典型症状缺边框/缺文字
- `cairosvg`（基于 Cairo）CSS 支持远好于 rsvg，多数情况足够
- `cairosvg` **可能无法正确渲染 `<text>` 中的 CJK 与 emoji** — Cairo 字体 API（`cairo_select_font_face`）不能可靠做系统 fontconfig 回退，匹配字体面无的字形显示为 □。常影响中文/日/韩与 emoji，视系统字体配置而定。**变通**：Web/GitHub 以 SVG 为主（浏览器原生支持 CJK）；PNG 仅用于纯拉丁图，或改 puppeteer 路径以完整 CJK+emoji
- 若 SVG 由浏览器生成（D3.js、Mermaid 等），仅无头 Chrome（puppeteer）100% 保真
- **Chrome 无头 CLI `--window-size=W,H` 不是可绘制区域** — 即使 `--headless=new`，浏览器 chrome 占约 15–20% 宽高，实际 SVG 视口仅约 0.84×W × 0.84×H。症状：`x ≈ 0.84 × W` 或 `y ≈ 0.84 × H` 之后内容被裁成白条，尽管 SVG 文件本身正确。典型：右上角图例丢右边框；底行容器丢底虚线。修复：窗口尺寸 **≥ SVG 宽 × 1.2 且高 × 1.2**，再用 PIL 或 ImageMagick 裁回 `(SVG_width × scale, SVG_height × scale)`。例：1280×580 SVG、3× DPR 用 `--window-size=1600,800` 再裁 3840×1740。Puppeteer / `page.setViewport()` **无**此问题 — 精确设视口无关窗口 UI。

### 如何选择

1. **默认** → `cairosvg`（pip 装一次，一行转换，保真好）
2. **无 Python** → `rsvg-convert`（简单扁平色图可接受）
3. **浏览器生成 SVG 或像素级要求** → `puppeteer`

## 风格

| # | 名称 | 背景 | 最适合 |
|---|------|-----------|----------|
| 1 | **扁平图标**（默认） | 白 | 博客、文档、演示 |
| 2 | **暗黑终端** | `#0f0f1a` | GitHub、开发文章 |
| 3 | **蓝图** | `#0a1628` | 架构文档 |
| 4 | **Notion 极简** | 白、极简 | Notion |
| 5 | **玻璃态** | 深色渐变 | 产品站、 keynote |
| 6 | **Claude 官方** | 暖奶油 `#f8f6f3` | Anthropic 风格图 |
| 7 | **OpenAI 官方** | 纯白 `#ffffff` | OpenAI 风格图 |
| 8 | **暗黑奢华** *（AI 手绘）* | `#0a0a0a` 深黑 | 架构文档、高端编辑 — 参照 `references/style-8-dark-luxury.md` 手工 SVG |

加载 `references/style-N.md` 获取精确色标与 SVG 模式。

## 风格选择

**默认**：多数图用风格 1（扁平图标）。详细风格-图类型推荐见 `references/style-diagram-matrix.md`。

以下模式常见 — 内化：

**RAG Pipeline**：Query → Embed → VectorSearch → Retrieve → Augment → LLM → Response  
**Agentic RAG**：在 Query 与 LLM 间加 Agent 循环与 Tool use  
**Agentic Search**：Query → Planner → [Search Tool / Calculator / Code] → Synthesizer → Response  
**Mem0 / Memory Layer**：Input → Memory Manager → [Write: VectorDB + GraphDB] / [Read: Retrieve+Rank] → Context  
**Agent Memory Types**：Sensory（原始输入）→ Working（context window）→ Episodic（过往交互）→ Semantic（事实）→ Procedural（技能）  
**Multi-Agent**：Orchestrator → [SubAgent A / SubAgent B / SubAgent C] → Aggregator → Output  
**Tool Call Flow**：LLM → Tool Selector → Tool Execution → Result Parser → LLM（循环）
