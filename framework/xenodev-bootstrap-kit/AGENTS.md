# XenoDev — ADP-next runtime harness SSOT

> **Repo role**: L4 build runtime(consume hand-off from IDS,produce hand-back back to IDS)
> **Companion repo**: `ideababy_stroller`(IDS — idea→PRD + governance + forge,SSOT for SHARED-CONTRACT)
> **Created**: 2026-05-10(per `ideababy_stroller/discussion/006/forge/v2/stage-forge-006-v2.md` verdict)
> **Constraint**: ≤ 8KB(Vercel benchmark)

## §1 · Safety Floor(non-overridable hard rules)

**binding from `ideababy_stroller/framework/SHARED-CONTRACT.md` §2**(per §6 v2.0 ssot_consumer 必填)。

3 件套 hard block in any sandbox mode,无 override:

1. **凭据隔离** — `.env.production*` / `.env.prod*` / `secrets/production/*` / `prod://` 不进 agent context。`.claude/safety-floor/credential-isolation/scan-credentials.sh` 实装。
2. **不可逆命令 hard block** — `rm -rf /` / `DROP TABLE` / `git push --force` to main / `aws s3 rm --recursive prod` 等 24 类。`.claude/hooks/block-dangerous.sh`(mirror from autodev_pipe)实装。
3. **备份破坏检测** — IAM 不允许同凭据删主存 + 备份。`.claude/safety-floor/backup-detection/snapshot.sh` + `diff-snapshot.sh` 实装。

**Failure case**:Cursor + Claude 9 秒删库(tomshardware 2025)。

## §2 · Reliability — three layers

per IDS AGENTS.md §2 同构:
1. **Safety Floor**(§1)— non-overridable
2. **Deterministic Feedback** — tests / lint / type-check / hook gates
3. **Learning Loop** — eval append-only event log(`lib/eval-event-log/`)+ hand-back 闭环

K2 disambiguated:Safety Floor non-negotiable;automation maximizes within deterministic feedback boundaries。

## §3 · L4 build runtime 定义

XenoDev = ADP-next 的运行时 harness(per stage doc verdict)。**唯一**职责:

```
hand-off 包 (from IDS)
  ↓ /Users/admin/codes/ideababy_stroller/discussion/<id>/<prd>/L4/HANDOFF.md
  ↓ workspace + source_repo_identity blocks (per SHARED-CONTRACT §6.2 + §3.1)
  ↓
spec-writer (XenoDev 自带,不调 IDS 的)
  ↓
task-decomposer (XenoDev 自带)
  ↓
parallel-builder (XenoDev 自带)
  ↓
ship + hand-back 包
  ↓ /Users/admin/codes/ideababy_stroller/discussion/<id>/handback/<ts>-<id>.md
  ↓ producer 端跑 lib/handback-validator/ 6 约束自检
  ↓
operator 在 IDS 跑 /handback-review <id>
```

**不做**:
- ❌ 不复制 forge 机制(forge 永远在 IDS 治理仓)
- ❌ 不产 PRD(PRD 在 IDS L3)
- ❌ 不产 idea(idea 在 IDS L1-L2)
- ❌ 不动 SHARED-CONTRACT.md(SSOT 在 IDS,XenoDev 持 mirror 只读)

## §4 · Cross-repo contract(XenoDev ↔ IDS)

per `ideababy_stroller/framework/SHARED-CONTRACT.md` §6 v2.0(contract_version 2.0,Status: ACTIVE-but-not-battle-tested)。

- **Forward hand-off**:IDS `/plan-start` v3.0 → `discussion/<id>/<prd>/L4/HANDOFF.md`(workspace + source_repo_identity)
- **Reverse hand-back**:XenoDev → `discussion/<id>/handback/*.md`(per §6.3 schema,producer 端跑 6 约束 validator)
- **Versioning**:semver on `contract_version`;XenoDev follows IDS bump
- **Mirror**:本仓 `framework/SHARED-CONTRACT.md` 是 IDS SSOT 的字节级 cp,跟随 IDS 变更

若 IDS unavailable,XenoDev 不应跑 build(无 hand-off 源);hand-back 包写入失败时 hard-fail,不尝试缓冲。

## §5 · spec/task workflow(XenoDev L4)

由 XenoDev schema **重新派生**,**不**从 IDS port(per stage doc §"模块 B" step 7)。首个真 PRD 起跑时实装:

- spec-writer:从 hand-off 包提 PRD outcomes → 产 spec.md(7 元素 + PPV 第 7 元素)
- task-decomposer:spec.md → tasks/T*.md(9 字段 frontmatter)+ dependency-graph.mmd
- parallel-builder:每个 task 独立 worktree;TDD;cross-model review for v1.0

实装位置:`.claude/skills/{spec-writer, task-decomposer, parallel-builder}/`(B2.2 起跑时落)

## §6 · Iron rules + defaults

- **No code without a spec**(L4 only;spec 由 XenoDev spec-writer 产)
- **TDD for production code**:test → red → implement → green
- **Pre-merge review mandatory**:`/task-review` verdict ≠ BLOCK
- **Cross-model review for v1.0 paths**
- **hand-back 必产**:每个 task ship 后必产 hand-back 包(写回 IDS,跑 6 约束 validator)
- **不动 SHARED-CONTRACT.md**(只读 mirror)
- **不复制 forge 机制**(forge 在 IDS 治理仓)
- **Output in Chinese**(operator 偏好)

**Tools**(同 IDS):`rg` / `pnpm` + Node 22 + TS strict + Biome / `uv` + `ruff` + `pytest` / Conventional Commits。

**Directory ownership**:
- `PRD.md`(operator cp from IDS hand-off)
- `specs/<feature>/{spec, tasks/T*}.md`(spec-writer + task-decomposer 产)
- `lib/{workspace-schema,eval-event-log,handback-validator}/`(从 IDS bootstrap-kit cp)
- `.claude/{hooks,safety-floor,skills,commands}/`(同 IDS 范式)
- `.eval/events.jsonl`(append-only event log)

**Prohibitions**:复制 forge / 改 SHARED-CONTRACT / 跑 IDS 的 spec-writer subagent / 不产 hand-back 包 / 跳过 6 约束 validator。

## §7 · References

- `framework/SHARED-CONTRACT.md`(IDS SSOT 的 mirror,只读)
- `lib/handback-validator/README.md`(§6.2.1 6 约束实装)
- `lib/workspace-schema/README.md`(§6.2 4 字段实装)
- `lib/eval-event-log/README.md`(3 类 event 接口)

**Out of scope**:
- IDS framework 修订(escalate to IDS;在 IDS 仓走 forge / scope-inject)
- Per-project AGENTS.md(`projects/<feature>/AGENTS.md` 各自定)
