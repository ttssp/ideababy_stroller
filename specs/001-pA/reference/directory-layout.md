# 目录布局 · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**对应 spec**: `spec.md` v0.2.1 · `architecture.md` v0.2 · `tech-stack.md` v0.1
**读者**: 1 名架构师 + 6–8 名初级工程师（写代码前必读）

> 本文件给下游 builder 一个**抄得下来就能跑**的工程蓝图。每个工程决策的权威来源在原 spec；本文件只把分散在 spec / tech-stack / 各 task file_domain 的"实际文件长什么样"汇总到一处，减少新人横向查找成本。遇到本文件与 spec.md / architecture.md / tech-stack.md 冲突时**以后者为准**。

---

## §1 完整目录树

下图列出 T001–T034 将创建的全部目录与关键文件。每个目录给出 1–3 句"这里放什么 / 不放什么"的注释。

```
pi-briefing/
├── .github/
│   └── workflows/
│       ├── ci.yml                       # typecheck + lint + test + build
│       └── drift-scan.yml               # drizzle schema.ts ↔ reference/schema.sql 漂移检测
├── .claude/
│   └── rules/                           # 项目级指令（inherited from repo 根；无需重复）
├── deploy/
│   ├── systemd/
│   │   ├── pi-briefing-web.service      # Next.js production server
│   │   ├── pi-briefing-worker.service   # oneshot worker；由 timer 触发
│   │   └── pi-briefing-worker.timer     # OnCalendar=*-*-* 06:00:00 Asia/Shanghai
│   ├── caddy/
│   │   └── Caddyfile                    # 反代 + 自动 Let's Encrypt
│   ├── postgres/
│   │   └── grants.sql                   # webapp_user / worker_user 权限脚本（T030）
│   └── credentials/
│       └── README.md                    # 如何把 API key 放进 /etc/pi-briefing/credentials/
├── docs/
│   ├── runbook/
│   │   ├── deploy.md                    # 冷启 VPS → 上线步骤
│   │   ├── backup-restore.md            # pg_dump 策略与恢复演练
│   │   └── self-report.md               # 周度 self-report 模板（T025 / T033）
│   └── README.md                        # 面向运维的一页快览（T031 预留）
├── projects/
│   └── 001-pA/
│       └── spikes/
│           └── T001-llm-provider-report.md   # T001 blind-test 产出（operator sign-off）
├── scripts/
│   ├── db-seed.ts                       # 创建 lab + 初始 topic（T003）
│   ├── validate-env.ts                  # CI / 部署前 env 自检（T007）
│   ├── pg-dump.sh                       # 日备脚本（T030）
│   ├── restic-backup.sh                 # 云盘副本（T030）
│   ├── export-import-round-trip.ts      # T032 E2E 的 round-trip 验证
│   └── seed-topics.ts                   # dev-only topic 种子（架构师自用）
├── src/
│   ├── app/
│   │   ├── layout.tsx                   # 根 layout；<html lang="zh-CN">
│   │   ├── page.tsx                     # "/" · 302 重定向到 /today（或 /login 未登录）
│   │   ├── (main)/
│   │   │   ├── layout.tsx               # 登录后的 shell（顶栏 + 导航）
│   │   │   ├── today/
│   │   │   │   └── page.tsx             # /today SSR briefing · 仅读 briefings 表
│   │   │   ├── topics/
│   │   │   │   ├── page.tsx             # /topics 列表 + admin CRUD
│   │   │   │   └── [id]/edit/page.tsx   # 编辑单个 topic
│   │   │   ├── papers/
│   │   │   │   └── [id]/history/page.tsx  # 某 paper 的 action + why 全历史（T017）
│   │   │   ├── breadcrumbs/
│   │   │   │   └── page.tsx             # breadcrumb 列表（T019）
│   │   │   └── resurface/
│   │   │       └── page.tsx             # resurface 触发列表（T022）
│   │   ├── admin/
│   │   │   ├── invite/page.tsx          # 生成 invite token + 复制链接（T027）
│   │   │   └── allow-continue/page.tsx  # Sentinel 签到页面（T026）
│   │   ├── login/
│   │   │   ├── page.tsx                 # 邮箱输入 / token 校验入口
│   │   │   └── verify/page.tsx          # 消费 invite token 建立 seat
│   │   └── api/
│   │       ├── actions/route.ts         # POST 写 actions 表（T015）
│   │       ├── topics/route.ts          # POST/GET topic CRUD（T009）
│   │       ├── topics/[id]/route.ts     # PATCH/DELETE 单 topic
│   │       ├── invite/route.ts          # admin 生成 invite token（T027）
│   │       ├── export/full/route.ts     # admin-only JSON 全量 export（T029）
│   │       ├── resurface/[id]/dismiss/route.ts   # dismiss resurface 事件（T023）
│   │       └── healthz/route.ts         # 监控探针（无 auth · 仅返 {ok:true, now})
│   ├── components/
│   │   ├── skip-why-input.tsx           # 红线 2 UI 层（D16 Layer 3）
│   │   ├── action-buttons.tsx           # 4-action 按钮组（T015）
│   │   ├── stale-banner.tsx             # worker 未跑 24h 时的软警告
│   │   ├── sentinel-banner.tsx          # day-30 < 3 seat 时的 escalate 横幅
│   │   └── ui/                          # 仅在极少量自绘原子组件时使用（不装 shadcn）
│   ├── lib/
│   │   ├── actions/
│   │   │   └── recordAction.ts          # 红线 2 API 层（D16 Layer 2）
│   │   ├── auth/
│   │   │   ├── invite.ts                # token 生成 / consume（T006）
│   │   │   ├── session.ts               # JWT sign/verify
│   │   │   └── middleware.ts            # require-auth / require-admin
│   │   ├── db/
│   │   │   ├── client.ts                # Drizzle · postgres driver · 两个 pool
│   │   │   └── roles.ts                 # webapp_user vs worker_user 切换
│   │   ├── llm/
│   │   │   ├── types.ts                 # SummaryRecord / RelationLabel 等
│   │   │   ├── provider.ts              # LLMProvider interface（ADR-4）
│   │   │   ├── anthropic.ts             # Claude adapter
│   │   │   ├── openai.ts                # GPT adapter
│   │   │   └── prompt-version.ts        # SUMMARY_PROMPT_VERSION 常量管理
│   │   ├── summary/
│   │   │   ├── persist.ts               # 事务写 llm_calls + paper_summaries（D15）
│   │   │   └── assembler.ts             # 组装 briefings row
│   │   ├── state-shift/
│   │   │   └── heuristic.ts             # §4.1 纯 SQL heuristic
│   │   ├── breadcrumbs/
│   │   │   └── record.ts                # 写 breadcrumbs 行 + 幂等
│   │   ├── resurface/
│   │   │   ├── timed.ts                 # 6w / 3mo / 6mo 调度
│   │   │   └── citation.ts              # citation-triggered 即时触发
│   │   ├── export/
│   │   │   ├── builder.ts               # JSON 文档组装（schema_version 1.1）
│   │   │   └── audit.ts                 # 写 export_log 行
│   │   ├── topics/
│   │   │   └── crud.ts                  # topic 读写 + empty-state 判断
│   │   ├── papers/
│   │   │   └── query.ts                 # /papers/:id/history 的查询
│   │   ├── arxiv/
│   │   │   ├── client.ts                # arXiv API fetcher（rate-limited）
│   │   │   └── parser.ts                # Atom / XML → papers row
│   │   └── env.ts                       # zod 校验 process.env（T007）
│   ├── workers/
│   │   ├── daily.ts                     # systemd timer 入口
│   │   ├── fetch-pass.ts                # arXiv fetch subroutine
│   │   ├── summary-pass.ts              # 事务写 paper_summaries
│   │   ├── state-shift-pass.ts          # heuristic + LLM judge 联合
│   │   ├── briefing-pass.ts             # 写 briefings 行
│   │   └── resurface-pass.ts            # 调 timed + citation 调度
│   └── db/
│       ├── schema.ts                    # Drizzle TS 定义（类型源头）
│       ├── types.ts                     # InferSelectModel / InferInsertModel
│       ├── index.ts                     # barrel（re-export schema + client + types）
│       └── migrations/
│           ├── 0000_initial.sql         # drizzle-kit generate 产出
│           ├── 0001_grants.sql          # 由 T030 在部署时 apply
│           └── meta/                    # drizzle-kit 的 snapshot metadata
├── tests/
│   ├── unit/
│   │   ├── actions.test.ts              # recordAction.ts 验证
│   │   ├── auth.test.ts                 # invite + session 单元
│   │   ├── state-shift.test.ts          # heuristic 边界
│   │   ├── summary-persist.test.ts      # 事务双表写入
│   │   └── export.test.ts               # schema_version 1.1 builder
│   ├── db/
│   │   ├── schema.test.ts               # 15 表 roundtrip（T003）
│   │   └── constraints.test.ts          # skip_requires_why + summary_sentence_cap
│   ├── env.test.ts                      # T007 env schema
│   ├── e2e/
│   │   ├── today-flow.spec.ts           # 登录 → /today → 4-action
│   │   ├── skip-requires-why.spec.ts    # 红线 2 UI 层闭合
│   │   ├── breadcrumb-resurface.spec.ts # 模拟 6 周时钟跳
│   │   ├── admin-export.spec.ts         # export → round-trip
│   │   └── sentinel-banner.spec.ts      # day-30 < 3 seat banner
│   └── fixtures/
│       ├── arxiv-abstracts/             # 离线 arXiv 样本
│       └── human-labeled-20.json        # T001 spike blind-test 语料
├── public/
│   ├── privacy.md                       # §3 数据使用声明（compliance.md）
│   └── favicon.ico                      # 纯装饰（可选）
├── .env.example                         # §3 的完整清单（禁止 commit 真实值）
├── .gitignore                           # 必含 .env* / node_modules / .next / dist
├── biome.json
├── drizzle.config.ts
├── lefthook.yml                         # pre-commit / commit-msg 钩子
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── next.config.mjs
├── playwright.config.ts
├── vitest.config.ts
├── next-env.d.ts                        # Next 自动生成，勿手改
└── README.md
```

