---
description: Run L3R2 (Opus side) — read opponent's L3R1, run scope-reality searches (what similar products include/exclude at v0.1), produce refined candidates + identify the one biggest tradeoff human must decide.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Bash(ln:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Scope · L3R2 (Opus side)

Idea **$ARGUMENTS**.

## Step 1 — preconditions

```bash
ls discussion/.../<target>/L3/L3R1-*.md
```

Need both `L3R1-Opus47Max.md` and `L3R1-GPT54xHigh.md`.
Need `L3R0-intake.md`.
If any missing, stop and tell human (`/status <target>`).

## Step 2 — read in order

1. `.claude/skills/scope-protocol/SKILL.md` (L3R2 template)
2. `discussion/.../<target>/L3/moderator-notes.md` (if exists; binding)
3. `discussion/.../<target>/L3/L3R0-intake.md` (re-check hard constraints)
4. `discussion/.../<target>/L3/L3R1-GPT54xHigh.md` (opponent, all sections)
5. `discussion/.../<target>/L3/L3R1-Opus47Max.md` (self)
6. `discussion/.../<target>/L2/stage-L2-explore-<target>.md` (context)

## Step 3 — scope-reality searches

**Allowed**:
- "What do products in [category] typically include at v0.1 / launch?"
- "What's the minimum viable feature set for [category] users?"
- "What did [similar product] ship first vs add later?"
- "What features does [similar product] NOT have and users don't miss?"

**Forbidden** (L4 territory):
- Tech stack queries
- Architecture queries
- Specific library / framework comparisons
- Pricing/cost of tools

Run **≥3** scope-reality searches. Cite URLs. ≤15 word quotes.

## Step 4 — write Opus's L3R2

Target: `discussion/.../<target>/L3/L3R2-Opus47Max.md`

Use L3R2 template:
- §1 From opponent's candidates — what sharpened my thinking
- §2 Scope-reality searches (table with URLs)
- §3 Refined candidates (2-3, each with full structure — sharpened from R1)
- §4 **The single biggest tradeoff** human must decide (name the axis)
- §5 What I'm less sure about now than in R1

Length: 600-1000 words. Heavy on §2, §3, §4.

## Step 5 — write Codex inbox task

Compute timestamp.

Write `.codex-inbox/<TS>-<target>-L3R2.md`:

```markdown
# Codex Task · <target> · L3R2

**Created**: <ISO>
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~8-14k

## Your role
You are GPT-5.4 xhigh, L3R2 on idea <target>. Read opponent's candidates,
search scope-reality, refine candidates, identify the key tradeoff axis.

## CONSTRAINTS
- SCOPE-REALITY SEARCH ONLY:
    Allowed: "what do similar products include/cut at v0.1"
    Forbidden: tech stack / architecture / specific implementations
- Quote ≤15 words verbatim

## Read in order
- .claude/skills/scope-protocol/SKILL.md
- discussion/.../<target>/L3/moderator-notes.md (if exists; binding)
- discussion/.../<target>/L3/L3R0-intake.md
- discussion/.../<target>/L3/L3R1-Opus47Max.md (opponent)
- your own L3R1
- discussion/.../<target>/L2/stage-L2-explore-<target>.md (context)

## Search
≥3 scope-reality queries. Cite URLs.

## Write
discussion/.../<target>/L3/L3R2-GPT54xHigh.md using the L3R2 template:
- §1 What sharpened from opponent
- §2 Scope-reality search (table)
- §3 Refined candidates (2-3)
- §4 Single biggest tradeoff axis
- §5 What I'm less sure about now

600-1000 words.

## When done
Write .codex-outbox/<TS>-<target>-L3R2.md with:
- Files written + word count
- Each refined candidate headline
- What the key tradeoff axis is (§4)
- Notable scope-reality findings
- Anything Claude Code should know
```

Update symlink:
```bash
cd .codex-inbox && ln -sf <TS>-<target>-L3R2.md latest.md
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L3R2 Opus side done.
File: discussion/.../<target>/L3/L3R2-Opus47Max.md (<n> words)
Scope-reality searches: <n> queries across <k> sources

Opus's key tradeoff axis (§4): <one line>
Refined candidates: <count> (down from/up from L3R1)

📋 Next step:

[1] Run Codex L3R2 (recommended)
    → in your Codex terminal:  cdx-run

[2] Show Codex kickoff for manual paste
    → I'll display .codex-inbox/latest.md

[3] Show me Opus L3R2 first
    → I'll show the file

[4] Inject a moderator note before Codex
    → tell me what to add

[5] Skip Codex L3R2 and synthesize what we have
    → /scope-advance <target>  (will note Codex L3R2 missing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```
