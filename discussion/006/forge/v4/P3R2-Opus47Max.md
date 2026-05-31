# Forge v4 · 006 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-05-31T10:05:00+08:00
**Visibility**: 我已读对方 P3R1(`P3R1-GPT55xHigh.md`)。
**Convergence mode**: strong-converge(从 forge-config frontmatter 读)
**Finalize form**: 单侧 finalize(operator 选项 3 · 因 P3R1 已 0 unresolved · Codex P3R2 确认性低故省一轮 · 本文件代表双侧已锁结论的 finalize)

## 1. 我对每条分歧的最终立场 + 让步

P1 层 6 项 backlog 双方 P1 已无分歧。P3R1 抛出的 3 个实现层分歧,Codex 逐条接受我的方向且在分歧 1 收紧。最终立场:

- **分歧 1**(R-Q6 脚本拆分 + 逻辑复用):
  - Codex 在 P3R1 给的论证:"必须从 verify-ppv-p2.sh 抽成共享 lib,再由两者调用 · 不能复制 awk 状态机"(`P3R1-GPT55xHigh.md:26`)→ **完全接受 · 这是对我立场的正确收紧**
  - 我的最终立场:抽独立 `validate-verdict-evidence.sh` wrapper + 把 7 字段解析/rehash/freshness 逻辑下沉到 **共享 shell lib**(`lib/handback-validator/verdict-evidence-lib.sh`),`verify-ppv-p2.sh`(producer 端)和新 `validate-verdict-evidence.sh`(consumer 端)都 source 同一 lib。SSOT=XenoDev `lib/handback-validator/`,IDS bootstrap-kit mirror 同一文件(SHA dual-verify)。
  - 让步给对方的部分:我 P3R1 说"100% 复用函数",Codex 指出"复用函数"仍可能各自 copy 一份——改为"共享同一 lib 文件、两者 source",这是更硬的 SSOT。接受。

- **分歧 2**(contract bump 绑定关系):
  - Codex 论证:"contract bump 不应作为纯 frontmatter hotfix 单独 ship · 否则版本已 bump 示例仍鼓励 singleton"(`P3R1-GPT55xHigh.md:31`)→ **完全接受**
  - 我的最终立场:**P0 原子 wave** = R-Q6 共享 lib + validator + R-Q7 immutable path(XenoDev writer)+ SHARED-CONTRACT B-4-IDS 示例 `review_log_path` 更新 + `contract_version: 2.2→2.3` + `status` + `last_updated` bump。四件事同一 commit/wave 落地,避免治理反债。
  - 让步给对方的部分:无 · 这是双方同向 · Codex 把"绑定"说成"原子波"更精确,采纳措辞。

- **分歧 3**(D-precedent 治理段编号):
  - Codex 论证:"接受 §8 · D-precedent 不进 §6(非 hand-back schema)· 不叫 §7(避与 HANDOFF §7 混淆)"(`P3R1-GPT55xHigh.md:36`)→ **完全接受**
  - 我的最终立场:SHARED-CONTRACT 新增 **§8 · D-precedent governance**(准入条件 / owner / 期限 / 验证门 · 不回审 v0.2 七次历史);cross_repo_split 升 **§6 normative**。两个编号锁定,0 撞号。
  - 让步给对方的部分:无 · §8 是我 P3R1 提的,Codex 接受。

## 2. 联合 verdict(单一)

**CONCERNS · v4 verdict:不动 v3 11 项大架构,以 2 wave 清理 6 项 post-v0.2-shipped 协议债。** v0.2 已真路径 ship(O1-O6 全 PASS · 双仓 push 完成),所以不是 BLOCK;但 consumer-side 7 字段缺验(R-Q6)、REVIEW-LOG singleton 可变路径(R-Q7)、contract_version 漂移三处是协议层可见债,所以不是 CLEAN。6 项 backlog 分两波:**P0 原子波**(R-Q6 共享 lib validator + R-Q7 immutable path + B-4-IDS 示例更新 + contract bump 2.3 · 四件事必须同 wave 原子落地)+ **P1 波**(D-precedent codify 升 SHARED-CONTRACT §8 · cross_repo_split §7 升 §6 normative)。B-3 IDS dir flock 继续 v0.3-note(12 包 round-trip 0 撞库 · 触发条件未实证 · 不进主线)。D-precedent codify 只立准入流程,不回审 v0.2 七次历史决议(K9 binding)。

**0 unresolved** · 双方 P1/P3R1 全程同向 · 3 个实现层细节 R1 已双向锁定。

## 3. 残余分歧降级为 v0.3-note

- **v0.3-note 1 · B-3 IDS dir flock**:沿用 v3 v0.2-note 决议 · 触发条件(并发 hand-back round-trip 撞库)v0.2 12 包未触发 · 等真路径并发(多 worktree ship)实证后再判升级 · 触发条件不变。
- **v0.3-note 2 · R-Q7 多 worktree 真路径压测**:R-Q7 immutable path 本 wave 落地是"协议先行" · 但其真实价值场景(async hand-back + 并发 review 覆盖)要等多 worktree 模式才大规模触发 · v0.3 回头看 immutable path 是否够。
- **v0.3-note 3 · 共享 lib 跨仓 drift 监控**:R-Q6 共享 lib SSOT 在 XenoDev · IDS mirror · 当前靠 SHA dual-verify · 若未来 lib 频繁改,需考虑是否上自动 mirror-sync hook(现在不上 · 手动 cp + SHA 够 · 12 包实证)。

