# Forge v5 · 001 · P2 · GPT55xHigh · SOTA 对标

**Timestamp**: 2026-08-02T13:47:28Z  
**Visibility**: 已读 Opus P1；`moderator-notes.md` 不存在。  
**Searches run**: 20 条，SOTA benchmark；不含技术栈、价格或实现细节。

## 1. SOTA 对标(或指定对标)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 可判/可验 gate | W3C + NASA | requirement 要抽成 assertion/test case，且 feasible/verifiable；证明：冻结前先证对象、窗口、失败线。 | O2(c)/C9 未定而 T040 想落测。 | T040 只测已冻结牙。 | https://www.w3.org/TR/test-methodology/ https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/ |
| oracle 谦抑 | Equivalent mutants | 等价 mutant 不可被任何测试杀死；证明：检测牙不是 truth oracle。 | O4 对，但 O2(c) 易被读成强判真。 | 证不出归 B。 | https://onlinelibrary.wiley.com/doi/full/10.1002/stvr.1473 |
| 样本设计 | SPIRIT 2013 | 预列 outcome/sample/analysis；证明：样本充分性属验收设计。 | “≥3”像产出 KPI。 | 放 acceptance/analysis 侧。 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3541470/ |
| 例外授权 | NIST RMF authorize | 风险接受由 authorizing official 负责；证明：例外需独立责任主体。 | C9 门②有声明口，门①无同构机制。 | 可补但非自豁免。 | https://csrc.nist.gov/Projects/risk-management/about-rmf/authorize-step |
| 窗口指标 | SRE/SLA + Goodhart | SLO/SLA 定义窗口和 claim；Goodhart 警告 proxy 过拟合。证明：O7 有效但不能凑判断数。 | O7 1/5 且低置信。 | 补窗口、样本、复核。 | https://sre.google/workbook/error-budget-policy/ https://aws.amazon.com/s3/sla/ https://openai.com/index/scaling-laws-for-reward-model-overoptimization/ |

## 2. 用户外部材料消化

n/a(K 无外部材料)。

## 3. 修正后的视角

1. 我 P1 的架构 refactor 站住，product keep 站住但收窄：§1 W3C/NASA/NIST/SRE 支持先证可判、可授权并保留 O7；§1 Goodhart/SPIRIT 推翻“让 judge 产出 ≥3 条即可”。P2 后应 narrow PASS/hold。
2. Opus P1 的 C9 非对称判断站住；补法要改：门①声明必须由风险 owner/审核方承担条件与期限，不能变成 writer 自我例外，见 §1 NIST。
3. Opus P1 的 T040 窄起跑站住，但仅限已冻结合规面，见 §1 W3C/NASA；同时“1 条低置信可能是 fallback”的不确定被本轮事实 `evidence=(e9)` 推翻，问题应改为正常路径判断密度低，按 §1 Goodhart/SPIRIT 补样本与证据设计。
## 4. 选源自查
- 关键词有偏：我主动搜了 `testable conformance`、`risk acceptance`、`Goodhart`，预设了“验收先于实现、代理指标危险”。缓解方式是同时查 NASA/SPIRIT/SLA 等独立领域。
- 没有找到强直接证据支持“半个 gate 可以 ship”这一命名模式；W3C/NASA 只支持 scoped verification，所以 T040 partial start 是推论，不是 SOTA 明文。
- 没有找到支持“作者本地 allowlist 就是合法例外”的材料；NIST 只支持有责任主体、期限、条件的风险接受。
- 结论总体支持 K 的方向，但仍可能有 confirmation bias：搜索围绕“可判/授权/指标”展开，较少覆盖“强制多样本输出是否在某些评审系统中有效”。这不改变当前 verdict，因为 OpenAI Goodhart 与 SPIRIT 已足够反证单纯凑数。
