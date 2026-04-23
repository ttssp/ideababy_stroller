---
description: Start L2 Explore phase for a forked direction (or directly if /inspire was skipped). Opus writes L2R1 — deep unpacking of the idea, no search, no tech/feasibility content.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a  or  001"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ln:*), Bash(ls:*), Bash(date:*), Glob, Grep
model: opus
---

# Explore · L2R1 (Opus side)

Idea **$ARGUMENTS** (may be a fork id like `001a` or a root id like `001`).

## Step 1 — locate the target

If `$ARGUMENTS` is a fork id (e.g. `001a`):
- Path: `discussion/<root>/<fork-id>/`
- Verify `FORK-ORIGIN.md` exists; if not, this fork wasn't properly created. Stop.

If `$ARGUMENTS` is a root idea (e.g. `001`):
- Detect whether L1 was run:
  - If `discussion/001/L1/stage-L1-inspire.md` exists, L1 was run but human is skipping the menu. OK.
  - If `discussion/001/L1/` doesn't exist, L1 was skipped via `--mode=skip`. OK.
  - If L1 is mid-run (R1 done, R2 not), stop and tell human:
    > "L1 is in progress. Either complete it (/inspire-next 001), advance it
    > (/inspire-advance 001), or explicitly skip with /explore-start 001 --skip-l1"

## Step 2 — setup

```bash
mkdir -p discussion/.../<target>/L2
```

(Path = `discussion/<root>/<fork-id>/L2/` if forked, or `discussion/<root>/L2/` if root direct)

Copy protocol:
```bash
cp .claude/skills/explore-protocol/SKILL.md discussion/.../<target>/L2/PROTOCOL.md
```

## Step 3 — detect skip-mode

Skip-mode is true if:
- This is a root idea AND no L1 stage file exists (human used `--mode=skip` at inspire-start)

If skip-mode → Opus's L2R1 must include §0 "Alternative framings considered".

## Step 4 — write Opus's L2R1

**HARD CONSTRAINTS**:
1. NO web search this round
2. DO NOT read GPT's L2R1
3. NO tech / architecture / cost / feasibility content

Read:
- `proposals/proposals.md` entry for the root idea
- If forked: `discussion/<root>/<fork-id>/FORK-ORIGIN.md` AND the relevant L1
  menu candidate description from `stage-L1-inspire.md`
- `.claude/skills/explore-protocol/SKILL.md`
- `CLAUDE.md`

Write `discussion/.../<target>/L2/L2R1-Opus47Max.md` using the L2R1 template:
- §0 (skip-mode only): Alternative framings considered, 3-4 paragraphs
- §1 The idea, unpacked (4-8 paragraphs — heart of the round)
- §2 What's genuinely novel
- §3 Utility — 3 concrete usage scenarios
- §4 Natural extensions
- §5 Natural limits
- §6 Three honest questions about this idea (these seed L2R2 search)

Length: 700-1300 words. Specific > abstract.

## Step 5 — write Codex inbox task

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`.

Write `.codex-inbox/<TS>-<target>-L2R1.md`:

```markdown
# Codex Task · <target> · L2R1 (Explore R1)

**Created**: <ISO>
**Skip-mode**: <true|false>
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~6-12k

## Your role
You are GPT-5.4 xhigh, Debater B, L2R1 on idea <target>. Deep unpack the idea —
its value, novelty, utility, extensions, limits. No tech/feasibility yet.

## HARD CONSTRAINTS
- NO web search this round
- DO NOT read discussion/.../L2/L2R1-Opus47Max.md (parallel independence)
- NO tech/architecture/cost/feasibility content

## Read in order
- proposals/proposals.md (entry for root idea)
- if forked: discussion/<root>/<fork-id>/FORK-ORIGIN.md AND the relevant
  candidate in discussion/<root>/L1/stage-L1-inspire.md
- .claude/skills/explore-protocol/SKILL.md
- AGENTS.md

## Write
discussion/.../<target>/L2/L2R1-GPT54xHigh.md using the L2R1 template:
- §0 (only if skip-mode is true)
- §1 The idea, unpacked (heart of the round, 4-8 paragraphs)
- §2 Novelty
- §3 Utility (3 concrete scenarios)
- §4 Natural extensions
- §5 Natural limits
- §6 Three honest questions

700-1300 words. Specific > abstract.

## When done
Write .codex-outbox/<TS>-<target>-L2R1.md with:
- Files written + word count
- Headline: in 1 sentence, what the idea actually is after your unpacking
- Top novelty claim and top limit you identified
- Anything Claude Code should know
```

Update symlink:
```bash
cd .codex-inbox && ln -sf <TS>-<target>-L2R1.md latest.md
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L2R1 Opus side done.
File: discussion/.../<target>/L2/L2R1-Opus47Max.md (<word-count> words)
<if skip-mode: "Skip mode — included §0 alternative framings">

In one sentence, what I now see this idea as:
"<sharpened reading from §1>"

Top novelty: <from §2>
Top limit: <from §5>

📋 Next step: get Codex's L2R1.

[1] Codex inbox is ready (recommended)
    → in your Codex terminal:  cdx-run

[2] I want to inject a steering note before Codex starts
    → tell me what to add (will go to L2/moderator-notes.md)

[3] Show full Codex kickoff for manual paste
    → I'll display .codex-inbox/latest.md

[4] Show me Opus's L2R1 first
    → I'll display the file

[5] Cancel — I want to revise something upstream
    → tell me what

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```
