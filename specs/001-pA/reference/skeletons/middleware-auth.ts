// ──────────────────────────────────────────────────────────
// Skeleton for src/middleware.ts (Next.js App Router middleware)
// Source task: T028 (session management)
// Owner: T028 implementation PR
// How to use: cp this file to src/middleware.ts (Next requires it at
// src/middleware.ts or project root — we use src/).
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/api-contracts.md §1.2 (auth rules)
//   - specs/001-pA/spec.md D3 (dual seat auth) · §6 O-verify-c6-api
//   - specs/001-pA/reference/schema.sql §3 (sessions table)
//
// Contract:
//   - Runs on Edge runtime (Next middleware default); jose is Edge-safe.
//   - Does NOT import Drizzle here — Edge runtime can't reach pg directly.
//     Instead, verify JWT signature only; DB check happens inside Server
//     Components via getCurrentSeat(). Middleware is the *first gate*;
//     DB revocation is enforced at the Server Component layer.
//   - Attaches the decoded seat to headers so Server Components skip a JWT
//     round-trip (see getCurrentSeat() for how headers are consumed).

import { NextResponse, type NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

// --------------------------------------------------------------------
// Route classification
// --------------------------------------------------------------------

const PUBLIC_ROUTES = [
  '/login',
  '/login/verify',
  '/login/invalid-token',
  '/api/healthz',
  '/api/invite', // admin-only, but its own handler asserts role
  '/privacy',
  '/favicon.ico',
];

const ADMIN_ROUTES = [
  '/admin',
  '/api/topics', // POST/PATCH/DELETE require admin; GET is allowed — handler double-checks
  '/api/invite',
  '/api/export',
  '/api/admin',
];

function isPublic(pathname: string): boolean {
  if (PUBLIC_ROUTES.some((p) => pathname === p || pathname.startsWith(`${p}/`))) return true;
  // Invite consumption route is pattern-matched separately
  if (pathname.match(/^\/api\/invite\/[^/]+\/consume$/)) return true;
  return false;
}

function isAdminRoute(pathname: string): boolean {
  return ADMIN_ROUTES.some((p) => pathname === p || pathname.startsWith(`${p}/`));
}

// --------------------------------------------------------------------
// JWT payload
// --------------------------------------------------------------------

type SessionPayload = {
  sub: string; // seat_id (string in JWT; caller parses to number)
  lab: number;
  role: 'admin' | 'member';
  iat: number;
  exp: number;
};

function getSessionSecret(): Uint8Array {
  const secret = process.env.SESSION_SECRET;
  if (!secret || secret.length < 64) {
    throw new Error('SESSION_SECRET missing or too short (< 64 hex chars)');
  }
  return new TextEncoder().encode(secret);
}

// --------------------------------------------------------------------
// Middleware entry
// --------------------------------------------------------------------

export async function middleware(req: NextRequest): Promise<NextResponse> {
  const { pathname } = req.nextUrl;

  if (isPublic(pathname)) {
    return NextResponse.next();
  }

  const cookie = req.cookies.get('pi_session');
  if (!cookie) {
    return redirectOrUnauthorized(req, 'SESSION_EXPIRED');
  }

  let payload: SessionPayload;
  try {
    const { payload: verified } = await jwtVerify(cookie.value, getSessionSecret());
    payload = verified as unknown as SessionPayload;
  } catch {
    return redirectOrUnauthorized(req, 'SESSION_EXPIRED');
  }

  // Admin-only gate (DB revocation check deferred to Server Component)
  if (isAdminRoute(pathname) && payload.role !== 'admin') {
    return jsonError(403, 'NOT_ADMIN', '仅管理员可操作');
  }

  // Forward decoded identity to downstream Server Components via headers.
  // TODO(T028): `getCurrentSeat()` in src/lib/auth/session.ts reads these,
  // then additionally queries `sessions` table to enforce revoked_at IS NULL.
  const headers = new Headers(req.headers);
  headers.set('x-seat-id', payload.sub);
  headers.set('x-lab-id', String(payload.lab));
  headers.set('x-role', payload.role);

  return NextResponse.next({ request: { headers } });
}

// --------------------------------------------------------------------
// Response helpers
// --------------------------------------------------------------------

function redirectOrUnauthorized(req: NextRequest, code: string): NextResponse {
  // Browser navigation → 302 to /login; API calls → 401 JSON
  const accept = req.headers.get('accept') ?? '';
  if (accept.includes('text/html')) {
    const loginUrl = new URL('/login', req.url);
    loginUrl.searchParams.set('redirect', req.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }
  return jsonError(401, code, '登录已过期,请重新登录');
}

function jsonError(status: number, code: string, message: string): NextResponse {
  return NextResponse.json({ error: { code, message } }, { status });
}

// --------------------------------------------------------------------
// Config · which paths go through the middleware
// --------------------------------------------------------------------

export const config = {
  matcher: [
    // Everything except Next internals and static assets.
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:png|jpg|svg|css|js|woff2?)$).*)',
  ],
};
