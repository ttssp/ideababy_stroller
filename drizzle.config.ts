// Drizzle Kit 配置 · 仅用于 generate / migrate / studio
// schema.ts(类型源头) → migrations/*.sql(authoritative DDL)
// 严格 strict 模式:手写 SQL 与 schema.ts 漂移即 abort,防 drift(directory-layout §6)
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  dialect: 'postgresql',
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dbCredentials: {
    // generate / migrate 用的连接;prod apply DDL 由 operator 用 superuser 一次性跑
    url: process.env.DATABASE_URL ?? '',
  },
  verbose: true,
  strict: true,
});
