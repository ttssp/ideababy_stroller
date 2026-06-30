---
doc_type: handback-decision-log
first_created: 2026-06-04T10:10:43Z
last_updated: 2026-06-30T09:03:24Z
total_decisions: 10
total_entries: 11
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry。2026-06-30 批量决议 7 包(T301-T306 v0.3 broker 交付批 + 20260630 下游用途 PRD 缺口包),total_decisions 3→10
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

---

## 2026-06-30T08:43:33Z · 008-pB-20260630T084333Z

**状态**:📥 已交付,**PENDING operator review**(待 IDS 跑 `/handback-review 008` 决议;本条由 producer/XenoDev 记录交付,非决议)。

**包**:`discussion/008/handback/20260630T084333Z-008-pB-20260630T084333Z.md`(6 约束 producer+consumer 双验 PASS)。

**性质**:PRD 缺口上报 + dogfood 回流。**非** spec/PRD 矛盾、**非**重大架构转向。tag=drift / severity=medium。

§1 摘要:operator 配 token 补 43 回放音频缺口(3 token 窗口接力·全集音频 100%)+ 增量链路验证 work + checkpoint 盲区自愈;借机系统盘点(8913 条三品类已采+结构化 99.97%),operator 质疑「下游用途没定,前期结构化是否纸上谈兵」→ 6 subagent 并行归纳结构化字典三层 + 红队评审收敛无悔层。

§2 触发:① **下游用途/消费目标从未定义**(根因·PRD 缺口)→ 字典第2/3层悬空;② operator 倾向「机器可信信号/跟单」但**提取可靠性未实测**(反讽+黑话 LLM 中等易错·无数字)→ 可行性悬而未决;③ KG-24(守护 _pending_replays 漏 skipped·high)/ KG-25(DeepSeek 坏 JSON 无容错·medium)随包回流。

§3 给 IDS 的 X 标的(待 forge 决议):
- [ ] PRD 补「下游用途/消费目标」定义
- [ ] 若定「机器可信信号」→ 先决议做信号提取可靠性 spike(小样本核准确率再判跟单可行性)
- [ ] 据用途从字典三层挑工作项(第1层无悔可先落 · 第2层据用途点名挑 · 第3层重提待确需)
- [ ] KG-24 / KG-25 纳入 forge 批审
- [ ] 无操作(收悉)

**Operator decision**: ✅ 已于 2026-06-30T09:03:24Z 决议 —— 见下方同 handback_id 的正式决议 entry(本 PENDING stub 由 producer 记录交付,决议体在下条 append)。
**Follow-up commits**: 见下方决议 entry。

---

## 2026-06-30T09:03:24Z · 008-pB · T301–T306 批量决议(v0.3 受控自动翻页 broker 交付批 · 6 包)

> **批量 entry 说明**:本条一次决议 6 个 hand-back 包(handback_id 见下表),因 6 包同属一条 bounded 交付线(v0.3 broker 主体)、tag 全 `feature`、disposition 同构(clean delivery → 收悉入库 + followup 攒批 forge)。逐包 §1/§3 摘要列于「逐包要点」表;统一 operator 决议在末尾。**未合并既有 entry,纯 append。**

| handback_id | task | severity | §1 ship 摘要 |
|---|---|---|---|
| 008-pB-20260620T143955Z | T301 | high | broker 凭据隔离地基(src/broker 三模块零改既有 + deny-secrets hook + PreToolUse 注册) |
| 008-pB-20260620T152346Z | T302 | medium | plan/manifest O12 门(committed 锚点 + 对锚真 capture · anti-false-green) |
| 008-pB-20260620T160012Z | T303 | high | broker 主体(parse + detail_broker · HTTP/token 注入 · 禁重定向 · contentId 绑定 · C5 symlink 拒 · dup-id 拒 · 字节上限) |
| 008-pB-20260620T162527Z | T304 | medium | 附件下载(assets.py 纯匿名 GET · token 绝不发 OSS · sha16 存储名 · 二进制只落 gitignored out/) |
| 008-pB-20260620T172643Z | T305 | medium | 批量受控运行(runner + checkpoint · checkpoint 后于 ingest 防假 all_done · 429/403 立停 · corpus 从 DB-WHERE-form 防 replay 串号假绿) |
| 008-pB-20260621T023151Z | T306 | low | v0.3 验收脚本(诚实分两段:机器段证本地自洽 + operator attestation · 全集逐 ID 非抽样) |

**Reviewed at**: 2026-06-30T09:03:24Z
**Tags**: feature(全 6 包)
**Severity**: high(T301/T303)· medium(T302/T304/T305)· low(T306)
**Related task**: T301 / T302 / T303 / T304 / T305 / T306(v0.3 DAG 全线)