**目录职责说明**（初级工程师常问）：

- `deploy/` 只放**部署产物**（systemd unit / Caddyfile / grants.sql）；绝不放可执行业务代码。`deploy/credentials/` 的 README 指引如何把 API key 存进 `/etc/pi-briefing/credentials/`，**不得**在此目录 checkin 实际 key 文件。
- `docs/runbook/` 面向**运维人**（= operator 本人），不是面向最终用户。用户文档位于 `public/privacy.md`。
- `scripts/` 用 `tsx` 直接跑的**一次性 / 运维 CLI**；任何会被业务代码 import 的模块必须在 `src/lib/`。
- `src/app/(main)/` 使用 Next 15 route group 语法——括号目录不参与 URL 段；内部放"登录后 shell"的所有页面。
- `src/db/schema.ts` 是 Drizzle TS 定义（类型源头），`src/db/migrations/0000_initial.sql` 是 `drizzle-kit generate` 产出的 authoritative DDL，`reference/schema.sql` 是**人读版**——三者通过 CI 互证无漂移（见 §9）。
- `src/workers/daily.ts` 是 **systemd worker 入口**；不被 Next.js 进程 import，失败不拖垮 Web（见 DECISIONS-LOG 2026-04-23 "单进程 vs 多进程部署"）。
- `tests/e2e/` 跑 Playwright；`tests/unit/` 与 `tests/db/` 跑 vitest。`tests/db/` 必须连真实 Postgres（CI 里用 service container）；其余单元测试 100% 离线。
- `public/` 只放**纯静态、对外可见**的文件；隐私声明 `privacy.md` 链在首页 footer。

