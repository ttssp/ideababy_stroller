# Local Dev Setup · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**读者**: 本项目初级工程师 day-1 第一件事就是跑完本文档
**时长预算**: ≤ 30 分钟(clone → CI-等价本地绿)

> 本文档是"clone 到 green"的**逐行 checklist**。照抄即可。遇坑看 §4 troubleshooting。与 `reference/directory-layout.md §11` 的 setup 步骤一致;本文档更详细解释每步**为什么**、**看到什么算成功**。

---

## §1 前置要求(5 分钟)

在 macOS 或 Ubuntu 22.04+ 上。Windows 用 WSL2(Ubuntu 22.04 发行版)。

| 工具 | 版本 | 检查命令 | 没有时怎么装 |
|---|---|---|---|
| git | ≥ 2.40 | `git --version` | macOS: `xcode-select --install` · Ubuntu: `apt install git` |
| Node | **22.x LTS** | `node -v` | `nvm install 22` 或 `mise use node@22` · **不要用** 23 / 20 |
| pnpm | **9.x** | `pnpm -v` | `corepack enable` 或 `npm i -g pnpm@9` |
| Postgres | **16.x** | `psql --version` | macOS: `brew install postgresql@16 && brew services start postgresql@16` · Ubuntu: `apt install postgresql-16` |
| openssl | any | `openssl version` | macOS / Ubuntu 自带 |

**注意**:
- Node 必须是 22 LTS;22.11+ 也行,但不要用奇数主版本
- pnpm 9 才有 `--frozen-lockfile` 与 `pnpm audit signatures`(CI 依赖)

---

## §2 从 clone 到 green 的 15 步 checklist

**你的终点判断**:第 15 步跑 `pnpm test` 全绿 + `pnpm build` 成功退出。

### Step 1 · Clone 并进入仓库

```bash
git clone git@github.com:<org>/pi-briefing.git
cd pi-briefing
```

**看到什么算成功**:`pwd` 输出以 `pi-briefing` 结尾,`ls specs/001-pA/` 能看到 `spec.md` 等文件。

### Step 2 · 确认 Node / pnpm 版本锁

```bash
node -v    # 应 v22.x.x
pnpm -v    # 应 9.x.x
```

如果不对 → 用 nvm / corepack 切回。

### Step 3 · 安装依赖

```bash
pnpm install --frozen-lockfile
```

**看到什么算成功**:最后一行 `Progress: resolved XXX, reused XXX, downloaded 0, added 0` + 退出码 0。

**第一次安装大约 2–5 分钟**(取决于网络;国内可设 `pnpm config set registry https://registry.npmmirror.com`)。

### Step 4 · 生成 SESSION_SECRET

```bash
openssl rand -hex 32
# 输出一个 64 字符的 hex 串,复制保留备用
```

### Step 5 · 创建 `.env`

```bash
cp .env.example .env
```

用编辑器打开 `.env`,**至少**填好以下字段(其余保持默认或空):

```bash
NODE_ENV=development
APP_ORIGIN=http://localhost:3000
DATABASE_URL=postgres://<你的本机用户>@localhost:5432/pi_briefing
DATABASE_URL_WORKER=postgres://<你的本机用户>@localhost:5432/pi_briefing
SESSION_SECRET=<step 4 生成的 64 字符>
ANTHROPIC_API_KEY=sk-ant-placeholder
OPENAI_API_KEY=sk-placeholder
LLM_PROVIDER=anthropic
ADMIN_EMAIL=your.email@example.com
ALERT_EMAIL=your.email@example.com
```

**为什么用本机用户名作 DB user**:dev 本地不造 `webapp_user` / `worker_user` 角色(那是生产拿 `deploy/postgres/grants.sql` 创建的);dev 直接用 superuser 连即可。
**LLM API key 占位符**是合法的,T001 spike 之前不会真正调用。

### Step 6 · 校验 env schema

```bash
pnpm validate-env
```

**看到什么算成功**:`ok — all required env keys present and type-valid`,退出码 0。
**失败时**:会列出缺失 / 类型不对的字段 —— 按提示补 `.env`。

### Step 7 · 起本地 Postgres

macOS:
```bash
brew services start postgresql@16
pg_isready              # 输出 "accepting connections"
```

Ubuntu:
```bash
sudo systemctl start postgresql
pg_isready
```

### Step 8 · 创建数据库

```bash
createdb pi_briefing
```

**失败排错**:如果报 `role "<你的用户>" does not exist`,说明 Postgres 初始化时没给你造 superuser:
```bash
sudo -u postgres createuser --superuser $USER
createdb pi_briefing
```

### Step 9 · 应用 schema

**在 T003 落地之前**(即 `src/db/schema.ts` 还不存在):直接应用 reference SQL。
```bash
psql -d pi_briefing -f specs/001-pA/reference/schema.sql
```

**T003 合并之后**(即 `src/db/schema.ts` 已就位):使用 Drizzle。
```bash
pnpm db:migrate
```

**看到什么算成功**:两种方式最后都跑:
```bash
psql -d pi_briefing -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
#  count
# -------
#     15
```

15 张表 = 对的。

### Step 10 · Seed 初始数据

```bash
pnpm db:seed
```

**看到什么算成功**:`seeded lab: My Research Lab (id=1)` + `seeded topic: ...`(可选)+ 退出码 0。

