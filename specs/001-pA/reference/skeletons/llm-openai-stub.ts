// ──────────────────────────────────────────────────────────
// Skeleton for src/lib/llm/openai.ts
// Source task: T004 (adapter interface) + T013 (summary pass integration)
// Owner: T004 implementation PR (blocked on T001 spike sign-off)
// How to use: cp this file to src/lib/llm/openai.ts and replace each
// TODO with the full implementation from
//   specs/001-pA/reference/llm-adapter-skeleton.md §4
// Structure is symmetric with anthropic.ts; only SDK shape and token
// field naming differ.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/llm-adapter-skeleton.md §4 (full implementation)
//   - specs/001-pA/reference/llm-adapter-skeleton.md §3.5 (truncateTo3Sentences util · shared)
//   - specs/001-pA/tech-stack.md §2.4 (interface contract)
//   - specs/001-pA/spec.md D10 / D15 (≤ 3 sentences red line 2)
//
// Shared helper skeleton:
//   - reference/skeletons/llm-utils.ts → cp to src/lib/llm/utils.ts
//   - import below resolves once that file is in place.

import OpenAI from 'openai';
import { env } from '@/lib/env.js';
import { truncateTo3Sentences } from './utils.js';
import type {
  JudgeRelationInput,
  JudgeRelationResult,
  LLMProvider,
  LLMProviderName,
  SummarizeInput,
  SummaryRecord,
} from './types.js';
import { LLMProviderError } from './types.js';

export class OpenAIProvider implements LLMProvider {
  readonly name: LLMProviderName = 'openai';

  private readonly client: OpenAI;
  private readonly model: string;

  constructor() {
    this.client = new OpenAI({
      apiKey: env.OPENAI_API_KEY,
      timeout: 30_000,
    });
    this.model = env.OPENAI_MODEL;
  }

  async summarize(_input: SummarizeInput): Promise<SummaryRecord> {
    // TODO(T004): Implement per reference/llm-adapter-skeleton.md §4.
    //   1. Render system + user prompts via renderSummarizeUser.
    //   2. Call this.client.chat.completions.create with max_tokens=256, temperature=0.2.
    //   3. extractText → truncateTo3Sentences.
    //   4. Build SummaryRecord using resp.usage.prompt_tokens / completion_tokens
    //      (NOT input_tokens / output_tokens — that is Anthropic's naming).
    //   5. Throw LLMProviderError on missing usage (retryable=true).
    //   6. Wrap OpenAI.APIError with retryable logic: 5xx or 429.
    throw new LLMProviderError('summarize not implemented', this.name, false);
  }

  async judgeRelation(_input: JudgeRelationInput): Promise<JudgeRelationResult> {
    // TODO(T004): Implement per reference/llm-adapter-skeleton.md §4.
    //   1. Render judge prompts.
    //   2. Call chat.completions.create with response_format {type:'json_object'}.
    //   3. Parse text as JSON directly (no fence stripping needed with json_object).
    //   4. Validate via VerdictSchema (discriminatedUnion).
    //   5. **Confidence floor** (§10 layer 3 · prevent confidence-inflation
    //      injection). Insert this literal block after VerdictSchema.parse:
    //
    //        const verdict: StateShiftVerdict =
    //          parsed.kind === 'shift' && parsed.confidence < 0.5
    //            ? { kind: 'incremental', confidence: parsed.confidence }
    //            : parsed;
    //
    //   6. Build JudgeRelationResult (use `verdict` not `parsed`).
    //   7. Map zod/SyntaxError/APIError to LLMProviderError.
    throw new LLMProviderError('judgeRelation not implemented', this.name, false);
  }
}

// --------------------------------------------------------------------
// Cost helper · also exported for T013 persistSummary
// --------------------------------------------------------------------

/**
 * Per 2026-04 R1-refreshed OpenAI GPT-5.4 pricing:
 *   input  $2.50/M token
 *   output $15.00/M token
 * Returns cents (integer) for `llm_calls.cost_cents`.
 * See reference/llm-adapter-skeleton.md §4 for the authoritative formula.
 */
export function calcCostOpenAICents(inputTokens: number, outputTokens: number): number {
  const inputRate = 250 / 1_000_000; // cents per token
  const outputRate = 1_500 / 1_000_000;
  return Math.round(inputTokens * inputRate + outputTokens * outputRate);
}