---

## §2 package.json 依赖清单

完整版本锁以 `tech-stack.md §5` 为准；下方样板已对齐该锁定。

```json
{
  "name": "pi-briefing",
  "version": "0.0.1",
  "private": true,
  "engines": {
    "node": "22.x",
    "pnpm": "9.x"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "worker:daily": "tsx src/workers/daily.ts",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "lint": "biome ci .",
    "format": "biome format --write .",
    "typecheck": "tsc --noEmit",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:studio": "drizzle-kit studio",
    "db:seed": "tsx scripts/db-seed.ts",
    "validate-env": "tsx scripts/validate-env.ts",
    "export:round-trip": "tsx scripts/export-import-round-trip.ts"
  },
  "dependencies": {
    "next": "15.0.3",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "typescript": "5.6.3",
    "drizzle-orm": "0.36.0",
    "postgres": "3.4.5",
    "zod": "3.23.8",
    "date-fns": "4.1.0",
    "nodemailer": "6.9.16",
    "fast-xml-parser": "4.5.0",
    "jose": "5.9.6"
  },
  "devDependencies": {
    "@biomejs/biome": "1.9.4",
    "drizzle-kit": "0.27.0",
    "vitest": "^3.0.0",
    "@playwright/test": "^1.48.0",
    "@types/node": "22.10.1",
    "@types/nodemailer": "6.4.16",
    "tsx": "^4.19.0",
    "lefthook": "^1.8.0"
  }
}
```

