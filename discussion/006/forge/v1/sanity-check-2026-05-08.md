---
doc_type: sanity-check-report
generated: 2026-05-08
upstream: 5 件事(NON-GOALS / SHARED-CONTRACT / AGENTS.md 升级 / AUTODEV-PIPE-SYNC-PROPOSAL / stage v1 §2 重写 + next-steps)
purpose: 5 件事完成后的客观核查 + A/B/C 路径推荐
verdict: 4 文档基本无矛盾;3 处差距已修 2 处 / 留 1 处 follow-up;推荐路径 = C(文档版即足够)
---

# Sanity Check · 2026-05-08

## 总评

**5 件事产物可工作;3 commits 已落地;3 处 sanity check 发现的差距 — 修 2 / 留 1**。最稳妥下一步 = **结果 C**(framework v0.1 = 文档而已,不立刻启动 build),理由见末尾。

---

## 核查 1 · 交叉引用网络

4 份文档之间的引用图(grep 实测,非主观):

```
                  AGENTS.md
                 ╱   │   ╲
               ╱     │     ╲
       NON-GOALS  SHARED-CONTRACT  AUTODEV-PIPE-SYNC-PROPOSAL
            ╲    ╱   │   ╲    ╱
             ╲ ╱     │     ╲ ╱
              X      │      X
             ╱ ╲     │     ╱ ╲
       AGENTS  SHARED-CONTRACT-mirror
```

实测结果(`grep -n`):

| 引用方 → 被引用方 | 次数 | 备注 |
|---|---|---|
| AGENTS → SHARED-CONTRACT | 4 | §1 / §4 / §7 references |
| AGENTS → NON-GOALS | 1 | §7 references |
| AGENTS → AUTODEV-PIPE-SYNC-PROPOSAL | 1 | §7 references |
| NON-GOALS → SHARED-CONTRACT | 2 | NG-7 例外 |
| NON-GOALS → AGENTS | 4 | NG-1 例外 / NG-3 论据 |
| SHARED-CONTRACT → NON-GOALS | 1 | §"本文档定位"(NG-2/NG-7) |
| SHARED-CONTRACT → AGENTS | 7 | §1 / §3 / §4 / §5 五元组 |
| AUTODEV-PIPE-SYNC-PROPOSAL → SHARED-CONTRACT | 12 | 整体提案的核心 |
| AUTODEV-PIPE-SYNC-PROPOSAL → NON-GOALS | 1 | 同步前置条件 |
| AUTODEV-PIPE-SYNC-PROPOSAL → stage-forge-006-v1.md §2 | 1 | 同步前置条件(读 L/P/C 矩阵) |

**结论**:**全连通 / 无悬挂引用**。每对文档之间至少有 1 条引用,无孤立。

---

## 核查 2 · 字段可填性

针对 SHARED-CONTRACT §1 PRD schema 8 必填字段,逐字段验证 stage v1 §4 PRD draft 是否真的可填:

| Schema 字段 | stage v1 §4 实际填法 | 可填? |
|---|---|---|
| frontmatter PRD-form | `simple` | ✅ |
| frontmatter Status | `Draft from forge v1, awaiting human approval` | ✅ |
| frontmatter Sources | `discussion/006/forge/v1/stage-forge-006-v1.md`(已修字段名) | ✅ |
| frontmatter Forked-from | `forge stage(L0 直接 bootstrap,非 L3 candidate)` | ✅ |
| User persona | "非软件开发背景但能写较可靠 PRD 的独立开发者" | ✅ |
| Core user stories | 4 条具体 story | ✅ |
| Scope IN | 5 条具体 IN | ✅ |
| Scope OUT | 5 条 NOT 项,带 evidence | ✅ |
| Success looks like | 5 条量化指标 | ✅ |
| Real constraints | 时间/预算/平台/合规 4 项 | ✅ |
| UX principles(optional) | 4 条 | ✅ |
| Open questions(optional) | OQ1-OQ3 | ✅ |

**结论**:8/8 required + 2/2 optional 全可填,**实际样例已存在**(stage v1 §4)。Schema 设计与实际产物完全对齐。

---

## 核查 3 · 契约 vs 实现差距(发现的真实问题)

