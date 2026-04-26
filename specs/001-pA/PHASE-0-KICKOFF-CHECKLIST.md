# Phase 0 启动 Checklist · 001-pA

**Purpose**: 在 operator 真正 kickoff Phase 0（第一个 `git commit` 之前）逐条确认。
**读者**: operator（本人）。不是初级工程师。
**预计**: 对照 30–60 分钟。

> ✅ = 已就位 · ⚠️ = 需要你/环境行动 · ❓ = 需你判断

---

## §0 · 前置决策（必须明确回答）

- [ ] **Codex R_final verdict 是什么**？
  - 已读 `.codex-outbox/20260423T175614-001-pA-L4-adversarial-r_final.md` → CLEAN / CLEAN-WITH-NOTES / CONCERNS / BLOCK
  - 如果 BLOCK：不启动 Phase 0，按 `STATUS.md § 应急路径` 修
  - 如果 CLEAN-WITH-NOTES 或 CONCERNS：是否接受"进 Phase 0 + 记 risks.md"？
    - 接受 → 继续
    - 不接受 → surgical patch
- [ ] **dogfood 名单**（per PRD Q6 = 自用为主）
  - operator 自己（1 seat）
  - lab-internal operator #1：姓名 / 每周投入（建议 ≥ 3 天 ≥ 10 分钟/天）
  - lab-internal operator #2：姓名 / 每周投入
  - 如果只有 operator 自己：**接受降级**，risks.md DOGFOOD-1 sentinel 在 day-30 触发后必须面对
- [ ] **5 周时间窗口是否真有？**
  - 预计 kickoff 日期：\_\_\_\_\_\_\_\_\_\_
  - 预计 v0.1 上线日：\_\_\_\_\_\_\_\_\_\_（+5 周）
  - **风险**：这 5 周内有任何会议/旅行/家事需提前标注，超过 7 天连续中断 = 走 BUS-1 SOP
- ~~**T001 LLM spike fixture 采集计划**~~ **(0.4.0 · DEFERRED to Phase 2)**
  - T001 已从 Phase 0 强制 gate 降格为 Phase 2 validation milestone（spec.md 0.4.0 / DECISIONS-LOG G11）· Phase 2 T001-v2 时再做 fixture 决策
  - v0.1 首轮 fixture（20 条 human-labeled）已存在于 `tests/fixtures/human-labeled-20.json` · Phase 2 T001-v2 复用 + 在真实 papers 表抽样补充

---

## §1 · 开发环境（localhost 可跑 = green CI）

### §1.1 软硬件

- [ ] **OS**: macOS / Linux / WSL2 —— 任选，CI 用 ubuntu-latest
- [ ] **Node 22.x LTS**: `node --version` → `v22.x.y`
- [ ] **pnpm 9+**: `pnpm --version` → `9.x.x`
- [ ] **Postgres 16**: `pg_config --version` → `PostgreSQL 16.x` · brew install / apt install
- [ ] **git**: 基础即可

### §1.2 本地 db 创建

```bash
# 创建本地 db
createdb pi_briefing_dev

# 跑 schema
psql pi_briefing_dev < specs/001-pA/reference/schema.sql
# 预期：15 张表、0 报错

# 验证表数
psql pi_briefing_dev -c '\dt' | grep -c "^ public"
# 预期：15
```

- [ ] 15 张表全部创建
- [ ] CHECK 约束可触发：
  ```bash
  psql pi_briefing_dev -c "INSERT INTO actions (seat_id, paper_id, action) VALUES (1, 1, 'skip');"
  # 预期：ERROR: violates check constraint "skip_requires_why"
  ```
- [ ] 不留 dev DB 污染 Phase 0 测试 fixture

### §1.3 Repo clone & install

- [ ] `git clone` 已完成
- [ ] `pnpm install --frozen-lockfile` (若 lockfile 已有)
- [ ] `.env` 已从 `.env.example` 拷贝并填写
  - `DATABASE_URL=postgres://...@localhost:5432/pi_briefing_dev`
  - `WORKER_DATABASE_URL=...`（先同 webapp user，Phase 3 再分）
  - `SESSION_SECRET=<64 char hex>` 用 `openssl rand -hex 32` 生成
  - `ANTHROPIC_API_KEY=sk-ant-xxx`
  - `OPENAI_API_KEY=sk-xxx`
  - `ALERT_EMAIL=your-email`
