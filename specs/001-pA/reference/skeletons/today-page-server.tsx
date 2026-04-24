// ──────────────────────────────────────────────────────────
// Skeleton for src/app/(main)/today/page.tsx
// Source task: T014 (/today SSR page)
// Owner: T014 implementation PR
// How to use: cp this file to src/app/(main)/today/page.tsx and fill TODOs.
// This is a Server Component (no 'use client'); it reads Postgres directly
// via Drizzle — NO HTTP round-trip to /api/today (which is deferred to v0.2
// per DECISIONS-LOG 2026-04-23 "/today page 数据 fetch 策略").
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/api-contracts.md §2.C (E9 deferred · SSR path here)
//   - specs/001-pA/spec.md IN-2 (digest-first briefing) · §6 O1/O2 metrics
//   - specs/001-pA/architecture.md ADR-2 (no LLM call in request path)
//   - specs/001-pA/reference/directory-layout.md §1 tree

import { desc, eq } from 'drizzle-orm';
import { redirect } from 'next/navigation';
import { briefings, topics } from '@/db/schema.js';
import { db } from '@/lib/db/client.js';
import { getCurrentSeat } from '@/lib/auth/session.js';
import { TodayClient } from './today-client.js';
import type { BriefingItem } from '@/lib/briefings/types.js';

export const dynamic = 'force-dynamic'; // every request re-reads DB (no ISR)
export const revalidate = 0;

export default async function TodayPage() {
  const seat = await getCurrentSeat();
  if (!seat) redirect('/login');

  // 1. Empty-state: no topics yet → send to /topics
  const topicCount = await db
    .select({ id: topics.id })
    .from(topics)
    .where(eq(topics.labId, seat.labId))
    .limit(1);
  if (topicCount.length === 0) {
    return <EmptyState kind="no-topics" />;
  }

  // 2. Fetch today's briefing rows for this lab (one row per topic × date).
  // Strategy: take the latest for_date present for this lab; if older than
  // today (worker failed last night), render with a stale banner.
  const briefingRows = await db
    .select()
    .from(briefings)
    .where(eq(briefings.labId, seat.labId))
    .orderBy(desc(briefings.forDate))
    .limit(50); // generous — lab has ≤ 15 topics; extra rows safe
  if (briefingRows.length === 0) {
    return <EmptyState kind="no-briefing-yet" />;
  }

  // 3. Group by for_date and keep the most recent date's rows.
  const firstRow = briefingRows[0];
  if (!firstRow) return <EmptyState kind="no-briefing-yet" />;
  const latestDate = firstRow.forDate;
  const todayRows = briefingRows.filter((r) => r.forDate === latestDate);

  // 4. Join topic + papers + summaries + self-actions into BriefingItem[].
  // TODO(T014): assemble items via src/lib/briefings/loadTodayBriefing.ts.
  //   Per architecture.md ADR-2 NO LLM call in this function;
  //   only read from pre-computed briefings + paper_summaries + actions.
  //   Return BriefingItem[] shape from reference/api-contracts.md §3.6.
  const items: BriefingItem[] = [];

  return (
    <TodayClient
      seat={{ id: seat.id, email: seat.email, role: seat.role }}
      forDate={latestDate}
      items={items}
      staleDate={latestDate !== todayLocalDate()}
    />
  );
}

// --------------------------------------------------------------------
// Local helpers
// --------------------------------------------------------------------

function todayLocalDate(): string {
  // TODO(T014): replace with date-fns-tz using env.APP_TIMEZONE.
  //   For now returns UTC-derived YYYY-MM-DD — NOT correct for prod.
  return new Date().toISOString().slice(0, 10);
}

function EmptyState({ kind }: { kind: 'no-topics' | 'no-briefing-yet' }) {
  if (kind === 'no-topics') {
    return (
      <div className="empty-state">
        <h1>还没有 topic</h1>
        <p>请先到 /topics 创建 8–15 个感兴趣的方向,briefing 才会每日生成。</p>
      </div>
    );
  }
  return (
    <div className="empty-state">
      <h1>还没有 briefing</h1>
      <p>worker 尚未跑完第一轮,请稍后刷新(或查看 /admin/lab-stats 的 lastWorkerStatus)。</p>
    </div>
  );
}
