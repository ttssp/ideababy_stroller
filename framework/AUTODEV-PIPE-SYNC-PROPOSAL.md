---
doc_type: framework-cross-repo-sync-proposal
status: draft-pending-execution
target_repo: autodev_pipe
generated: 2026-05-08
upstream: ideababy_stroller framework/SHARED-CONTRACT.md (v1)
purpose: 当 operator 切到 autodev_pipe 仓库工作时,按本文档落地 3 节同步动作
---

# autodev_pipe 同步提案 — 落地 SHARED-CONTRACT v1

## 本文档定位

本文档是 **autodev_pipe 仓库需要做的同步动作清单**。它写在 ideababy_stroller(idea→PRD repo)这边,因为本会话 cwd 在 ideababy_stroller,**无法直接编辑 autodev_pipe 仓库**。

**operator 后续切到 autodev_pipe 时,按本文档逐节执行**。

> **Why this proposal exists, not direct edits**:跨 repo 工作时,在源仓库这边写一份"建议清单"是工业范式(参见 GitHub PR template / Backstage migration guide / Helm chart 升级 checklist)。避免 operator 切仓后忘记跨仓变更,也保留 audit trail。
>
> **Why bind contract bidirectionally**:Newman *Building Microservices* ch.7 Consumer-Driven Contracts — 契约必须 consumer 端也声明,producer 单方面声明无效。Pact framework / Linux kernel + glibc syscall ABI 范式同样原则。仅在 ideababy_stroller 这边声明 "autodev_pipe 应 honor X" 不构成有效契约,**autodev_pipe 仓库自身的 AGENTS.md 也必须复述并标注 binding 来源**。

---

## 同步前置条件

执行本文档动作前,确认:

- ✅ ideababy_stroller `framework/SHARED-CONTRACT.md` v1 已存在
- ✅ ideababy_stroller `framework/NON-GOALS.md` v1 已存在
- ✅ ideababy_stroller `AGENTS.md` 已升级 ≤8KB(`wc -c AGENTS.md`)
- ✅ operator 已 `cd <autodev_pipe path>`(本会话不会代切目录)
- ✅ operator 已通读 `discussion/006/forge/v1/stage-forge-006-v1.md` §2 重写后的 L/P/C 分层表(知道 autodev_pipe 在 L/P/C 矩阵中的归属)

---

## 同步动作清单(3 节)

### 节 1 · autodev_pipe README.md 改版

#### 当前状态(predicted)

autodev_pipe 仓库的 README.md 大概率还在描述 v3.1 design doc / STARTER_KIT 视角,未显式声明它的"角色"是 PRD→code build harness。

#### 改版动作

在 autodev_pipe README.md 的开头(在任何 v3.1 / STARTER_KIT 内容之前)插入**关系段落**:

```markdown
## Repo role(2026-05-08+)

This repo is the **build harness** half of a two-repo framework:

- **`ideababy_stroller`** — idea→PRD harness (L1 inspire / L2 explore / L3 scope / L4 plan + forge cross-cutting layer)
- **`autodev_pipe`** (this repo) — PRD→code harness (build worker / review coordinator / runtime safety)

The two repos are **independently released**, **no version pinning**, coordinated only via `SHARED-CONTRACT.md` (SSOT in ideababy_stroller, mirror in this repo).

**This repo consumes**:
- PRD documents (plain markdown, 8 required fields per `SHARED-CONTRACT.md` §1) produced by `ideababy_stroller /plan-start`
- HANDOFF.md instructions (per SHARED-CONTRACT §3) telling operator how to invoke `autodev_pipe-cli build`

**This repo honors as binding**:
- `ideababy_stroller framework/SHARED-CONTRACT.md` §2 Safety Floor (production credential isolation / irreversible command hard block / backup destruction detection) — non-overridable in any sandbox mode

**This repo does NOT do**:
- Idea generation / inspire / explore / scope (those happen in `ideababy_stroller`)
- PRD writing (PRD comes from `ideababy_stroller /plan-start`, immutable here)

For contract version + breaking change protocol, see `SHARED-CONTRACT.md` (mirrored from ideababy_stroller).
```

