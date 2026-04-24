// ──────────────────────────────────────────────────────────
// Skeleton for src/lib/llm/utils.ts
// Source task: T004 (adapter interface) — shared helper consumed
//   by both src/lib/llm/anthropic.ts and src/lib/llm/openai.ts.
// Owner: T004 implementation PR (blocked on T001 spike sign-off)
// How to use: cp this file to src/lib/llm/utils.ts verbatim.
//   The function body is the authoritative implementation for
//   RED LINE 2 application-layer defense (≤ 3 sentences) and is
//   referenced from reference/llm-adapter-skeleton.md §3.5.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/llm-adapter-skeleton.md §3.5 (design rationale)
//   - specs/001-pA/spec.md D10 / D15 (≤ 3 sentences red line 2)
//   - specs/001-pA/reference/schema.sql paper_summaries.summary_sentence_cap
//     (DB CHECK · last-line defense; uses regexp_matches terminator-count
//      strategy · 2026-04-24 G1 fix · app layer below is the layer-4 defense
//      per llm-adapter-skeleton.md §10)
//
// G1 fix (R_final B1 · 2026-04-24):
//   - Previous implementation split on `(?<=[.!?。！？])\s+`, silently
//     collapsing pure-Chinese text (no whitespace) into a single segment
//     and letting 5-sentence Chinese inputs pass the ≤ 3 check.
//   - New strategy: capture "chunk ending with terminator" using
//     `/[^.!?。！？]+[.!?。！？]+/g`, which works regardless of whitespace.
//     Defensive: if the LLM returns trailing text without a terminator,
//     the residual is appended as one sentence with `。` to prevent DB
//     CHECK rejection at INSERT time (adapter invariant is "always
//     terminated before persist").
//
// Test references:
//   - specs/001-pA/reference/testing-strategy.md §2.4 (required cases:
//     pure Chinese 3/5-sentence, English, mixed, no terminator, single,
//     whitespace-less boundaries).

/**
 * Split on English (.!?) and Chinese (。！？) sentence terminators,
 * return joined string of first ≤ 3 sentences + boolean flag.
 *
 * Guarantees (adapter invariant before INSERT into paper_summaries):
 *   1. Return value satisfies DB CHECK `summary_sentence_cap`
 *      (1..3 terminator matches).
 *   2. Empty input returns empty string (caller should treat as
 *      "LLM returned nothing" and skip persist).
 *   3. Unterminated input is defensively terminated with `。` so
 *      `summary_sentence_cap` (which now rejects 0 terminators)
 *      does not reject otherwise-valid LLM output.
 *
 * @param text raw LLM response (may be empty, may be N sentences)
 * @returns `{ text, truncated }` where `truncated = true` iff input
 *   had more than 3 sentences and the returned text is the first 3 only.
 */
export function truncateTo3Sentences(text: string): { text: string; truncated: boolean } {
  const trimmed = text.trim();
  if (!trimmed) return { text: '', truncated: false };
  // Capture each "chunk ending with terminator". Works whether chunks
  // have whitespace between them or not (pure Chinese has none).
  const matches = trimmed.match(/[^.!?。！？]+[.!?。！？]+/g) ?? [];
  const lastTerminated = matches.join('');
  const residual = trimmed.slice(lastTerminated.length).trim();
  // Defensive terminator append: DB CHECK now rejects 0 terminators,
  // so if the LLM omits a trailing period we add `。` to preserve the
  // LLM's content without triggering DB reject.
  const sentences = residual.length > 0 ? [...matches, `${residual}。`] : matches;
  if (sentences.length === 0) {
    // Edge case: input was only whitespace-and-punctuation (theoretically
    // unreachable after trim()); normalize to empty to signal "nothing".
    return { text: '', truncated: false };
  }
  if (sentences.length <= 3) return { text: sentences.join('').trim(), truncated: false };
  return { text: sentences.slice(0, 3).join('').trim(), truncated: true };
}
