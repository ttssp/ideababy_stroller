// ──────────────────────────────────────────────────────────
// Skeleton for src/lib/llm/anthropic.ts
// Source task: T004 (adapter interface) + T013 (summary pass integration)
// Owner: T004 implementation PR (blocked on T001 spike sign-off)
// How to use: cp this file to src/lib/llm/anthropic.ts and replace each
// TODO with the full implementation from
//   specs/001-pA/reference/llm-adapter-skeleton.md §3
// The full skeleton in that file is ~80 lines of real logic; this stub
// compiles cleanly so downstream tasks (T007 provider select, T013 persist)
// are not blocked while T001 spike is still pending.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/llm-adapter-skeleton.md §3 (full implementation)
//   - specs/001-pA/reference/llm-adapter-skeleton.md §3.5 (truncateTo3Sentences util)
//   - specs/001-pA/tech-stack.md §2.4 (interface contract)
//   - specs/001-pA/spec.md D10 / D15 (≤ 3 sentences red line 2)
//
// Shared helper skeleton:
//   - reference/skeletons/llm-utils.ts → cp to src/lib/llm/utils.ts
//   - import below resolves once that file is in place.

import Anthropic from '@anthropic-ai/sdk';
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

export class AnthropicProvider implements LLMProvider {
  readonly name: LLMProviderName = 'anthropic';

  private readonly client: Anthropic;
  private readonly model: string;

  constructor() {
    this.client = new Anthropic({
      apiKey: env.ANTHROPIC_API_KEY,
      // SDK default 600s is too long for a worker; 30s aligns with
      // reference/llm-adapter-skeleton.md §3.
      timeout: 30_000,
    });
    this.model = env.ANTHROPIC_MODEL;
  }

  async summarize(_input: SummarizeInput): Promise<SummaryRecord> {
    // TODO(T004): Implement per reference/llm-adapter-skeleton.md §3.
    //   1. Render system + user prompts via renderSummarizeUser (prompt-version.ts).
    //   2. Call this.client.messages.create with max_tokens=256, temperature=0.2.
    //   3. extractText → truncateTo3Sentences.
    //   4. Build SummaryRecord {summaryText, promptVersion, modelName: this.model,
    //      inputTokens: resp.usage.input_tokens, outputTokens: resp.usage.output_tokens,
    //      latencyMs, truncated, requestHash}.
    //   5. Wrap any thrown error in LLMProviderError (retryable if 5xx or 429).
    //   6. NEVER log the prompt or response body (SEC-4).
    throw new LLMProviderError('summarize not implemented', this.name, false);
  }

  async judgeRelation(_input: JudgeRelationInput): Promise<JudgeRelationResult> {
    // TODO(T004): Implement per reference/llm-adapter-skeleton.md §3.
    //   1. Render judge prompts via renderJudgeUser.
    //   2. Call this.client.messages.create with max_tokens=512, temperature=0.1.
    //   3. Extract text → extractJSON (strip ```json fences).
    //   4. Parse via VerdictSchema (zod discriminatedUnion).
    //   5. **Confidence floor** (§10 layer 3 · prevent confidence-inflation
    //      injection). Insert this literal block after VerdictSchema.parse:
    //
    //        const verdict: StateShiftVerdict =
    //          parsed.kind === 'shift' && parsed.confidence < 0.5
    //            ? { kind: 'incremental', confidence: parsed.confidence }
    //            : parsed;
    //
    //   6. Build JudgeRelationResult (use `verdict` not `parsed`) and return.
    //   7. Map zod/SyntaxError to retryable LLMProviderError; APIError per status.
    throw new LLMProviderError('judgeRelation not implemented', this.name, false);
  }
}

// --------------------------------------------------------------------
// Cost helper · also exported for T013 persistSummary
// --------------------------------------------------------------------

/**
 * Per 2026-04 Anthropic Sonnet 4.6 pricing:
 *   input  $3/M token
 *   output $15/M token
 * Returns cents (integer) for `llm_calls.cost_cents`.
 * See reference/llm-adapter-skeleton.md §3 for the authoritative formula.
 */
export function calcCostAnthropicCents(inputTokens: number, outputTokens: number): number {
  const inputRate = 300 / 1_000_000; // cents per token
  const outputRate = 1_500 / 1_000_000;
  return Math.round(inputTokens * inputRate + outputTokens * outputRate);
}
