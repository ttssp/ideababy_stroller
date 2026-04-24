// ──────────────────────────────────────────────────────────
// Skeleton for src/workers/daily.ts
// Source task: T011 (daily worker orchestrator)
// Owner: T011 implementation PR
// How to use: cp this file to src/workers/daily.ts. Run locally with
//   pnpm worker:daily
// In production this file is the entry point for pi-briefing-worker.service
// (systemd oneshot, triggered by pi-briefing-worker.timer at 06:00 Asia/Shanghai).
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/architecture.md ADR-1 (06:00 cron) · ADR-2 (no LLM in web path)
//   - specs/001-pA/spec.md Phase 1 / Phase 2 task breakdown
//   - specs/001-pA/reference/directory-layout.md §1 src/workers/ tree
//
// Contract:
//   - This file MUST NOT import anything from 'next/*'. It runs in pure Node
//     under systemd; Next's runtime is absent.
//   - Each pass writes exactly one row to `fetch_runs` with status in
//     {running, ok, failed, partial}. Operator reads this table.
//   - On any fatal error, exit 1 so systemd logs the unit failure.

import { env } from '@/lib/env.js';
// TODO(T011): un-comment these imports as each subroutine file lands.
// import { runFetchPass } from './fetch-pass.js';
// import { runSummaryPass } from './summary-pass.js';
// import { runStateShiftPass } from './state-shift-pass.js';
// import { runBriefingPass } from './briefing-pass.js';
// import { runResurfacePass } from './resurface-pass.js';

type PassFn = () => Promise<void>;

async function runPass(name: string, fn: PassFn): Promise<void> {
  const started = Date.now();
  // eslint-disable-next-line no-console
  console.info('[worker]', name, 'start');
  try {
    await fn();
    // eslint-disable-next-line no-console
    console.info('[worker]', name, 'ok', { ms: Date.now() - started });
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('[worker]', name, 'failed', { ms: Date.now() - started, err });
    throw err;
  }
}

async function main(): Promise<void> {
  // eslint-disable-next-line no-console
  console.info('[worker] start', {
    tz: env.APP_TIMEZONE,
    at: new Date().toISOString(),
    catchupHours: env.WORKER_CATCHUP_WINDOW_HOURS,
  });

  try {
    // TODO(T011): Implement catchup logic (ADR-1):
    //   1. SELECT max(started_at) FROM fetch_runs WHERE status='ok' AND source='arxiv';
    //   2. If > 24h ago → do a single catchup pass before today's pass.
    //   3. Write one fetch_runs row at end of each pass.

    // Fetch pass — arXiv API → papers table (T011 subtask).
    await runPass('fetch', async () => {
      throw new Error('TODO(T011): implement runFetchPass in ./fetch-pass.ts');
    });

    // Summary pass — for each candidate paper × topic, call LLM, persist (T013).
    await runPass('summary', async () => {
      throw new Error('TODO(T013): implement runSummaryPass in ./summary-pass.ts');
    });

    // State-shift pass — heuristic (+ optional LLM judge) → briefings staging.
    await runPass('state-shift', async () => {
      throw new Error('TODO(T012): implement runStateShiftPass in ./state-shift-pass.ts');
    });

    // Briefing pass — assemble briefings row per (lab, topic, for_date).
    await runPass('briefing', async () => {
      throw new Error('TODO(T014): implement runBriefingPass in ./briefing-pass.ts');
    });

    // Resurface pass — timed + citation-triggered (spec.md §4.2).
    await runPass('resurface', async () => {
      throw new Error('TODO(T021): implement runResurfacePass in ./resurface-pass.ts');
    });

    // eslint-disable-next-line no-console
    console.info('[worker] success');
    process.exit(0);
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('[worker] fatal', err);
    process.exit(1);
  }
}

// --------------------------------------------------------------------
// Run only when invoked as an entry point (not when imported in tests)
// --------------------------------------------------------------------
// eslint-disable-next-line @typescript-eslint/no-floating-promises
main();