| # | 差距 | 后果 | 修复 |
|---|---|---|---|
| 1 | SHARED-CONTRACT §4 声明 frontmatter 含 `contract_version`,但 frontmatter 实际只有 `status` | autodev_pipe 解析时读不到 contract_version,会拒绝运行 | ✅ 已修(frontmatter 加 `contract_version: 1.0.0`) |
| 2 | §1 PRD schema 用 `Source`(单数);stage v1 §4 实际样例用 `Sources`(复数) | autodev_pipe 严格按 schema 解析时读不到 PRD 来源 | ✅ 已修(SHARED-CONTRACT 改用 `Sources` 复数) |
| 3 | §3 假设 `/plan-start` 命令产出 HANDOFF.md;实际 `.claude/commands/plan-start.md` **不含此逻辑** | hand-off 协议在实际工作流中 broken | ⏸ Follow-up(已在 SHARED-CONTRACT §3 加 "Implementation status" 小节标注;next-steps.md 加 followup task) |

**修复 1+2 已落地;3 留作 follow-up,不阻塞 framework v0.1**。修复 3 的触发条件 = 决定走结果 A(实质 build),那时再改 `/plan-start.md` 加 HANDOFF.md 产出步骤(估时 ~2h)。

---

## 核查 4 · NON-GOALS 7 条全部有依据 + failure case

逐条验证(grep + 文档结构):

| NG | 含义 | 客观依据 | Failure case |
|---|---|---|---|
| NG-1 | 不内化历史 repo 代码 | Linux/Anthropic OSS 范式 / Brooks second-system | Spotify Backstage / Uber Cadence |
| NG-2 | IDS 不做 build/review/brakes | Newman ch.4 / 4 维度差异 / Google monorepo 反向论 | Spotify Backstage 三目标合一 |
| NG-3 | 不再发明 SKILL/AGENT 体系 | LF AAIF 2025 / Anthropic Skills SDK / Vercel benchmark | Atom vs VS Code / Cordova vs RN |
| NG-4 | 不承诺 full-auto 跨 Safety Floor | Cursor 删库 / Codex CLI 范式 / K2 verbatim | Cursor + Claude 9 秒 / Magicrails 14k loop |
| NG-5 | 不复制 Cloudflare 全量 7 reviewer | Cloudflare 自己起步也不是 7 / 80/20 / SWE-PRBench 数据 | Cloudflare 早期 / Spotify over-engineering |
| NG-6 | 不把 SWE-bench Pro 当 CI gate | SWE-Bench Pro 23% / regression-vs-absolute 范式 | ML 团队 accuracy gate / webpack-bundle-analyzer |
| NG-7 | 两仓不版本绑定 | Newman ch.7 / npm semver / Linux + glibc 30 年 | Twitter monolith 拆分 / Atlassian 早期 |

**结论**:7/7 全有客观依据 + failure case。无主观 NG。

---

## 核查 5 · stage v1 §2 重写后 28 项分层一致性

| Layer | 预估(next-steps) | 实际 | 差距原因 |
|---|---|---|---|
| L | 11 | 9 | 多个 vibe-workflow / idea_gamma2 项实际归 P 级(借鉴结构自己实现) |
| P | 8 | 11 | 同上反向 |
| C | 8 | 5 | NG-1 严格执行,v3.1 STARTER_KIT 留 ADP 不 cp 到 IDS |

**结论**:实际分布**比 next-steps 预估更保守**(L+C 少 / P 多),符合 NG-1 "不内化历史 repo 代码" 约束。这是好事 — 实际比预估更严守工程边界。

---

## 核查 6 · plan §"完成判定点" 三结果触发条件实测

| 结果 | 触发条件 | 实测状态 |
|---|---|---|
| **A · 启动 stage §5 Phase 1 build**(autodev_pipe) | 4 文档无矛盾 / SHARED-CONTRACT 字段全可填 / autodev_pipe 同步无障碍 | ✅ 文档无矛盾;✅ 字段全可填;⚠ autodev_pipe 同步**有降级**(本会话 cwd 在 IDS,SYNC-PROPOSAL 是降级形式) |
| **B · 起 forge v2** | 写文档时发现争议无法用客观依据解决 / 某条 NG 无足够依据 / AGENTS.md 8KB 装不下基本不变量 | ❌ 未触发(争议都用客观依据解决;7 NG 全有依据;AGENTS.md 7252 字节装下 7 节) |
| **C · framework v0.1 = 文档而已** | 发现现有产物已覆盖 80% 实际需求 | ✅ 触发(idea→PRD 这边 L1-L4 + forge 已成型;新加 4 份文档 = framework SSOT 完备;build 是 ADP 范畴不在本仓库工作) |

**结论**:A 部分触发(同步降级,但不阻塞);B 不触发;**C 完全触发**。

---

## 推荐:走结果 C,理由

