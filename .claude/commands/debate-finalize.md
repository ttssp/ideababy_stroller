---
description: Write Opus's final standalone position on an idea, consolidating all rounds
argument-hint: "<idea-number>  (e.g. 001)"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Glob, Grep
model: opus
---

# Debate Finalization — Opus Side

Idea **$ARGUMENTS**. You are writing your **final position document**.

## Step 1 — Full read
Read every file in `discussion/$ARGUMENTS/`:
- Protocol
- All your own rounds
- All GPT rounds
- Moderator notes

Use `ls discussion/$ARGUMENTS/ | sort`.

## Step 2 — Write your final standalone position

Target: `discussion/$ARGUMENTS/$ARGUMENTS-Opus47Max-final.md`.
This document must stand on its own — a reader who skipped the debate should understand
your final view from this single file.

Structure:

```markdown
# Idea $ARGUMENTS · Opus · Final Position

## 1. My final recommendation (TL;DR, 5 bullets max)
The cleanest possible statement of what I'd build and how.

## 2. Full technical proposal
Architecture, stack, data model, key modules, deployment, observability.
Pinned versions where it matters. Diagrams via Mermaid if they save words.

## 3. MVP plan
### 3.1 Phase 0 — Proof of concept (days)
### 3.2 Phase 1 — v0.1 shippable (weeks)
### 3.3 Phase 2 — v1.0 commercial (weeks/months)

## 4. Consensus with GPT
Points where we genuinely agreed by the end. Be strict — "we both mentioned X" is
not consensus; "we both committed to X as the way forward" is.

## 5. Residual disagreements
Where we still differ. For each:
- What they think
- What I think
- My honest view on which of us is more likely right, and why
- What experiment would settle it

## 6. Where GPT was stronger than me
Intellectual honesty. Name ≥2 things where their framing or catch was better than mine.

## 7. Where I was stronger than GPT
Name ≥2 things you caught that they didn't, and why it matters.

## 8. Top 5 actionable recommendations for the moderator (operator)
Concrete, prioritized. Each with:
- Recommendation
- Why
- Effort estimate
- Risk if skipped

## 9. What I would want to know before shipping
3–5 open questions the moderator must still answer (interviews, metrics, legal).

## 10. Signing off
"I believe this proposal is ready for SDD conversion." OR
"I believe another round would materially change my recommendation, because: ..."
```

## Style
- No new speculative ideas — this document consolidates, it doesn't extend.
- Every recommendation must be traceable to a specific round or consensus point.

## After writing
Tell the human: "Opus final written. Ask Codex to write its final via their equivalent
command. Then `/debate-conclude $ARGUMENTS`."
