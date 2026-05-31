# XenoDev Task Brief · 006 forge v4 · P0 原子波 · XenoDev 半边

> **怎么用**:把本文件**从「给 XenoDev Claude Code 的 prompt」分隔线以下**整段复制,贴进 XenoDev 仓终端的 Claude Code。
> **来源**:IDS forge v4 verdict(`discussion/006/forge/v4/stage-forge-006-v4.md` · operator C 全收)· 本 brief 是 cross_repo_split 协议的 XenoDev-side 派工记录。
> **分工**:XenoDev session 做本 brief(SSOT 半边);做完把 lib + wrapper 的最终内容 + SHA 给 IDS operator,IDS session 做 mirror/contract 半边。
> **顺序**:XenoDev 先(SSOT 在 XenoDev,IDS mirror 的 SHA dual-verify 需源文件已存在)。

---

# 给 XenoDev Claude Code 的 prompt（以下整段复制）

你在 XenoDev build runtime 仓(`/Users/admin/codes/XenoDev`)。执行 idea 006 forge v4 verdict 的 **P0 原子波 · XenoDev 半边**。这是已审定的协议层改造,**请先进 plan mode 出方案给 operator 批准,再执行**(改动涉及已 ship 的 producer PPV,回归证明是重点)。

## 任务背景

forge v4 判定 v0.2-shipped 后暴露 3 处协议债。P0 原子波四件事跨两仓:XenoDev 半边 = 抽共享 lib + R-Q7 immutable path;IDS 半边(operator 另做)= mirror + contract bump。你只做 XenoDev 半边。

## 你要做的 6 件事

### 1. 新建 `lib/handback-validator/verdict-evidence-lib.sh`(共享 lib · source-able)
把 `scripts/verify-ppv-p2.sh` 里的 7 字段 verdict-evidence 解析 + verify 逻辑抽成共享 lib。
- **范式**:严格仿同目录 `lib/handback-validator/_yaml-helpers.sh` —— 被 source、**不要** `set -euo pipefail`(会污染 caller)、`local` var + return code 控错、0 外部依赖(awk/grep/sed,无 yq)、干净中文注释。
- **函数清单**(每个带 `mode` 参数 producer|consumer):
  - `parse_evidence_field <hb> <field>` — 合并 verify-ppv-p2 现有**两套** parser:`extract_hb_evidence`(line 81-130,块+inline 解 verdict/findings_count)+ `parse_hb_evidence_field`(line 185-200,块解 5 字段)+ `parse_hb_evidence_inline`(line 209-224,inline 解)。块形式子键可调 `_yaml-helpers.sh` 的 `extract_yaml_field`,**但 inline map `{...}` 不行**(见关键约束 C),inline 必须保留 `parse_hb_evidence_inline` 逻辑搬进 lib。
  - `verify_evidence_required <hb>` — 7 字段齐全性 + verdict enum + findings_count 整数(producer + consumer 都跑)
  - `verify_evidence_rehash <hb> <repo_root>` — review_log_path 可达 + SHA rehash 比对(**producer only** · 见约束 A)
  - `verify_evidence_consistency <hb> <review_log>` — target_file/ts/codex_model 与 REVIEW-LOG 一致(**producer only**)
  - `verify_evidence_freshness <hb> <review_log>` — R-Q5 时序 check(RL.ts ≤ HB.created ≤ +600s · **producer only**)
  - 7 字段 = verdict / findings_count / review_log_path / review_log_sha256 / target_file / ts / codex_model

### 2. 改 `scripts/verify-ppv-p2.sh`(producer · 行为必须零变化)
- 顶部 source `$SCRIPT_DIR/../lib/handback-validator/verdict-evidence-lib.sh`(注意相对路径 scripts/ ↔ lib/)
- Step 2(line 81-130)+ Step 5(line 163-300)改调 lib 函数,**逻辑严格等价**
- **K10 边界**:line 174-184 / 231-243 的"真路径"脏注释**只动被抽进 lib 的那些行**,verify-ppv-p2 剩余脏注释**不要清**(operator 决策,避免改动面膨胀掩盖真实 diff)