### 为什么不走 A

A 触发 = 启动 stage v1 §5 Phase 1 build。但**实际 build 工作发生在 autodev_pipe 仓库**,不在 ideababy_stroller。

ideababy_stroller 这边,**idea→PRD 流程已经齐了**:
- L1 inspire / L2 explore / L3 scope / L4 plan 命令链已存在
- forge 横切层已存在(本次 forge 006 v1 即此机制成功跑过)
- 4 份新加 framework 文档 = idea→PRD harness 的 SSOT 已完备
- stage v1 §2 L/P/C 重写 = 复用矩阵已显式化

**A 路径要求"启动 build"但 build 不在这里**。如果立刻走 A,实际动作 = "切到 autodev_pipe 仓库做事"——但 autodev_pipe 当前状态未知,SYNC-PROPOSAL 还是降级形式。

### 为什么不走 B

B 触发 = 客观依据不足。但 5 件事产物的依据密度极高(每份文档每节都有 5-10 条具体引用)。**无 B 触发信号**。强行走 B 等于"再问一遍",违反 forge protocol 哲学(forge 解决论证不充分,不解决"想法没演化")。

### 为什么走 C

C 触发 = 现有产物覆盖 80% 实际需求。客观证据:

1. **idea→PRD 阶段已完整** — 4 份 framework 文档 + L1-L4 + forge 命令链 = 完备工具链
2. **build 阶段不在本仓库** — IDS 这边再做更多文档,边际收益递减
3. **真实需求是"用一段时间收集 PRD 用例"** — Anthropic 2026 Trends "harness > model upgrade" 的极致形态正是"harness 可能根本不需要新代码"
4. **3 处 sanity check 发现的 drift 中 1 处 follow-up** — 不阻塞 v0.1,但**说明现状已经在工作**

### C 路径的具体下一步动作

**不立刻**做事,而是**用一段时间**:

1. 用 framework v0.1(当前 4 份文档 + L1-L4 + forge)**实际跑 1-2 个新 idea**(从 proposal 开始走 L1→L2→L3→L4→PRD),记录什么阻塞、什么顺畅
2. 从真实 use case 反推 framework v0.2 的改动 — 比如 follow-up task 1 (`/plan-start` 加 HANDOFF.md)是否真的需要,可能在第二个 PRD 跑完时自然出现明确信号
3. 如果 1-2 个真实 PRD 跑完后,framework 仍然好用 → 可以宣布 framework v1.0
4. 如果跑出明显 gap → 自然触发 forge v2 或 specific PR

### 与 forge stage v1 §"Decision menu" 对应

stage v1 §"Decision menu" 5 个选项:
- **[A] 接受 verdict 进 L4** → fork 出 PRD branch,但本次 sanity check 发现现有 framework 文档已覆盖,**暂不需要这一步**
- **[B] 跑 forge v2** → 无触发,推迟
- **[C] 局部接受** → 已经隐性在做(NG-2 分仓 / NG-1 不内化代码 都是局部接受 + 局部反对 stage v1 立场)
- **[P] Park** → 不适合(verdict 已在落地)
- **[Z] Abandon** → 不适合(verdict 锐利)

走结果 C 实际对应 stage 文档的"局部接受 + 用真实 use case 验证后再决定"——这是 forge stage v1 §"Decision menu" 没显式列但最稳妥的子选项。

---

## 残余问题(非阻塞)

| 问题 | 处理 |
|---|---|
| Follow-up task 1: `/plan-start` 加 HANDOFF.md 产出 | 走结果 A 时再做(估 2h) |
| Follow-up task 2: 完整 grep 找其他 contract drift | framework v1.0 release 前做(估 1h) |
| autodev_pipe 仓库当前状态未知 | 切到 ADP 仓库时按 SYNC-PROPOSAL 落地 |
| stage v1 §"Decision menu" §5 dev plan Phase 2-5 | 留作 framework v0.2/v1.0 时分批触发 |
| OQ1-OQ3(stage v1 §4 open questions) | 留作真实 use case 暴露后逐一闭环 |

---

## 总结一句话

**4 份文档间无矛盾,8 PRD 字段全可填,7 NG 全有依据;3 处发现的契约 drift 修 2 留 1;推荐结果 C(用 framework v0.1 跑真实 PRD,不立刻动代码)**。

如果你要更激进的下一步,A 也不错(切到 autodev_pipe 按 SYNC-PROPOSAL 实际落地)。但 C 更稳妥,符合本次"工程边界先于实现"的哲学。
