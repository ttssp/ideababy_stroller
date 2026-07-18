# Forge v6 · 009 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-17T16:46:02Z
**Searches run**: 10, SOTA-benchmark
**Visibility**: 我已读对方 P1；`moderator-notes.md` 不存在。

## 1. SOTA 对标(或指定对标)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| E1 citation 回锚 | Google LangExtract README | LLM 输出 extraction text；示例要求逐字、不改写；无法在源文定位时 `char_interval=None`，由调用方过滤或审阅。 | 候选①同样把 offset 从 LLM 手里收回，改为 quote-then-anchor。 | 大方向站住；但必须显式记录 ungrounded，而不是把「找不到」混进普通 below/advisory。 | https://github.com/google/langextract |
| 多处匹配 / provenance | LangExtract resolver | exact 阶段已不是简单首现：默认 DP 会按输出顺序选择不重叠 occurrence，让重复提及映射到 successive occurrences；之后才进入 lesser/fuzzy。 | 双方 P1 卡在「首现」vs「typed rejection」。 | 对方「确定性」站住，我的「不静默首现」也站住；但 SOTA 更接近 order-preserving occurrence DP + match provenance。 | https://raw.githubusercontent.com/google/langextract/main/langextract/resolver.py |
| 非逐字失配 | LangExtract fuzzy alignment | exact 失败后可开 LCS/difflib fuzzy，默认阈值 0.75，并给 `MATCH_FUZZY`；完全失败才无 interval。 | 我 P1 倾向 exact-only typed rejection；对方倾向复用 `UNANCHORABLE_CITATION`。 | exact-only 被推翻为过严；但 fuzzy 不能静默当 exact，需写 `match_mode`/score/detail。复用枚举可保 caliber v1，但 detail 必须分 exact/normalized/fuzzy/not_found。 | https://raw.githubusercontent.com/google/langextract/main/langextract/resolver.py |
| 推理模型输出预算 | DeepSeek Thinking/API docs | thinking 默认 enabled；`reasoning_content` 与 final `content` 同为生成物；usage 将 `reasoning_tokens` 放在 completion breakdown 下；`max_tokens` 约束 generated tokens，当前模型最大输出 384K。 | 候选①以「答案短」论证 4096 安全，但 56/58 失败可能是推理预算烧掉。 | 我 P1 的疑虑站住：预算要按 reasoning+JSON 合计保守估算；若用 reasoner，4096 仍可截断。候选①需禁 thinking 或设大输出上限并监控 reasoning_tokens。 | https://api-docs.deepseek.com/guides/thinking_mode/ ; https://api-docs.deepseek.com/api/create-chat-completion/ ; https://api-docs.deepseek.com/quick_start/pricing/ |
| ASR 中文 exact 回锚 | AWS/HF ASR evaluation + 中文模型卡 | ASR 评测通常先归一化大小写、标点、数字等；中文因无天然词界，常用 CER；Breeze/TEA 等中文 ASR benchmark 会处理标点、句断、繁简、大小写。 | exact `str.find` 对原始 ASR 文本做唯一门槛。 | exact-only 会系统性低估 E1 密度：真实信号会因标点、空格、全半角、繁简、数字写法或轻微正字差异变成 unanchored。 | https://aws.amazon.com/blogs/machine-learning/evaluating-an-automatic-speech-recognition-service/ ; https://huggingface.co/learn/audio-course/chapter5/evaluation ; https://huggingface.co/MediaTek-Research/Breeze-ASR-26 ; https://huggingface.co/JacobLinCool/TEA-ASR-1.1-mini |

## 2. 用户外部材料消化

n/a。K 中无外部链接、文本片段或文件路径；本轮只执行 SOTA-benchmark search。

## 3. 修正后的视角

- P1 判断「LLM 不应产字符 offset，候选① quote-then-anchor 是骨架」→ **站住**。LangExtract 的主路径也是让 LLM 给文本证据，再由 resolver 映射到 source interval；这比让 LLM 直接报偏移更贴合能力边界。
- P1 判断「多处匹配与非逐字引用走 typed rejection，不静默首现」→ **部分被推翻**。多处匹配不该直接 reject，也不该固定首现；SOTA 给的是 order-preserving occurrence DP。非逐字也不必一刀切 reject，可走 normalized/fuzzy，但必须保留 provenance，不能把 fuzzy 当 exact。
- 对方 P1 判断「首现锚定确定性可辩护」→ **只保留确定性，不保留首现唯一规则**。首现可作为最小 fallback，但 P3 应收敛到「确定性 occurrence 选择 + ambiguity/detail」，否则同一句复现时 span 身份不可解释。
- 对方 P1 判断「复用 `UNANCHORABLE_CITATION` 避免 caliber v2 连锁」→ **站住但要收紧**。枚举复用合理，避免阈值重预注册；但 detail/status 必须区分 exact、normalized、fuzzy、not_found、ambiguous，否则 E1 报告仍无法解释密度偏差。
- P1 判断「输出预算上界仍可能截断」→ **站住且更强**。DeepSeek 当前 docs 让 thinking 成为默认，reasoning tokens 属于 generated completion 的一部分；候选①的量化预算不能只算 JSON quote 长度。若 max_tokens=4096，reasoning 烧到 3k 后，剩余 JSON 空间仍可能不足；建议用 non-thinking 或 32K+ 上限，并把 finish_reason/usage 变硬门。
- P1 判断「exact-only 在中文 ASR 上会制造偏差」→ **站住**。ASR 参照系普遍承认正字法归一化对指标影响很大；E1 若只 exact raw find，偏差方向是低估真实可用信号密度，同时高估 `UNANCHORABLE_CITATION`。P3 不应改变金标 exact-match 口径，但 extractor 侧应输出 match tier，让 calibration 能分层读数。