**注**：
- **production 依赖精确 pin**（无 `^` / `~`；tech-stack.md §4）；devDeps 可用 `^`。
- **T001 spike 通过后**才追加 `@anthropic-ai/sdk` 或 `openai`，**只加一个**（tech-stack.md §5 备注）。
- production dep 上限 30 个（tech-stack.md §4）；当前 11 个 → buffer 19 个。

### §2.1 依赖 rationale（每个依赖为什么在这）

| 包 | 用途 | 为什么是它而不是别的 |
|---|---|---|
| `next` | Web framework · SSR · Server Actions | tech-stack.md §1 · 覆盖所有 v0.1 交互；App Router 支持 /today SSR |
| `react` / `react-dom` | UI 渲染 | Next 的伴随依赖；版本跟随 Next 15 |
| `typescript` | 编译器 | CLAUDE.md 项目偏好；strict 模式靠它 |
| `drizzle-orm` | ORM | tech-stack.md §1 · 比 Prisma 轻 40% · migration 即 SQL 文件 |
| `postgres` | DB driver | Drizzle 官方推荐；无 connection pool 地狱 |
| `zod` | 运行时 schema 校验 | env 启动期 fail-fast；API 请求体校验 |
| `date-fns` | 日期 | tree-shake 友好；不用 moment |
| `nodemailer` | SMTP | 备用——DECISIONS-LOG 2026-04-23 决议 invite 不发邮件，但保留 lib 以防 v0.1 晚期启用 |
| `fast-xml-parser` | arXiv Atom feed 解析 | 10kb；不拉 xml2js 等重型库 |
| `jose` | JWT sign/verify | 比 jsonwebtoken 新；对 Edge runtime 友好 |
| `@biomejs/biome` | lint + format | 一个二进制替 ESLint + Prettier |
| `drizzle-kit` | migration 生成 | Drizzle 的 CLI 伴侣 |
| `vitest` | 单元测试 | CLAUDE.md 项目偏好；Node 原生 test runner 生态仍不完整 |
| `@playwright/test` | E2E | 跨浏览器；Next 官方推荐 |
| `@types/node` | Node 类型 | TS strict 必需 |
| `@types/nodemailer` | 类型 | nodemailer 无内置类型 |
| `tsx` | 直接跑 TS 脚本 | `scripts/*.ts` 的运行器；避免先 build |
| `lefthook` | git 钩子管理 | 比 husky 轻；pre-commit 跑 biome + tsc |

**刻意不装**（摘自 tech-stack.md §3，仅列初级工程师最易误装的）：Supabase / Firebase · Vercel AI SDK · tRPC · Prisma · Redis · BullMQ · Docker · shadcn / Radix · pgvector · axios · moment。

---

## §3 .env.example

下方是 v0.1 完整环境变量清单，**不含任何真实值**。operator `cp .env.example .env` 后逐个替换。**CI 在每次 install 后跑 `pnpm validate-env` 以防 .env.example 与 zod schema 漂移**。