**Validator self-check**(Step 4.2 / 4.3):
- 6 约束自检(consumer mode):**初次 FAIL · 修复后 PASS**。
  - **FAIL 根因**(6 包同因):frontmatter `handback_target` / `workspace.*` 硬编码 `/Users/admin/codes/`(producer 在旧 Mac 产),但本仓现已搬到 `/home/ys/codes/`(operator 换机)→ check-1 canonical-path 字面前缀比较 FAIL。**非包损坏 / 非 path-traversal 攻击**:6 文件物理上均在正确 `discussion/008/handback/` 目录、非 symlink;repo identity(`expected_remote_url` = `git@github.com:ttssp/ideababy_stroller.git` + `git_common_dir_hash` = `28d25bf82af4c0e2`)与新机产的 20260630 包字节级一致 → 同一仓库,仅机器路径前缀变。
  - **operator 决议(换机 FAIL 处理)**:**先修 frontmatter 再决议**。批量 `s#/Users/admin/codes/#/home/ys/codes/#g`(仅机器前缀;`discussion/<id>/handback/` 段、`handback_id`、三个 id token 全不动 → 约束 5 三处一致 / 约束 6 charset 不受影响)。pre-fix 快照存 scratchpad `T301-T306-prefix-fix-snapshot.txt`。
  - **修后 re-run**:6/6 **PASS**(validate-handback.sh exit 0,绝对路径调用)。
- verdict-evidence precheck(Step 4.3):**N/A**(6 包均无 `ids_verdict_evidence:` 父键;tag=feature 集成交付包,非 build-ship verdict 包,正常)。

**Operator decisions**:
- [ ] 修 PRD §"—"(经 /scope-inject)
- [ ] 修 SHARED-CONTRACT §"—"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **无操作(收悉,作为 practice-stats 入库)** —— 6 包性质 = clean v0.3 delivery,与已决议 v0.1(20260615)/ v0.2(20260617)包同构。
- [x] **§3 内实质项 → 并入 `/expert-forge 008`**(非本批 feature 交付本身触发,而是 §3 携带的两条 forge 标的,详见下条 20260630 决议):
  - **T301 §3 前提更正**:列表 API 只给最近 **1 年**(止于 **2025-06-16** · total=**1114**),**非** forge v3 假定的 2025-07-21。此更正推翻 forge v3 的一条采集上界假设 → **必须进 forge 重审**(framework 张力,已记 XenoDev dogfood)。
  - **T303 §3 第三态预警**:若 detail 出验证码/反爬第三态 → 回 forge v4(本批未触发,标注待观察)。

**Operator note**:
v0.3「受控自动翻页」broker 交付批(T301-T306 全 6 task ship),codex 每 task 3 轮收口抓 critical(合成路径/解释器构造/SSRF userinfo/token 经 3xx 泄/replay 串号假绿/假 all_done 等)全当轮修。性质 = clean delivery,对 IDS 治理层除下述 forge 标的外无文档改动,决议纯收悉入库。

**两类未当场改项的路由**(决议级说明,非本批待办):
- **§3 各 `FU-v0.3-T30x-1` followup**(T301 残留 / T303 oversize-raw_ref partial-ingest[T305 已解] / T304 per-asset 失败可见[T305 已解] / T305 fsync 性能+jitter 真随机 / T306 run-evidence+附件期望数对账):按 CLAUDE.md「dogfood 铁律」由 XenoDev `dogfood-backlog.md` 累积,**攒批走 forge**,不在本 hand-back 内当场改。本批不为其单开 pending。
- **T306 §3 诚实边界**(checkpoint-sha 本地自洽非真 fetch 证明 / operator-attest 人工背书 / assets.json 期望数对账缺 detail 响应):codex 已接受为诚实人工边界,operator 知悉,真 fetch 验收靠 operator attestation,验收完成前 v0.3 不算最终 accepted。**不**在 IDS log 开 pending 追踪(单包决议级,非项目追踪面板)。

**∴ 本批决议 = 收悉入库;§3 携带的 T301 API 上界更正 + T303 第三态预警 → 并入 `/expert-forge 008`(见下条)。** 无 PRD 直接修订 / 无 SHARED-CONTRACT 直接修订 / 无 XenoDev spec 修订触发。

**Follow-up commits**: 本次 review 含一次 frontmatter 修复(6 包机器前缀 `/Users/admin/codes/`→`/home/ys/codes/`)+ HANDBACK-LOG append;git commit 待 operator 确认后产出。

---

## 2026-06-30T09:03:24Z · 008-pB-20260630T084333Z(正式决议 · 承接上方 PENDING stub)

**Reviewed at**: 2026-06-30T09:03:24Z
**Tags**: drift
**Severity**: medium
**Related task**: FU-downstream-purpose

