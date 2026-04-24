// ──────────────────────────────────────────────────────────
// Skeleton for src/app/api/healthz/route.ts
// Source task: T030 (deploy scripts + healthz)
// Owner: T030 implementation PR
// How to use: cp this file to src/app/api/healthz/route.ts.
// Used by Caddy health check and systemd watchdog. Keep this endpoint
// CHEAP — no LLM calls, no heavy joins. DB ping only.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/api-contracts.md §2.H E18 (/api/healthz)
//   - specs/001-pA/SLA.md (§1.1 p95 target)
//   - specs/001-pA/reference/error-codes-and-glossary.md HEALTH_DEGRADED

import { sql } from 'drizzle-orm';
import { NextResponse } from 'next/server';
import { db } from '@/lib/db/client.js';

// Capture process start so we can report uptime.
const START_TIME = Date.now();

// GIT_SHA is injected at build time (next.config.mjs reads process.env.GIT_SHA
// and exposes via `publicRuntimeConfig`/env substitution). In dev returns 'dev'.
const VERSION = process.env.GIT_SHA ?? 'dev';

export async function GET(): Promise<NextResponse> {
  // Single-shot DB ping; no retry (if it fails, reporting is honest).
  try {
    await db.execute(sql`select 1`);
  } catch {
    return NextResponse.json(
      {
        error: {
          code: 'HEALTH_DEGRADED',
          message: 'DB ping failed',
        },
      },
      { status: 500 },
    );
  }

  return NextResponse.json({
    status: 'ok',
    uptimeSec: Math.floor((Date.now() - START_TIME) / 1000),
    version: VERSION,
    now: new Date().toISOString(),
  });
}

// force-dynamic so Next doesn't cache this across requests.
export const dynamic = 'force-dynamic';
export const revalidate = 0;