## 4. W 形态产出的初步草稿建议(给 synthesizer)

W=4 形态(verdict-only / decision-list / refactor-plan / next-dev-plan)的草稿:

### W 含 verdict-only → verdict 关键句
"v4:不动 v3 大架构,2 wave 清理 6 项 post-v0.2 协议债;P0 原子波(R-Q6 共享 lib + R-Q7 immutable path + B-4 示例 + contract 2.3)+ P1 波(D-precedent §8 + cross_repo_split §6);B-3 续 v0.3-note。0 unresolved。"

### W 含 decision-list → 6 项 backlog 4 列矩阵
- **保留**(keep): B-3 IDS dir flock(续 v0.3-note · 触发条件不变)
- **调整**(refactor): R-Q7(REVIEW-LOG singleton → immutable per-review path)· contract_version(2.2 → 2.3 + status + last_updated)· cross_repo_split(HANDOFF §7 per-instance 扩展 → SHARED-CONTRACT §6 normative)
- **删除**(cut): 无
- **新增**(new): R-Q6(consumer-side 7 字段 verify · 共享 lib + validator)· D-precedent(SHARED-CONTRACT §8 governance · 准入流程)

### W 含 refactor-plan → 关键模块(3 组)
1. **handback-validator 模块**(XenoDev `lib/handback-validator/` · SSOT)
   - 当前问题:consumer mode 只跑 6 约束 · 7 字段 verdict-evidence 无验证 · `verify-ppv-p2.sh` 的 7 字段逻辑是 producer 端独有
   - 目标态:抽 `verdict-evidence-lib.sh` 共享 lib · producer(`verify-ppv-p2.sh`)+ consumer(新 `validate-verdict-evidence.sh`)都 source · IDS mirror 同一文件
   - 改造步骤:① 从 `verify-ppv-p2.sh:231-303` 抽 7 字段解析/rehash/freshness 函数到 lib ② `verify-ppv-p2.sh` 改为 source lib ③ 新建 consumer wrapper ④ IDS `/handback-review` Step 4 调 wrapper ⑤ bootstrap-kit mirror + SHA dual-verify
   - 风险:抽 lib 时改坏 producer 端已 ship 的 PPV → 必须 producer 端回归测试(v0.2 已 PASS 的 case 重跑)
2. **REVIEW-LOG path 模块**(XenoDev `.claude/skills/codex-review/`)
   - 当前问题:singleton `REVIEW-LOG.md` · 新 review `cat >` 覆盖 · hand-back `review_log_sha256` 绑定失效风险
   - 目标态:`real-review/<task>-round<N>-REVIEW-LOG.md` immutable per-review · singleton 可留 latest pointer
   - 改造步骤:① 改 codex-review writer path 范式 ② hand-back gen 绑 immutable path ③ SHARED-CONTRACT B-4-IDS 示例 `review_log_path` 同步改 ④ 不 cleanup 老 immutable 文件
   - 风险:已存在的 v0.2 hand-back 绑的是 singleton path → 需确认历史 hand-back 不被破坏(forward-only · 老的不动)
3. **SHARED-CONTRACT 治理模块**(IDS `framework/SHARED-CONTRACT.md`)
   - 当前问题:contract_version 漂移 · cross_repo_split 无 normative · D-precedent 无流程
   - 目标态:frontmatter 2.3 · §6 加 cross_repo_split normative · §8 加 D-precedent governance
   - 改造步骤:① frontmatter bump(与 P0 波同 commit)② §6 收编 HANDOFF §7 六子节为 normative ③ 新 §8 写 D-precedent 准入(owner/期限/验证门)④ Changelog v0.3 entry
   - 风险:§6 收编后 HANDOFF §7 与 SHARED-CONTRACT §6 的"谁是 SSOT"要写清(HANDOFF §7 引用 §6 · 不再自带完整协议)

### W 含 next-dev-plan → 关键 milestone(2 波 + 估时)
- **P0 原子波**(估 0.5-1 天 · 改 XenoDev 为主 + IDS contract/示例)
  - target_repo: XenoDev(共享 lib + validator + R-Q7 writer)· IDS(SHARED-CONTRACT B-4 示例 + contract bump · bootstrap-kit mirror)
  - milestone:R-Q6 consumer 端能 verify producer 写的 7 字段 + R-Q7 immutable path 落地 + contract 2.3 + 示例同步 → 一个原子 commit/wave
- **P1 波**(估 0.5 天 · 纯 IDS SHARED-CONTRACT)
  - target_repo: IDS
  - milestone:§6 cross_repo_split normative + §8 D-precedent governance + Changelog → contract 可能再 bump 到 2.4(P1 波是否独立 bump,留 synthesizer/operator 定:我倾向 P1 波合进 2.3 同一次发布,不单独 2.4 · 因两波间隔短)
- **B-3**:不进 dev-plan · 续 v0.3-note

---

**Finalize 完成**:strong-converge 单一 verdict · 0 unresolved · 6 项 backlog 决策矩阵 + 3 模块 refactor-plan + 2 波 next-dev-plan 草稿齐全 · 3 条 v0.3-note。synthesizer 可直接出 stage-forge-006-v4.md。
