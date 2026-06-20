---
doc_type: handback-decision-log
first_created: 2026-06-04T10:10:43Z
last_updated: 2026-06-17T01:46:45Z
total_decisions: 3
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

## 2026-06-16T00:36:17Z · 008-pB-20260615T234706Z

**Reviewed at**: 2026-06-16T00:36:17Z
**Tags**: feature
**Severity**: medium
**Related task**: T112

**Validator self-check**(Step 4.2 / 4.3):
- 6 约束自检(consumer mode):**PASS**(all 6 constraints,validate-handback.sh exit 0,绝对路径调用)
- verdict-evidence precheck:**N/A**(无 `ids_verdict_evidence:` 块;tag=feature 集成交付包,非 build-ship verdict 包,正常)

**Operator decisions**:
- [ ] 修 PRD §"—"(经 /scope-inject)
- [ ] 修 SHARED-CONTRACT §"—"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **无操作(收悉,作为 practice-stats 入库)**

**Operator note**:
008-pB v0.1 集成 ship 交付包(T101-T112 全 12 task 闭环,406 test 全绿零回归)。性质 = clean v0.1 delivery,**非** drift / spec-gap / 架构转向 / Safety Floor 违反 → 对 IDS 治理层无文档改动,operator 决议纯收悉入库。

未勾选项的处理(决议级说明,非本包待办):
- **§3④ dogfood backlog**(KG-21 模块名遮蔽 / cli.py 统一 + FU-T110/T111/T102-3 等):按 CLAUDE.md「dogfood 铁律」框架级变更**攒批走 `/expert-forge 006`**,不在本 hand-back 内当场改 SHARED-CONTRACT。本包不为其单开 pending —— 由 XenoDev `dogfood-backlog.md` 累积,operator 后续起 forge 006 时统一审。
- **§3②③⑤ operator 真机验收清单**(O1/O2/O3/O5b 真手机微信 + 2 周观察窗;P2/P3 verify-ppv-p2/p3.sh 真路径校验;PPV accepted-limit 确认):属 operator 侧 v0.1 主观验收,IDS 治理层无法代验,不构成 IDS 文档动作。operator 知悉,验收完成前 v0.1 不算最终 accepted;但**不**在 IDS log 内开 pending 追踪(单包决议级,非项目追踪面板)。

**∴ 本包决议 = 收悉入库。** 无 PRD 修订 / 无 SHARED-CONTRACT 修订 / 无 XenoDev spec 修订触发。

**Follow-up commits**: 无(纯信息式收悉,无 IDS 改动产生 commit)。

## 2026-06-17T01:46:45Z · 008-pB-20260617T011156Z

**Reviewed at**: 2026-06-17T01:46:45Z
**Tags**: feature
**Severity**: medium
**Related task**: T222(v0.2 DAG 终点 · ship)

**Validator self-check**(Step 4.2 / 4.3):
- 6 约束自检(consumer mode):**PASS**(all 6 constraints,validate-handback.sh exit 0,绝对路径调用)
- verdict-evidence precheck:**N/A**(无 `ids_verdict_evidence:` 块;tag=feature 集成交付包,非 build-ship verdict 包,正常)

**Operator decisions**:
- [ ] 修 PRD §"—"(经 /scope-inject)
- [ ] 修 SHARED-CONTRACT §"—"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **无操作(收悉,作为 practice-stats 入库)**

**Operator note**:
008-pB **v0.2 全闭环 ship** 交付包(9 task:Wave EXP T201/T203/T204/T202 + Wave 004 T210/T205 + Wave US7 T220/T221/T222,DAG 终点 T222)。三块 bounded scope 闭环:① Obsidian 库→vault 单向 exporter(US8 载体 · forge v2 主交付)② 完整 004 输出契约(frozen binding + maxLength + P5 验证器)③ US7 盘中预警采集 + 及时通知 + 三形态统一时间线集成。732 test 全绿零回归。性质 = clean v0.2 delivery,**与上一个已决议 v0.1 包(20260615T234706Z)同构** —— tag=feature、无 PRD 矛盾、无重大架构转向、无 Safety Floor 违反 → 对 IDS 治理层无文档改动,operator 决议纯收悉入库。