**Validator self-check**(Step 4.2 / 4.3):
- 6 约束自检(consumer mode):**PASS**(all 6 constraints,validate-handback.sh exit 0,绝对路径调用)。本包 producer 已在新机 `/home/ys/codes/` 产,frontmatter 路径前缀正确,无 T301-T306 的换机 stale-path 问题。
- verdict-evidence precheck(Step 4.3):**N/A**(无 `ids_verdict_evidence:` 父键;tag=drift PRD 缺口上报包,非 build-ship verdict 包,正常)。

**Operator decisions**:
- [x] **起 `/expert-forge 008`** —— 本包 §3 显式建议,且 forge 标的累积已达起 forge 阈值(下游用途未定义[根因]+ 信号提取可靠性 spike 需 forge 列为 PRD 工作项[防 V4 静默定产品方向]+ T301 API 上界更正推翻 forge v3 假设 + KG-24/KG-25 框架级缺陷)。
- [x] **PRD 补「下游用途/消费目标」定义 + 信号提取可靠性 spike**(forge 决议后落地路径 = `/scope-inject 008` 或新 PRD 版本)。候选用途 operator 已倾向「机器可信信号/跟单」;若定此 → **先**做信号提取可靠性 spike(小样本 ~100-200 条核 LLM 在反讽+黑话语料的 `stance_direction`/`conviction`/`action_type` 准确率)再判跟单可行性 + 是否需置信度门槛。
- [x] **KG-24 / KG-25 纳入 forge 批审**(框架级数据缺陷,详见 XenoDev `dogfood-backlog.md`):
  - **KG-24**(high):增量守护 `_pending_replays_fn` 只认 manifest `status=downloaded` 不认 `skipped` → 多 token 窗口断点续下时漏 ASR(本次 31/43 被漏,守护只补 12)。
  - **KG-25**(medium):DeepSeek 结构化提取无坏-JSON 容错 → LLM 对特定正文稳定返非法 JSON(未转义控制字符),`json.loads` 一次失败即抛被守护静默吞 → 该条永久缺 summary。
- [ ] 无操作

**Operator note**:
本包性质 = **PRD 缺口上报 + dogfood 回流**(tag=drift),非 spec/PRD 矛盾、非重大架构转向,但携带的根因(下游用途从未定义)+ 可行性空白(信号提取可靠性从无实测)+ forge v3 假设被更正(T301 API 上界)+ 两条框架级缺陷,**累积构成起 forge 的充分理由**。

**为何走 forge 而非直接 /scope-inject 改 PRD**:per CLAUDE.md「重大架构转向 / 框架级问题必须 /expert-forge(防 V4 失败模式)」+ 本包 §3 自身建议「信号提取可靠性 spike 需 forge 先列为 PRD 工作项,避免 build runtime 静默决定产品方向」。下游用途定义 = 产品方向级决策 + 信号 spike = 可行性前置 gate + T301 推翻 forge v3 采集假设,**单纯 /scope-inject 改 PRD 措辞兜不住**,须 forge 内系统重审后再落 PRD。

**结构化字典三层**(`docs/STRUCTURE-DICTIONARY-draft.md` 随包参考,forge 内据用途取舍):
- **第1层无悔**(与用途无关可先落):`entity_type` 填板块黑洞(现在不抓永久丢,真硬)、`tech_side` 三值、黑话词典;`asker` 经红队评审降为「搭便车字段」(依附 entity_type 重提)。
- **第2层赌用途**:据 forge 定的用途**点名挑**(定信号→stance/conviction/action;定情绪指数→sentiment;定财报量化→vs_consensus),不全做。
- **第3层结构关系**:全量重提成嵌套树图**只在**用途确需图谱级查询时才决议(红队驳「可逆不亏」:可逆的是重提,不可逆的是已烧的 LLM 成本)。

**语料约束**(operator 确认,forge 输入):本语料**永远只出自 trader韭团队一家**,不扩展其他作者 → 字典可针对性过拟合该团队文体(右/左侧方言、四桶仓位、黑话谐音、期权打法),作者特异性是 feature 不是 bug。

**非本包范围**(forge 决议后的下一轮,非 IDS 本次动作):实装信号提取 / 跑可靠性 spike / 落地字典无悔层 / 43 回放 ASR(非阻塞,等本机 GPU 空闲;operator 本机 GPU 当前被自有任务占用)。

**∴ 本包决议 = 起 `/expert-forge 008`,在 forge 内系统决议下游用途 + 信号 spike + 字典三层取舍 + KG-24/KG-25 批审;forge 后据结论走 /scope-inject 或新 PRD 版本。**

**Follow-up commits**: HANDBACK-LOG append(本条)+ 上方 T301-T306 批量决议 + 6 包 frontmatter 换机修复;git commit 待 operator 确认后产出。forge 启动后产 `discussion/008/forge/v<N>/` 文档。