```bash
# ====================================================================
# pi-briefing v0.1 env template · 2026-04-23
# 复制到 .env 后填写；绝对不要 commit 带真实值的 .env
# （.gitignore 已含 .env*，但仍要做 gitleaks 扫描 · SEC-3）
# ====================================================================

# --- Application ---
NODE_ENV=development                    # development|production|test
APP_ORIGIN=http://localhost:3000        # full base URL incl scheme
APP_TIMEZONE=Asia/Shanghai              # used by worker cron + DST 处理

# --- Postgres ---
# webapp_user: SELECT/INSERT/UPDATE on user-facing tables
DATABASE_URL=postgres://webapp_user:REPLACE@localhost:5432/pi_briefing
# worker_user: 额外 INSERT 权限到 papers / briefings / llm_calls / paper_summaries
DATABASE_URL_WORKER=postgres://worker_user:REPLACE@localhost:5432/pi_briefing
DATABASE_POOL_WEBAPP=5                  # webapp_user pool size
DATABASE_POOL_WORKER=2                  # worker_user pool size

# --- LLM provider binding (post-T001 spike) ---
# T001 spike 未跑完前两项都填 claude 即可（adapter 是 stub）
LLM_PROVIDER=anthropic                  # anthropic|openai
LLM_FALLBACK_PROVIDER=openai            # primary outage 时使用
ANTHROPIC_API_KEY=sk-ant-REPLACE_ME
ANTHROPIC_MODEL=claude-sonnet-4-6-20250701
OPENAI_API_KEY=sk-REPLACE_ME
OPENAI_MODEL=gpt-5.4-turbo
LLM_MONTHLY_COST_USD_CAP=50             # enforced by worker; alert at $40 (C11)

# --- arXiv ---
ARXIV_API_BASE=http://export.arxiv.org/api/query
ARXIV_RATE_LIMIT_MS=3000                # per arXiv ToS · ≤ 1 req / 3s (LEG-2)

# --- Auth ---
# SESSION_SECRET 必须 ≥ 32 字节；用 `openssl rand -hex 32` 生成
SESSION_SECRET=REPLACE_WITH_64_HEX_CHARS
INVITE_TOKEN_TTL_HOURS=24               # T006 · 单次使用 + 24h 有效

# --- SMTP (optional in v0.1 · DECISIONS-LOG invite 不发邮件) ---
# 若启用邮件通道就填写；否则留空字符串不启用
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
SMTP_FROM=operator@example.com

# --- Cron / worker ---
WORKER_DAILY_TIME=06:00                 # HH:MM 在 APP_TIMEZONE
WORKER_CATCHUP_WINDOW_HOURS=24          # on-boot catchup 窗口

# --- Dogfood / bootstrap ---
LAB_DEFAULT_NAME=My Research Lab        # scripts/db-seed.ts 写入 labs.name
ADMIN_EMAIL=operator@example.com        # scripts/db-seed.ts 建 admin seat

# --- Observability ---
LOG_LEVEL=info                          # debug|info|warn|error
ALERT_EMAIL=operator@example.com        # pg-dump 失败 / cron 漏跑告警收件

# --- Feature flags (保持默认即可) ---
SENTINEL_ENABLED=true                   # day-30 < 3 seat banner 开关（T026）
STALE_BANNER_ENABLED=true               # worker 未跑 24h 软警告
```

**敏感 env 注入规则**：`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `SESSION_SECRET` 在生产通过 `systemd LoadCredential=` 注入到 `${CREDENTIALS_DIRECTORY}/<name>` 文件（见 T007 systemd unit + SEC-3），**不**放到 `/etc/pi-briefing/env` 的 EnvironmentFile 里。`DATABASE_URL*` 这种非极敏感的可以放 EnvironmentFile。

---

## §4 tsconfig.json

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "allowJs": false,
    "jsx": "preserve",
    "incremental": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/lib/*": ["src/lib/*"],
      "@/db": ["src/db/index.ts"],
      "@/db/*": ["src/db/*"]
    },
    "plugins": [{ "name": "next" }]
  },
  "include": ["src", "tests", "scripts", "next-env.d.ts", ".next/types/**/*.ts"],
  "exclude": ["node_modules", ".next", "dist"]
}
```

