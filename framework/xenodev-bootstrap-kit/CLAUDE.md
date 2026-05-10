# XenoDev — 项目宪法(Project Constitution)

> **版本**:v0.1
> **创建**:2026-05-10(per `ideababy_stroller/discussion/006/forge/v2/stage-forge-006-v2.md` verdict)
> **定位**:ADP-next 的运行时 harness;唯一 L4 build runtime

## 本仓的核心使命

**消费 IDS 产的 hand-off 包,产出可 ship 的代码,跑完后产 hand-back 包写回 IDS。**

- ✅ **In scope**:spec → tasks → parallel build → ship → hand-back
- ❌ **Out of scope**:idea(在 IDS L1)/ PRD(在 IDS L3)/ 治理(在 IDS forge)/ 跨仓协议设计(SSOT 在 IDS framework/SHARED-CONTRACT.md)

## 三件硬约束(non-overridable)

per `ideababy_stroller/framework/SHARED-CONTRACT.md` §1 + §2:

1. **凭据隔离** — `.env.production*` / `secrets/production/*` / `prod://` 不进 agent context(`.claude/safety-floor/credential-isolation/`)
2. **不可逆命令 hard block** — `rm -rf /` / `DROP TABLE` / force-push main 等 24 类(`.claude/hooks/block-dangerous.sh`)
3. **备份破坏检测** — v0.1 实装为本地 snapshot+diff(filesystem `*.backup`/`*.bak`/`*.snapshot` + `.git/config` push policy + permissions.deny diff;`.claude/safety-floor/backup-detection/`)。**v0.2 trigger**:IAM lint + runtime cloud-API interceptor(用云时加,per `safety-floor-3/README.md` OQ-backup-1)

## 关键实装位置

| 组件 | 路径 | Provenance |
|---|---|---|
| Safety Floor 件 1(凭据隔离) | `.claude/safety-floor/credential-isolation/` | from IDS bootstrap-kit/safety-floor-1/ |
| Safety Floor 件 2(命令拦截) | `.claude/hooks/block-dangerous.sh` | from IDS bootstrap-kit/safety-floor-2/(mirror autodev_pipe) |
| Safety Floor 件 3(备份检测) | `.claude/safety-floor/backup-detection/` | from IDS bootstrap-kit/safety-floor-3/ |
| workspace schema 4 字段 validator | `lib/workspace-schema/` | from IDS bootstrap-kit/workspace-schema/ |
| Eval append-only event log | `lib/eval-event-log/` | from IDS bootstrap-kit/eval-event-log/ |
| §6.2.1 6 约束 validator | `lib/handback-validator/` | from IDS bootstrap-kit/handback-validator/ |
| spec-writer / task-decomposer / parallel-builder skill | `.claude/skills/` | XenoDev 自派生(B2.2 起跑时实装) |

## 工作流(per stage doc §"模块 B")

```
1. operator cd XenoDev
2. cat /Users/admin/codes/ideababy_stroller/discussion/<id>/<prd>/L4/HANDOFF.md
3. cp PRD 进 XenoDev/PRD.md
4. spec-writer 产 specs/<feature>/spec.md(7 元素 + PPV)
5. task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task → ship
7. 每个 task ship 后产 hand-back 包(§6.3 schema)
8. 跑 lib/handback-validator/validate-handback.sh(6 约束自检)
9. 写到 IDS discussion/<id>/handback/<ts>-<id>.md
10. operator 在 IDS 跑 /handback-review <id> 决议
```

## 跨仓引用

- **IDS 仓路径**:`/Users/admin/codes/ideababy_stroller`(只读;SSOT)
- **autodev_pipe(V4)**:`/Users/admin/codes/autodev_pipe`(已 archive,只 mirror block-dangerous.sh)
- **SHARED-CONTRACT**:本仓 `framework/SHARED-CONTRACT.md` 是 IDS SSOT 的字节级 mirror,只读

## 偏好(per `~/.claude/CLAUDE.md` 全局)

- 提交信息:Conventional Commits(feat/fix/chore/docs/test/refactor)
- 不主动 `git push`,push 前需 operator 确认
- 代码注释中文 / 先结论后细节
- TDD for production code
- 报错信息真实粘贴(不只说"有错误")

## 当出问题时

1. 先看 `.eval/events.jsonl`(operator interventions / review_failures)
2. 跑 hand-back validator dry-run:`bash lib/handback-validator/validate-handback.sh test-fixtures/valid/<file>.md /Users/admin/codes/ideababy_stroller`
3. 仍不通 → 在 IDS 仓起 `/expert-forge 006`(forge 永远在 IDS 治理仓)
4. 重大架构转向 → 必须先 forge,不静默停(防 V4 失败模式)

## 不在本 CLAUDE.md 范围

- Per-project: `projects/<feature>/CLAUDE.md`
- Personal: `~/.claude/CLAUDE.md`
- Path-scoped: `.claude/rules/*.md`
- IDS framework 协议层细节(在 IDS 仓 framework/SHARED-CONTRACT.md)