- [ ] `pnpm typecheck` 绿（Phase 0 之前没代码也应绿 —— 预期 "No errors"）

---

## §2 · 凭据与第三方账号

- [ ] ~~**Anthropic API key**：已申请 + 充值 ≥ $20（T001 spike + 前 2 周测试）~~
  - **0.4.0 修订**：T001 已 defer 到 Phase 2 · Phase 0/1 全程走 stub heuristic 不调真 SDK · API key 推迟到 Phase 2 T001-v2 kickoff 前充值
- [ ] ~~**OpenAI API key**：已申请 + 充值 ≥ $20~~
  - 同上 · Phase 2 T001-v2 kickoff 前充值即可
- [ ] **GitHub private repo**：已建，push 权限验证
- [ ] **Backblaze B2** (或类似 S3 兼容)：账号 + bucket `pi-briefing-backups-<username>`（Phase 3 时用）
- [ ] **域名**：已备（可选，Phase 3 前决定）—— e.g. `pi-briefing.你域名.com`

---

## §3 · 数据源调研（**0.4.0 · T001 fixture 部分 DEFERRED 到 Phase 2**）

- [ ] **arXiv cs.AI + cs.LG + cs.CL 日更数量**：你了解过吗（仍是 Phase 0 必需 · 影响 T005 fetch worker 设计）
  - 预期 100–300 篇/天 跨 3 个 category
  - 8–15 topic 每 topic 0–20 candidate/day
- [ ] **个人 lab 真实覆盖的 topic 列表**（8–15 个）：草稿在哪（仍是 Phase 0 必需 · T010 topic CRUD 用）
  - 写在 `projects/001-pA/lab-topics-draft.md`（可选，非必需）
  - 示例：RLHF / efficient-attention / multi-modal-reasoning / mechanistic-interp / inference-time-compute / ...
- ~~[ ] **已知的 10 个 state-shift 案例**（T001 fixture 用）：至少能举 5 个~~ **(0.4.0 · DEFERRED 到 Phase 2 T001-v2)**
  - v0.1 首轮 fixture 已存在于 `tests/fixtures/human-labeled-20.json` · Phase 2 复用

---

## §4 · 技术决策锁定（Phase 0 前必须确定）

- [ ] **LLM primary provider**: Anthropic / OpenAI / GLM5.1 / 其他
  - **0.4.0 修订**：Phase 2 T001-v2 spike 完后才确定 · Phase 0/1 全程默认 stub heuristic · env 也不必现在备齐(Phase 2 T001-v2 kickoff 前补即可)
- [ ] **Postgres 托管**：本地开发 localhost；v0.1 部署 self-host VPS
  - VPS provider 选：DigitalOcean / Hetzner / Linode / AWS Lightsail
  - Region：近你（亚洲优先 sgp1 / 美东 nyc1）
  - 规格：≥ 4GB RAM（Postgres + Next.js + worker 同机）
- [ ] **前端 UI lib**：per tech-stack，不用 shadcn/ui 重装，CSS modules 足够
  - 接受 v0.1 UI 粗糙（SLA v0.1 明确 Speed > Polish）
- [ ] **时区**: Asia/Shanghai (per `.env.example APP_TIMEZONE`)
  - worker 定时 06:00 Asia/Shanghai = UTC 22:00 前一天
  - 若 operator 不在亚洲，改成 local tz

---

## §5 · Spec 包本身的状态复核（秒查）

- [ ] `spec.md` 版本 0.2.2 · changelog 4 条完整
- [ ] `architecture.md` 版本 0.2 · ADR-1..7 齐
- [ ] `schema.sql` 版本 0.2.2 · 15 张表 · paper_summaries.llm_call_id 可 null
- [ ] `dependency-graph.mmd` 25 tasks · 关键路径约 59h
- [ ] `tasks/T001.md..T034.md` · 25 个文件
- [ ] `reference/` 7 份参考 + `skeletons/` 14 份代码（含 llm-utils.ts） + `workflows/` 6 份 SOP
- [ ] `DECISIONS-LOG.md` 含 pre-R_final F1-F6 条目
- [ ] `OPEN-QUESTIONS-FOR-OPERATOR.md` Q1-Q5 已 resolve · Q3 deferred
- [ ] `STATUS.md` · 当前版本
- [ ] **CI workflow**（`.github/workflows/ci.yml`）：**Phase 0 T002 任务产出，当前尚未存在**（不是 gap，是 T002 的 Outputs）