### 3. 新建 `lib/handback-validator/validate-verdict-evidence.sh`(consumer wrapper · shallow)
- source 同一 lib,**只调** `verify_evidence_required`(mode=consumer)
- path 不可达**不** fail-closed(consumer 在 IDS 跑,本地无 XenoDev REVIEW-LOG · 见约束 A)

### 4. R-Q7 · REVIEW-LOG 改 immutable per-review path(改 2 个 SKILL)
- `.claude/skills/codex-review/SKILL.md` §3.6.2(line 280 `cat > .claude/skills/codex-review/REVIEW-LOG.md`):改成写 immutable `real-review/<scope>-round<N>.md`(命名含 round/ts 唯一性 + 写前 noclobber 防同 round 重跑覆盖)**同时** overwrite singleton `REVIEW-LOG.md` 作 **latest pointer**(策略 A:两者并存,各司其职)
- `.claude/skills/codex-review/SKILL.md` §3.6.4(line 317-318):**必须同步改** anti-pattern —— 当前写"append 不覆盖 = ❌""consumer 只读最新",与 immutable 改造直接矛盾;改成"immutable per-review + latest pointer 并存"
- `.claude/skills/parallel-builder/SKILL.md` §3.1.1/§3.1.2(line 342/351 示例):改示例 `review_log_path` 文案为 immutable 范式。**resolve 逻辑 line 262-277 不要改**(已通用,immutable path 仍在 repo 内,自动跟随)

### 5. 新建 `tests/integration/test-verdict-evidence-lib.sh`(characterization 单测)
覆盖 Step 5 全分支:块/inline 正例 · root-level verdict 负例(必须拒) · non-int findings 负例 · 缺字段 fail-closed · SHA mismatch(producer) · path 不可达(producer fail vs consumer 容忍,**两个 mode 各测一次**) · freshness 两向边界(diff<0 / diff>600s)

### 6. 回归验证(抽 lib 无回归 · 三层夹逼 · 这是本任务重点)
- **L1 floor**:`tests/integration/test-ids-verdict-evidence.sh` **必须仍全绿、一字不改**(它自带独立 parser,不 source 新 lib,是验"协议语义"的最强独立锚点)+ `round-trip-006a-pM.sh` 通
- **L2 降级基线**:抽 lib **前**把 verify-ppv-p2 Step 5 段原样拷进临时 probe,跑 self-contained fixture(临时 REVIEW-LOG + 临时 hand-back · SHA/时序自洽)存输出;抽 lib **后** source lib 跑同 fixture,`diff` 必须一致。
  - ⚠️ **不要把基线锚在「现状 verify-ppv-p2 全链 PASS」** —— 它依赖一次真 producer run 产生 SHA 匹配 + 时序新鲜的 hand-back,现状直接跑大概率不 PASS。基线锚在「Step 5 段函数行为等价」。
- **L3**:新单测(第 5 步)全绿

## 经 IDS-side 一手验证的 3 个关键约束(别踩坑)

> 以下都是 IDS operator 用真实代码 grep / 文件存在性验证过的,不是推测。

### 约束 A · consumer verify 深度必须 < producer(高危)
真实 hand-back 的 `review_log_path: .claude/skills/codex-review/REVIEW-LOG.md` 是 **XenoDev** repo-relative。**IDS 本地无此文件**(已验证)。consumer 在 IDS 跑 `shasum` 必然找不到文件。
→ 若 consumer 照搬 producer 的 rehash/path-resolve/fail-closed,**100% 误拒所有合法 hand-back**。
→ 所以第 1 步函数分 mode:producer=full(齐全+rehash+一致性+freshness),consumer=shallow(只齐全性+enum+格式,path 不可达不 fail-closed)。复用 `validate-handback.sh` 既有 `--mode=consumer|producer` 范式(line 27-49)。
→ B-4-IDS line 940-941 normative「不可达=REJECT」只对 producer 成立 —— **本 wave 不改这段 normative**(IDS operator 会在 Changelog 记 known-gap follow-up)。

