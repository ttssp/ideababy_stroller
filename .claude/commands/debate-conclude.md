---
description: [DEPRECATED v3.0 — use /inspire-start → /explore-start → /scope-start → /plan-start instead] Synthesize the entire debate into a single conclusion document
argument-hint: "<idea-number>  (e.g. 001)"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Glob, Grep, Agent(conclusion-synthesizer)
model: opus
---

# Conclude Debate — Synthesize

Idea **$ARGUMENTS**. Fold the full debate into a single decision document.

## Precondition check

Before synthesizing, verify:
1. Both `$ARGUMENTS-Opus47Max-final.md` and `$ARGUMENTS-GPT55xHigh-final.md` exist.
2. If either is missing, **stop** and tell the human which one to produce first.

Run: !`ls discussion/$ARGUMENTS/*-final.md 2>/dev/null || echo "MISSING"`

## Delegation

Delegate this task to the **`conclusion-synthesizer`** subagent, which runs in its own
context window so the main session stays clean:

> "Use the conclusion-synthesizer subagent to produce the conclusion for idea $ARGUMENTS.
> Pass it the full path to `discussion/$ARGUMENTS/` and the target output path
> `conc/$ARGUMENTS-Opus47Max-GPT55xHigh-byOpus47Max-<YYMMDD>.md` where YYMMDD is today's
> date (UTC, 6-digit, e.g. 260421)."

The subagent will read the whole folder and produce the conclusion file per the template
defined in its system prompt.

## Post-processing (main thread)

After the subagent returns, you must:

1. **Read** the conclusion it produced.
2. **Sanity-check** for four failure modes:
   - False consensus (claiming agreement where the finals actually disagreed) → fix
   - Missing disagreements (finals disagreed but conclusion is silent) → fix
   - Vague next steps (no file paths, no commands) → fix
   - More than 15 consecutive words quoted from any round → rewrite as paraphrase
3. **Insert** a `## Moderator Checkpoint` section at the top containing three questions
   for the human to verify before spec work begins.
4. **Commit-safe**: save, then tell the human the path and ask for review.

## Output
One line: `Conclusion written to conc/<filename>.md — review before spec kick-off.`
