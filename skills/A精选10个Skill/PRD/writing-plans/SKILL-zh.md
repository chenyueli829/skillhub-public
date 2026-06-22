---
name: writing-plans
description: 当你已有规格说明或多步骤任务的需求、且尚未开始写代码时使用
---

# 编写实现计划

## 概述

编写详尽的实现计划，假定执行工程师对代码库**零上下文**、品味也**未必可靠**。文档中应写清他们所需的一切：每个任务要动哪些文件、代码、测试、可能需要查阅的文档，以及如何验证。把整个计划拆成一口能吃下的小任务。遵循 DRY、YAGNI、TDD，并频繁提交。

假定对方是熟练开发者，但几乎不了解我们的工具链或问题域，且对良好的测试设计也不太熟。

**开始时须声明：**「我正在使用 writing-plans skill 来创建实现计划。」

**上下文：** 若在隔离 worktree 中工作，该 worktree 应在执行时通过 `superpowers:using-git-worktrees` skill 创建。

**计划保存路径：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- 用户对计划存放位置有偏好时，以用户偏好覆盖此默认路径

## 范围检查

若规格涵盖多个彼此独立的子系统，本应在头脑风暴阶段拆成子项目规格。若尚未拆分，应建议拆成多份计划——每个子系统一份。每份计划单独完成后都应产出可运行、可测试的软件。

## 文件结构

在定义任务之前，先梳理将创建或修改哪些文件，以及各自职责。分解决策在此阶段锁定。

- 设计边界清晰、接口明确的单元；每个文件应有一个清晰职责。
- 你更容易推理能一次性放进上下文的代码；文件聚焦时编辑也更可靠。优先小而专的文件，而非职责过多的大文件。
- 经常一起改动的文件应放在一起。按职责拆分，而非按技术分层。
- 在既有代码库中遵循既有模式。若代码库使用大文件，不要单方面重构——但若你正在修改的文件已臃肿，在计划中纳入拆分是合理的。

此结构指导任务分解。每个任务应产出可独立理解、自成一体的变更。

## 一口大小任务粒度

**每一步是一个动作（约 2–5 分钟）：**
- 「写失败测试」——一步
- 「运行测试确认失败」——一步
- 「写最小实现使测试通过」——一步
- 「运行测试确认通过」——一步
- 「提交」——一步

## 计划文档头部

**每份计划必须以如下头部开头：**

```markdown
# [功能名称] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [一句话描述要构建什么]

**Architecture:** [2–3 句说明实现思路]

**Tech Stack:** [关键技术/库]

---
```

## 任务结构

````markdown
### Task N: [组件名称]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 禁止占位

每一步必须包含工程师所需的**实际内容**。以下为**计划失败**——绝不要写：
- 「TBD」「TODO」「稍后实现」「补充细节」
- 「添加合适的错误处理」/「添加校验」/「处理边界情况」（无具体代码）
- 「为上述内容写测试」（无具体测试代码）
- 「与 Task N 类似」（应重复代码——工程师可能乱序阅读任务）
- 只描述要做什么、不展示怎么做的步骤（涉及代码的步骤必须有代码块）
- 引用在任何任务中都未定义的类型、函数或方法

## 牢记

- 始终使用精确文件路径
- 每一步的代码必须完整——若某步改代码，须展示代码
- 精确命令与预期输出
- DRY、YAGNI、TDD、频繁提交

## 自检

写完完整计划后，用新眼光对照规格检查计划。这是你自己运行的清单——不是派发子代理。

**1. 规格覆盖：** 浏览规格中每一节/每一条需求。能否指向实现它的任务？列出缺口。

**2. 占位扫描：** 在计划中搜索红旗——「禁止占位」一节中的任何模式。修复它们。

**3. 类型一致性：** 后续任务中的类型、方法签名、属性名是否与前面任务一致？Task 3 叫 `clearLayers()`、Task 7 却叫 `clearFullLayers()` 就是 bug。

若发现问题，就地修复。无需重新走一遍审阅——修完继续。若发现规格需求没有对应任务，补上任务。

## 执行交接

保存计划后，提供执行方式选择：

**「计划已完成并保存至 `docs/superpowers/plans/<filename>.md`。两种执行方式：**

**1. 子代理驱动（推荐）** — 每个任务派发全新子代理，任务间审阅，迭代快

**2. 会话内联执行** — 在本会话用 executing-plans 执行，批量执行并设检查点

**选哪种？」**

**若选择子代理驱动：**
- **必需子 skill：** 使用 `superpowers:subagent-driven-development`
- 每任务全新子代理 + 两阶段审阅

**若选择会话内联执行：**
- **必需子 skill：** 使用 `superpowers:executing-plans`
- 批量执行并在检查点供审阅