---

## §6 · Phase 0 执行顺序（**0.4.0 修订 · T001 已 defer** · 小心关键路径）

**绝对优先级**：

1. ~~**T001 LLM spike** (独立，8h · 可完全独立开工，不等任何东西)~~ **(0.4.0 · DEFERRED 到 Phase 2)**
   - 详见 spec.md 0.4.0 changelog · DECISIONS-LOG G11 · v0.1 首轮 spike 已 freeze 在 `projects/001-pA/spikes/T001-llm-provider-report.md`
2. **T002 monorepo scaffold** (4h · Phase 0 第一个开工 task) **← 0.4.0 后变成 Phase 0 入口**
   - blocks: T003, T004, T007, T008
   - 产 `package.json`, `tsconfig.json`, `biome.json`, `.env.example`, CI `ci.yml`
3. **T003 schema spine** (10h · 等 T002) ← 最大阻塞节点
   - blocks: T005, T006, T010, T012, T021, T023, T024
   - cp `reference/skeletons/db-schema.ts` → `src/db/schema.ts` + 修 TODO
   - 跑 `pnpm drizzle-kit generate` → 得 `src/db/migrations/0000_initial.sql`
   - diff 生成的 migration vs `reference/schema.sql` → 手工核对 0 漂移
4. **T004 LLM interface** (6h · 等 T002) - Opus 级 task **(0.4.0：依赖只剩 T002 · 走 stub 模式)**
   - cp `llm-types.ts` + `llm-*-stub.ts` + `llm-utils.ts` → `src/lib/llm/`
   - 按 `reference/llm-adapter-skeleton.md §3/§4` 填 TODO + **遵守 T004.md §"Stub 实现范围 (0.4.0)"**：默认 `LLM_*_ENABLED=false` 走 stub heuristic · 真 SDK 路径作为 dead-code 留在 `if (process.env.LLM_*_ENABLED)` 后(Phase 2 翻 env 后无需改代码即生效)
   - **必做**: F2 confidence downgrade (§3 末段) · F1 truncateTo3Sentences import · F3 adversarial fixtures 15 case 齐(stub 模式下也跑 · 验证 stub 不被 prompt injection 影响)

**顺着跑完 Phase 0 的其余 task**（T005 arXiv / T006 auth / T007 env / T008 test harness），然后进 Phase 1。Phase 1 全程默认 `LLM_JUDGE_ENABLED=false` 走 heuristic-only(§4.1 anchor 被 ≥ 2 篇引用即 shift)+ T013 走 fallback summary 模板。

**避免同时开工太多**：solo operator 一次最多 2 个 task 并行。

---

## §7 · 心理准备

- [ ] **接受 v0.1 是 dogfood 而非 launch**：没有 polish，没有真实用户（只有你+≤2 lab），60 天才能验证
- [ ] **接受 kill-window 60 天**：第 30 天如果 PI（你）只看不标注，还要撑 30 天再评判
- [ ] **接受 T001 spike 已 defer + Phase 1 默认 fallback heuristic**（0.4.0）：v0.1 首轮 spike 在 GLM5.1 上延迟 + 成本两硬 gate fail · 已降格为 Phase 2 validation milestone · Phase 1 系统全程不依赖 LLM judge 也能跑 —— **不意味着项目失败**，是成本可控选择 · Phase 2 T001-v2 仍 fail 则永久 fallback
- [ ] **接受 114h 总预算零 slack**：任何 task 翻倍都会挤到 6 周 —— 你是否提前想好"可砍的优先顺序"（STATUS.md 建议：T016 history page · T020 breadcrumb 独立列表 · T031 restic 云同步 可推迟）
- [ ] **接受"文档 15000 行"的代价**：初级工程师/未来自己接手时有完整参照，但你这 5 周里不太会重读所有文档，主要用到的是 `tasks/T*.md` + `reference/skeletons/*` + `reference/workflows/*`

---

## §8 · BUS-1 应急预案（operator 缺席 > 7 天）

