// ──────────────────────────────────────────────────────────
// Skeleton for src/lib/env.ts
// Source task: T002 (monorepo scaffold) + T007 (env zod schema)
// Owner: T007 implementation PR
// How to use: cp this file to src/lib/env.ts and fill TODOs.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/directory-layout.md §3 (.env.example full list)
//   - specs/001-pA/tech-stack.md §1 (pinned versions, zod 3.23)
//   - specs/001-pA/spec.md C11 (LLM cost envelope $50/mo)
//   - specs/001-pA/reference/llm-adapter-skeleton.md §3/§4 (env usage)
//
// Contract:
//   - Exports a lazy-evaluated `env` Proxy; access triggers one-shot parse.
//   - Parse failure throws `ENV_INVALID` at boot; no silent defaults for
//     secrets. See scripts/validate-env.ts (T007) for CI-time assertion.
//   - All fields read-only; never write `process.env[k]` at runtime.

import { z } from 'zod';

// --------------------------------------------------------------------
// Schema · matches directory-layout.md §3 .env.example 1:1
// --------------------------------------------------------------------

const EnvSchema = z.object({
  // --- Application ---
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  APP_ORIGIN: z.string().url(),
  APP_TIMEZONE: z.string().min(1).default('Asia/Shanghai'),

  // --- Postgres (webapp_user + worker_user; two distinct DSNs) ---
  DATABASE_URL: z.string().url(),
  DATABASE_URL_WORKER: z.string().url(),
  DATABASE_POOL_WEBAPP: z.coerce.number().int().positive().default(5),
  DATABASE_POOL_WORKER: z.coerce.number().int().positive().default(2),

  // --- LLM provider binding (post-T001 spike) ---
  LLM_PROVIDER: z.enum(['anthropic', 'openai']),
  LLM_FALLBACK_PROVIDER: z.enum(['anthropic', 'openai']).optional(),
  ANTHROPIC_API_KEY: z.string().min(1),
  ANTHROPIC_MODEL: z.string().min(1).default('claude-sonnet-4-6-20250701'),
  OPENAI_API_KEY: z.string().min(1),
  OPENAI_MODEL: z.string().min(1).default('gpt-5.4-turbo'),
  LLM_MONTHLY_COST_USD_CAP: z.coerce.number().positive().default(50),

  // --- arXiv ---
  ARXIV_API_BASE: z.string().url().default('http://export.arxiv.org/api/query'),
  ARXIV_RATE_LIMIT_MS: z.coerce.number().int().nonnegative().default(3000),

  // --- Auth ---
  // SESSION_SECRET must be at least 64 hex chars (= 32 bytes).
  SESSION_SECRET: z.string().min(64),
  INVITE_TOKEN_TTL_HOURS: z.coerce.number().int().positive().default(24),

  // --- SMTP (optional; empty string = disabled in v0.1) ---
  SMTP_HOST: z.string().default(''),
  SMTP_PORT: z.coerce.number().int().positive().default(587),
  SMTP_USER: z.string().default(''),
  SMTP_PASS: z.string().default(''),
  SMTP_FROM: z.string().default(''),

  // --- Cron / worker ---
  WORKER_DAILY_TIME: z
    .string()
    .regex(/^\d{2}:\d{2}$/, 'WORKER_DAILY_TIME must be HH:MM')
    .default('06:00'),
  WORKER_CATCHUP_WINDOW_HOURS: z.coerce.number().int().positive().default(24),

  // --- Dogfood / bootstrap ---
  LAB_DEFAULT_NAME: z.string().min(1).default('My Research Lab'),
  ADMIN_EMAIL: z.string().email(),

  // --- Observability ---
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  ALERT_EMAIL: z.string().email(),

  // --- Feature flags ---
  SENTINEL_ENABLED: z.coerce.boolean().default(true),
  STALE_BANNER_ENABLED: z.coerce.boolean().default(true),
});

export type Env = z.infer<typeof EnvSchema>;

// --------------------------------------------------------------------
// Lazy Proxy · parse-on-first-access, cached thereafter
// --------------------------------------------------------------------

let cached: Env | null = null;

function loadEnv(): Env {
  if (cached) return cached;
  const parsed = EnvSchema.safeParse(process.env);
  if (!parsed.success) {
    // eslint-disable-next-line no-console
    console.error('[env] invalid process.env:', parsed.error.format());
    throw new Error('ENV_INVALID — fix .env before starting (see validate-env script)');
  }
  cached = parsed.data;
  return cached;
}

/**
 * Typed env accessor. First access throws if env is invalid; subsequent
 * accesses hit the cached parsed object. Do NOT destructure at module top
 * level — importers should touch `env.X` inside functions so tests can
 * control process.env before first access.
 */
export const env: Env = new Proxy({} as Env, {
  get(_target, prop: string) {
    const loaded = loadEnv();
    return loaded[prop as keyof Env];
  },
  has(_target, prop: string) {
    const loaded = loadEnv();
    return prop in loaded;
  },
});

// --------------------------------------------------------------------
// Test hook · reset cache so vitest can swap process.env between cases
// --------------------------------------------------------------------

/**
 * Clears the cached env. Intended for tests only (tests/unit/env.test.ts).
 * Do NOT call from production code.
 */
export function __resetEnvCacheForTests(): void {
  cached = null;
}