### 约束 B · R-Q7 真 writer 是 SKILL 不是 gen-handback.sh(高危)
`gen-handback.sh` 对 evidence **0 命中**(已验证)。真 writer = codex-review SKILL line 280;真 inject = parallel-builder SKILL line 331-362。R-Q7 改 codex-review + parallel-builder 两个 SKILL,**别去找 gen-handback.sh**。

### 约束 C · `extract_yaml_field` 不能解 inline map(中)
`_yaml-helpers.sh` line 34 的 grep regex `^${indent}${field}:` 只匹配**块形式**行首字段,inline map `{...}` 里的子键解不出。
→ lib 里块形式子键可用 `extract_yaml_field`,inline map **必须保留** verify-ppv-p2 现有 `parse_hb_evidence_inline`(line 209-224)逻辑搬进 lib。

## 6 个不变量(实现期持续核对)
1. `test-ids-verdict-evidence.sh` 一字不改(独立验证锚点)
2. `verify-ppv-p2.sh` 脏注释只清被抽进 lib 的行(K10)
3. consumer verify 深度 < producer(约束 A)
4. latest pointer 与 immutable evidence 并存(verify-ppv-p2 line 37 默认值不动)
5. (本不变量属 IDS 半边)
6. (本不变量属 IDS 半边)

## scope 边界(不做什么)
- ❌ 不改 B-4-IDS line 940-941 normative 文字(超 P0 scope · IDS operator 留 follow-up)
- ❌ 不清 verify-ppv-p2 / REVIEW-LOG 正文残留脏注释(K10 operator 决策)
- ❌ 不动 parallel-builder resolve line 262-277 / verify-ppv-p2 line 37/246(已通用,自动跟随)
- ❌ 不碰 IDS 半边(mirror cp / SHARED-CONTRACT / contract bump / handback-review.md)—— 那是 IDS operator 做
- ❌ 不碰 P1 波(D-precedent / cross_repo_split 升 §6)

## 完成后交付给 IDS operator
1. `lib/handback-validator/verdict-evidence-lib.sh` 最终内容 + `shasum -a 256`
2. `lib/handback-validator/validate-verdict-evidence.sh` 最终内容 + `shasum -a 256`
3. 回归三层验证结果(L1 全绿截图/输出 · L2 diff 一致 · L3 新单测全绿)
4. R-Q7 改后 review_log_path 的 immutable 范式实例(eg `real-review/T0XX-round1.md`)—— IDS operator 要据此改 SHARED-CONTRACT 示例(line 910/924)
5. XenoDev 仓 commit(不 push · 等 operator 确认)

## commit 规约(XenoDev 仓)
- Conventional Commits · commit 前跑 `git status --untracked-files=all`
- 建议 XenoDev 半边合 1 个 commit(抽 lib + verify-ppv-p2 改调 + wrapper + R-Q7 两 SKILL + 新单测)
- **不主动 push**

---

## (IDS operator 自留 · 不贴给 XenoDev)IDS 半边等 XenoDev 交付后做
- cp lib + wrapper 到 `framework/xenodev-bootstrap-kit/handback-validator/` + SHA dual-verify
- MANIFEST-v0.2.md 加两行(建议 §wave-4)+ mirror-sha 测试 + 扩 verify-ppv-p1 v02_scope_path
- 改 handback-review.md Step 4 加调 wrapper + allowed-tools 权限
- 改 SHARED-CONTRACT:示例 line 910/924 改 immutable + frontmatter 2.2→2.3 + status + last_updated + Changelog(含 R9 known-gap)
- 不变量 5(cp 先于改调用)+ 6(bump 与示例同 commit)
- IDS 验证:verify-ppv-p1 通 + /handback-review smoke 不误拒