§2 关键决议(均 build 阶段 operator 已拍板,**非** IDS 侧新转向):
- **预警同源决议**(T220 探针实证 reachability.md:12):盘中预警同源同渠道·共享 v0.1 登录态 → **不引第 2 条 O5b 恢复路径**(O5b 单一恢复路径假设成立 · PRD v1.1)。
- **预警形态隔离**:预警**不进共享 records 表**(form ∈ frozen {article,replay} **不解冻** T210 binding)→ 独立 alert 日志 + durable kind wrapper;vault 内用 `vault/alerts/` 文件夹判别形态(非 frontmatter form)。
- **T222 决议 A 跨域授权**:codex R1 揭露「集成是空的」(预警不进 vault / notify 无 caller / 验收假绿)→ operator 显式授权跨域扩 file_domain 到 `src/export/obsidian.py` 真接三形态。**未动 PRD 产品决策、未解冻 frozen form** → 不构成 IDS 修订触发。
- **codex 3 轮收口抓多个 CRITICAL/high**(全当轮修 + 独立复验):T202 source_id 路径逃逸(CRITICAL)+ 原地写截断(high→_atomic_write)· T205 --no-export 绕过(CRITICAL)+ rmtree 先于校验(CRITICAL)+ verifier 用真 vault 当 scratch(high)。

未勾选项的处理(决议级说明,非本包待办):
- **§3④ dogfood backlog + FU**(随本包回流):
  - **KG-23**(框架级 ship 流程缺陷):codex `--scope working-tree` 漏已 commit 改动 → ship 每轮 commit 后须 `--base main --scope branch`(R3 首踩 vacuous approve)。**operator 决议**:按 CLAUDE.md「dogfood 铁律」**攒批走 `/expert-forge 006`**,由 XenoDev `dogfood-backlog.md` 累积,不在本 hand-back 内当场改 SHARED-CONTRACT。本包**不**为 KG-23 单开 pending —— forge 006 起时统一审。
  - **FU-T220-1 / FU-T221-1 / FU-T222-1**(预警同源 + O7 阈值 + 决议 A 跨域真接)+ **FU-T205-1 / FU-T210-2/3 / FU-T202-2 / FU-T203-1**(PPV 真密码学溯源属真采集阶段 / 摘要长度上限是 spec line 55/272 known-gap):同 KG-23,XenoDev backlog 累积,攒批 forge,不在本包决议内当场改。
- **§3②③ operator 真机验收清单**(IDS 治理层无法代验,不构成 IDS 文档动作,**不**开 pending 追踪 —— 单包决议级非项目追踪面板):
  - **O6** 连续 2 周三形态(图文+回放+预警)全部零漏(人工核对采集 vs 实际发布)。
  - **O7** 盘中预警 ≤300s 及时通知(operator 制造真预警抽查;需配真 webhook env `XENODEV_ALERT_WEBHOOK_URL` + 起 cron/daemon 周期跑;notify_pending_alerts 生产路径已就绪)。
  - **O10b** Obsidian Bases/只读查询实测四维(日期/形态/标的/已看)命中(脚本证明不了 Calendar/Bases 查询路径本身;预警形态判别 = `vault/alerts/` 文件夹)。
  - **③ 机器可验项已自动验过**(可复核):`bash specs/008-pB/scripts/verify-v0.2-acceptance.sh <db> <base> vault` → O8/O9/O10a 经 verify-ppv-p4.sh + 预警端到端真路径。
- **§3⑤ accepted-limit 确认**:PPV 反作弊对 v0.2 威胁模型(反 exporter mock-pass / 库→vault 真路径 / 完整 004 契约)合格;DB 自身真溯源(handoff/workspace 签名)是更上游(T106/采集层)+ 跨仓 handoff 事,同 v0.1 P1 accepted-limit,留真采集/forge。operator 知悉,验收完成前 v0.2 不算最终 accepted。

**∴ 本包决议 = 收悉入库。** 无 PRD 修订 / 无 SHARED-CONTRACT 修订 / 无 XenoDev spec 修订触发;KG-23 等 dogfood/FU 攒批走 forge 006(铁律默认,本包不单开 pending)。

**Follow-up commits**: 无(纯信息式收悉,无 IDS 改动产生 commit)。
