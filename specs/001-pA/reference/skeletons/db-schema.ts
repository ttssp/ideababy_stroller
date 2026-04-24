// ──────────────────────────────────────────────────────────
// Skeleton for src/db/schema.ts
// Source task: T003 (Drizzle schema for 15 tables)
// Owner: T003 implementation PR
// How to use: cp this file to src/db/schema.ts, run `pnpm db:generate`,
// then diff the generated 0000_initial.sql against reference/schema.sql
// (CI job `schema-drift` enforces 1:1 parity).
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/schema.sql (15 tables · human-readable DDL)
//   - specs/001-pA/architecture.md §5 (ER diagram)
//   - specs/001-pA/spec.md D15 / D16 (summary_sentence_cap / skip_requires_why)
//   - specs/001-pA/tasks/T003.md (column inventory + R1/R2 patches)
//
// Conventions:
//   - snake_case DB columns · camelCase TS identifiers (`.snake` helper
//     not used — Drizzle column() names are explicit literals).
//   - `bigserial` → `bigint` TS (mode: 'number') for ids up to 2^53 safe range.
//   - timestamps are `timestamptz` with `defaultNow()` unless noted.
//   - CHECK constraints live in table extras block (second arg to pgTable).

import { sql } from 'drizzle-orm';
import {
  bigint,
  bigserial,
  check,
  date,
  doublePrecision,
  index,
  integer,
  jsonb,
  pgTable,
  primaryKey,
  text,
  timestamp,
  uniqueIndex,
} from 'drizzle-orm/pg-core';

// --------------------------------------------------------------------
// 1. labs · tenant boundary (single-lab deploy in v0.1)
// --------------------------------------------------------------------
export const labs = pgTable('labs', {
  id: bigserial('id', { mode: 'number' }).primaryKey(),
  name: text('name').notNull(),
  // R1 additions for day-30 sentinel (T026)
  firstDayAt: timestamp('first_day_at', { withTimezone: true }).notNull().defaultNow(),
  allowContinueUntil: timestamp('allow_continue_until', { withTimezone: true }),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
});

// --------------------------------------------------------------------
// 2. seats · lab members (≤ 15 rows; C9)
// --------------------------------------------------------------------
export const seats = pgTable(
  'seats',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    labId: bigint('lab_id', { mode: 'number' })
      .notNull()
      .references(() => labs.id, { onDelete: 'restrict' }),
    email: text('email').notNull(),
    role: text('role').notNull(),
    // R1→R2 Q2 auth columns
    inviteTokenHash: text('invite_token_hash'),
    inviteExpiresAt: timestamp('invite_expires_at', { withTimezone: true }),
    invitedAt: timestamp('invited_at', { withTimezone: true }),
    lastLoginAt: timestamp('last_login_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    labEmailUniq: uniqueIndex('seats_lab_email_unique').on(t.labId, t.email),
    roleEnum: check('seats_role_enum', sql`${t.role} in ('admin', 'member')`),
    inviteTokenUniq: uniqueIndex('seats_invite_token_hash_uniq')
      .on(t.inviteTokenHash)
      .where(sql`${t.inviteTokenHash} is not null`),
  }),
);

// --------------------------------------------------------------------
// 3. sessions · login session store (JWT hash lookup + revocation)
// --------------------------------------------------------------------
export const sessions = pgTable(
  'sessions',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    seatId: bigint('seat_id', { mode: 'number' })
      .notNull()
      .references(() => seats.id, { onDelete: 'cascade' }),
    tokenHash: text('token_hash').notNull(),
    issuedAt: timestamp('issued_at', { withTimezone: true }).notNull().defaultNow(),
    expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
    loginDate: date('login_date').notNull(), // redundant, used by O1/O3 index
    ip: text('ip'),
    userAgent: text('user_agent'),
    // R1→R2 Q2 auth columns
    revokedAt: timestamp('revoked_at', { withTimezone: true }),
    lastActiveAt: timestamp('last_active_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    tokenHashUniq: uniqueIndex('sessions_token_hash_uniq').on(t.tokenHash),
    seatLoginDateIdx: index('sessions_seat_login_date_idx').on(t.seatId, t.loginDate),
    seatLastActiveIdx: index('sessions_seat_last_active_idx').on(t.seatId, t.lastActiveAt),
  }),
);

