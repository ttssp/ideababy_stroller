// ──────────────────────────────────────────────────────────
// Skeleton for src/lib/actions/recordAction.ts
// Source task: T015 (4-action API · D16 Layer 2 red-line-2 gate)
// Owner: T015 implementation PR
// How to use: cp this file to src/lib/actions/recordAction.ts and fill TODOs.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/spec.md D16 (skip_requires_why 三层兜底 · this file is Layer 2)
//   - specs/001-pA/reference/api-contracts.md §2.C E10 (POST /api/actions)
//   - specs/001-pA/reference/error-codes-and-glossary.md §1 (error codes)
//   - specs/001-pA/reference/schema.sql §8 (actions table CHECKs)
//
// Contract:
//   - Called by both the Next Server Action (from skip-why-input.tsx) and
//     the REST route handler (src/app/api/actions/route.ts). Both paths
//     converge here so validation lives in exactly one place.
//   - Must validate BEFORE writing DB — DB CHECK `skip_requires_why` is
//     Layer 1 safety net, but a trigger from Layer 1 means Layer 2 has
//     a bug (log the discrepancy).

'use server';

import { and, eq, gt } from 'drizzle-orm';
import { z } from 'zod';
import { actions, breadcrumbs, papers, paperTopicScores } from '@/db/schema.js';
import { db } from '@/lib/db/client.js';
import { getCurrentSeat } from '@/lib/auth/session.js';

// --------------------------------------------------------------------
// Input schema · zod refine captures D16 Layer 2 gate
// --------------------------------------------------------------------

const ActionInputSchema = z
  .object({
    paperId: z.number().int().positive(),
    action: z.enum(['read_now', 'read_later', 'skip', 'breadcrumb']),
    why: z.string().trim().max(280).optional(),
  })
  .refine(
    (v) => v.action !== 'skip' || (v.why !== undefined && v.why.trim().length >= 5),
    { message: 'skip 必须填写 why (至少 5 字符)', path: ['why'] },
  );

export type ActionInput = z.infer<typeof ActionInputSchema>;

// --------------------------------------------------------------------
// Return discriminated union · error codes per api-contracts §4
// --------------------------------------------------------------------

export type RecordActionResult =
  | { ok: true; actionId: number; breadcrumbId?: number }
  | {
      ok: false;
      code:
        | 'SKIP_WHY_REQUIRED'
        | 'WHY_TOO_LONG'
        | 'INVALID_ACTION'
        | 'PAPER_NOT_FOUND'
        | 'DUPLICATE_ACTION'
        | 'PAPER_NOT_IN_LAB_TOPICS'
        | 'NOT_AUTHENTICATED';
      message: string;
      fields?: Record<string, string>;
    };

// --------------------------------------------------------------------
// Entry point
// --------------------------------------------------------------------

export async function recordAction(raw: unknown): Promise<RecordActionResult> {
  // 1. Auth gate
  const seat = await getCurrentSeat();
  if (!seat) {
    return { ok: false, code: 'NOT_AUTHENTICATED', message: '登录已过期,请重新登录' };
  }

  // 2. Validate input (D16 Layer 2 red-line-2 gate lives here)
  const parsed = ActionInputSchema.safeParse(raw);
  if (!parsed.success) {
    const issue = parsed.error.issues[0];
    const path0 = issue?.path[0];
    if (path0 === 'why') {
      // Either skip-without-why OR why too long
      if (issue?.code === 'too_big') {
        return {
          ok: false,
          code: 'WHY_TOO_LONG',
          message: 'why 最多 280 字符',
          fields: { why: 'max 280 chars' },
        };
      }
      return {
        ok: false,
        code: 'SKIP_WHY_REQUIRED',
        message: 'skip 必须填写 why (至少 5 字符)',
        fields: { why: '至少需要 5 个非空白字符' },
      };
    }
    return {
      ok: false,
      code: 'INVALID_ACTION',
      message: '无效的 action 类型',
    };
  }
  const input = parsed.data;

  // 3. Paper existence
  const paper = await db
    .select({ id: papers.id })
    .from(papers)
    .where(eq(papers.id, input.paperId))
    .limit(1);
  if (paper.length === 0) {
    return { ok: false, code: 'PAPER_NOT_FOUND', message: '论文不存在' };
  }

  // 4. Duplicate action guard (60s window; see api-contracts E10 Notes)
  // TODO(T015): If (seat, paper, action) within last 60s exists → return DUPLICATE_ACTION.
  //   Hint: select from actions where seat_id = seat.id and paper_id = input.paperId
  //   and action = input.action and created_at > now() - interval '60 seconds'.
  const duplicate = await db
    .select({ id: actions.id })
    .from(actions)
    .where(
      and(
        eq(actions.seatId, seat.id),
        eq(actions.paperId, input.paperId),
        eq(actions.action, input.action),
        gt(actions.createdAt, new Date(Date.now() - 60_000)),
      ),
    )
    .limit(1);
  if (duplicate.length > 0) {
    return { ok: false, code: 'DUPLICATE_ACTION', message: '检测到重复 action' };
  }

  // 5. breadcrumb path needs a topic_id; derive from paper_topic_scores
  let topicIdForBreadcrumb: number | null = null;
  if (input.action === 'breadcrumb') {
    const match = await db
      .select({ topicId: paperTopicScores.topicId })
      .from(paperTopicScores)
      .where(eq(paperTopicScores.paperId, input.paperId))
      .limit(1);
    if (match.length === 0 || match[0] === undefined) {
      return {
        ok: false,
        code: 'PAPER_NOT_IN_LAB_TOPICS',
        message: '该论文未匹配任何 topic',
      };
    }
    topicIdForBreadcrumb = match[0].topicId;
  }

  // 6. Insert (transactional when action='breadcrumb')
  // TODO(T015): wrap in db.transaction when action='breadcrumb'.
  //   Inside tx:
  //     a. INSERT actions → returning id
  //     b. if breadcrumb: INSERT breadcrumbs(seat_id, paper_id, topic_id) → returning id
  //        On conflict (active unique index) → caller's re-breadcrumb path (see api-contracts E14).
  //        For v0.1 a plain INSERT is acceptable; the partial unique index will
  //        surface a clean error we map to DUPLICATE_ACTION.
  try {
    const [row] = await db
      .insert(actions)
      .values({
        seatId: seat.id,
        paperId: input.paperId,
        action: input.action,
        why: input.why ?? null,
      })
      .returning({ id: actions.id });
    if (!row) throw new Error('actions insert returned no row');

    let breadcrumbId: number | undefined;
    if (input.action === 'breadcrumb' && topicIdForBreadcrumb !== null) {
      const [bc] = await db
        .insert(breadcrumbs)
        .values({
          seatId: seat.id,
          paperId: input.paperId,
          topicId: topicIdForBreadcrumb,
        })
        .returning({ id: breadcrumbs.id });
      if (bc) breadcrumbId = bc.id;
    }

    return breadcrumbId !== undefined
      ? { ok: true, actionId: row.id, breadcrumbId }
      : { ok: true, actionId: row.id };
  } catch (err) {
    // D16 Layer 1 (DB CHECK skip_requires_why) should never trigger here
    // because zod refine caught it first. If it does, we have a bug where
    // zod and DB are out of sync — re-throw and log for operator triage.
    // TODO(T015): log err with requestId to src/lib/log.ts before re-throwing.
    throw err;
  }
}
