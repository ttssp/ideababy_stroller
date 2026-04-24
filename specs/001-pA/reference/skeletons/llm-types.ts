// ──────────────────────────────────────────────────────────
// Skeleton for src/lib/llm/types.ts
// Source task: T004 (LLM adapter interface)
// Owner: T004 implementation PR
// How to use: cp this file to src/lib/llm/types.ts. Zero runtime logic —
// this is the type contract shared by anthropic.ts / openai.ts / persist.ts.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/llm-adapter-skeleton.md §2 (this file verbatim)
//   - specs/001-pA/tech-stack.md §2.4 (camelCase convention)
//   - specs/001-pA/architecture.md ADR-4 (hot-swap) · ADR-6 (audit separation)
//   - specs/001-pA/spec.md D10 / D15 / D16

/** Env-selectable provider identifier. Also the prefix of `paper_summaries.model_name`. */
export type LLMProviderName = 'anthropic' | 'openai';

/** State-shift judgement labels; see spec.md §4.1 provisional definition. */
export type RelationLabel = 'shift' | 'incremental' | 'unrelated';

// --------------------------------------------------------------------
// Input shapes · adapter's pure-function params (adapter does NOT touch DB)
// --------------------------------------------------------------------

export interface PaperInput {
  /** arXiv ID (e.g. '2404.12345') · only used for audit hash, never in prompts. */
  readonly arxivId: string;
  readonly title: string;
  readonly abstract: string;
  /** Author list · audit only · NOT passed into prompts (SEC-4). */
  readonly authors: readonly string[];
  readonly categories: readonly string[];
  readonly publishedAt: Date;
}

export interface TopicInput {
  readonly id: number;
  readonly name: string;
  readonly keywords: readonly string[];
}

export interface SummarizeInput {
  readonly paper: PaperInput;
  readonly topic: TopicInput;
}

export interface JudgeRelationInput {
  readonly candidatePaper: PaperInput;
  readonly earlierAnchor: PaperInput;
  readonly topic: TopicInput;
}

// --------------------------------------------------------------------
// Output shapes · caller persists these
// --------------------------------------------------------------------

/**
 * R1 B1 output contract. Caller (T013 `persistSummary`) inside a transaction:
 *   1) INSERT `llm_calls(provider, purpose='summarize', input_tokens, ...)` RETURNING id
 *   2) INSERT `paper_summaries(paper_id, topic_id, summary_text, llm_call_id, model_name, prompt_version)`
 *      ON CONFLICT (paper_id, topic_id, prompt_version) DO UPDATE (upsert for worker re-run idempotency)
 *
 * Adapter does NOT write these tables (kept pure + mockable).
 */
export interface SummaryRecord {
  /** ≤ 3 sentences (adapter's `truncateTo3Sentences` has enforced this).
   *  DB CHECK `summary_sentence_cap` is the final safety net. */
  readonly summaryText: string;
  /** e.g. 'v1.0-2026-04'; from `getCurrentPromptVersion('summarize')`. */
  readonly promptVersion: string;
  /** adapter `.name`; e.g. 'claude-sonnet-4-6' or 'gpt-5.4'.
   *  Fallback path uses 'fallback-heuristic-v1'. */
  readonly modelName: string;
  /** For `llm_calls` INSERT and monthly cost accumulation (C11). */
  readonly inputTokens: number;
  readonly outputTokens: number;
  /** Call latency (audit + SLA §1.1 p95 observation). */
  readonly latencyMs: number;
  /** True if the raw response had > 3 sentences and was truncated (audit). */
  readonly truncated: boolean;
  /** SHA-256(promptVersion + arxivId + topicId) hex · for `llm_calls.request_hash` dedup. */
  readonly requestHash: string;
}

/**
 * State-shift verdict · discriminated union.
 *   - `shift`: candidate materially changes field understanding vs anchor;
 *              confidence must be ≥ 0.5 (adapter auto-downgrades below that)
 *   - `incremental`: candidate advances but does not alter anchor's conclusion
 *   - `unrelated`: candidate does not engage with anchor's claim
 *
 * `anchorPaperId` is the DB id of the anchor (not arxivId) — adapter echoes
 * it verbatim so caller can round-trip to `briefings.anchor_paper_id`.
 */
export type StateShiftVerdict =
  | {
      readonly kind: 'shift';
      readonly rationale: string; // 10–500 chars; concrete (e.g. "anchor assumed X, candidate shows ¬X")
      readonly anchorPaperId: number;
      readonly confidence: number; // [0.5, 1]
    }
  | {
      readonly kind: 'incremental';
      readonly confidence: number; // [0, 1]
    }
  | {
      readonly kind: 'unrelated';
      readonly confidence: number; // [0, 1]
    };

/** judgeRelation full result · caller writes `llm_calls(purpose='judge')`. */
export interface JudgeRelationResult {
  readonly verdict: StateShiftVerdict;
  readonly inputTokens: number;
  readonly outputTokens: number;
  readonly latencyMs: number;
  readonly requestHash: string;
}

// --------------------------------------------------------------------
// LLMProvider interface · adapters (anthropic.ts / openai.ts) must both implement
// --------------------------------------------------------------------

export interface LLMProvider {
  readonly name: LLMProviderName;

  /**
   * Produce a ≤ 3-sentence summary for (paper, topic).
   * Does NOT write DB; caller takes `SummaryRecord` and runs T013 `persistSummary`.
   * Throws `LLMProviderError` on failure (caller decides whether to fall back).
   */
  summarize(input: SummarizeInput): Promise<SummaryRecord>;

  /**
   * Judge whether `candidatePaper` is a state shift vs `earlierAnchor`
   * within the given topic. Does NOT write DB; caller writes `llm_calls(purpose='judge')`.
   */
  judgeRelation(input: JudgeRelationInput): Promise<JudgeRelationResult>;
}

// --------------------------------------------------------------------
// Error · caller can distinguish retryable vs non-retryable
// --------------------------------------------------------------------

export class LLMProviderError extends Error {
  constructor(
    message: string,
    public readonly provider: LLMProviderName,
    /** true = network/5xx/429; caller may switch to fallback provider.
     *  false = schema violation / 4xx client error. */
    public readonly retryable: boolean,
    public readonly cause?: unknown,
  ) {
    super(message);
    this.name = 'LLMProviderError';
  }
}