// --------------------------------------------------------------------
// 4. topics · lab-owned topic pool (8–15 active; IN-1)
// --------------------------------------------------------------------
export const topics = pgTable(
  'topics',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    labId: bigint('lab_id', { mode: 'number' })
      .notNull()
      .references(() => labs.id, { onDelete: 'restrict' }),
    name: text('name').notNull(),
    keywordPool: text('keyword_pool').array().notNull().default(sql`'{}'::text[]`),
    arxivCategories: text('arxiv_categories').array().notNull().default(sql`'{}'::text[]`),
    seedAuthors: text('seed_authors').array().notNull().default(sql`'{}'::text[]`),
    createdBySeatId: bigint('created_by_seat_id', { mode: 'number' }).references(
      () => seats.id,
      { onDelete: 'set null' },
    ),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
    archivedAt: timestamp('archived_at', { withTimezone: true }),
  },
  (t) => ({
    labIdIdx: index('topics_lab_id_idx').on(t.labId),
    keywordGin: index('topics_keyword_pool_gin').using('gin', t.keywordPool),
    categoriesGin: index('topics_arxiv_categories_gin').using('gin', t.arxivCategories),
  }),
);

// --------------------------------------------------------------------
// 5. papers · global arXiv paper table (deduped by arxiv_id)
// --------------------------------------------------------------------
export const papers = pgTable(
  'papers',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    arxivId: text('arxiv_id').notNull(),
    title: text('title').notNull(),
    abstract: text('abstract').notNull(),
    authors: text('authors').array().notNull().default(sql`'{}'::text[]`),
    categories: text('categories').array().notNull().default(sql`'{}'::text[]`),
    primaryCategory: text('primary_category'),
    publishedAt: timestamp('published_at', { withTimezone: true }).notNull(),
    fetchedAt: timestamp('fetched_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    arxivIdUniq: uniqueIndex('papers_arxiv_id_uniq').on(t.arxivId),
    publishedAtIdx: index('papers_published_at_idx').on(t.publishedAt),
    categoriesGin: index('papers_categories_gin').using('gin', t.categories),
  }),
);

// --------------------------------------------------------------------
// 6. paper_citations · citation graph edges
// --------------------------------------------------------------------
// cited_arxiv_id is text (not FK) because referenced paper may not be
// in `papers` yet.
export const paperCitations = pgTable(
  'paper_citations',
  {
    citingPaperId: bigint('citing_paper_id', { mode: 'number' })
      .notNull()
      .references(() => papers.id, { onDelete: 'cascade' }),
    citedArxivId: text('cited_arxiv_id').notNull(),
    discoveredAt: timestamp('discovered_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    pk: primaryKey({ columns: [t.citingPaperId, t.citedArxivId] }),
    citedArxivIdx: index('paper_citations_cited_arxiv_idx').on(t.citedArxivId),
  }),
);

// --------------------------------------------------------------------
// 7. paper_topic_scores · matcher results (paper ↔ topic)
// --------------------------------------------------------------------
export const paperTopicScores = pgTable(
  'paper_topic_scores',
  {
    paperId: bigint('paper_id', { mode: 'number' })
      .notNull()
      .references(() => papers.id, { onDelete: 'cascade' }),
    topicId: bigint('topic_id', { mode: 'number' })
      .notNull()
      .references(() => topics.id, { onDelete: 'cascade' }),
    matchSignal: text('match_signal').notNull(),
    matchedKeywords: jsonb('matched_keywords')
      .$type<string[]>()
      .notNull()
      .default(sql`'[]'::jsonb`),
    score: doublePrecision('score'),
    computedAt: timestamp('computed_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    pk: primaryKey({ columns: [t.paperId, t.topicId] }),
    signalEnum: check(
      'paper_topic_scores_signal_enum',
      sql`${t.matchSignal} in ('keyword', 'category', 'seed_author')`,
    ),
    topicIdx: index('paper_topic_scores_topic_idx').on(t.topicId),
  }),
);

// --------------------------------------------------------------------
// 8. actions · 4-action records (per seat × per paper; D4 fixed set)
// --------------------------------------------------------------------
// D16 Layer 1 mechanical enforcement: skip_requires_why CHECK.
export const actions = pgTable(
  'actions',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    seatId: bigint('seat_id', { mode: 'number' })
      .notNull()
      .references(() => seats.id, { onDelete: 'cascade' }),
    paperId: bigint('paper_id', { mode: 'number' })
      .notNull()
      .references(() => papers.id, { onDelete: 'cascade' }),
    action: text('action').notNull(),
    why: text('why'),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    actionEnum: check(
      'actions_action_enum',
      sql`${t.action} in ('read_now', 'read_later', 'skip', 'breadcrumb')`,
    ),
    whyLength: check(
      'actions_why_length',
      sql`${t.why} is null or char_length(${t.why}) <= 280`,
    ),
    // RED LINE 2 · D16 Layer 1
    skipRequiresWhy: check(
      'skip_requires_why',
      sql`${t.action} != 'skip' or (${t.why} is not null and char_length(btrim(${t.why})) >= 5)`,
    ),
    seatCreatedIdx: index('actions_seat_created_idx').on(t.seatId, t.createdAt),
    paperIdx: index('actions_paper_idx').on(t.paperId),
  }),
);