#### 完成标准

- README.md 第一节(在 v3.1 / STARTER_KIT 段之前)是 "Repo role"
- 段落明确"消费 PRD"和"honor Safety Floor"两件事
- 段落引用 ideababy_stroller `framework/SHARED-CONTRACT.md` 完整路径

---

### 节 2 · autodev_pipe AGENTS.md 创建/升级

#### 当前状态(predicted)

autodev_pipe 仓库可能已经有 `templates/AGENTS.md`(stage v1 §2 表 #5 提及),但**根目录 AGENTS.md** 状态未知。如果不存在,创建;如果存在,升级。

#### 创建/升级动作

autodev_pipe 根目录 `AGENTS.md` 必须包含**至少 6 节**,**总字节 ≤ 8KB**(同 Vercel benchmark 阈值,适用于 autodev_pipe 自己的 AGENTS.md):

```markdown
# autodev_pipe — PRD→code build harness SSOT

> **Repo role**: PRD→code build harness (build worker / review coordinator / runtime safety / cost control / Learning Loop)
> **Companion repo**: `ideababy_stroller`(idea→PRD)
> **Updated**: <ISO date> — restructured per ideababy_stroller framework/SHARED-CONTRACT.md v1
> **Constraint**: ≤ 8KB(Vercel benchmark)

## §1 · Safety Floor (binding from ideababy_stroller)

The following three rules are **binding from ideababy_stroller framework/SHARED-CONTRACT.md §2**. They are non-overridable in any sandbox mode (`suggest` / `auto-edit` / `full-auto`). No prompt / config / sandbox setting can disable them. SSOT lives in ideababy_stroller; this section is a mirror.

1. **Production credential isolation** — [verbatim from SHARED-CONTRACT §2 件 1]
2. **Irreversible command hard block** — [verbatim from SHARED-CONTRACT §2 件 2]
3. **Backup destruction detection** — [verbatim from SHARED-CONTRACT §2 件 3]

If autodev_pipe-cli detects ideababy_stroller's SHARED-CONTRACT.md `contract_version` is incompatible with `supported_contract_versions` (this file §3), it must REFUSE to start, not "尽力解析".

**Failure case prevented**: Cursor + Claude 9-second database deletion (tomshardware 2025).

## §2 · Sandbox modes (Codex CLI Pattern)

Three modes (Pattern borrowed from OpenAI Codex CLI 2025 design):

- `suggest` — agent proposes edits, operator approves each
- `auto-edit` — agent edits + commits within file_domain, operator approves push
- `full-auto` — agent edits + commits + pushes to non-protected branches

**All three honor Safety Floor (§1)**. `full-auto` does NOT mean "bypass Safety Floor".

## §3 · Contract versioning

This repo is independently released, no version pinning to ideababy_stroller. Coordinated via SHARED-CONTRACT.md.

- **`supported_contract_versions`**: <semver range, e.g., `>=1.0.0 <2.0.0`>
- **Breaking change protocol** (binding from ideababy_stroller): deprecation ≥ 4 weeks + migration ≥ 4 weeks + cutover ≥ 1 week
- **Mirror policy**: this repo's `SHARED-CONTRACT.md` (§4 below) is byte-level cp from ideababy_stroller; never edit here, edit there

## §4 · SHARED-CONTRACT mirror

See `SHARED-CONTRACT.md` in this repo (mirror of `ideababy_stroller framework/SHARED-CONTRACT.md`).

## §5 · Build pipeline modules

(autodev_pipe-internal — references stage-forge-006-v1.md §3 模块 2-4 归属此 repo)

- Module 2 · Safety / Permission layer — implements Safety Floor §1
- Module 3 · Quality / Review layer — review coordinator MVP 4 件套
- Module 4 · Learning Loop layer — retrospective + Eval Score
- (Plus internal modules: in-process brakes / cost circuit breaker / sandbox modes / etc.)

## §6 · Iron rules

- Honor Safety Floor (§1) — non-overridable
- Refuse to start if SHARED-CONTRACT.md mirror is missing or `contract_version` outside supported range
- Output build / review verdicts in machine-parseable format (TBD: JSON or structured markdown)
- Cross-model review for v1.0 paths (Opus + Codex)
- Default deny: `full-auto` requires explicit operator opt-in per session

(Continue with tool defaults / directory ownership / prohibitions if space permits)
```

#### 完成标准

- autodev_pipe 根 `AGENTS.md` 存在
- `wc -c AGENTS.md` ≤ 8192
- ≥ 6 节,且 §1 显式标 "binding from ideababy_stroller"
- §3 显式声明 `supported_contract_versions`(semver 区间)
- 总字节字段不允许 verbatim cp ideababy_stroller AGENTS.md(那是 IDS 视角,这是 ADP 视角)

---

### 节 3 · autodev_pipe SHARED-CONTRACT.md mirror

#### 当前状态(predicted)

autodev_pipe 仓库当前没有 SHARED-CONTRACT.md(因为它是本次 v1 才在 ideababy_stroller 这边产生的)。

#### 创建动作

在 autodev_pipe 根目录创建 `SHARED-CONTRACT.md`,**字节级 cp** ideababy_stroller `framework/SHARED-CONTRACT.md`,加 mirror 标记:

```markdown
---
doc_type: framework-shared-contract-mirror
mirror_of: ideababy_stroller/framework/SHARED-CONTRACT.md
mirror_synced: <ISO date>
mirror_policy: byte-level cp; never edit here, edit upstream
status: v1
---

> **Mirror notice**: 这是 ideababy_stroller `framework/SHARED-CONTRACT.md` 的 mirror。
> SSOT 在 ideababy_stroller 仓库。本文件**永不直接编辑**——任何变更必须先在
> upstream 完成(走三阶段 breaking change 流程),再 cp 到这里。
> 如发现 mirror 与 upstream 字节级不一致,以 upstream 为准。

[verbatim cp of ideababy_stroller/framework/SHARED-CONTRACT.md content from §"## 本文档定位" onwards]
```

#### 同步检查脚本(autodev_pipe 仓库根)

可在 autodev_pipe 加一个脚本 `scripts/check-contract-sync.sh`(或对应语言版本):

```bash
#!/bin/bash
# Check SHARED-CONTRACT mirror is byte-level identical to upstream

UPSTREAM="${IDEABABY_STROLLER_PATH:-../ideababy_stroller}/framework/SHARED-CONTRACT.md"
LOCAL="./SHARED-CONTRACT.md"

if [ ! -f "$UPSTREAM" ]; then
  echo "ERROR: upstream not found at $UPSTREAM"
  echo "Set IDEABABY_STROLLER_PATH env var or place repo at sibling location"
  exit 1
fi

# Strip the mirror frontmatter from local copy before diffing
LOCAL_BODY=$(awk '/^# SHARED-CONTRACT/,EOF' "$LOCAL")
UPSTREAM_BODY=$(awk '/^# SHARED-CONTRACT/,EOF' "$UPSTREAM")

if [ "$LOCAL_BODY" != "$UPSTREAM_BODY" ]; then
  echo "DRIFT DETECTED: $LOCAL is not a byte-level mirror of $UPSTREAM"
  diff <(echo "$LOCAL_BODY") <(echo "$UPSTREAM_BODY")
  exit 1
fi

echo "OK: SHARED-CONTRACT mirror in sync"
```

可以挂在 autodev_pipe pre-commit hook 或 CI gate 上。

#### 完成标准

- autodev_pipe 根 `SHARED-CONTRACT.md` 存在
- frontmatter 标 `mirror_of` + `mirror_policy: byte-level cp; never edit here`
- body 与 ideababy_stroller `framework/SHARED-CONTRACT.md` 从 `# SHARED-CONTRACT` heading 之后字节级一致(可用 `diff` 验证)
- (推荐)有 `scripts/check-contract-sync.sh` + pre-commit hook,防止 drift

---

## 客观依据汇总

| 同步动作 | 依据 | 来源 |
|---|---|---|
| 节 1 README "Repo role" 段 | Microservice repo split 范式必须显式声明角色 | Newman *Building Microservices* ch.4 |
| 节 1 引用 ideababy_stroller path | Linux kernel + glibc 30 年 ABI 协调范式;明确 SSOT 位置 | Linux kernel 文档 |
| 节 2 AGENTS.md ≤ 8KB | Vercel benchmark 100% activation 阈值 | Vercel 2025 工程博客 |
| 节 2 §1 binding 声明 | Consumer-Driven Contracts:契约必须 consumer 端也声明 | Newman ch.7 / Pact framework |
| 节 2 §3 contract_version semver 区间 | npm/pip/cargo 生态共识 | semver.org |
| 节 2 拒绝运行(版本不兼容)而非"尽力解析" | Fail-fast 范式 | Erlang/OTP 设计哲学 |
| 节 3 byte-level mirror | Linux kernel `include/uapi/` headers 对 libc 的 mirror 范式(30 年验证) | Linux kernel 历史 |
| 节 3 同步检查脚本 | drift detection 是 contract testing 标配 | Pact / OpenAPI ecosystem |

---

## 风险与化解

| 风险 | 化解 |
|---|---|
| autodev_pipe 当前 README 已有内容,改版冲突 | 在 README 顶部新增 "Repo role" 节,不删原内容,用 `> **Latest update**` 标注新增 |
| autodev_pipe 已有 AGENTS.md(在 templates 下不在根),路径冲突 | 区分 `templates/AGENTS.md`(给 ADP 用户的模板)与根 `AGENTS.md`(ADP 自己的 SSOT) |
| Mirror drift(operator 不小心改了 autodev_pipe SHARED-CONTRACT.md) | 节 3 的同步检查脚本 + pre-commit hook + CI gate 三层防御 |
| autodev_pipe 还在 v3.1 design 阶段,没有 build/cli 实现 | 同步动作不阻塞 — AGENTS.md / README / mirror 都是文档,可在没有实现的情况下写;实现按 stage v1 §5 dev plan 推进 |
| 跨仓 contract 升级时,mirror 需要手动 sync | 长期可考虑 git submodule 或 monorepo subtree split 自动化;v1 阶段手工 cp 即可 |

---

## 执行顺序建议

operator 切到 autodev_pipe 时:

1. 节 1 README 改版(0.5h,纯文档)
2. 节 3 SHARED-CONTRACT mirror 创建(0.5h,文件 cp)
3. 节 2 AGENTS.md 创建/升级(1-2h,需要根据 autodev_pipe 当前实际状态适配)
4. 测试 `scripts/check-contract-sync.sh`(0.5h)
5. commit + push autodev_pipe(取决于 operator)

总时长:**~3h**(对应 plan 中事 4 估时 0.5d)。

---

## 验证(在 autodev_pipe 仓库)

```bash
# 在 autodev_pipe 仓库根
test -f README.md && grep -c '## Repo role' README.md  # 应 = 1
test -f AGENTS.md && wc -c AGENTS.md  # ≤ 8192
test -f AGENTS.md && grep -c 'binding from ideababy_stroller' AGENTS.md  # ≥ 1
test -f SHARED-CONTRACT.md && grep -c '^mirror_of:' SHARED-CONTRACT.md  # = 1
bash scripts/check-contract-sync.sh  # 应 echo "OK: SHARED-CONTRACT mirror in sync"
```

---

## Changelog

- 2026-05-08 v1: 初稿,3 节同步动作 + 同步检查脚本
