---
phase: P2
side: Opus47Max
forge_id: 006
forge_version: v3
generated: 2026-05-27T12:55:00Z
z_mode: 不对标 · 纯内部审阅
searches_used: 0
word_count_approx: 890
---

# P2 · Opus side · 参照系评估(no search · Z mode 不对标)

## §1 · SOTA 对标

**N/A**(Z mode = 不对标 · 纯内部审阅)。本 phase 跳 web search · 跳 SOTA 检索 · 不开外部 prior-art / failure-case / 演化路径分支。

per forge-protocol §"P2 template" 分支语义:Z mode `不对标` 时 §1 只需声明 mode + 说明跳过理由,不需写 SOTA 表格。

- **mode**:不对标 · 纯内部审阅
- **跳过理由**:K8 v3 mission 锁定"v0.1 落地后的修订 batch"。所有标的来自本仓内或 XenoDev SSOT,**没有"找外部对标"的开放问题**;协议 4 项修订(B-1 EXDEV / B-2 enum / B-3 flock / B-4 verdict-evidence)的"为什么"已在 HANDBACK-LOG batch 2 ENTRY 11/14/15/17 + producer 真实 ship 数据中说清,SOTA 检索无附加价值。
- **效率取舍**:节省 Phase 2 约 ~6 次 web search(v2 跑了 12 次 SOTA,本次 0 次)。

## §2 · 用户外部材料消化

**N/A**(K 中无外部链接 / 文件引用;`moderator-notes.md` 不存在;`_x-input-draft-by-operator.md` 也不存在 — 都是 v3 fresh intake 后未注入态)。

唯一可消化的"用户给的额外材料"= K8/K9/K10/K11 4 段 binding text · 已在 P1 §0 引用 · P2 不重复。

## §3 · 修正后的视角(P1 哪些站住、哪些被推翻)

### §3.1 · 读完对方 P1 后的 cross-check

读了 Codex P1(`P1-GPT55xHigh.md` · CONCERNS · ~900 字),与自己 P1 对齐情况:

**高度对齐(no contention · v3 strong-converge 基本盘)**:
- 11 项 backlog 分类 + 主要倾向(双方都给 N×4-9 mirror / R×3-4 修订)
- K8/K10 锚:Codex §0 直接引 K8/K10 · 边界纪律一致
- 3 件 R2 不确定事项 **主题完全相同**:
  - (1) mirror rebuild 边界规则(Opus = "是否分波 + bootstrap.sh 升级风险";Codex = "字节级 cp vs 包装层 + manifest+provenance+SHA")
  - (2) event enum 单复数方向
  - (3) case F regression 根因 + 修法
- Y 视角覆盖完全一致(架构 + 工程纪律 + Y5)

**微差异(non-blocking · v3 P3R1 可整合)**:
- **mirror rebuild priority 分布略不同**:
  - Opus:templates/gen/score = **P0**,skills/hooks/tests = **P1**(理由:gen 不能跑 = 硬阻;skills 是 SKILL 文档不阻 bootstrap)
  - Codex:skills/tests/templates+gen+score = **P0**,hooks = **P1**(理由:tests 镜像 = T012 gate 可复验;skills 是真路径合同源)
  - 实质冲突小 — 双方都同意"全部 P0/P1 都要做",只在"哪个最先 cp"上一念之差
- **B-3(IDS dir flock)priority**:Opus = P2(当前 fail-closed cleanup 足够),Codex = P1(跨 session 写 LOG 需排他)。Codex 略激进。
- **R2 mirror 收敛方向措辞不同但内核同**:Opus 倾"分波"(时间维度),Codex 倾"manifest + provenance + SHA"(机制维度)— **两者可合并**:"分波 ship + 每波 manifest + SHA dual-verify"(K10 边界纪律延伸)。

**0 推翻**:Opus P1 没有需要 retract 的判断。Codex P1 没有提出 Opus P1 未触及的反驳维度。

### §3.2 · 我现在站住的判断

1. **Cluster A · mirror rebuild · 分波 ship**(同意分波 + 同意 manifest/SHA)
   - **wave 1**(P0 硬阻):templates/handback.template.md + gen-handback.sh + score-handback.sh(3 文件 · gen 真路径必依赖 template;score-handback 接 writer JSON 接口)
   - **wave 2**(P0 ship gate 可复验):tests/integration/ 全 8 sh + bootstrap.sh 升级新路径(测 T012 SHIP GATE 可在 IDS bootstrap 出生的新 idea 跑)
   - **wave 3**(P1 SSOT 教学):skills/ 4 SKILL(parallel-builder + spec-writer + codex-review + task-decomposer)+ hooks/wrappers/(1 wrapper)
   - 每 wave:跨仓 cp + SHA dual-verify + IDS mirror commit + bootstrap-kit/README 同步描述
   - **K10 延伸**:wave 边界 = "1 wave 1 commit · 不混波"

2. **Cluster B · 协议级 4 项 · 不全做 · 按硬阻先后**
   - **B-2 enum 单复数** = P0 硬阻(corruption 风险 · 5 文件 grep 一致 · 5 分钟修)— v3 ship 范围
   - **B-1 EXDEV cross-device publish 段** = P1(producer 已实装,协议补段文档 lag)— v3 ship 范围
   - **B-3 IDS dir flock** = P2(当前 fail-closed cleanup 已足够;真路径 race 未实测)— v3 不做 · v0.3 note
   - **B-4 `--ids-verdict-evidence` flag** = P1(F10 cross-repo trust real gap)— v3 ship 范围 · 但**改 SHARED-CONTRACT §6 是 RECOMMENDED,实装真路径(`--ids-verdict-evidence` flag · REVIEW-LOG.md machine-readable schema)在 XenoDev 端单独 task ship**

3. **Cluster C · lib bug 3 项 · 全 v3 ship · 优先 C-3 + C-1**
   - **C-3 case F stale regression** = P0 必修(main 14/15 fail 真 regression · 6 个月不修等于 spec evolves to silently broken)
   - **C-1 scan-credentials exit code** = P0 必修(Safety Floor 件 1 真聚合能力)
   - **C-2 gen-handback `--out` 默认前缀** = P1 (UX bug · 不阻塞 ship)

### §3.3 · 对 K 的对齐性自检(为 R1 提前打底)

- ✅ K8 (v3 mission · 11 项 backlog 三类):本 P2 §3.2 11 项一一对应,**无遗漏**
- ✅ K9 (v2 verdict 不重审):本 P2 §3.2 完全不触及大架构 · 只动落地后细节
- ✅ K10 (边界先定、批量 SSOT、不越界):**wave 1/2/3 分波是 K10 直接落地**(每 wave 锁子树边界 · 批量 cp + SHA · 不越界);**B-3 不做** = K10 真路径(不向 v0.3 范畴扩张)
- ⚠ K11 (strong-converge · 一一对一收敛):本 P2 已对 11 项一一表态;**残余 1 项可能落 v0.2-note** = B-3(flock)— 这是符合 K11 "残余分歧 v0.2-note 旁注"的合规旁注,而非压扁分歧
- ✅ k_provenance verbatim:K 文本未 edit

---

**Soft hand-off to Codex P2**:本 P2 已 cross-check 对方 P1 · 0 推翻 · 微差异已锁定收敛方向。Phase 3R1 可直接进联合收敛:11 项 backlog wave 1/2/3 分波 + B-3 v0.2-note 旁注 + B-4 协议改 + 真路径实装拆分。