// --------------------------------------------------------------------
// 9. breadcrumbs · active breadcrumb tracking (resurface source)
// --------------------------------------------------------------------
export const breadcrumbs = pgTable(
  'breadcrumbs',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    seatId: bigint('seat_id', { mode: 'number' })
      .notNull()
      .references(() => seats.id, { onDelete: 'cascade' }),
    paperId: bigint('paper_id', { mode: 'number' })
      .notNull()
      .references(() => papers.id, { onDelete: 'cascade' }),
    topicId: bigint('topic_id', { mode: 'number' })
      .notNull()
      .references(() => topics.id, { onDelete: 'cascade' }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    dismissedAt: timestamp('dismissed_at', { withTimezone: true }),
    lastResurfaceAt: timestamp('last_resurface_at', { withTimezone: true }),
  },
  (t) => ({
    // One active breadcrumb per (seat, paper); re-breadcrumb creates a new row.
    activeUniq: uniqueIndex('breadcrumbs_active_unique')
      .on(t.seatId, t.paperId)
      .where(sql`${t.dismissedAt} is null`),
    seatCreatedIdx: index('breadcrumbs_seat_created_idx').on(t.seatId, t.createdAt),
  }),
);

// --------------------------------------------------------------------
// 10. resurface_events · resurface history (O2 source of truth)
// --------------------------------------------------------------------
export const resurfaceEvents = pgTable(
  'resurface_events',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    breadcrumbId: bigint('breadcrumb_id', { mode: 'number' })
      .notNull()
      .references(() => breadcrumbs.id, { onDelete: 'cascade' }),
    triggerType: text('trigger_type').notNull(),
    triggerPaperId: bigint('trigger_paper_id', { mode: 'number' }).references(() => papers.id, {
      onDelete: 'set null',
    }),
    contextText: text('context_text').notNull(),
    surfacedAt: timestamp('surfaced_at', { withTimezone: true }).notNull().defaultNow(),
    clickedAt: timestamp('clicked_at', { withTimezone: true }),
    dismissedAt: timestamp('dismissed_at', { withTimezone: true }),
  },
  (t) => ({
    triggerEnum: check(
      'resurface_trigger_enum',
      sql`${t.triggerType} in ('timed_6wk', 'timed_3mo', 'timed_6mo', 'citation')`,
    ),
    breadcrumbIdx: index('resurface_events_breadcrumb_idx').on(t.breadcrumbId, t.surfacedAt),
    surfacedAtIdx: index('resurface_events_surfaced_at_idx').on(t.surfacedAt),
  }),
);

// --------------------------------------------------------------------
// 11. briefings · daily precomputed briefing (one row per topic × date)
// --------------------------------------------------------------------
export const briefings = pgTable(
  'briefings',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    labId: bigint('lab_id', { mode: 'number' })
      .notNull()
      .references(() => labs.id, { onDelete: 'restrict' }),
    topicId: bigint('topic_id', { mode: 'number' })
      .notNull()
      .references(() => topics.id, { onDelete: 'cascade' }),
    forDate: date('for_date').notNull(),
    stateSummary: text('state_summary').notNull(),
    // Max 3 entries (CHECK below); ordered by display rank.
    triggerPaperIds: bigint('trigger_paper_ids', { mode: 'number' })
      .array()
      .notNull()
      .default(sql`'{}'::bigint[]`),
    anchorPaperId: bigint('anchor_paper_id', { mode: 'number' }).references(() => papers.id, {
      onDelete: 'set null',
    }),
    llmProvider: text('llm_provider'),
    tokenCostCents: integer('token_cost_cents'),
    assembledAt: timestamp('assembled_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    labTopicDateUniq: uniqueIndex('briefings_lab_topic_date_uniq').on(
      t.labId,
      t.topicId,
      t.forDate,
    ),
    triggerCardinality: check(
      'briefings_trigger_paper_cardinality',
      sql`array_length(${t.triggerPaperIds}, 1) is null or array_length(${t.triggerPaperIds}, 1) <= 3`,
    ),
    labForDateIdx: index('briefings_lab_for_date_idx').on(t.labId, t.forDate),
  }),
);