**非默认 flag 说明**（初级工程师首次读 tsconfig 常问）：

| flag | 作用 | 为什么启用 |
|---|---|---|
| `strict` | 启动 8 个严格检查 | CLAUDE.md 偏好 + tech-stack.md §1 · 编译期抓 bug |
| `noUncheckedIndexedAccess` | `arr[i]` 类型为 `T \| undefined` | Next 15 路由参数访问 + Drizzle 结果数组 |
| `noImplicitOverride` | 子类 override 必须写 `override` | 减少继承 bug（v0.1 少用 OO，但开着无成本） |
| `exactOptionalPropertyTypes` | `?: T` 与 `: T \| undefined` 严格区分 | zod schema 与 Drizzle 类型对齐 |
| `isolatedModules` | 每文件能独立编译 | Next 的 SWC 转译器要求 |
| `moduleResolution: bundler` | Next 15 + Drizzle 混合解析 | 避免 NodeNext 对 .ts → .js 的强制 |
| `jsx: preserve` | 交给 Next 编译 | Next 自己处理 JSX |
| `allowJs: false` | 禁 JS 文件入 src | 保强类型边界 |
| `skipLibCheck` | 跳过 deps 的类型检查 | Drizzle / Next 升级时避免级联挂 |

`paths` 别名策略：业务代码一律用 `@/lib/...` / `@/components/...`；禁止相对路径超过 2 级（`../../../`）——新人一眼看不懂的就是坏代码。

---

## §5 biome.json

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": { "enabled": true },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "all",
      "semicolons": "always"
    },
    "jsxRuntime": "reactJsx"
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": {
        "noNonNullAssertion": "error",
        "useConst": "error",
        "useTemplate": "error"
      },
      "suspicious": {
        "noExplicitAny": "error",
        "noConsoleLog": "warn"
      },
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error"
      },
      "complexity": {
        "noExcessiveCognitiveComplexity": { "level": "warn", "options": { "maxAllowedComplexity": 15 } }
      }
    }
  },
  "files": {
    "ignore": [".next", "dist", "node_modules", "src/db/migrations/**", "public/**"]
  }
}
```

**Rule 说明**：
- `noNonNullAssertion: error` — 禁止 `foo!.bar`；配合 `noUncheckedIndexedAccess` 强制空值显式处理。
- `noExplicitAny: error` — any 完全禁（若第三方库逼我们写 any，写 `unknown` + 类型守卫）。
- `noConsoleLog: warn` — prod 代码用 `src/lib/log.ts` 统一日志，console.log 仅开发。
- `noExcessiveCognitiveComplexity` — 单函数复杂度超 15 强烈提示拆分。

---

## §6 drizzle.config.ts

```ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  dialect: 'postgresql',
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dbCredentials: {
    // drizzle-kit generate / migrate 用 superuser 连接；prod 不会直接跑 migrate
    // 而是 apply 预先 generate 的 0000_initial.sql。
    url: process.env.DATABASE_URL ?? '',
  },
  verbose: true,
  strict: true,
});
```

**注**：
- `strict: true` 让 `drizzle-kit generate` 在检测到手写 SQL 与 schema.ts 不一致时 abort（防 drift）。
- `dbCredentials.url` 用 `DATABASE_URL`（webapp_user）而非 worker URL —— generate/migrate 只关心 DDL，不关心 role；但实际 prod apply DDL 由 operator 用 superuser 跑一次（部署 runbook）。

---

## §7 playwright.config.ts

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,  // e2e 之间共享 Postgres → 串行更可靠
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } },
    },
  ],
  webServer: process.env.CI
    ? {
        command: 'pnpm start',
        url: 'http://localhost:3000/api/healthz',
        reuseExistingServer: false,
        timeout: 120_000,
      }
    : undefined,
});
```

**注**：
- v0.1 仅 desktop 1280 × 800（Scope OUT-5 · 无 mobile）。
- `fullyParallel: false` 因 Postgres schema 共享；v0.2 可改用 schema-per-worker 后再开并行。
- CI 启动时用 `pnpm start`（已 build 的 production server）而非 `pnpm dev`，更接近生产。

