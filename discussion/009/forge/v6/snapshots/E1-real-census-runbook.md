# E1 真密度普查 · operator runbook(command skeleton + preflight 清单)

> **状态**:接线已就绪 + **真 DeepSeek 端到端验过**(HANDBACK-LOG #22 决议 3 · `build_llm_proposer` 接
> DeepSeek OpenAI-兼容端点 · 2026-07-17)。凭据由 operator 提供(`DEEPSEEK_API_KEY`)· **不进 agent 上下文**
> (C13 · 沿用 smoke path 凭据纪律)。
> **性质**:runbook · 真跑 = operator 拍板后的动作(会烧 key)。**本文档的命令已用小样本真跑验过(exit 0)**。

## ⚠ 真跑前必知(真 smoke 实测暴露 · 2026-07-17)

1. **SOCKS 代理坑**:环境若设 `ALL_PROXY=socks5://...`,httpx 需 `socksio` 包否则报
   `ImportError: Using SOCKS proxy, but the 'socksio' package is not installed`。**解**:跑命令前
   `env -u ALL_PROXY -u all_proxy ...`(用 `HTTPS_PROXY` 的 http 代理 · 无需 socksio)· 或 `uv pip install httpx[socks]`。
2. **max_tokens 截断**:长 qa/replay 转写(qa 可上万字)· DeepSeek 输出可能被 `max_tokens=4096` 截断
   (`finish_reason=length`)→ census **计 `llm_parse_failures` + 醒目 WARN**(不静默当"0 信号")。见 §4。
3. **失败计数 = 密度可信度闸**:census 输出的 `llm_api_failures` / `llm_parse_failures` **任一 > 0 → 该次
   0-accepted 不可信**(是"LLM 挂了"非"真稀疏")· 必须查根因重跑,别据此下密度结论。
4. **弱锚审计**:`weak_anchor_accepted`(accepted 里 ticker 不在 span 切片字面出现的条数)· 隐性信号合法弱锚,
   但**高率疑幻觉 offset** → operator 抽查引文质量(不自动毙 · 决:记审计不拒)。

---

## 0 · 为什么要跑(先读)

E1 密度普查目前**只跑过 `literal_ticker_proposer` 替身**(英文 ASR 转写里中文情绪词/隐性荐股无法字面命中)
→ 产出 `accepted 0 / verdict=below_threshold_advisory`,这是**下界/占位,非真密度**。真密度需**真 LLM 提取器**
读中文原文语义抽 —— 这是 M3' ROI 闸门的最后一公里(forge v5 §underweights「没人读语料正文」)。

阈值 30 是 **advisory 参考**(决议 2)· 真密度出来后由 operator 看**完整报告**人工终裁 E2 go/no-go(非自动毙刀)。

---

## 1 · Preflight 检查清单(跑前逐项确认)

- [ ] **①凭据就位**:`DEEPSEEK_API_KEY` env 直接存 key 值(`--api-key-env DEEPSEEK_API_KEY` 直读值 · 非文件路径)。
      验证只查 presence/长度,**永不 grep/cat/echo 出 key 内容**(C13 · 有一次泄露前科)。
      ```bash
      # 只验存在 + 长度(不打印内容)
      test -n "$DEEPSEEK_API_KEY" && echo "DEEPSEEK_API_KEY 就位(len=${#DEEPSEEK_API_KEY})" || echo "未设"
      ```
- [ ] **②预注册已签**:`density_threshold` 全 9 行 `threshold_hash=97c58440426f8770`(非 NULL)。
      ```bash
      sqlite3 "$DECISION_LEDGER_DB" "SELECT DISTINCT threshold_hash FROM density_threshold WHERE caliber_version='v1';"
      # 期望单行:97c58440426f8770(若见 NULL 或空 → 先跑 preregister · 见 §2 step 0)
      ```
- [ ] **③collection.db 只读可达**:`/home/ys/codes/XenoDev/out/collection.db` 存在(9081 record · article 1179/
      qa 7545/replay 357)· census 用 `mode=ro` 只读(C10 · 零写采集侧)。
- [ ] **④抽样方案已预注册**:census 分层抽样 = per-form(article/qa/replay)× `--sample-size`。抽中 source_id
      集落 `trial_ledger.sampled_source_ids`(可复现 · D-12 不可改)。OOS 窗 [2025-12-01, 2026-02-01) 内 record
      **不参与**密度(C12 · 保留作 OOS · 防抄考卷)。