// --------------------------------------------------------------------
// 12. fetch_runs · worker run audit (on-boot catchup source)
// --------------------------------------------------------------------
export const fetchRuns = pgTable(
  'fetch_runs',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    runDate: date('run_date').notNull(),
    source: text('source').notNull(),
    status: text('status').notNull(),
    itemsFetched: integer('items_fetched').notNull().default(0),
    startedAt: timestamp('started_at', { withTimezone: true }).notNull().defaultNow(),
    finishedAt: timestamp('finished_at', { withTimezone: true }),
    errorText: text('error_text'),
    notes: text('notes'),
  },
  (t) => ({
    statusEnum: check(
      'fetch_runs_status_enum',
      sql`${t.status} in ('ok', 'failed', 'partial', 'running')`,
    ),
    runDateSourceIdx: index('fetch_runs_run_date_source_idx').on(t.runDate, t.source),
  }),
);

// --------------------------------------------------------------------
// 13. llm_calls · LLM audit trail (C11 cost envelope; NO response body)
// --------------------------------------------------------------------
export const llmCalls = pgTable(
  'llm_calls',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    provider: text('provider').notNull(),
    model: text('model').notNull(),
    purpose: text('purpose').notNull(),
    inputTokens: integer('input_tokens').notNull(),
    outputTokens: integer('output_tokens').notNull(),
    costCents: integer('cost_cents').notNull(),
    latencyMs: integer('latency_ms').notNull(),
    paperId: bigint('paper_id', { mode: 'number' }).references(() => papers.id, {
      onDelete: 'set null',
    }),
    requestHash: text('request_hash'),
    calledAt: timestamp('called_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    purposeEnum: check('llm_calls_purpose_enum', sql`${t.purpose} in ('summarize', 'judge')`),
    calledAtIdx: index('llm_calls_called_at_idx').on(t.calledAt),
    purposeIdx: index('llm_calls_purpose_idx').on(t.purpose),
  }),
);

// --------------------------------------------------------------------
// 14. paper_summaries · LLM-generated ≤ 3-sentence summary (R1 · D15)
// --------------------------------------------------------------------
// RED LINE 2 mechanical enforcement (paper_summaries side; D15):
//   summary_sentence_cap CHECK counts English (.!?) + Chinese (。！？)
//   terminators directly using regexp_matches(..., 'g'). Rejects
//   unterminated text AND >3-sentence text. Works for pure Chinese
//   without whitespace (G1 fix · R_final B1 2026-04-24).
// F5 (2026-04-24): llm_call_id NULLABLE + ON DELETE SET NULL for
//   JSON export round-trip (api-contracts.md §3.11 option (a)).
export const paperSummaries = pgTable(
  'paper_summaries',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    paperId: bigint('paper_id', { mode: 'number' })
      .notNull()
      .references(() => papers.id, { onDelete: 'cascade' }),
    topicId: bigint('topic_id', { mode: 'number' })
      .notNull()
      .references(() => topics.id, { onDelete: 'cascade' }),
    summaryText: text('summary_text').notNull(),
    llmCallId: bigint('llm_call_id', { mode: 'number' }).references(() => llmCalls.id, {
      onDelete: 'set null',
    }),
    modelName: text('model_name').notNull(),
    promptVersion: text('prompt_version').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    // RED LINE 2 · D15 · G1 fix (R_final B1 · 2026-04-24):
    // Count sentence-terminal punctuation occurrences (English + Chinese).
    // Accept 1..3 terminators; reject 0 or >3. Whitespace-independent,
    // so pure Chinese "中文。第二句。第三句。" correctly counts as 3.
    sentenceCap: check(
      'summary_sentence_cap',
      sql`coalesce(array_length(regexp_matches(${t.summaryText}, '[.!?。！？]', 'g'), 1), 0) between 1 and 3`,
    ),
    // Per (paper, topic, prompt_version) unique
    uniqueKey: uniqueIndex('paper_summaries_unique_key').on(t.paperId, t.topicId, t.promptVersion),
    paperIdx: index('paper_summaries_paper_idx').on(t.paperId),
    topicIdx: index('paper_summaries_topic_idx').on(t.topicId),
  }),
);

// --------------------------------------------------------------------
// 15. export_log · JSON export audit (SEC-1; R1 addition)
// --------------------------------------------------------------------
export const exportLog = pgTable(
  'export_log',
  {
    id: bigserial('id', { mode: 'number' }).primaryKey(),
    labId: bigint('lab_id', { mode: 'number' })
      .notNull()
      .references(() => labs.id, { onDelete: 'restrict' }),
    seatId: bigint('seat_id', { mode: 'number' })
      .notNull()
      .references(() => seats.id, { onDelete: 'restrict' }),
    exportType: text('export_type').notNull(),
    rowCountsJsonb: jsonb('row_counts_jsonb')
      .$type<Record<string, number>>()
      .notNull(),
    byteSize: integer('byte_size').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => ({
    typeEnum: check('export_log_type_enum', sql`${t.exportType} in ('full')`),
    labCreatedIdx: index('export_log_lab_created_idx').on(t.labId, t.createdAt),
  }),
);
