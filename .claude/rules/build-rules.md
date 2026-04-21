---
paths:
  - projects/**
---

# Rules for code inside projects/

Loaded only when modifying files under any `projects/NNN-*/` directory.

## Context reference

Every session working here must be aware of:
1. Your task file at `specs/NNN-*/tasks/T<NNN>.md` — **read this first**
2. The overall spec at `specs/NNN-*/spec.md`
3. Your task's `file_domain` — you may not edit outside it

## TDD is mandatory

For any new behavior in `src/`:
1. Write a failing test in `tests/` that encodes the expected behavior
2. Run it, confirm it fails **for the right reason** (not because of a missing import)
3. Write the minimum implementation to make it pass
4. Run all tests to confirm no regression
5. Refactor; re-run tests

Do NOT:
- Write the implementation first and retrofit tests
- Skip tests because "it's trivial"
- Delete failing tests to unblock a commit

## Commit discipline

Conventional Commits, one logical change per commit:

```
feat(T003): add JWT token issuance

Body explains what and why. Wraps at 72 chars.
Reference the task file: closes specs/NNN-*/tasks/T003.md
```

Types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `perf`, `ci`, `build`.

Scope is always the task ID (or `all` for cross-cutting commits that touch foundation).

## Security rules

- No secrets in code, not even as "example" or "TODO" placeholders
- All sensitive config via env vars; documented in `.env.example` (no real values)
- No `eval` / `new Function()` / template strings for SQL / shell commands
- User input is untrusted until explicitly validated at the boundary

## Dependency additions

Adding a new dependency requires:
1. Entry in `specs/NNN-*/tech-stack.md` table with rationale
2. Justification in the commit message
3. Locked version in `package.json` (no `^` or `~` for production deps)
4. Run `pnpm audit --prod` after adding; 0 critical/high required

## Don't

- Edit shared files (package.json, tsconfig, CI) unless your task file says you own them
- Pull new libraries in the middle of a task — scope it first
- Introduce generated code that's not in `.gitignore`
- Leave `console.log` / `print()` debugging statements
- Leave `TODO` comments without a linked task ID