---

## §8 vitest.config.ts

```ts
import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    environment: 'node',
    globals: false,
    include: ['tests/unit/**/*.test.ts', 'tests/db/**/*.test.ts', 'tests/env.test.ts'],
    exclude: ['tests/e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.d.ts', 'src/db/migrations/**'],
      thresholds: { lines: 60, functions: 60, branches: 50, statements: 60 },
    },
    poolOptions: {
      threads: { singleThread: false, maxThreads: 4 },
    },
    testTimeout: 15_000,
    hookTimeout: 30_000,
  },
});
```

**注**：
- `tests/db/**` 需要真实 Postgres（CI 用 `services: postgres:16` 起 container）；`tests/unit/**` 全离线。
- `tsconfig-paths` plugin 让 vitest 识别 `@/lib/...` 别名。
- 覆盖率阈值 v0.1 设 60/50 · v1.0 时提到 80/70（SLA.md 对齐）。

**devDeps 需要补 `vite-tsconfig-paths`**——此包不在 §2 样板中，是 vitest 运行 alias 所必需；T008 task 启用 vitest 时需追加到 devDeps（属于 T008 scope）。

---

## §9 CI pipeline (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    name: typecheck + lint + test + build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: pi_briefing_test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    env:
      DATABASE_URL: postgres://postgres:postgres@localhost:5432/pi_briefing_test
      DATABASE_URL_WORKER: postgres://postgres:postgres@localhost:5432/pi_briefing_test
      SESSION_SECRET: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
      LLM_PROVIDER: anthropic
      LLM_FALLBACK_PROVIDER: openai
      ANTHROPIC_API_KEY: dummy
      OPENAI_API_KEY: dummy
      APP_ORIGIN: http://localhost:3000
      NODE_ENV: test
      ADMIN_EMAIL: ci@example.com
      LAB_DEFAULT_NAME: CI Lab
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 22.x
          cache: 'pnpm'
      - name: Install dependencies (frozen)
        run: pnpm install --frozen-lockfile
      - name: Audit (production deps only)
        run: pnpm audit --prod --audit-level=high
      - name: Validate env schema
        run: pnpm validate-env
        env:
          DATABASE_URL: ${{ env.DATABASE_URL }}
      - name: Typecheck
        run: pnpm typecheck
      - name: Lint + format check
        run: pnpm lint
      - name: Apply migrations
        run: psql "$DATABASE_URL" -f specs/001-pA/reference/schema.sql
      - name: Unit + DB tests
        run: pnpm test
      - name: Build
        run: pnpm build

  schema-drift:
    name: drizzle ↔ reference/schema.sql drift scan
    runs-on: ubuntu-latest
    needs: check
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 22.x
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      # 让 drizzle-kit generate 的 0000_initial.sql 与 reference/schema.sql
      # 在表 / 列 / CHECK / index 级别一致；如漂移就 fail
      - run: pnpm db:generate
      - name: Diff drizzle migration vs reference
        run: |
          node scripts/compare-ddl.js \
            --drizzle src/db/migrations/0000_initial.sql \
            --reference specs/001-pA/reference/schema.sql \
            --fail-on-drift

  # ------------------------------------------------------------------
  # export-route-scan (Hardening H5 · R1 deferred by operator)
  # ------------------------------------------------------------------
  # 启用条件：H5 闭合 + operator sign-off。一旦启用，此 job 扫描
  # `src/app/api/export/**/route.ts` 内是否 import `requireAdmin`。
  # 当前**注释掉**；文件位置保留供未来 plug-in。
  # ------------------------------------------------------------------
  # export-route-scan:
  #   name: require-admin presence on export routes
  #   runs-on: ubuntu-latest
  #   steps:
  #     - uses: actions/checkout@v4
  #     - name: Grep all export routes for requireAdmin import
  #       run: |
  #         routes=$(find src/app/api/export -name route.ts 2>/dev/null || true)
  #         [ -z "$routes" ] && { echo "no export routes yet"; exit 0; }
  #         fail=0
  #         for f in $routes; do
  #           if ! grep -q 'requireAdmin' "$f"; then
  #             echo "::error file=$f::export route missing requireAdmin import"
  #             fail=1
  #           fi
  #         done
  #         exit $fail