- [ ] **⑤成本预估**(见 §3)· 确认预算 · 温度 0 + `allow_fallback=False`(禁静默降 Haiku · 确定性 C4)。
- [ ] **⑥金标 gate 现状**:两层金标未真跑(需真人第二源 D-7)· gate fail-closed 默认关。密度普查**不**依赖
      金标(密度是 advisory 参考 · 金标是信号质量硬门 · 两者正交 · 见 gate.py docstring)。

---

## 2 · Command skeleton(逐步)

```bash
# ── 环境(operator 按新机路径调 · 凭据 DEEPSEEK_API_KEY 已在 bashrc · 不给值)──
export DECISION_LEDGER_DB=<你的 data.sqlite 路径>        # 009 三表所在库(004 decision_ledger)
COLLECTION_DB=/home/ys/codes/XenoDev/out/collection.db  # 只读采集库(显式传 · 不隐式读 config · dogfood G-R3)

cd /home/ys/codes/XenoDev-009/projects/004-pB

# ── step 0(若未预注册):建表 + 签字预注册(无 LLM · P1)──
DECISION_LEDGER_DB_URL="sqlite:///$DECISION_LEDGER_DB" uv run alembic upgrade head
uv run python -m decision_ledger.extraction.preregister --caliber-version v1 --db "$DECISION_LEDGER_DB"
# 期望 OK 行含 threshold_hash=97c58440426f8770(signed · advisory)

# ── step 1:真密度普查(真 DeepSeek · 温度 0 · 读中文原文语义抽)──
#   ⚠ env -u ALL_PROXY:绕 socks5 代理坑(见"真跑前必知"#1)· --api-key-env 直读 DEEPSEEK_API_KEY 值(C13)。
env -u ALL_PROXY -u all_proxy uv run python -m decision_ledger.extraction.census \
  --collection-db "$COLLECTION_DB" \
  --caliber-version v1 \
  --extractor-variant v1 \
  --db "$DECISION_LEDGER_DB" \
  --proposer llm \
  --api-key-env DEEPSEEK_API_KEY \
  --model deepseek-v4-flash \
  --sample-size 40
# 每 form 抽 40(可调)· OOS 窗自动排除 · 写 extracted_signals/extraction_rejections/trial_ledger
# ⚠ 看输出末行的 llm_api_failures/llm_parse_failures/weak_anchor_accepted(见 §4 解读)· 每 record 增量 commit(中断不丢已跑)

# ── step 2:读完整密度报告(operator 人工终裁的输入)──
sqlite3 "$DECISION_LEDGER_DB" <<'SQL'
-- per-market 密度(accepted 数 · 决议 1 horizon-independent)
SELECT extractor_variant, caliber_version,
       (SELECT count(*) FROM extracted_signals es WHERE es.caliber_version='v1') AS accepted_total;
-- 拒绝构成(哪些 rejection_reason 占多 · 诊断替身弱 vs 真稀疏)
SELECT rejection_reason, count(*) FROM extraction_rejections
  WHERE caliber_version='v1' GROUP BY rejection_reason ORDER BY 2 DESC;
-- 抽样规模(可复现 · trial_ledger)
SELECT DISTINCT market, horizon FROM trial_ledger WHERE row_kind='e1_trial';
SQL
```

---

## 3 · 成本 / 调用量预估

- **调用量**:census 每**参与 record**(抽中 且 非 OOS 窗 且 有正文)调 **1 次** LLM。
  - `--sample-size N` × 3 form = 上限 `3N` 次(实际略少:OOS 窗排除 + 空正文跳过 + form pool 不足 N 则取全池)。
  - 例:`--sample-size 40` → 上限 120 次;`--sample-size 200` → 上限 600 次。
  - ⚠ qa pool 7545 / article 1179 / replay 357 —— `--sample-size` > 357 时 replay 取全池(357)。
- **单次**:温度 0 · max_tokens 4096(输出上限)· 输入 = 一条 record **全文**(qa/article 短 · replay 转写可上万字)。
  DeepSeek-flash 便宜 → **每次约 $0.001–0.01**(随正文长度 · 真账单为准)。
