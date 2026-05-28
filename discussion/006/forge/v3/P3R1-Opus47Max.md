---
phase: P3R1
side: Opus47Max
forge_id: 006
forge_version: v3
generated: 2026-05-27T13:08:00Z
disagreements_count: 3
word_count_approx: 870
---

# P3R1 · Opus side · 联合收敛 R1(v3)

## §1 · 整合摘要

双方 P1/P2 已读 · 0 推翻 · K8-K11 全 ✅ · v3 strong-converge 基本盘极稳。**核心共识 7 条**:

1. **分波执行 + 每波 manifest + provenance + SHA dual-verify + bootstrap verify**(K10 边界纪律真路径)
2. **wave 1 P0 hard-block 子集**:templates/gen-handback/score-handback mirror(producer 入口硬依赖)+ B-2 enum 单复数统一 + C-1 scan-credentials exit code + C-3 case F regression
3. **协议 4 项处置一致**:B-1 EXDEV 协议段 = P1 改 / B-2 enum = P0 改 / B-3 IDS dir flock = v0.2-note / B-4 `--ids-verdict-evidence` flag = P1 协议改 + 真路径 task
4. **Cluster A mirror rebuild 9 文件全 N(new)**:7 子树 cp · 0 推翻 v2 verdict · 0 触动大架构
5. **Cluster C lib bug 3 项 priority 完全一致**:C-1 P0 / C-2 P1 / C-3 P0
6. **K11 残余 1 项 v0.2-note**:B-3 IDS dir flock(双方 P2 都接受 v0.2-note)— 合规旁注非压扁分歧
7. **3 件 R1 不确定事项**(详 §3 关键分歧清单):wave 顺序 / 协议改与真路径拆分边界 / manifest 机制具体形态

## §2 · 我的初步 verdict 草案(单段 3-5 行 · 不 hedge)

**v3 verdict 初稿**:v0.2 = 11 项 backlog 三类 batch ship · **3 wave 顺序**(wave 1 = templates/gen/score mirror + C-1 + C-3 + B-2 enum 统一 / wave 2 = skills+hooks mirror + B-1 EXDEV 协议改 + B-4 verdict-evidence 协议改 + C-2 + tests/integration mirror / wave 3 = bootstrap.sh 升级新路径 + 跑通新 idea bootstrap → verify-all SHIP-READY)· 每 wave 1 IDS commit + manifest(source path / target path / SHA / 验证命令)· B-3 IDS dir flock 留 v0.2-note(并发未实证 · 当前 fail-closed cleanup 足够)· B-4 `--ids-verdict-evidence` flag 协议改入 v3 + 真路径实装 task 落 XenoDev 单独 ship · v0.2 ship 关闭判据 = 新 idea bootstrap 跑通 + verify-all-outcomes.sh + manifest 完整 + B-3 v0.2-note 在 SHARED-CONTRACT changelog 显式记。

## §3 · 关键分歧清单(3 条 · R2 期望收敛方向)

### D1 · wave 顺序:tests/integration 放 wave 2 还是 wave 3?

- **Opus 立场**:tests/integration 放 **wave 2**(与 skills+hooks 同波)+ wave 3 留 bootstrap.sh 升级 + 真新 idea bootstrap 验证。理由:tests/integration mirror cp 是文件级 SSOT,与 bootstrap.sh 升级是不同动作;混波让 wave 3 真路径过载。
- **对方立场**(Codex P2 §3.2 row 5):tests/integration 放 **wave 3**,priority P1/P2。引用 ≤15 words:"随 wave 3 验证"。
- **R2 期望收敛方向**:
  - 折中方案:**wave 2 cp tests 文件 + 改 wave 3 = "跑 wave 2 cp 后的 tests 在 IDS bootstrap 出生的新 idea 内"** — 即 wave 2 完文件,wave 3 完真路径联调。
  - 若 Codex 坚持 wave 3 = cp + 验证一起 → Opus 让步(tests cp 是 5 个文件级别,wave 顺序 1 波差异不大)。

### D2 · 协议改 vs 真路径实装的边界(B-4 verdict-evidence flag)

- **Opus 立场**(P2 §3.2 B-4):**改 SHARED-CONTRACT §6 是 v3 范围;真路径实装 `--ids-verdict-evidence` flag + REVIEW-LOG.md machine-readable schema 在 XenoDev 端单独 task ship,不在 v3 forge 范围**。理由:v3 是 IDS 仓 forge,XenoDev task ship 不该塞进 forge stage doc 的 W5 dev plan(那是 v2 verdict 已设定的双仓边界)。
- **对方立场**(Codex P2 §3.2 row 10):"维持;替代单 bit trust" — **未显式拆分协议改 vs 实装**。
- **R2 期望收敛方向**:Codex 显式表态是否同意 Opus 拆分(协议改 = v3 ship · 真路径实装 = XenoDev 端 v0.2 task)。若同意 → wave 2 协议改入 v3 IDS commit + W5 dev plan 标"XenoDev side: T0XX `--ids-verdict-evidence` 实装 task"。若反对 → 显示 Codex 倾向 v3 直接覆盖 XenoDev task 的根据。

### D3 · manifest 机制具体形态(共识但细节未定)

- **共识**:每 wave 1 manifest · 含 source path / target path / SHA / 验证命令(双方 P2 完全一致)
- **未定 1**:manifest 写哪里?(`framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md`?或 `discussion/006/v0.2/MANIFEST-wave-{1,2,3}.md`?)
- **未定 2**:bootstrap-kit/README.md 是否同步更新描述 4 个新子树(skills + hooks + tests + templates)?
- **未定 3**:bootstrap.sh 升级让新 idea bootstrap 自动消费新子树 — 这是 XenoDev 端 task 还是 IDS 端 task?
- **R2 期望收敛方向**:Codex 给具体位置 + 是否同意 manifest 入 `framework/xenodev-bootstrap-kit/` 子树(以 SSOT 边界内 ack 收口),bootstrap.sh 升级落 IDS bootstrap-kit/bootstrap.sh(因 IDS 是 SSOT owner)还是 XenoDev 真路径?

## §4 · 对 K 的对齐性自检(逐条 ✅/⚠/❌)

- ✅ **K8** v3 mission(11 项 backlog 三类)— §1 §2 §3 全覆盖 · 0 漏 · 0 越界
- ✅ **K9** v2 verdict 不重审 — §2 verdict 草案 0 触动 IDS=治理 / XenoDev=唯一 L4 / 双向 hand-off
- ✅ **K10** 边界先定、批量 SSOT、不越界 — wave 1/2/3 每波 1 commit + manifest + SHA · K10 直接落地;**B-3 不做** = K10 真路径(v0.3 范畴不入 v3)
- ⚠ **K11** strong-converge 一一对一 — 11 项中 10 项已收敛 verdict;残余 1 项(B-3 IDS dir flock)落 v0.2-note(合规旁注 · 非压扁分歧 · K11 §"残余分歧用 v0.2-note 旁注" 显式允许)
- ✅ **k_provenance** verbatim — K 文本本 P3R1 未 edit

---

**Soft hand-off to Codex P3R1**:本 R1 共识 7 条 + 分歧 3 条 + verdict 初稿。HARD CONSTRAINTS 已遵守:NO new search · ≥1 关键分歧(列 3 条)· verdict 初稿 §2 已给。Codex P3R1 期望:(a) 对 D1/D2/D3 显式表态;(b) 给 R2 期望收敛方向;(c) 同意 strong-converge 路径 OR 显式反对。
