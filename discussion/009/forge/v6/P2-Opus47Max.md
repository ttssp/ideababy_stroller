# Forge v6 · 009 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-07-17T10:20:00Z
**Searches run**: 3 次 SOTA-benchmark search + 1 次深读(LangExtract 锚定机制)
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| census proposer 输出契约 | **LangExtract**(Google · Gemini 生产级抽取库) | LLM 只产**引文子串**非偏移;锚定分层:exact `text.find` → difflib.SequenceMatcher 滑窗 fuzzy(阈 0.85)→ NOT_FOUND;多处出现**默认取首现**;`SpanMatch.status ∈ {EXACT, FUZZY, NOT_FOUND}` 携带锚定 provenance;全程确定性 | 让 LLM 直接产 span_start/end 整数(真跑 56/58 截断证伪) | 候选①有**生产级现成先例**,且比我们两个 P1 都多一层:锚定方法本身是分层+带 provenance 的 | developers.googleblog.com / shanechang.com(深读) |
| 回锚失配率预期 | LLM-IE 结构化输出文献(arXiv 2402.13364 等) | LLM 引文常见失配:多/缺空格、时态变化、缩写展开(小模型尤甚);业界用 difflib fuzzy 对齐补救 | 现契约无任何对齐层;若新契约走 exact-only,这些失配全变 UNANCHORABLE 拒 | **exact-only 的隐性代价被量化了**:失配是常态非例外,纯 exact 会把真信号错杀成拒绝 → 密度读数系统性低估(E1 是密度普查!) | arxiv.org/pdf/2402.13364 · medium(NER+LLM) |
| 引文可信边界 | GopherCite / RAG attribution 验证文献 | verbatim quote 是产出形态,但**验证=独立在原文里找到它**,不信 LLM 自报;长文场景 50-90% 引文经人核不完全成立 | 新契约的 `str.find` 回锚正是「独立找到」这个信任边界 | 我们方向对;文献同时警示 LLM 引文幻觉率高 → typed rejection + 计数不可省 | arxiv 2605.06635 / mbrenndoerfer.com |
| max_tokens 截断根因 | DeepSeek 官方文档 + reasoning-token 分析 | **reasoning_content 计入 max_tokens**(不计入 64K context);经验法则:max_tokens ≥ 4× 预期可见输出(思考预算通常 1-2× 可见输出);finish_reason=length + 零可见输出 = 预算全被推理烧掉 | max_tokens=4096,可见输出与**文本长度**耦合(数偏移任务),推理烧完预算即截断 | 根因机制获文档级证实;候选①把可见输出与文本长度**解耦**后,4×法则给出可算的安全上界 | api-docs.deepseek.com(create-chat-completion / reasoning_model / json_mode)· tokenmix.ai |

## 2. 用户外部材料消化

n/a —— K 中无外部链接/文件(X 标的即全部材料,P1 已消化)。

## 3. 修正后的视角

- P1 判断 (a)「候选①为骨架」→ **站住且加强**:LangExtract 是生产级同构先例(LLM 产引文、
  代码回锚),NER-LLM 文献也以 fuzzy 对齐为惯例。候选②(输出侧分块)在对标中**无先例**。
- P1 判断 (b)「首现锚定确定性可辩护」→ **站住**(LangExtract 默认即首现,确定性成立);
  **但我 P1 的「exact-only + 拒」需修正**:文献证实空白/标点/缩写失配是**常态**,exact-only
  会把大量真信号错杀成 UNANCHORABLE → **E1 密度被系统性低估,恰好违背本 forge 的目的**
  (拿到真密度读数)。修正立场:契约采**分层锚定 + 每层计数 + provenance 字段**(exact →
  确定性归一化(空白/全半角)→ fuzzy(difflib 阈值,确定性)),fuzzy 层命中标 weak-anchor
  类审计位;NOT_FOUND 才走 typed rejection。这与对方 P1「最多允许空白规范化这类可解释规则,
  且必须计数」**大方向兼容**——残余分歧收窄为:fuzzy 层(0.85 阈)是否进契约,还是先 exact+
  归一化两层、fuzzy 留作 v2 开关。留 P3(若需要)或 synthesizer 收敛。
- P1 §3-2「推理预算语义不确定」→ **已解**(文档级):reasoning tokens 计入 max_tokens。
  契约条款可写死:max_tokens ≥ 4× 预期可见输出(候选①下可见输出 ≈ N_max 条 × 引文上限,
  与 record 长度无关,可量化——满足 K-② 的「不许应该够了」);finish_reason allowlist 守门
  保留;模型无关性成立(条款不绑 DeepSeek,任何推理型模型同一算法)。
- P1 判断 (c)(d) → **站住无修正**(SOTA 无反例;LangExtract 的 status/provenance 分层反而
  支持 (d) 中「锚定方法入 provenance」的加强——落库形态(0018 加列 vs detail 字段)属
  refactor-plan 细节,留 synthesizer)。
