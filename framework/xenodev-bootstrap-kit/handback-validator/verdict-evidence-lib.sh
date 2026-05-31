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
