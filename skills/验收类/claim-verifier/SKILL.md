---
name: claim-verifier
description: >
  Use this skill to verify the credibility of claims, data points, and observations in an article or document.
  Trigger when: user asks to "verify sources", "check credibility", "validate data", "fact-check", "校验数据来源",
  "验证可信度", or pastes an article asking "is this accurate?".
  The skill extracts all factual claims, searches for primary sources, scores credibility 1–5,
  annotates each claim with a source link, and outputs a structured verification report.
---

# Claim Verifier Skill

## Overview

This skill systematically verifies the factual claims and data points in an article.
It separates **verifiable facts** (numbers, quotes, attributions, events) from **opinions/analysis**,
searches for primary sources for each claim, scores credibility, and returns an annotated report
with inline source links — ready to paste back into the original document.

---

## When to Use

- User pastes an article and asks "is this accurate?" or "verify the sources"
- User asks to add citation links to a document
- User wants a credibility audit before publishing or sharing
- User says "校验数据来源" / "验证可信度" / "加引用" / "fact-check this"

---

## Execution Steps

### Step 1 — Extract Claims

Read the full article. For each paragraph, extract:

| Type | Description | Example |
|---|---|---|
| **Stat** | Specific numbers, percentages, market sizes | "$91B market by 2026" |
| **Quote** | Named attribution to a person or org | "Gartner predicts 40%..." |
| **Event** | Dated announcement, product launch, acquisition | "Stripe acquired Bridge in Feb 2025" |
| **Opinion** | Analysis or interpretation — skip verification | "This will reshape the industry" |

Only verify **Stat**, **Quote**, and **Event** claims. Skip opinions.

---

### Step 2 — Score Credibility (1–5)

For each claim, search for the primary source and assign a score:

| Score | Meaning | Criteria |
|---|---|---|
| ⭐⭐⭐⭐⭐ | **Verified** | Found in official press release, company IR, or original analyst report |
| ⭐⭐⭐⭐ | **Likely accurate** | Confirmed by 2+ independent reputable media (Reuters, FT, TechCrunch, etc.) |
| ⭐⭐⭐ | **Plausible** | One secondary source found; primary not directly accessible (paywalled) |
| ⭐⭐ | **Unverified** | Claim widely cited but no traceable primary source found |
| ⭐ | **Disputed / Wrong** | Contradicted by primary source, or numbers mismatch |

---

### Step 3 — Search Protocol

For each claim, run searches in this priority order:

1. **Official source first**: company investor relations, press releases, official blog
2. **Named analyst report**: Gartner, McKinsey, IDC, Forrester — look for official page, not summaries
3. **Tier-1 media**: Reuters, Bloomberg, FT, WSJ, TechCrunch, The Verge
4. **Cross-check numbers**: if claim says "$X billion", search for the exact figure + source name
5. **Date-verify**: confirm the claim matches the stated time period

> ⚠️ Do NOT accept a claim as verified if the only source is another article that merely repeats the number.
> Always trace back to the original report or announcement.

---

### Step 4 — Output Format

Return a **Verification Report** in this structure:

```markdown
## 📋 Verification Report
> Article: [title or first line]
> Verified: [date]
> Claims checked: X | Verified: X | Unverified: X | Disputed: X

---

### ✅ Verified Claims

| Claim | Score | Primary Source |
|---|---|---|
| [exact claim text] | ⭐⭐⭐⭐⭐ | [Source Name](URL) |

---

### ⚠️ Unverified / Needs Caution

| Claim | Score | Issue | Best Available Source |
|---|---|---|---|
| [exact claim text] | ⭐⭐ | No primary source found | [closest source](URL) |

---

### ❌ Disputed / Incorrect

| Claim | Score | What the Source Actually Says | Correction Source |
|---|---|---|---|
| [exact claim text] | ⭐ | [actual figure/statement] | [Source](URL) |

---

### 💡 Suggested Inline Citations

Copy-paste these to replace bare claims in the original document:

- "**$91B market by 2026**" → add `[^1]` → footnote: `[^1]: [Fortune Business Insights, 2026](URL)`
- "**Gartner predicts 40%**" → add `[^2]` → footnote: `[^2]: [Gartner Press Release, Aug 2025](URL)`
```

---

### Step 5 — Annotate the Original (Optional)

If user requests "annotate inline" or "加到原文":
1. Re-output the full article with `[^N]` footnote markers added after each verified claim
2. Append the `## 参考文献` block at the end using `[^N]: [Title](URL)` syntax
3. Mark unverified claims with `[⚠️ source not found]` inline so the author knows to investigate

---

## Quality Rules

1. **Never fabricate a source URL** — if you cannot find a real URL, mark score ⭐⭐ and explain
2. **Distinguish between claim types** — a McKinsey blog post is not the same as a McKinsey formal report
3. **Flag "best case" / "scenario" data** — analyst projections labeled as scenarios should be quoted with caveats
4. **Cross-check numbers precisely** — "$3–5 trillion" ≠ "$5 trillion"; report exact wording from source
5. **Date matters** — a 2023 report cited as a 2026 fact should be flagged as potentially outdated

---

## Example Run

**Input**: "Gartner predicts 40% of enterprise apps will embed AI agents by end of 2026"

**Search**: `Gartner 40% enterprise apps AI agents 2026 press release`

**Found**: https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025

**Result**:
- Score: ⭐⭐⭐⭐⭐
- Exact wording matches. Official Gartner newsroom. Published Aug 26, 2025.
- Suggested footnote: `[^]: [Gartner, Aug 2025](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-...)`

---

## Notes

- This skill works best with **Exa web search** for finding primary sources
- For paywalled reports (Gartner, McKinsey), look for the official summary/press release page instead
- If the article already has citations (like `[^1]`), verify those URLs are live and match the claimed content