- **总估**:`--sample-size 40` ≈ **$0.1–1**;`--sample-size 200` ≈ **$0.5–5**(DeepSeek-flash 比 Sonnet 便宜一个量级)。
- **无缓存**:DeepSeek 走 openai SDK **无内置缓存**(天然无 cache 串号面)· 重跑每次真调(不省 key)· 谨慎重跑。
- **⚠ chunking(真跑实测)**:census 传 record **全文**给 LLM · 长 qa/replay 转写(上万字)会撑爆 `max_tokens`
  输出截断(`finish_reason=length` → 计 parse_failure)。当前**不自动 chunk**(切分会破 span 偏移的原文回锚)。
  高截断率 → operator 选:①先跑短文 form(article)②或后续加 map-reduce 分段(E2 设计输入候选 · 非本轮)。

---

## 4 · 结果解读(诚实纪律)

**先看可信度闸(任一不过 → 密度结论无效 · 重跑)**:
- `llm_api_failures > 0` 或 `llm_parse_failures > 0` → **0-accepted 不可信**(是 LLM 挂/截断非真稀疏)· 查根因
  (代理 / max_tokens 截断 / 限流)后重跑,**别据此下密度结论**。
- `weak_anchor_accepted / accepted` 高 → 引文质量存疑(疑幻觉 offset)· 抽查 `extracted_signals`
  的 span 切片是否真对应信号。

**双口径密度(H1 复审 · operator 决 · 看区间人工终裁)**:census 输出两个密度,**都真,不预设哪个对**:
- **strong(下界 · 仅强锚 · 抗幻觉)**:ticker 字面在 span 切片里的信号数 · 对"幻觉 offset 落真实无关文本"鲁棒 ·
  但会**漏真隐性信号**(分析师不显说 ticker)→ 保守低估。
- **all(上界 · 强+弱 · 含隐性含幻觉)**:全部 accepted · 含真隐性信号,但也含幻觉水分。
- **读法**:真密度落在 [strong, all] 区间。区间窄 = 引文质量高可信;区间宽(strong≪all)= 大量弱锚,
  须抽查是"真隐性信号"还是"幻觉" → 决定信上界还是下界。
- **原子性 + 重跑纪律**:census 是**单原子事务**(全 run 一次 commit)—— 中途失败**全回滚**(无部分写 · 崩后重跑干净)。
  但**重跑到已有数据的库会追加**(不去重 · 无 UNIQUE)→ 重跑请用**空库 / 新 --db 路径**(或先手动清本 caliber/variant 行)。

**verdict 三态(字段本身携可信度)**:
- `meets_threshold`:每 market **强锚下界** ≥ 阈值 = 有真实强锚证据(最可信)。
- `meets_threshold_unverified`:仅**上界**达标 · 达标全靠弱锚(隐性 or 幻觉)→ **须抽查 extracted_signals 引文** 判真假 · 别当 meets 放行 E2。
- `below_threshold_advisory`:连上界都有 market < 阈值 = 确凿低(advisory · 非自动毙刀)。

**可信度闸 + 双口径都看后,读密度**:

| 真 LLM 密度结果 | 语义 | 下一步 |
|---|---|---|
| **仍显著低于 30** | 诚实 STOP 成立(真稀疏 · 非替身弱)| 回 IDS forge 重估闭环前提(M3' ROI 锚点不成立)· 产 hand-back |
| **接近/超 30** | 密度足以支撑未来 E2 | operator 拍板 E2 go(解锁三条件之一满足)· 产 hand-back 请授权 E2 |
| **拒绝构成异常**(如全 no_direction)| 提取器/prompt 需调 | 迭代 `_build_extraction_prompt` · 非密度结论 |

- 无论结果如何,**产新 hand-back** 写回 IDS `discussion/009/handback/` → `/handback-review 009` 裁 E2/E3。
- **阈值 30 不可回改**(C6):不能因"差一点"就改阈值粉饰(密度不足是诚实结论 · 改阈值 = BLOCK)。

---

## Provenance

- 接线授权(决议 3)+ advisory 语义(决议 2)+ per-market 口径(决议 1):HANDBACK-LOG #22(2026-07-17)。
- DeepSeek 接入(openai SDK 指 base_url · `--api-key-env` 直读值):operator 指定 deepseek-v4-flash + DEEPSEEK_API_KEY(2026-07-17)。
- 凭据纪律:`~/.claude/CLAUDE.md` C13 + smoke path 前例(009-pForge 决议 1)。
- 鲁棒性/可观测(失败计数 + 弱锚审计 + 增量 commit + 截断检测 + 空白 span 拒 + 异常脱敏):red-team + code-reviewer
  双跑对 DeepSeek delta 的 3 ship-blocker + 补丁(2026-07-17 · 真 smoke 实测暴露 max_tokens 截断 → 提到 4096)。
