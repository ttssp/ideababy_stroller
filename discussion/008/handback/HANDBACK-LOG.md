---
doc_type: handback-decision-log
first_created: 2026-06-04T10:10:43Z
last_updated: 2026-06-04T10:10:43Z
total_decisions: 1
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry
---

# HANDBACK-LOG · discussion 008

per `framework/SHARED-CONTRACT.md` §6.4,本文件是 operator 在 IDS 端对 XenoDev hand-back 包的决议日志。append-only。

## 2026-06-04T10:10:43Z · 008-pB-20260604T095517Z

**Reviewed at**: 2026-06-04T10:10:43Z
**Tags**: prd-revision-trigger
**Severity**: high
**Related task**: T005

**Validator self-check**(Step 4.2 / 4.3):
- 6 约束自检(consumer mode):**PASS**(all 6 constraints,validate-handback.sh exit 0)
  - 注:首次用 repo-relative 路径调 validator 时 check-5 误报「cannot extract discussion_id」;改用绝对路径后 PASS。属调用形态问题,非包损坏。
- verdict-evidence precheck:**N/A**(无 `ids_verdict_evidence:` 块;gate-FAIL 包非 build-ship,正常)

**Operator decisions**:
- [ ] 修 PRD §"采集手段/C5 边界"(经 /scope-inject)→ **改走 forge,不在本 hand-back 内直接改 PRD**
- [ ] 修 SHARED-CONTRACT §"—"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **hand-back 核心结论被 operator 证伪 → 起 `/expert-forge 008` 重定 C5 边界 + 重评可达性**
- [ ] 无操作(收悉)

**Operator note**:
hand-back 的 go/no-go 结论(回放 FAIL · 图文 go)**前提错误,整体不成立**,理由两条:

1. **「图文合规可达 ✓」是误判**:探针证据 `article-sample-001.png` 只是 operator 截了一张屏,不是合规采集到图文原内容。真要采集图文/text 原内容,**和回放一样需要抓包**。探针把「人能正常浏览 + 截屏」误当成了「能合规采集原内容」——「浏览可达」≠「采集可达」,二者合规边界不同。

2. **C5 红线判定本身错误**:hand-back 把回放采集归为「复用已失效 token 模拟未授权请求 → 规避访问控制 → 踩 DMCA§1201/CFAA」。但 operator 确认实际采集手段 = **付费订阅用户 · 用当前有效登录态抓自己合法请求返回的视频/图文地址直接下载 · 自用不传播**。此手段拿的是**已被授权访问的内容,未规避任何本不该有的访问权** → **C5 未踩** → 回放与图文在 C5 边界内**均可达**。

**∴ 探针 FAIL 是基于错误的 C5 判定得出,结论不可信。**回放是 008 **核心价值 · 必须获取**,「图文先走 / 回放移 v0.2」的推荐路径不成立(= 掏空 008 核心)。

**决议路由**:C5 边界重定(从「任何抓包=踩线」→「付费自用·有效登录态抓自己流量 OK」)是**框架级 + 法律红线 + 探针结论整体推翻** = 重大方向变更。per CLAUDE.md「重大架构转向必须 /expert-forge(防 V4)」+ hand-back §3 自身「⚠️ 改 C5 须 IDS 显式决议」+ §3 选项 3「重大方向变更走 forge 而非 hand-back 内决」→ **起 `/expert-forge 008`**,在 forge 内:
- 重定 C5 采集边界判定标准(区分「有效登录态抓自己流量」vs「复用过期 token 规避」)
- 据新 C5 重评图文 + 回放采集可达性
- 据重评结论决定 PRD 修订(forge 后再 /scope-inject 或新 PRD 版本)
- 必要时回 XenoDev 按正确 C5 理解重跑探针(明确区分 浏览 vs 采集)

**⚠️ 残留法律风险标注**(operator 已知悉):DMCA§1201 规避访问控制条款,美国法下「付费 + 自用」**不天然豁免**。本决议成立的关键依赖 = 采集手段确为「有效登录态抓自己合法流量」而**非**「复用过期/失效 token」。此法律定性的最终确认 + C5 措辞应在 forge 内严谨落定。

**Follow-up**: forge v1 已完成(2026-06-04 · converged · strong-converge)。verdict = **refactor-and-reset**:① 修 C5 措辞(「正常能看到」→「有权访问 + 有效登录态采原内容」)② 回放 scope 复位至 v0.1(cut 本 handback「回放移 v0.2」依据)③ token 失效介入成本升为显式 outcome ④ Phase-0 gate 判准从「合规可达性」→「自动化稳定性」。stage 文档:`discussion/008/forge/v1/stage-forge-008-v1.md`。下一步:operator 选 Decision menu [A] → /scope-inject 008-pB 改 PRD。本 handback 的 FAIL 论证(回放合规下不可达)已被 forge 显式作废。
**Follow-up commits**: PRD 修订已落地(2026-06-05 · 直接改 PRD 本体,非重开 L3)。`discussion/008/008-pB/PRD.md` v1.0→v1.1:① C5 改写(「正常能看到」→「有权访问+有效登录态采原内容」)② 回放 scope 复位 v0.1 ③ 新增 O5b outcome(token 失效扫码一次)④ Phase-0 gate 判准改向(自动化稳定性)⑤ US3/O3 回放摘要加稳定时间戳 ⑥ 三形态共享登录态(operator 拍板)。FORK-ORIGIN.md 旧 C5 同步划改。operator 同期拍板 3 决策点(扫码一次/稳定时间戳/共享登录态)。git commit 待 operator 确认后产出。
