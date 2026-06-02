#!/usr/bin/env bash
# review-log-writer-lib.sh — R-Q7 immutable REVIEW-LOG writer（source-able 抽离件）
#
# 结论先:本 lib 把 codex-review SKILL §3.6.2 内联在 Markdown bash 代码块里的
# immutable 写 + noclobber 原子占位 + singleton latest-pointer 逻辑,抽成一个
# **被 source 的函数** write_review_log_immutable,让并发同秒 stress 测试能真调它跑。
# Provenance:idea 006 forge v5 · P0 原子波(M0-2)· 抽自 SKILL §3.6.2 line 287-338。
#
# 为什么必须抽（约束 A · brief §2 一手验证）:
#   原 writer 嵌在 .claude/skills/codex-review/SKILL.md 的 Markdown bash 代码块里,
#   不是 source-able 脚本/函数 → 测试无法 source 调用 → 这套 immutable 范式从没真跑过
#   (real-review/ 目录至今不存在)。抽成 lib 后 SKILL 改为调用,stress 测试才能压并发。
#
# 设计范式（严格仿同目录 verdict-evidence-lib.sh）:
#   - 此 helper **被 source**,不直接执行;不应有 set -euo pipefail(会污染调用方 shell 选项)。
#     函数本身用 local var + return code 控错(原 SKILL 块用 exit 1,抽成 lib 改 return 1 —
#     这是抽离的标准等价转换,调用方语义不变)。
#   - 0 外部依赖(只 mkdir/tr/printf/cat · 与既存 validator 一致)。
#   - 中文注释 · 先结论后细节。
#
# ⚠️ 行为等价（不变量 4 · brief §5）:
#   命名方案(ts-based scope-slug)/ noclobber 原子占位 / latest-pointer 语义保持等价。
#   immutable 记录 + singleton **内容** 与原 SKILL §3.6.2 byte-equal(L2 验)。
#   **一处增强(非 byte-equal · 行为等价)**:singleton 写从原裸 `cat > REVIEW-LOG.md` 改为
#   temp 文件 + 原子 `mv` rename(per codex adversarial-review F2 · 防 different-ts 并发 writer
#   race/tear singleton)· 产出**内容**不变 · 只是写入路径更原子 · 仍是 single latest pointer。

