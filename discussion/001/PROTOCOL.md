# Debate Protocol — v2.0 (pointer)

**Authoritative version**: `.claude/skills/debate-protocol/SKILL.md`.
This file is copied into each `discussion/NNN/` folder at debate start, giving
the debaters local access without reaching into `.claude/`.

## Three-stage structure (summary)

| Stage | Name | Purpose | Posture | Min sources/round |
|---|---|---|---|---|
| 1 | Explore | Diverge, find prior art, switch poles R2 | Opposing | 5 |
| 2 | Position | Converge on evidence, produce direction menu | Cooperative | 2 |
| 3 | Converge | Architecture & MVP (only if moderator approves) | Engineering | 0 |

**Between stages**: moderator decides. Options at end of Stage 2:
- **Advance** — pick a direction, enter Stage 3
- **Fork** — split into sub-debates (new proposals NNNa, NNNb)
- **Park** — archive for later
- **Abandon** — evidence says don't build; write lesson

## Pole assignments (Stage 1 only)

- S1R1: Opus = POSITIVE, GPT = NEGATIVE (independent, don't read each other)
- S1R2: **switch** — Opus = NEGATIVE, GPT = POSITIVE (must steelman genuinely)
- S1R3+: moderator-directed or whichever pole the debater was weaker on

## File naming

```
NNN-<Model>-S<stage>R<round>.md         # round files
NNN-moderator-notes.md                   # appended anytime
NNN-stage1-synthesis.md                  # auto, at S1→S2
NNN-stage2-checkpoint.md                 # auto, at S2→S3 (moderator decision gate)
NNN-<Model>-final.md                     # after Stage 3 (or S2 if advancing directly)
```

## Style mandates

- Numbers > adjectives, with citations
- Quote ≤15 words verbatim, paraphrase + URL otherwise
- No authority fallacy (evidence, not "X does this")
- Stage 1: be willing to be wrong. Stage 2: converge on what survived. Stage 3: engineer.
- Concessions required in every round from S1R2 onward
- No sycophancy

## Codex-side kickoff prompts

See full templates in `.claude/skills/debate-protocol/SKILL.md` §"Codex-side kickoffs".

Copy-paste helpers for each stage, in order:
- S1R1 (GPT = NEGATIVE)
- S1R2 (GPT = POSITIVE, switched)
- S2R1 (cooperative)
- S3R1 (engineering; only after moderator Advance)
- Finals

## Quality bars for stage advancement

**S1 → S2**: ≥2 rounds/side · poles switched at least once · ≥10 unique source URLs across S1
**S2 → S3**: ≥1 round/side with direction menu · moderator explicitly picked a direction
**S3 → Finals**: ≥3 resolved disagreements · ≥5 beyond-proposal consensus points · ≥2 "what the other caught" items per side

## Moderator injection

Append to `NNN-moderator-notes.md`:
```markdown
## Injection @ <stage-round-tag>
**Type**: Hard constraint | Soft guidance
**Binding on**: Opus | GPT | Both
<the note>
```

Both sides must respond in their next round under `## Moderator injection response`.
