#!/usr/bin/env bash
# verdict-evidence-lib.sh — 共享 verdict-evidence 解析 + verify helpers
#
# 结论先:本 lib 把 scripts/verify-ppv-p2.sh 的 7 字段 ids_verdict_evidence 解析
# + verify 逻辑抽成 source-able 共享件,让 producer(verify-ppv-p2.sh)与
# consumer(validate-verdict-evidence.sh)双方复用,行为严格等价。
# Provenance:idea 006 forge v4 · P0 原子波 · 抽自 verify-ppv-p2.sh line 55-300。
#
# 设计范式(严格仿同目录 _yaml-helpers.sh):
#   - 此 helper **被 source**,不直接执行;不应有 set -euo pipefail
#     (会污染调用方 shell 选项)。函数本身用 local var + return code 控错。
#   - 0 外部依赖(只 awk/grep/sed/shasum/date · 与既存 5 validator 一致)。
#   - 中文注释 · 先结论后细节。
#
# ⚠️ 行为等价铁律(经一手实证 · 见 tests/integration/test-verdict-evidence-lib.sh):
#   块形式子键解析**不可**改调 _yaml-helpers.sh 的 extract_yaml_field —— 后者会
#   strip 行内注释 / 引号 / 尾随空白,而原 producer awk 全保留;这些值喂给
#   verdict enum grep + findings_count 整数校验 + target_file/ts/codex_model 精确 =
#   比较,strip 与否会**翻转** producer 的 FAIL/PASS exit path。故块形式 parser 逐字
#   port 原 awk(gsub/sub 不 strip),inline map 同样逐字 port。
#
# ── mode 语义(per validate-handback.sh --mode 范式)──
#   producer:full 校验(required + rehash + consistency + freshness)
#   consumer:shallow 校验(只 required)· 因真 hand-back 的 review_log_path 是
#     XenoDev repo-relative,IDS consumer 本地无此文件,跑 rehash/path-fail-closed
#     会 100% 误拒合法包(forge v4 一手验证)。
#
# ── 接口 ──
#   is_nonneg_int <val>
#     非负整数 → return 0;否则 return 1(无输出)
#   parse_evidence_field <file> <field>
#     从 ids_verdict_evidence 父键(块形式 OR inline map)解任意子字段;
#     stdout = raw value(保留注释/引号/尾空格);未找到 → 空 string
#   parse_evidence_verdict_findings <file>
#     专解 verdict + findings_count(原 extract_hb_evidence 状态机 · 2-空格-exact);
#     stdout = "<verdict>\t<findings>"(tab 分隔)
#   verify_evidence_required <file> <mode>
#     verdict/findings 无条件查(空 + enum + int);若有 ids_verdict_evidence 父键则
#     5 额外字段(review_log_path/sha256/target_file/ts/codex_model)必填;
#     两 mode 都跑;PASS → return 0;FAIL → stderr 报因 + return 1
#   verify_evidence_rehash <file> <xenodev_root>      [producer only]
#     resolve $xenodev_root/review_log_path · rehash sha256 对比 · 不可达 fail-closed
#   verify_evidence_consistency <file> <xenodev_root> [producer only]
#     target_file/ts/codex_model 与 REVIEW-LOG 自身 frontmatter 一致性
#   verify_evidence_freshness <review_log> <file>     [producer only]
#     REVIEW-LOG ts 与 hand-back created 时序:TS_DIFF <0(倒序)或 >600s(stale)→ FAIL

# ──────────────────────────────────────────────────────────────
# is_nonneg_int — 共用整数校验(port verify-ppv-p2.sh line 55-60)
# architecture.md §3.4 schema 规定 findings_count: <int>
# ──────────────────────────────────────────────────────────────
is_nonneg_int() {
  case "$1" in
    ''|*[!0-9]*) return 1 ;;
    *) return 0 ;;
  esac
}

