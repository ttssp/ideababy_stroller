---
description: Start Stage 1 Round 1 of the three-stage debate. Opus takes the POSITIVE pole (what would make this spectacular). Must run ≥5 web searches.
argument-hint: "<idea-number> (e.g. 001)"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Bash(date:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Debate · Stage 1 Round 1 (Opus · POSITIVE pole)

You are Opus 4.7 Max, Debater A. Idea **$ARGUMENTS**. This is the first round of
a three-stage debate. Your pole in S1R1 is **POSITIVE**: steelman the opportunity.
GPT-5.4 takes the NEGATIVE pole in parallel — you do not read theirs yet.

## Setup
```
mkdir -p discussion/$ARGUMENTS
test -f discussion/PROTOCOL.md && cp discussion/PROTOCOL.md discussion/$ARGUMENTS/PROTOCOL.md
```

## Read (in this order)
1. `proposals/proposals.md` — find entry `**$ARGUMENTS**`
2. `.claude/skills/debate-protocol/SKILL.md` (or `discussion/$ARGUMENTS/PROTOCOL.md`)
3. `CLAUDE.md`

**DO NOT** read any `discussion/$ARGUMENTS/$ARGUMENTS-GPT*.md` file. S1R1 must be independent.
Verify with `ls discussion/$ARGUMENTS/`; if GPT files exist, refuse to open them.

## Mandatory: run ≥5 web searches
Use the WebSearch tool. Query intents (run at least one of each):
- "is there an existing product that does X" (prior art)
- "company Y shut down / acquired / pivoted" (failure cases, if obvious candidates exist)
- "users complaining about X" (demand signals, Reddit, HN, SO)
- academic / industry literature on the domain
- market size / TAM / adjacent trends

Log every query in the output under §2.

## Write S1R1

Target: `discussion/$ARGUMENTS/$ARGUMENTS-Opus47Max-S1R1.md`

Template:
```markdown
# Idea $ARGUMENTS · S1R1 · Opus 4.7 Max · Pole: POSITIVE

**Timestamp**: <from `date -u +"%Y-%m-%dT%H:%M:%SZ"`>
**Visibility**: I did NOT read the GPT S1R1.

## 1. Idea restated in my own words (2–3 paragraphs)

## 2. Searches I ran (≥5; query → 1-line finding, with URL)
- q: "..." → <finding> · <url>
- ...

## 3. Prior art discovered
For each: name, status (live/dead/pivoted), 1-line what-it-does, 1-line why-it-matters-to-us.

## 4. Evidence for POSITIVE pole (with citations)
Why this could be a 10x opportunity given the evidence. Be specific: market gap,
mis-served users, tech-enablers that didn't exist before, etc.

## 5. Signals that would flip my pole to negative
Specific things that, if true, would change my mind.

## 6. Open questions only more search can answer

## 7. Self-critique
"If I had to argue the NEGATIVE pole, my strongest argument would be: ..."
```

## Style
- 200–500 lines
- Numbers > adjectives, with citations
- Quote ≤15 words; paraphrase + URL otherwise
- Be genuinely bullish — this is your pole — but evidence-grounded

## After writing
`ls -la discussion/$ARGUMENTS/` to confirm file. Tell the human:
"S1R1 written (pole: POSITIVE). Now launch Codex S1R1 (NEGATIVE pole) in a separate terminal.
The Codex kickoff prompt is in PROTOCOL.md §'Codex-side kickoffs'."