```

**scripts/compare-ddl.js 的职责**（将与 CI 同期实现；当前为未来占位）：
- 解析两份 SQL，提取 `CREATE TABLE ...` 列结构、`CHECK` 谓词、`CREATE INDEX`；
- 忽略注释、空行、格式差异；
- 任一差异 → non-zero exit。

---

## §10 Pre-commit 钩子（推荐）

使用 **lefthook**（比 husky 轻；配置一个 yaml 即可）。

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    biome:
      glob: '*.{ts,tsx,js,json,jsonc}'
      run: pnpm biome check --write {staged_files}
      stage_fixed: true
    typecheck:
      run: pnpm typecheck

commit-msg:
  commands:
    conventional-commits:
      run: |
        grep -qE '^(feat|fix|chore|docs|test|refactor|perf|ci|build|revert)(\([a-z0-9-]+\))?!?: .+' {1} \
          || { echo "commit subject must be Conventional Commits (CLAUDE.md)"; exit 1; }
```

**初始化**：`pnpm lefthook install` 在仓库 clone 后一次即可。

---

## §11 First-time setup runbook

> 从 clone 到 green CI 的**逐行**步骤。初级工程师照抄即可。

```bash
# 1. Clone & enter
git clone git@github.com:<org>/pi-briefing.git
cd pi-briefing

# 2. Toolchain
nvm install 22      # 或 mise use node@22
corepack enable     # pnpm 9
pnpm -v             # → 9.x

# 3. Dependencies
pnpm install --frozen-lockfile

# 4. Env
cp .env.example .env
# 用编辑器填入：
#   DATABASE_URL=postgres://<localuser>@localhost:5432/pi_briefing
#   DATABASE_URL_WORKER= 同上（本地 dev 用同一 superuser 可）
#   SESSION_SECRET=$(openssl rand -hex 32)
#   ANTHROPIC_API_KEY= 先填 sk-ant-xxx 占位（T001 spike 前不会真实调用）
#   ADMIN_EMAIL=your@email.com
pnpm validate-env   # 必须 exit 0

# 5. Postgres
# macOS: brew services start postgresql@16
# Ubuntu: sudo systemctl start postgresql
createdb pi_briefing
psql -d pi_briefing -f specs/001-pA/reference/schema.sql
# 或等 T003 落地后改用：pnpm db:migrate

# 6. Seed
pnpm db:seed         # 写入 labs + 示例 topic（T003）

# 7. Typecheck / lint / test
pnpm typecheck
pnpm lint
pnpm test

# 8. 本地跑
pnpm dev
# 打开 http://localhost:3000

# 9. 跑 worker 一次（T011 落地后可用）
pnpm worker:daily

# 10. 提交前
pnpm lefthook install  # 一次性
# 然后正常 git commit —— pre-commit 会跑 biome + typecheck
```

**常见首次坑**：

| 现象 | 原因 | 解法 |
|---|---|---|
| `pnpm install` 卡在某个包 | 国内网络 | 用 `pnpm config set registry https://registry.npmmirror.com` |
| `psql: FATAL: role "webapp_user" does not exist` | 本地 dev 没造角色 | dev 阶段直接用 DATABASE_URL=`postgres://<本机用户>@localhost:5432/pi_briefing`；生产才走 webapp_user |
| `pnpm dev` 启动报 zod error | `.env` 缺 key | `pnpm validate-env` 报哪个 key 就补哪个 |
| `pnpm test` 卡 DB 测试 | 未起 Postgres | `pg_isready` 检查；或 skip `tests/db/**` 用 `pnpm vitest run tests/unit` |
| Playwright 下载 chromium 慢 | 首次装浏览器 | `PLAYWRIGHT_DOWNLOAD_HOST=` 走清华镜像 |

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 11 节 · 与 spec.md v0.2.1 / tech-stack.md v0.1 / architecture.md v0.2 对齐 |