# ──────────────────────────────────────────────────────────────
# parse_evidence_verdict_findings — 专解 verdict + findings_count
# 逐字 port verify-ppv-p2.sh line 81-130 extract_hb_evidence 状态机。
# ⚠️ 注意:本提取体用 2-空格-exact 缩进 + `[A-Za-z_]` 退块语义,与
#   parse_evidence_field 的 any-indent + `[a-zA-Z]` 略不同 —— 二者各保留原样
#   以严格等价 producer(混并单一 parser 会改 producer 行为,经设计评审确认)。
# 同时支持块形式(Form A)与 inline map(Form B)。
# stdout: "<verdict>\t<findings>"
# ──────────────────────────────────────────────────────────────
parse_evidence_verdict_findings() {
  local hb="$1"
  awk '
    BEGIN { in_fm = 0; in_block = 0; v = ""; f = ""; }
    /^---$/ {
      if (in_fm == 0) { in_fm = 1; next }
      else { exit }
    }
    in_fm == 1 {
      # Form B · inline map
      if ($0 ~ /^ids_verdict_evidence:[[:space:]]*\{/) {
        line = $0
        if (match(line, /verdict:[[:space:]]*[A-Za-z_-]+/)) {
          val = substr(line, RSTART, RLENGTH)
          sub(/^verdict:[[:space:]]*/, "", val)
          v = val
        }
        if (match(line, /findings_count:[[:space:]]*[0-9]+/)) {
          val = substr(line, RSTART, RLENGTH)
          sub(/^findings_count:[[:space:]]*/, "", val)
          f = val
        }
        next
      }
      # Form A · 父键开块
      if ($0 ~ /^ids_verdict_evidence:[[:space:]]*$/) {
        in_block = 1
        next
      }
      # 在父键块内 · 仅读缩进 2 空格的子键
      if (in_block == 1) {
        # 遇到下一个顶层键(非缩进 alphabetic) · 退出 block
        if ($0 ~ /^[A-Za-z_]/) { in_block = 0 }
        else if ($0 ~ /^  verdict:[[:space:]]/) {
          gsub(/^  verdict:[[:space:]]*/, "")
          v = $0
        }
        else if ($0 ~ /^  findings_count:[[:space:]]/) {
          gsub(/^  findings_count:[[:space:]]*/, "")
          f = $0
        }
      }
    }
    END {
      print v "\t" f
    }
  ' "$hb"
}

# ──────────────────────────────────────────────────────────────
# parse_evidence_field — 解 ids_verdict_evidence 父键下任意子字段
# 内部分支:先块形式(port verify-ppv-p2.sh line 185-200 parse_hb_evidence_field),
#   空则 fallback inline map(port line 209-224 parse_hb_evidence_inline)。
# ⚠️ 不 strip 注释/引号/尾空格(逐字 port · 见铁律)。
# stdout: raw value;未找到 → 空 string
# ──────────────────────────────────────────────────────────────
parse_evidence_field() {
  local hb="$1" field="$2" val
  # 块形式(any-indent + `[a-zA-Z]` 退块 · 保留注释/引号/尾空格)
  val=$(awk -v f="$field" '
        /^---$/{n++; if(n==2) exit; next}
        n==1 && /^ids_verdict_evidence:[[:space:]]*$/ { in_block=1; next }
        n==1 && in_block && /^[a-zA-Z]/ { in_block=0 }
        n==1 && in_block && /^[[:space:]]+/ {
            sub(/^[[:space:]]+/, "", $0)
            if (match($0, "^"f":[[:space:]]*")) {
                val = substr($0, RSTART+RLENGTH)
                print val
                exit
            }
        }
    ' "$hb")
  # fallback · inline map(per SHARED-CONTRACT §6 B-4-IDS · 2 yaml 写法)
  if [ -z "$val" ]; then
    val=$(awk -v f="$field" '
        /^---$/{n++; if(n==2) exit; next}
        n==1 && /^ids_verdict_evidence:[[:space:]]*\{/ {
            line = $0
            if (match(line, f"[[:space:]]*:[[:space:]]*[^,}]+")) {
                m = substr(line, RSTART, RLENGTH)
                sub(/^[^:]+:[[:space:]]*/, "", m)
                gsub(/^[[:space:]]+|[[:space:]]+$/, "", m)
                print m
                exit
            }
        }
    ' "$hb")
  fi
  printf '%s' "$val"
}

# ──────────────────────────────────────────────────────────────
# verify_evidence_required — 7 字段齐 + enum + 整数(两 mode 都跑)
# 逐字 port verify-ppv-p2.sh:
#   - verdict/findings 无条件查(line 136-145):空 + enum + int
#   - 5 额外字段 gate 在 `grep -q '^ids_verdict_evidence:'`(line 231-241)
# ⚠️ 保留 producer 不对称:verdict/findings 无条件 · 5 字段有条件;
#   presence-guard regex 用 `^ids_verdict_evidence:`(无尾锚,inline+块都匹配)。
# Args: $1=file $2=mode(producer|consumer · 本函数两 mode 行为相同,mode 仅为对称/messaging)
# Returns: PASS → 0;FAIL → stderr 报因 + 1
# ──────────────────────────────────────────────────────────────
verify_evidence_required() {
  local hb="$1" mode="${2:-consumer}"
  local EVIDENCE HB_VERDICT HB_FINDINGS

  # verdict + findings(无条件 · port Step 2 line 132-147)
  EVIDENCE=$(parse_evidence_verdict_findings "$hb")
  HB_VERDICT=$(echo "$EVIDENCE" | cut -f1)
  HB_FINDINGS=$(echo "$EVIDENCE" | cut -f2)

  [ -n "$HB_VERDICT" ] \
    || { echo "PPV-P2 FAIL: hand-back frontmatter 缺 ids_verdict_evidence.verdict (父键绑定后未找到子键 · 注意只接受块形式或 inline map · 不接受 root-level verdict)" >&2; return 1; }
  [ -n "$HB_FINDINGS" ] \
    || { echo "PPV-P2 FAIL: hand-back frontmatter 缺 ids_verdict_evidence.findings_count" >&2; return 1; }

  echo "$HB_VERDICT" | grep -qE '^(approve|needs-attention)$' \
    || { echo "PPV-P2 FAIL: hand-back ids_verdict_evidence.verdict=$HB_VERDICT 非 enum {approve, needs-attention}" >&2; return 1; }
  is_nonneg_int "$HB_FINDINGS" \
    || { echo "PPV-P2 FAIL: hand-back ids_verdict_evidence.findings_count=$HB_FINDINGS 非非负整数(architecture.md §3.4 schema <int>)" >&2; return 1; }

  # 5 额外字段(有条件 · gate 在 ids_verdict_evidence 父键存在时 · port line 231-241)
  if grep -q '^ids_verdict_evidence:' "$hb"; then
      local HB_RL_PATH HB_RL_SHA256 HB_TARGET_FILE HB_RL_TS_FIELD HB_CODEX_MODEL
      HB_RL_PATH=$(parse_evidence_field "$hb" review_log_path)
      HB_RL_SHA256=$(parse_evidence_field "$hb" review_log_sha256)
      HB_TARGET_FILE=$(parse_evidence_field "$hb" target_file)
      HB_RL_TS_FIELD=$(parse_evidence_field "$hb" ts)
      HB_CODEX_MODEL=$(parse_evidence_field "$hb" codex_model)
      local required_field val
      for required_field in HB_RL_PATH HB_RL_SHA256 HB_TARGET_FILE HB_RL_TS_FIELD HB_CODEX_MODEL; do
          eval "val=\$$required_field"
          if [ -z "$val" ]; then
              echo "PPV-P2 FAIL: hand-back ids_verdict_evidence 真路径缺字段 $required_field · per SHARED-CONTRACT §6 B-4-IDS 7-field immutable binding · fail-closed" >&2
              return 1
          fi
      done
  fi
  return 0
}

# ──────────────────────────────────────────────────────────────
# resolve_review_log_path — [producer only] canonicalize + allowlist review_log_path
# 安全 chokepoint(per codex adversarial-review Finding 2 · trust-boundary 加固):
#   review_log_path 是 hand-back 可控输入 · 原 `$xenodev/$path` 裸拼接无 canonicalize/
#   allowlist → `../` 段或 repo 内 review-log 区外的 frontmatter-shaped + SHA 匹配文件
#   会被当 evidence 源(已实证逃逸)。本 helper 做两道防线:
#     (1) canonicalize(realpath -P · 解 `../` / symlink 到物理真路径)
#     (2) allowlist:解出的真路径必须落在 review-log canonical 区:
#         <xenodev>/.claude/skills/codex-review/REVIEW-LOG.md(singleton latest-pointer)
#         <xenodev>/.claude/skills/codex-review/real-review/(immutable per-review 记录)
#   出区 / 不可达 / 不在 allowlist → fail-closed(stderr 报因 + return 1)。
# rehash / consistency / verify-ppv-p2 Step 0 rebind 全经本 helper(单一 chokepoint)。
# Args: $1=review_log_path(hand-back 原值) $2=xenodev_root
# Returns: stdout = 解出的物理真路径(通过 allowlist);拒 → stderr + return 1
# ──────────────────────────────────────────────────────────────
resolve_review_log_path() {
  local rl_path="$1" xenodev="$2"
  local raw resolved allow_singleton allow_realdir xen_canon
  raw="$xenodev/$rl_path"
  # canonicalize 到物理真路径(解 ../ + symlink)· 文件须存在
  # 注:macOS BSD realpath **不支持 -P**(GNU flag)· 裸 realpath 两平台都解 symlink + ../
  # 到物理真路径且要求路径存在(同 date -j/-d 的 dual-platform 范式)。
  resolved=$(realpath "$raw" 2>/dev/null || true)
  if [ -z "$resolved" ] || [ ! -f "$resolved" ]; then
      echo "PPV-P2 FAIL: hand-back review_log_path=$rl_path 真路径 resolve 真路径 不存在或不可 canonicalize ($raw) · per B-4-IDS 真路径 immutable binding 真路径 fail-closed" >&2
      return 1
  fi
  # allowlist:canonical 真路径必须 == singleton 或落在 real-review/ 区内
  # (xenodev 自身也 canonicalize · 防 xenodev 含 symlink 时前缀对不上 · eg macOS /var→/private/var)
  xen_canon=$(realpath "$xenodev" 2>/dev/null || printf '%s' "$xenodev")
  allow_singleton="$xen_canon/.claude/skills/codex-review/REVIEW-LOG.md"
  allow_realdir="$xen_canon/.claude/skills/codex-review/real-review/"
  case "$resolved" in
    "$allow_singleton") : ;;                 # OK · singleton latest-pointer
    "$allow_realdir"*) : ;;                   # OK · real-review/<…> immutable 记录
    *)
      echo "PPV-P2 FAIL: hand-back review_log_path=$rl_path 真路径 canonical=$resolved 真路径不在 allowlist · per codex F2 trust-boundary · 只准 .claude/skills/codex-review/REVIEW-LOG.md 或 real-review/ 下 · fail-closed" >&2
      return 1
      ;;
  esac
  printf '%s' "$resolved"
  return 0
}

# ──────────────────────────────────────────────────────────────
# verify_evidence_rehash — [producer only] review_log_path resolve + sha256 rehash
# 逐字 port verify-ppv-p2.sh line 244-253 + 272-276(不可达 fail-closed)·
# resolve 经 resolve_review_log_path(canonicalize + allowlist · per codex F2)。
# Args: $1=file $2=xenodev_root
# Returns: PASS → 0;mismatch / 不可达 / 出 allowlist → stderr 报因 + 1
# ⚠️ consumer 绝不调本函数(review_log_path 是 XenoDev repo-relative,IDS 不可达)。
# ──────────────────────────────────────────────────────────────
verify_evidence_rehash() {
  local hb="$1" xenodev="$2"
  local HB_RL_PATH HB_RL_SHA256
  HB_RL_PATH=$(parse_evidence_field "$hb" review_log_path)
  HB_RL_SHA256=$(parse_evidence_field "$hb" review_log_sha256)

  if [ -n "$HB_RL_PATH" ] && [ -n "$HB_RL_SHA256" ]; then
      local HB_RL_PATH_RESOLVED REHASH
      # canonicalize + allowlist(per codex F2 · 不可达/出区即 fail-closed · 内含原"不存在"报因)
      HB_RL_PATH_RESOLVED=$(resolve_review_log_path "$HB_RL_PATH" "$xenodev") || return 1
      # rehash(防 stale REVIEW-LOG 被改 / 伪造)
      REHASH=$(shasum -a 256 "$HB_RL_PATH_RESOLVED" | awk '{print $1}')
      if [ "$REHASH" != "$HB_RL_SHA256" ]; then
          echo "PPV-P2 FAIL: hand-back review_log_sha256=$HB_RL_SHA256 真路径 vs 真路径 rehash=$REHASH · stale/伪造 · per R-Q5 + R2 P1" >&2
          return 1
      fi
  fi
  return 0
}

# ──────────────────────────────────────────────────────────────
# verify_evidence_consistency — [producer only] target_file/ts/codex_model 一致性
# 逐字 port verify-ppv-p2.sh line 255-271。
# 前提:review_log_path resolve 后存在(由 verify_evidence_rehash 先跑保证);
#   本函数自身亦 resolve 并仅在文件存在时比对(与原行为一致:rehash 段已 fail-closed
#   不可达,故 producer 链中 consistency 必在可达后跑)。
# Args: $1=file $2=xenodev_root
# Returns: 一致 → 0;mismatch → stderr 报因 + 1
# ──────────────────────────────────────────────────────────────
verify_evidence_consistency() {
  local hb="$1" xenodev="$2"
  local HB_RL_PATH HB_RL_SHA256 HB_TARGET_FILE HB_RL_TS_FIELD HB_CODEX_MODEL
  HB_RL_PATH=$(parse_evidence_field "$hb" review_log_path)
  HB_RL_SHA256=$(parse_evidence_field "$hb" review_log_sha256)
  HB_TARGET_FILE=$(parse_evidence_field "$hb" target_file)
  HB_RL_TS_FIELD=$(parse_evidence_field "$hb" ts)
  HB_CODEX_MODEL=$(parse_evidence_field "$hb" codex_model)

  if [ -n "$HB_RL_PATH" ] && [ -n "$HB_RL_SHA256" ]; then
      local HB_RL_PATH_RESOLVED REAL_RL_TARGET REAL_RL_TS REAL_RL_MODEL
      # canonicalize + allowlist(per codex F2 · 单一 chokepoint · producer 链中 rehash 已先跑保证可达)
      HB_RL_PATH_RESOLVED=$(resolve_review_log_path "$HB_RL_PATH" "$xenodev") || return 1
      # verify target_file / ts / codex_model 与 REVIEW-LOG 一致
      REAL_RL_TARGET=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^target_file:/{print $2; exit}' "$HB_RL_PATH_RESOLVED")
      REAL_RL_TS=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^ts:/{print $2; exit}' "$HB_RL_PATH_RESOLVED")
      REAL_RL_MODEL=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^codex_model:/{print $2; exit}' "$HB_RL_PATH_RESOLVED")

      if [ -n "$HB_TARGET_FILE" ] && [ "$HB_TARGET_FILE" != "$REAL_RL_TARGET" ]; then
          echo "PPV-P2 FAIL: hand-back target_file=$HB_TARGET_FILE != REVIEW-LOG target_file=$REAL_RL_TARGET" >&2
          return 1
      fi
      if [ -n "$HB_RL_TS_FIELD" ] && [ "$HB_RL_TS_FIELD" != "$REAL_RL_TS" ]; then
          echo "PPV-P2 FAIL: hand-back ts=$HB_RL_TS_FIELD != REVIEW-LOG ts=$REAL_RL_TS" >&2
          return 1
      fi
      if [ -n "$HB_CODEX_MODEL" ] && [ "$HB_CODEX_MODEL" != "$REAL_RL_MODEL" ]; then
          echo "PPV-P2 FAIL: hand-back codex_model=$HB_CODEX_MODEL != REVIEW-LOG codex_model=$REAL_RL_MODEL" >&2
          return 1
      fi
  fi
  return 0
}

# ──────────────────────────────────────────────────────────────
# verify_evidence_freshness — [producer only] REVIEW-LOG ts 与 hand-back created 时序
# 逐字 port verify-ppv-p2.sh line 279-300(含 dual macOS/GNU date fallback)。
# REVIEW-LOG ts 必须 ≤ hand-back created;> 600s = stale fail-closed。
# Args: $1=review_log 路径 $2=file(hand-back)
# Returns: 在界内 → 0;倒序 / stale → stderr 报因 + 1
# ──────────────────────────────────────────────────────────────
verify_evidence_freshness() {
  local review_log="$1" hb="$2"
  local RL_TS HB_CREATED RL_TS_EPOCH HB_TS_EPOCH TS_DIFF
  RL_TS=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^ts:/{print $2; exit}' "$review_log")
  HB_CREATED=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^created:/{print $2; exit}' "$hb")
  if [ -n "$RL_TS" ] && [ -n "$HB_CREATED" ]; then
      # ISO 8601 timestamp diff(dual macOS `date -j` / GNU `date -d`)
      RL_TS_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$RL_TS" +%s 2>/dev/null || date -d "$RL_TS" +%s 2>/dev/null)
      HB_TS_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$HB_CREATED" +%s 2>/dev/null || date -d "$HB_CREATED" +%s 2>/dev/null)
      if [ -n "$RL_TS_EPOCH" ] && [ -n "$HB_TS_EPOCH" ]; then
          TS_DIFF=$((HB_TS_EPOCH - RL_TS_EPOCH))
          if [ "$TS_DIFF" -lt 0 ]; then
              echo "PPV-P2 FAIL: hand-back created($HB_CREATED) 早于 REVIEW-LOG ts($RL_TS) · per R-Q5 时序加固" >&2
              return 1
          fi
          if [ "$TS_DIFF" -gt 600 ]; then
              echo "PPV-P2 FAIL: REVIEW-LOG ts($RL_TS) vs hand-back created($HB_CREATED) 真路径 diff=${TS_DIFF}s > 10min · stale REVIEW-LOG 真路径 fail-closed · per R-Q5" >&2
              return 1
          fi
      fi
  fi
  return 0
}

# ──────────────────────────────────────────────────────────────
# verify_evidence_latest — [producer only] G3 堵重放窗 · verdict-direction latest 校验
#
# 结论先:freshness(600s 窗)只证"不太旧",**不**证"绑的是当前最新那份"。本函数加一道
# latest 校验堵重放场景:10:00 approve → 10:05 needs-attention → 10:06 绑旧 approve 仍在
# 600s 窗内过 gate。Provenance:idea 006 forge v5 · P0 原子波(M0-3 · brief §4)。
# SOTA 借鉴:TUF rollback/freeze(版本单调 · 旧 metadata 不能覆盖新状态)· 滤掉 threshold signing。
#
# 真相源(约束 B · 不新加字段):singleton REVIEW-LOG 的 latest_review_log 字段
#   (由 write_review_log_immutable 每次 review 写 · 指向当次 immutable 记录)就是
#   "当前最新那份是谁"。本函数读它与 hand-back 绑的 bound log 比对。
#
# ⚠️ 边界 = verdict-direction guard(operator 决议 · per codex adversarial-review F1 加固):
#   初版"硬 latest equality"会**误杀合法的较早 task** —— 同 target_file=working-tree 下,
#   review task A → review task B 后 singleton.latest 翻到 B,ship A 的合法 hand-back(绑 A
#   自己真做过的 immutable log)被硬 equality 当 replay 拒。多 worktree 并发跑起来后这是常态。
#   codex F1[high] 已复现。改为 **target_file scoping + verdict-direction 耦合**:
#     - bound == latest         → 过(当前最新 · 恒安全)
#     - bound == singleton 本身 → 过(live pointer · 不可能 replay · 见下)
#     - bound.target_file != latest.target_file → 过(跨 scope · latest 是别的 target 的 review ·
#       不构成本 scope replay 真相源 · per codex F1 二轮:单 global singleton 不分 scope overwrite)
#     - 同 scope 非-latest 具体 immutable 记录:
#         · bound.verdict 比 latest.verdict **更乐观**(bound=approve 而 latest=needs-attention)
#           → **拒**(这正是 replay 签名:绑旧 approve 偷过同 scope 的新 needs-attention)
#         · 否则(verdict 不矛盾 / bound 同等或更保守)→ **过**(合法的较早 task · A 自己的 log)
#   原理:replay 之所以危险,是用旧 approve 覆盖当前已知的 needs-attention 坏态。只有这一方向
#   危险。bound 同 verdict 或 bound=needs-attention 不构成"偷乐观",放行不误杀合法异步 ship。
#   freshness(Step 5 的 600s 窗)独立兜"绝对太旧",两道叠加。
#
# 边界其余(operator plan 期决议 · brief §4 步骤 1):
#   - **缺 latest_review_log 字段 / singleton 不存在 → skip 放行(return 0)**:transitional
#     /legacy workspace(writer 首跑前)· 硬拒会误杀合法 legacy 包(违反不变量「不误杀合法包」)。
#     已知 gap(per codex F2[medium]):此 skip 在最易出 stale 元数据的 transitional 态重开重放窗;
#     operator 决议维持 skip-open(writer 首跑后字段就有 · 全新无 review workspace 本就无包可 ship)·
#     记 IDS handoff known-gap。
#
# K9 依赖:拒旧乐观 log 的底气来自 operator 批准的 K9 收紧(ship 强制绑 immutable + latest)。
#
# Args:
#   $1 = bound_review_log  hand-back 绑的 effective REVIEW_LOG(已经 Step 0 canonicalize)
#   $2 = singleton_path    singleton REVIEW-LOG 路径(.claude/skills/codex-review/REVIEW-LOG.md)
#   $3 = xenodev_root      用于 canonicalize latest_review_log(经 resolve_review_log_path allowlist)
# Returns:
#   bound==latest / bound==singleton / verdict 不矛盾 / 缺字段 skip → 0;
#   bound 偷乐观(approve vs latest needs-attention)/ latest 不可达 → stderr 报因 + 1
# ⚠️ consumer 绝不调本函数(同 rehash/consistency · review_log_path 是 XenoDev repo-relative)。
# ──────────────────────────────────────────────────────────────
verify_evidence_latest() {
  local bound_review_log="$1" singleton_path="$2" xenodev="$3"
  local LATEST_RAW BOUND_CANON LATEST_CANON SINGLETON_CANON BOUND_VERDICT LATEST_VERDICT

  # singleton 不存在 → 无真相源可比 · skip(transitional · 与 Step 0 未绑分支一致 · 不在此 fail)
  [ -f "$singleton_path" ] || return 0

  # bound_review_log 已是 Step 0 canonicalize 后的物理真路径 · 再 canonicalize 一次保险(幂等)
  BOUND_CANON=$(realpath "$bound_review_log" 2>/dev/null || printf '%s' "$bound_review_log")
  SINGLETON_CANON=$(realpath "$singleton_path" 2>/dev/null || printf '%s' "$singleton_path")

  # ⚠️ 绑 singleton 本身 → 恒过(不可能是 replay)。
  #   singleton(REVIEW-LOG.md)是 live latest-pointer:每次 review 被 overwrite 成当前最新。
  #   绑它 == 隐式绑"whatever latest is" · 永远反映当前 verdict · 不存在绑旧的可能。
  #   replay 威胁模型只针对绑**具体 immutable 记录**(10:00 approve 这种定格快照)。
  #   注:绑 singleton 是 verify-ppv-p2.sh:43 的 default · test-ids-verdict-evidence case A/B
  #   的 canonical 合法形态;硬拒它会误杀绝大多数合法包(本验证步实测暴露)。
  if [ "$BOUND_CANON" = "$SINGLETON_CANON" ]; then
      return 0
  fi

  # 绑的是具体 immutable 记录 → 读 singleton 当前指向的 latest_review_log。
  # 读 singleton 的 latest_review_log 字段(awk frontmatter · 同 lib 既有范式)
  LATEST_RAW=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^latest_review_log:/{sub(/^latest_review_log:[[:space:]]*/, "", $0); print $0; exit}' "$singleton_path")

  # 缺字段 → skip 放行(operator 决议 · 防误杀 legacy · writer 首跑后字段就有 · per codex F2 known-gap)
  if [ -z "$LATEST_RAW" ]; then
      return 0
  fi

  # latest_review_log canonicalize + allowlist(复用单一 chokepoint · 不可达/出区 fail-closed)
  LATEST_CANON=$(resolve_review_log_path "$LATEST_RAW" "$xenodev") || {
      echo "PPV-P2 FAIL: singleton latest_review_log=$LATEST_RAW 不可 canonicalize / 出 allowlist · per G3 fail-closed" >&2
      return 1
  }

  # bound == latest → 过(当前最新 · 恒安全)
  if [ "$BOUND_CANON" = "$LATEST_CANON" ]; then
      return 0
  fi

  # ── target_file scoping(per codex F1 二轮加固)──
  # 单 global singleton 对**每个** review 都 overwrite(不分 scope)· latest 可能是**无关 scope**
  # 的 review。replay 威胁只在**同一 review scope 内**成立(绑旧 approve 偷过同 scope 的新 needs-attention);
  # 跨 scope 的 needs-attention(review 了别的 target)不该 invalidate 本 scope 的旧 approve。
  # 故:先比 bound 与 latest 的 target_file —— 不同 scope → latest 非本 scope 真相源 → 放行(不误杀)。
  # 同 scope 才走 verdict-direction guard。
  BOUND_TARGET=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^target_file:/{print $2; exit}' "$BOUND_CANON")
  LATEST_TARGET=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^target_file:/{print $2; exit}' "$LATEST_CANON")
  if [ -n "$BOUND_TARGET" ] && [ -n "$LATEST_TARGET" ] && [ "$BOUND_TARGET" != "$LATEST_TARGET" ]; then
      # 跨 scope · latest 是别的 target 的 review · 不构成本 scope 的 replay 真相源 → 放行
      return 0
  fi

  # bound 是非-latest 的**同 scope** 具体 immutable 记录 → verdict-direction guard(per codex F1 加固):
  #   只拒"偷乐观"(bound=approve 而 latest=needs-attention · replay 签名)· 其余放行不误杀合法较早 task。
  BOUND_VERDICT=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^verdict:/{print $2; exit}' "$BOUND_CANON")
  LATEST_VERDICT=$(awk '/^---$/{n++; if(n==2) exit; next} n==1 && /^verdict:/{print $2; exit}' "$LATEST_CANON")

  if [ "$BOUND_VERDICT" = "approve" ] && [ "$LATEST_VERDICT" = "needs-attention" ]; then
      echo "PPV-P2 FAIL: hand-back 绑的旧 review log(同 scope target_file=$BOUND_TARGET · verdict=approve)比当前 latest(verdict=needs-attention)更乐观 · 疑似 replay 偷过新的 needs-attention · per G3" >&2
      echo "  bound=$BOUND_CANON (approve)" >&2
      echo "  latest(singleton.latest_review_log)=$LATEST_CANON (needs-attention)" >&2
      return 1
  fi
  return 0
}