- [ ] 已跟 ≥ 1 位 lab 成员说"我如果失联超 7 天，按 `docs/runbook/operator-absent.md` 走"（Phase 3 T033 产物）
- [ ] Phase 3 T033 里会产 `operator-absent.md`，现在只需心理承诺
- [ ] v0.1 期间不给 lab 外部 seat · 最多 3 seat 全部内部
- [ ] 若你知道 Phase 0 中间有 > 7 天空档（出差/家事），**推迟 kickoff 到空档后**

---

## §9 · Phase 0 完成的判定（**0.4.0 修订 · 已删 T001 sign-off** · 进 Phase 1 前）

- ~~[ ] T001 报告产出 + `approved-provider` 确定~~ **(0.4.0 · DEFERRED 到 Phase 2)**
- [ ] T002 scaffold + CI 绿（`pnpm typecheck && pnpm test && pnpm lint && pnpm build`）
- [ ] T003 schema 落盘 + 15 表可见 + CHECK 生效
- [ ] T004 2 个 adapter + interface 通过 contract tests（**stub 模式 · `LLM_*_ENABLED=false` · 详见 T004.md §"Stub 实现范围"**）
- [ ] T005 arXiv fetcher 可拉回 10 篇 paper
- [ ] T006 auth skeleton + session middleware 可 E2E 登入
- [ ] T007 env 校验 + systemd 模板 ready（**包含 `LLM_JUDGE_ENABLED` 默认 `false` + `LLM_SUMMARIZE_ENABLED` 默认 `false`**）
- [ ] T008 test harness 跑通（1 trivial unit + 1 trivial E2E）
- [ ] **Phase 0 总工时** ≤ 32h（**0.4.0 修订**：原 40h - T001 8h = 32h · 理论 29h + 3h slack）

如果超 40h → 检查是否打算砍 scope，回 STATUS.md"应急路径"表。

---

## §10 · 第一个 commit 前最后 1 分钟

- [ ] 把你心里的"为什么我要做这个"再写一遍在 `DECISIONS-LOG.md` 最底下（30 字以内）
  - 示例："我自己就是 PI，每天漏看 3 篇 paper；60 天赌 briefing-as-ritual 能不能成立；失败就回 L2 重新 explore"
- [ ] `git init`（如果还没）
- [ ] `git add specs/ proposals/ discussion/ CLAUDE.md ...`（**不包括 src/** —— src/ 在 Phase 0 逐步 commit）
- [ ] `git commit -m "chore(001-pA): freeze spec v0.4.0 before Phase 0 kickoff

Spec package passes R_final adversarial review (verdict: <CLEAN/CLEAN-WITH-NOTES/CONCERNS>).
Starting Phase 0 with T002 (T001 deferred to Phase 2 per 0.4.0).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"`
- [ ] `git tag spec/001-pA/v0.4.0`
- [ ] 建 GitHub private repo · `git push -u origin main` + `git push --tags`

---

## 附录 · 如果 Phase 0 中第一周就撞墙

| 症状 | 首选排查 | SOP |
|---|---|---|
| ~~T001 两家 provider 都 < 70%~~ | **0.4.0 后 N/A** | T001 已 defer 到 Phase 2 · Phase 0/1 一律 fallback heuristic · Phase 2 T001-v2 才会再面对此症状 |
| T003 schema 跑 CHECK 报语法错 | `EXPLAIN` 看约束名；`regexp_split_to_array` 在 Postgres 16 需启用 | 见 `reference/ops-runbook.md §12 release workflow` 末尾的 troubleshooting |
| `pnpm install` 卡在某个包 | pin 版本 vs 实际 registry 有冲突 | 降版本到 tech-stack.md 未 pin 的相邻版 · 在 DECISIONS-LOG 记录 |
| TS strict 下 skeleton 不编译 | `noUncheckedIndexedAccess` 严苛 | 加 `!` non-null assertion 或 `?? throw` 短路 · 别关闭 strict |
| ~~Anthropic API 403~~ | **0.4.0 后 N/A** | Phase 0/1 全程 stub heuristic 不调真 SDK · API key issues 推迟到 Phase 2 T001-v2 |

---

**最后一句**：对着 checklist 走 30–60 分钟，绿色越多，开工越稳。红色越多，越要诚实告诉自己"是否真的 ready"。
