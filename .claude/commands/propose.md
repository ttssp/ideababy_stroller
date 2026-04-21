---
description: Interactively capture a new idea into proposals.md using AskUserQuestion
argument-hint: "(optional) <short-title>"
allowed-tools: Read, Edit, Write, Bash(date:*), Bash(grep:*), AskUserQuestion
model: sonnet
---

# Propose a New Idea

You help the human draft a new proposal entry in `proposals/proposals.md`.

## Step 1 — Find the next number

Read `proposals/proposals.md`. Find the highest existing entry number (e.g. `**007**`).
The new entry will be `**008**` (zero-padded to 3 digits).

If the file doesn't exist, create it with a `# Proposals` header and start at `**001**`.

## Step 2 — Interview the human

Use the **AskUserQuestion** tool to gather these fields, one or two at a time.
Do not ask more than 3 at once; wait for answers before next batch.

**Batch 1 — essentials:**
1. One-sentence title (free text)
2. Ambition level:
   - XL: platform-scale (IM, protocol, full iOS app)
   - L: full SaaS product
   - M: single-purpose tool / utility
   - S: script / one-off

**Batch 2 — motivation:**
3. Why now? (free text, 2–4 sentences)
4. Who is the target user? (free text)

**Batch 3 — constraints:**
5. Budget ceiling (Dev infra / month)
   - Under $50
   - $50–500
   - $500–2000
   - No cap yet
6. Platform preference:
   - Web only
   - iOS + Web
   - Cross-platform mobile
   - CLI / terminal
   - Backend / service only
   - Undecided

**Batch 4 — open questions:**
7. "What are 3 things you're uncertain about?" (free text — used to seed the debate)

## Step 3 — Write the proposal block

Append to `proposals/proposals.md`:

```markdown

---

## **$NEXT_NUM**: <title>

**提出日期**: $TODAY (UTC)
**状态**: draft
**初始野心等级**: <XL/L/M/S>

### 动机 (Why)
<answer to q3>

### 目标用户 (Who)
<answer to q4>

### 核心想法 (What)
<one-paragraph rewording of the title that the human can correct>

### 初始约束 (Constraints)
- 预算: <answer to q5>
- 平台: <answer to q6>

### 已知未知 (Open Questions)
- <open question 1>
- <open question 2>
- <open question 3>

### 期望产出
<one-line; ask the human if not given>
```

## Step 4 — Preview and confirm

Show the human the appended block and ask:
> "Review. Should I commit this, or let's edit?"

If they want edits, iterate. Once confirmed, stop (don't run git yourself).

## Step 5 — Next-step guidance

Print:
> "Proposal **$NEXT_NUM** recorded. When you're ready to debate it, open a Claude Code
> session in this repo and run:
>   `/debate-start $NEXT_NUM`
> Then open a Codex terminal and paste the debate kickoff prompt from
> `discussion/PROTOCOL.md` §Codex R1 template."
