// ──────────────────────────────────────────────────────────
// Skeleton for src/app/api/export/full/route.ts
// Source task: T023 (JSON export endpoint · admin-only)
// Owner: T023 implementation PR
// How to use: cp this file to src/app/api/export/full/route.ts.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/api-contracts.md §2.G E17 (GET /api/export/full)
//   - specs/001-pA/spec.md IN-6 (data portability hard constraint)
//   - specs/001-pA/compliance.md §7 (monthly self-audit via export_log)
//   - specs/001-pA/risks.md SEC-1 (double admin check)
//   - specs/001-pA/reference/api-contracts.md §3.11 (ExportEnvelope shape)
//
// Contract:
//   - Double admin check (SEC-1): middleware asserts role='admin' and this
//     handler asserts again from the session table.
//   - Writes one row to `export_log` synchronously BEFORE streaming the
//     response body; if `buildFullExport` throws, no export_log row.
//   - SEC-5: no filesystem path / filename query params accepted.

import { NextResponse, type NextRequest } from 'next/server';
import { getCurrentSeat } from '@/lib/auth/session.js';
// TODO(T023): implement these modules per reference/directory-layout.md §1.
// import { buildFullExport } from '@/lib/export/builder.js';
// import { writeExportLog } from '@/lib/export/audit.js';

export async function GET(_req: NextRequest): Promise<NextResponse> {
  const seat = await getCurrentSeat();
  if (!seat) {
    return NextResponse.json(
      { error: { code: 'SESSION_EXPIRED', message: '登录已过期,请重新登录' } },
      { status: 401 },
    );
  }
  // SEC-1 double check (middleware already gated /api/export/**)
  if (seat.role !== 'admin') {
    return NextResponse.json(
      { error: { code: 'NOT_ADMIN', message: '仅管理员可操作' } },
      { status: 403 },
    );
  }

  try {
    // TODO(T023): build full export envelope (schemaVersion '1.1')
    //
    // Envelope contents (schemaVersion 1.1 · 12 top-level resource collections,
    // camelCase throughout · G3 fix 2026-04-24 · R_final B3):
    //   labs, seats, topics, papers, paperTopicScores, paperCitations,
    //   paperSummaries, briefings, actions, breadcrumbs, resurfaceEvents,
    //   fetchRuns
    // Top-level fields: schemaVersion, exportedAt, lab { id, name, firstDayAt,
    //                   exportedAt, exportedBySeatId }, then 12 arrays above
    //
    // Excluded (intentional):
    //   - sessions: runtime state, regenerated per login (not portable)
    //   - llmCalls: cost/audit internal; shipping would leak provider / model
    //     metadata unrelated to portability (separate audit table, kept in-DB)
    //   - exportLog: audit of this very endpoint; this route WRITES to it
    //     synchronously but does NOT include it in the envelope body
    //
    // Stub requirement (F5 · 2026-04-24 · R_final hardening):
    //   paperSummaries.llmCallId FK points to llmCalls, which is NOT
    //   included in the envelope. Round-trip import (T024) must either:
    //     (a) set llmCallId = null at import time (DEFAULT for v0.1), or
    //     (b) create stub llmCalls rows per api-contracts.md §3.11 note.
    //   The exporter emits llmCallId verbatim; the importer decides policy.
    //
    // G3 fix (2026-04-24): buildFullExport(labId: number) takes labId as
    //   a parameter (pulled from seat.labId below). It does NOT read
    //   `env.LAB_ID` (no such env var in directory-layout §3). This
    //   supports future multi-lab deployments without refactor.
    //
    // See reference/api-contracts.md §3.11 for exact shape + round-trip notes.
    const envelope = await buildFullExportStub(seat.labId);

    const body = JSON.stringify(envelope);
    const byteSize = new TextEncoder().encode(body).byteLength;

    // TODO(T023): writeExportLog({labId, seatId, exportType:'full', rowCountsJsonb, byteSize}).
    //   Must SYNCHRONOUSLY complete before the response returns;
    //   if it throws, DO NOT return the body (a successful export with
    //   failed audit breaks compliance.md §7).
    await writeExportLogStub(seat.labId, seat.id, envelope, byteSize);

    const filename = buildFilename(new Date());
    return new NextResponse(body, {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Disposition': `attachment; filename="${filename}"`,
      },
    });
  } catch (err) {
    // TODO(T023): log err with requestId and correlate to systemd journal.
    // biome-ignore lint/suspicious/noConsoleLog: fallback until log.ts lands
    console.error('[export/full] failed', err);
    return NextResponse.json(
      { error: { code: 'EXPORT_FAILED', message: '导出失败,请联系 operator' } },
      { status: 500 },
    );
  }
}

export const dynamic = 'force-dynamic';
export const revalidate = 0;

// --------------------------------------------------------------------
// Temporary stubs · replace by T023 implementations
// --------------------------------------------------------------------

async function buildFullExportStub(_labId: number): Promise<unknown> {
  throw new Error('TODO(T023): implement buildFullExport(labId: number) — see reference/api-contracts.md §3.11');
}

async function writeExportLogStub(
  _labId: number,
  _seatId: number,
  _envelope: unknown,
  _byteSize: number,
): Promise<void> {
  throw new Error('TODO(T023): implement writeExportLog to insert into export_log table');
}

function buildFilename(d: Date): string {
  const yyyy = d.getUTCFullYear();
  const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(d.getUTCDate()).padStart(2, '0');
  return `pi-briefing-export-${yyyy}${mm}${dd}.json`;
}