### Step 11 · TypeScript 检查

```bash
pnpm typecheck
```

**看到什么算成功**:退出码 0,无 error。有 warning 可以忽略(`skipLibCheck` 允许 node_modules 有小问题)。

### Step 12 · Lint + format 检查

```bash
pnpm lint
```

**看到什么算成功**:`Checked XXX files in XXms. No fixes needed.`

如果报 "X errors" → 跑 `pnpm format` 自动修 格式类问题;剩余 logical 问题手工修。

### Step 13 · 单元 + DB 测试

```bash
pnpm test
```

**看到什么算成功**:`Test Files XX passed (XX)` + `Tests XXX passed (XXX)` + 退出码 0。
**有失败时**:看失败的测试名,去对应的 `tests/unit/*.test.ts` 文件里读 assertion。

### Step 14 · Build

```bash
pnpm build
```

**看到什么算成功**:最后 `✓ Compiled successfully` + `Route (app)` 表格 + 退出码 0。
用时约 30s–2min(首次)。

### Step 15 · 本地跑

```bash
pnpm dev
```

浏览器打开 `http://localhost:3000/api/healthz`:
```json
{"status":"ok","uptimeSec":3,"version":"dev","now":"2026-04-23T..."}
```

### (可选) Step 16 · lefthook git hooks

首次 clone 后跑一次:
```bash
pnpm lefthook install
```

之后每次 `git commit` 会自动跑 biome + typecheck;commit message 会被 conventional-commits 正则校验。

---

## §3 可选:跑 E2E 测试

```bash
pnpm playwright install chromium       # 首次需下载 ~120MB
pnpm test:e2e
```

**看到什么算成功**:`X passed` 行 + 退出码 0。国内网络可先 `export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright` 再下载。

---

## §4 Troubleshooting(高频坑)

| 现象 | 原因 | 解法 |
|---|---|---|
| `pnpm install` 卡住某个包 | 国内 npm 镜像慢 | `pnpm config set registry https://registry.npmmirror.com` 后重跑 |
| `psql: FATAL: role "<user>" does not exist` | Postgres 初始化漏了 superuser | `sudo -u postgres createuser --superuser $USER` |
| `pnpm dev` 启动报 `ENV_INVALID` zod 错 | `.env` 缺某个 key | 跑 `pnpm validate-env`,按报错补 |
| `createdb pi_briefing` 报 `database already exists` | 之前跑过 | `dropdb pi_briefing && createdb pi_briefing`(**会丢 local 数据**) |
| `pnpm test` 里 `tests/db/` 用例卡住 | Postgres 没起 | `pg_isready` 先确认;若 CI-only 机子,临时 `pnpm vitest run tests/unit` |
| Playwright 装 chromium 慢 | 默认从 Google 下 | `export PLAYWRIGHT_DOWNLOAD_HOST=...` 走镜像 |
| `pnpm typecheck` 报 `Cannot find module '@/lib/...'` | tsconfig 路径没识别 | 确认 `tsconfig.json` 里 `paths` 配置未被编辑器覆盖;重启 VSCode |
| `pnpm build` 报 `Module not found: '@anthropic-ai/sdk'` | LLM SDK 尚未安装(T001 之前) | 正常;这个 SDK 在 T001 spike 后才加入 package.json。 skeleton 的 import 会在 T004 PR 里真正变可解析 |
| `pnpm dev` 起来后登录失败循环 | invite 链接 token 已消费 | admin 重新生成(`/admin/invite`)一个新 token |
| 第一次跑 worker 没有 output | 你在 T011 landing 之前 | 正常;`skeletons/worker-daily.ts` 里 5 个 pass 都 throw TODO,等 T011 PR |

---

## §5 "Clone 到 green"≤ 30 min 的拆解

| 阶段 | 预期时长 | 占比 |
|---|---|---|
| Step 1–3 (clone + install) | 5 min | 17% |
| Step 4–6 (env setup) | 3 min | 10% |
| Step 7–10 (postgres + schema + seed) | 5 min | 17% |
| Step 11–14 (typecheck / lint / test / build) | 10 min | 33% |
| Step 15–16 (run + hooks) | 2 min | 7% |
| Buffer for one trouble shoot hit | 5 min | 16% |
| **总** | **30 min** | 100% |

**如果你超过 45 分钟仍未到 Step 15**:停下来找架构师 / 资深同学 pair 一次 —— 项目上手难度不应该更高;大概率环境某处出了非本文档覆盖的坑,收录进 `docs/runbook/onboarding-issues.md` 造福后来人。

---

## §6 日常开发 loop(setup 完之后)

```bash
# 1. 切换到你的 task 分支
git checkout -b feat/T015-skip-why-input

# 2. 开发时持续跑
pnpm dev            # 前端 hot reload
pnpm test:watch     # 测试 watch 模式

# 3. 提交前必跑
pnpm typecheck && pnpm lint && pnpm test

# 4. 提交
git add .
git status --untracked-files=all     # 确认无遗漏(CLAUDE.md 规范)
git commit -m "feat(T015): add skip-why-input component"

# 5. push 前跟 operator 确认一次(CLAUDE.md)
```

---

## §7 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 15 步 setup + troubleshooting · 对齐 directory-layout §11 |