# ──────────────────────────────────────────────────────────────
# write_review_log_immutable — 产一条 immutable per-review 记录 + overwrite singleton latest-pointer
#
# 结论先:每次 review 产**不可变**记录(noclobber 守同秒碰撞 · 绝不覆盖已存在),
# 同时 overwrite singleton REVIEW-LOG 作 latest pointer(写 latest_review_log 字段指向该记录)。
# 动机:老单点 cat > 覆盖会 invalidate 老 hand-back 的 review_log_sha256 binding(R-Q7 协议债)。
#
# 命名方案 = ts-based(拒 round-count 的 TOCTOU race · 原 §3.6.2 scope 内无 $round/$scope 变量):
#   immutable 文件:<rr_dir_base>/real-review/<scope-slug>-<ts-slug>.md
#   <scope-slug> = target_file 经 tr 转文件名安全;<ts-slug> = ts 去冒号(秒级已唯一)
#   noclobber 守同秒碰撞(抄 gen-handback.sh 的 set -o noclobber 原子占位)→ 真 immutable
#
# Args:
#   $1 = rr_dir_base    review-log 根目录(生产传 .claude/skills/codex-review · 测试可指向 tmp)
#   $2 = review_type    REVIEW_TYPE(adversarial-review|review · 调用方已 normalize)
#   $3 = target_file    TARGET_FILE(scope · 默认 working-tree)
#   $4 = verdict        VERDICT(approve|needs-attention · 调用方已 enum 校验)
#   $5 = findings_count FINDINGS_COUNT(non-neg int · 调用方已校验)
#   $6 = codex_model    CODEX_MODEL
#   $7 = duration       DURATION(seconds)
#   $8 = ts             TS(ISO 8601 · 调用方算 date -u)
# Returns:
#   PASS → stdout = 产出的 immutable 记录路径($RR_FILE) · return 0
#   同秒/重跑碰撞(noclobber 拒)→ stderr 报因 · return 1(不覆盖已存在记录 · immutable 契约)
# ──────────────────────────────────────────────────────────────
write_review_log_immutable() {
  local rr_dir_base="$1" review_type="$2" target_file="$3" verdict="$4"
  local findings_count="$5" codex_model="$6" duration="$7" ts="$8"
  local RR_DIR SCOPE_SLUG TS_SLUG RR_FILE REVIEW_BODY

  # ⚠️ 契约:rr_dir_base **必须 repo-relative**(per codex adversarial-review F2 三轮加固)。
  #   原因:RR_FILE / latest_review_log 直接由 rr_dir_base 拼成 · 若传**绝对**路径,singleton 存的
  #   latest_review_log 是绝对的,而 resolve_review_log_path 无条件 `$xenodev/$path` 拼接 → 双拼接
  #   不可达 → verify_evidence_latest 把 writer 自己的产物当出界拒(内部契约自相矛盾)。
  #   SKILL §3.6.2 真路径调用恒传相对 `.claude/skills/codex-review`(满足)· 这里显式 fail-closed
  #   防未来 caller 误传绝对 base 引入静默 G3 误杀。
  case "$rr_dir_base" in
    /*)
      echo "ERR: write_review_log_immutable 的 rr_dir_base 必须 repo-relative(收到绝对路径: $rr_dir_base)" >&2
      echo "  原因:绝对 base → latest_review_log 绝对 → resolve_review_log_path 双拼接不可达 → G3 自我误杀" >&2
      echo "  修法:cd 进 repo root 后传相对路径(如 .claude/skills/codex-review · 仿 SKILL §3.6.2)" >&2
      return 1
      ;;
  esac

  RR_DIR="$rr_dir_base/real-review"
  mkdir -p "$RR_DIR"
  SCOPE_SLUG=$(printf '%s' "$target_file" | tr -c 'A-Za-z0-9._-' '-')
  TS_SLUG="${ts//:/}"                                   # 2026-05-29T073000Z(冒号去掉)
  RR_FILE="$RR_DIR/${SCOPE_SLUG}-${TS_SLUG}.md"

  # immutable body(7 协议字段 frontmatter · 与 singleton 同内容)
  REVIEW_BODY="---
schema_version: 0.1
review_type: ${review_type}
target_file: ${target_file}
verdict: ${verdict}
findings_count: ${findings_count}
codex_model: ${codex_model}
duration_seconds: ${duration}
ts: ${ts}
---

# Review · ${target_file} · ${ts}

(findings 详情 free-form body · 从 /tmp/codex-review.log 真路径 append 或手写)"

  # (1) immutable 记录 · noclobber 原子占位防覆盖(同秒/重跑碰撞 → 拒)· 绝不覆盖已存在记录
  if ! ( set -o noclobber; : > "$RR_FILE" ) 2>/dev/null; then
      echo "ERR: immutable review 记录已存在 · 拒覆盖(immutable 不可变契约): $RR_FILE" >&2
      echo "  真路径修法:同一 ts 已有记录 · 等下一秒重跑 review · 或 inspect 既有记录" >&2
      return 1
  fi
  # body 写入 · **必须查 exit status**(per codex F3 三轮加固):ENOSPC / 重定向失败 / 中断时,
  #   占位已建但 body 写空/截断 → 若不查,会更新 singleton 指向半文件 + return 0 假成功,
  #   且占位已存在挡同秒重试。修:写失败 → 删占位(放开重试)+ return 1(不发布半成品 evidence)。
  if ! printf '%s\n' "$REVIEW_BODY" > "$RR_FILE"; then
      rm -f "$RR_FILE" 2>/dev/null
      echo "ERR: immutable review body 写入失败(ENOSPC/中断?)· 已删占位放开重试: $RR_FILE" >&2
      return 1
  fi

  # (2) singleton latest-pointer · **temp 文件 + 原子 mv** 覆盖写到 canonical path
  #     (per codex adversarial-review F2 二轮加固:原裸 `cat > REVIEW-LOG.md` 无 lock/rename ·
  #      两个 different-ts writer 并发都成功时会 race singleton · last-writer-wins 且理论可 tear)。
  #     修法:先写 temp(同目录 · 同 fs)· 再 `mv` 原子 rename 入位(POSIX rename 同目录原子 ·
  #      读者要么见旧整本要么见新整本 · 绝不见半本)· 仍是 single latest pointer(行为等价)。
  #     temp 名用 RR_FILE basename(ts-slug 已保证每 writer 唯一)+ PID · 防并发 temp 互撞。
  #     consumer 默认读此 singleton(verify-ppv-p2.sh:43 default)· canonical path 不动。
  local SINGLETON_TMP="$rr_dir_base/.REVIEW-LOG.md.tmp.$(basename "$RR_FILE").$$"
  # heredoc 写 temp · **必须查 exit status**(per codex F2 四轮加固):若 ENOSPC/中断时
  #   heredoc 写半本就 mv 入位,会把截断 metadata 原子发布成 latest → 毒化 G3 真相源。
  if ! cat > "$SINGLETON_TMP" <<EOF
---
schema_version: 0.1
review_type: ${review_type}
target_file: ${target_file}
verdict: ${verdict}
findings_count: ${findings_count}
codex_model: ${codex_model}
duration_seconds: ${duration}
ts: ${ts}
latest_review_log: ${RR_FILE}
---

# Review · ${target_file} · ${ts}

> latest pointer · immutable 记录见 ${RR_FILE}

(findings 详情 free-form body · 从 /tmp/codex-review.log 真路径 append 或手写)
EOF
  then
      rm -f "$SINGLETON_TMP" 2>/dev/null
      echo "ERR: singleton temp 写入失败(ENOSPC/中断?)· 未 rename · 不毒化 latest: $SINGLETON_TMP" >&2
      return 1
  fi
  # rename 前**校验 temp frontmatter 完整**(恰 2 个 --- + latest_review_log 末字段在)·
  #   双保险:即便 heredoc exit 0 但内容异常(理论)· 也不把坏 metadata 发布成 latest。
  if [ "$(grep -c '^---$' "$SINGLETON_TMP")" != "2" ] || ! grep -q "^latest_review_log: ${RR_FILE}\$" "$SINGLETON_TMP"; then
      rm -f "$SINGLETON_TMP" 2>/dev/null
      echo "ERR: singleton temp frontmatter 不完整(写半本?)· 未 rename · 不毒化 latest: $SINGLETON_TMP" >&2
      return 1
  fi
  # 原子 rename 入位(失败则清 temp + return 1 · 不留半 temp)
  if ! mv -f "$SINGLETON_TMP" "$rr_dir_base/REVIEW-LOG.md"; then
      rm -f "$SINGLETON_TMP" 2>/dev/null
      echo "ERR: singleton REVIEW-LOG 原子 rename 失败: $rr_dir_base/REVIEW-LOG.md" >&2
      return 1
  fi

  # 回产出路径(让调用方/测试知道产了哪份 immutable 记录)
  printf '%s' "$RR_FILE"
  return 0
}
