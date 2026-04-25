# Risk Register · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**格式**：每条风险含 `ID · 类别 · Likelihood (L/M/H) · Impact (L/M/H) · Trigger · Mitigation · Owner`；**所有风险 owner = operator**（C13 solo operator），但每条列"实际感知与响应者"更清晰。

---

## 1. 技术（Technical）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| TECH-1 | **LLM 对 AI 前沿论文的 novelty / state-shift 判断准确率 < 70%**，briefing 退化成"paper list"，O1/O4/O5 全挂 | M | H | T001-v2 spike 在真实端到端数据上 `< 14/20 正确` 或延迟/成本任一 gate fail | **0.4.0 修订**：T001 已从 Phase 0 强制 gate 降格为 Phase 2 validation milestone；**Phase 0/1 默认 fallback heuristic**（`LLM_JUDGE_ENABLED=false` · §4.1 anchor 被 ≥ 2 篇引用即 shift · T013 走 fallback summary 模板 `abstract 头两句 + [⚠️ LLM unavailable]` · `model_name='fallback-heuristic-v1'` 写入 `paper_summaries`）；Phase 2 T001-v2 通过则 operator 手工翻 `LLM_JUDGE_ENABLED=true`；T001-v2 仍 fail 则永久 fallback（系统不依赖 LLM judge 也能跑）。**v0.1 status (2026-04-24)**：首轮 spike 在 GLM5.1 fixture 上 judge_accuracy=14/20 擦边过 accuracy gate，但 p95_summarize=46289ms（超 5000ms gate 9.3×）+ 月度成本 $1838.5（60k calls 外推 placeholder pricing · 超 $50 gate 36.8×）两条硬 gate 失败 → defer 到 Phase 2（详见 `projects/001-pA/spikes/T001-llm-provider-report.md` + DECISIONS-LOG G11） | operator（+ T001-v2 报告给 Codex 审） |
| TECH-2 | **arXiv API 限速 / 维护窗 / 接口变更**，daily worker 长期失败导致 briefing 空窗 | M | M | 连续 ≥ 2 天 `fetch_runs.status != 'ok'` | 3 次 exponential backoff retry · on-boot catchup（≤ 24h 窗口）· 监控 cron 每日检查 `last_success`，2 天未更新发邮件 | operator |
| TECH-3 | **LLM provider 单点故障**（Anthropic / OpenAI outage 或账号被封） | L | H | LLM adapter 连续 ≥ 5 次调用失败 | **Interface 可热切**（ADR-4）：env 里备 `LLM_FALLBACK_PROVIDER`，primary 失败时自动切次 provider；Phase 0 T007 把两家 adapter 都实现 | operator |
| TECH-4 | **Postgres 数据损坏 / 单盘爆盘** | L | H | `pg_dump` 失败 3 天 · 磁盘 > 90% | 每日 `pg_dump` 到外挂盘（见 SLA §1.3）· 每周 `restic`/`rclone` 副本到 operator 的云盘 · 监控磁盘 usage | operator |
| TECH-5 | **State-shift heuristic（§4.1）假阳性泛滥**，briefing 充斥无意义 shift 标记 → PI 放弃阅读 | M | M | PI 连续 ≥ 5 天 self-report "今日 shift 多数无意义" | heuristic 标记 `provisional`；day-7 / day-14 / day-21 review heuristic 参数（增加阈值 / 加白名单 earlier-works 要求） | operator |
| TECH-6 | **Drizzle / Next 15 / Node 22 中出现 breaking change 或 regression** 让 build 塌 | L | M | CI 突然红 | 版本锁精确 pin（tech-stack.md §5）；每月 `pnpm update --interactive` 审视，不做自动升级 | operator |
| TECH-7 | **citation-triggered resurface 噪声过大**（新 paper 引用的老 paper 恰好是用户 breadcrumb，但主题无关） | M | M | O2 指标看似达标但 user 抱怨"resurface 都不相关" | 限制 citation trigger 仅当"新 paper 与 breadcrumb 至少共享 1 个 topic 匹配信号"时触发；context_text 带明确 "topic X" | operator |
| **TECH-8**（R1 新增 · G1 · 2026-04-24 R_final B1 fix 后重写） | **`paper_summaries.summary_sentence_cap` CHECK 新语义（数终结符 1..3）会拒绝无句末标点的 LLM 输出**，极端情况下导致 summary 丢失 | L | M | LLM 返回 `"A single sentence no period"`（无 `.!?。！？`） → CHECK 数 0 终结符 → INSERT 失败 | adapter 的 `truncateTo3Sentences`（`src/lib/llm/utils.ts`）在持久化前**defensive 追加** `。` 给无终结符文本 → DB CHECK 视作 1 句通过；测试矩阵覆盖纯中文 3 句 / 5 句 / 英文混合 / 无终结符 / 空串；若 worker 绕过 adapter 直接 INSERT（非预期路径）遇 CHECK 拒绝时 log `[RED-LINE-2-DB-REJECT]` + skip paper（不阻断整批）；已废弃旧 `regexp_split_to_array` 策略（无法正确处理纯中文无空格） | operator |
| **TECH-9**（R1 新增） | **Operator 为满足 skip_why ≥ 5 chars 而凑字数**（e.g. `nope.xx`）→ why 文本无语义但通过 CHECK | M | L | 周度 self-report 抽查发现 skip.why 平均字数 < 12 或大量 placeholder 模式 | 周度 self-report 强制包含 "本周 skip 列表抽样 ≥ 3 条 + why 文本质量自评"；UI 层**不**做语义检查（误杀成本高）；若 operator 自己都在敷衍 5-char，说明 O4/O5 承诺本身不成立，视为 DOGFOOD-1 的更深层信号 | operator |

## 2. 运营（Operational）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| OPS-1 | **Operator 20h/周无法持续**（工作 / 健康 / 家庭扰动） | **H** | M | 某周实际投入 < 10h 持续 ≥ 2 周 | 每 2 周 checkpoint（在 self-report 中记录实际工时），允许 timeline slip 但 log slip；若 week-10 仍未完成 Phase 1，operator 自问是否降 scope | operator |
| OPS-2 | **Cron 时间漂移 / DST / VPS 重启错过 06:00 窗口** | M | M | `fetch_runs` 上没有当天记录 | systemd timer `OnCalendar=daily 06:00 Asia/Shanghai` · `Persistent=true`（错过后立即跑）· on-boot catchup | operator |
| OPS-3 | **VPS provider 出问题**（被封 / 被盗 / 账单忘付） | L | H | SSH 不通 / provider console 异常 | 每月月初检查账单；`pg_dump` 副本存在 operator 云盘，可 ≤ 4h 换 provider 重建 | operator |
| OPS-4 | **Systemd service 自我毒化**（内存泄漏累积使 Next 进程 OOM） | L | M | `journalctl` 出现 oom-killer 记录 | Node 进程单次请求预期内存占用 < 100MB；加 `MemoryMax=2G` 限制；每周 `systemctl restart pi-briefing-web.service` 预防性重启 | operator |
| OPS-5 | **日志噪声淹没告警**（所有邮件告警被误判为垃圾） | M | L | operator 连续 1 周未查看告警邮箱 | 用专属 operator 邮箱 + 过滤器；告警 subject 前缀 `[pi-briefing ALERT]`；每周 `self-report` 强制 review 告警邮箱 | operator |

## 3. 安全（Security）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| SEC-1 | **JSON export endpoint 包含全部 lab data**，非 admin 盗用 → 全量泄露 | L | H | 401/403 middleware bug · 非 admin 能 GET `/api/export/full` | admin middleware 在路由层 + controller 层双重检查；CI 扫描 export route 必须带 `requireAdmin`；**R1 新增**：每次成功 export 同步 append 到 `export_log` 表（lab_id, seat_id, row_counts, byte_size）；operator 每月自审（compliance.md §7）检查异常 export 模式（频率 / 大小突变 / 未知 seat_id） | operator |
| SEC-2 | **Email invite token 泄露**（token 明文出现在日志） | L | M | 新 seat 被未知账号登入 | token 以 hash 存库 · 明文仅出现在邮件正文 · 24h 有效 + 单次使用 · session log 含 IP / User-Agent | operator |
| SEC-3 | **LLM API key 泄露**（环境变量被 push 到 git / 日志） | L | H | 异常 billing 出现 | key 走 systemd `LoadCredential=` 注入 · `.env*` 在 `.gitignore` 中 · CI 用 `gitleaks` 扫描 | operator |
| SEC-4 | **Seat email 作为 PII 泄露给 LLM**（prompt 中意外包含） | L | L | LLM call log 出现 email | adapter 在传给 LLM 前强制 strip：只传 `{title, abstract}`；adapter 单元测试断言 payload 不含任何邮箱正则匹配 | operator |
| SEC-5 | **Arbitrary file read via export filename**（export 允许指定 path） | L | H | export endpoint 被探测 | export 路由绝对不接受用户指定 filename；只返回内存生成的 JSON；无 filesystem path 参数 | operator |
| SEC-6 | **Dependency supply chain attack**（malicious package 更新） | L | H | `pnpm audit` 红 / 异常外连 | pin 所有 deps；`pnpm audit signatures` 在 CI 前置；版本升级 manual review | operator |
| **SEC-10**（G4 H4 · 2026-04-24 R_final 重写 · 原 GET-based 风险消除 · 替代为 POST CSRF 风险） | **POST `/api/invite/consume` 被跨站 CSRF 触发** · 外部网站可伪造 `<form action="https://<lab-domain>/api/invite/consume">` 诱导已登录 admin 消费 token | L | L | 外部域名诱导 POST；监控 `Origin` header 不匹配但 POST 成功的 `export_log` 异常行 | 1. `SameSite=Lax` session cookie（Chrome/Safari/Firefox 均支持）→ 跨站表单无法带 session cookie · 2. `Origin` header 强制匹配 `env.APP_ORIGIN`（不匹配 → 403 `CSRF_ORIGIN_MISMATCH`）· 3. （v0.2 加固）one-time nonce：前端生成 UUID · cookie 同步 · body 回传一次性验证 · 4. invite URL 使用 URL fragment（`/login#invite=<token>`），token 永不进 server log · 5. **历史**（drift 5 · 2026-04-23 旧 GET 方案已作废）：见 `DECISIONS-LOG.md 2026-04-24 drift 5 amendment` | operator |
| **SEC-11**（2026-04-24 · G10 CVE 登记） | **nodemailer 6.9.16 保留（未升 8.0.4）** · GHSA-rcmh-qjqh-p98v（high DoS）+ GHSA-c7w3-x93f-qmm8（low SMTP injection） | L | M | Phase 3 前 operator 启用 SMTP（`SMTP_HOST` 在 `.env.example` 由空变实） | v0.1 `DECISIONS-LOG` 已决议 invite 不发邮件（`SMTP_HOST` 在 `.env.example` 留空即不启用）；nodemailer 6→8 跨 2 major 有 breaking，升级成本远超"未启用代码"的风险收益。**触发条件**：Phase 3 前若 operator 启用 SMTP，必须先 bump nodemailer 到 ≥8.0.4 并重跑测试。 | operator |

## 4. 商业（Commercial）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| COM-1 | **v0.1 不收钱是明确决策**（C3），但 60 天后若 operator 想商业化，早期决策里是否有不可逆的 lock-in | L | M | operator 60 天后想收费时发现不可能 | 数据模型已留 `seats.role` + `labs` 隔离 · JSON export 保证用户退出成本为零 · auth 预留但无 billing · `OP-Q3` 等待 operator 在 v0.1 ship 时确认免费范围 | operator |
| COM-2 | **V1.0 若要商业化，Anthropic/OpenAI 成本随用户数 × 增长不可控** | M | M | 若 10 个 lab × 10 seat × 15 topic 并行 | v0.1 的 per-topic shared judgment（ADR-3）本身就 cost-aware；v1.0 可在此基础叠 per-lab 价格 | operator（v1.0 时） |
| COM-3 | **60 天 dogfood 因为 persona 单一失败**（O4 下调后仍只是自述证据） | **H** | H | day-30 active seats < 3 · day-60 O1/O2/O5 均未达成 | 详见 DOGFOOD-1；day-60 复盘回 L2，不是 pivot 到 B | operator |
| COM-4 | **Elicit / ResearchRabbit / Undermind 在 60 天内出直接对位 feature**，"为啥用这个不用 Elicit" 被问住 | L | M | 竞品发布同类 state-shift / breadcrumb 功能 | 红线 1 守 8–15 topic 护城河；红线 3 守 lab-private；这两条差异化在 60 天内不可能被竞品抄 | operator |

## 5. 合规 / 法律（Compliance / Legal）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| LEG-1 | **中国 PDPA / 欧盟 GDPR 风险**（v0.1 数据全在 operator 机器，似无 controller-processor 关系，但 lab 成员的 reading behavior 是 PII） | L | M | Lab 成员询问"我的数据如何被使用" | `compliance.md` §"Data locality & operator statement" 一页 markdown 明确数据去向 · JSON export 满足 portability 权利 · 无第三方 analytics | operator |
| LEG-2 | **arXiv 使用条款违反**（API 调用过快 / metadata 再分发） | L | L | arXiv 封 IP | 遵循 arXiv API rate limit（≤ 1 req/3s）· metadata 仅内部展示不公开发布（OUT-8 红线 3 已守） | operator |
| LEG-3 | **LLM provider ToS 变更**（例如 Anthropic 关闭 API 或限制 research 用途） | L | M | Provider 发公告 | Interface 抽象保证 hot-swap；OpenAI 作为备；v0.2 考虑 local LLM | operator |

## 6. Dogfood / 验证循环（Product validation）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| **DOGFOOD-1** | **v0.1 验证循环 degenerate 为"operator 自用"**（C10 · 无外部 lab 参与）· 无法从 2 名 lab 成员上获得真实 dogfood 信号 · O4（"≥ 2 个漏看案例"）**已降级**为周度自陈 + 截图（L4 intake Q6）· 若 2 名 lab-internal operator 不愿持续参与则进一步塌缩 | **H** | H | **Sentinel**：day-30 `active_seats_30d < 3` → `/today` 顶部显示 escalate banner，阻塞新 feature 开发 · day-60 `active_seats_30d < 2` → 必须回 L2 重新 scope；**R1 新增**：sentinel 读 `labs.first_day_at`（T003 R1 前置）计算 since_day；读 `labs.allow_continue_until` 判断 operator 是否已签到（7 天窗口） | 1. Day-0 前 operator 书面确认 ≥ 2 名 lab-internal 同意参与 60 天 dogfood · 2. Sentinel 自动监控 active seat · 3. O4 下调为周度 self-report + 截图 · 4. 每周 self-report 强制包含"本周 active seat 情况"自填项 · 5. 若只剩 operator 自用，O1/O2 仍可观察（个人 ritual），但 O3 不可能，视为 kill | operator |
| **DOGFOOD-2** | **Operator 自己读 briefing 但从不 4-action**（只消费 briefing 不留痕）→ breadcrumb 表为空 → O2/O5 不可能达成 | M | H | week-2 结束 `actions` 表中 `read_now` + `breadcrumb` 行数 < 10 | `/today` 顶部显示"本周尚未对 N 篇 paper 做 action"软提示 · self-report 模板强制填"本周 breadcrumb 次数" · week-4 仍低 → operator sign-off 继续或 kill | operator |
| DOGFOOD-3 | **Operator 的 "why I disagree" 字段从未被填**（OUT-1 已决定不闭环）→ 未来 v0.2 taste agent 缺 seed | L | L | 60 天累计 disagree < 5 条 | v0.1 不关心；仅作为 v0.2 前置信号，不影响 v0.1 验证 | operator |

## 7. 人员 / 业务连续性（Personnel · Bus-factor）

| ID | 风险 | L | I | Trigger | Mitigation | Owner |
|---|---|---|---|---|---|---|
| **BUS-1** | **Solo operator 单点失能 > 7 天**（病假 / 出差 / 家庭事件 / 失联） | M | H | operator 连续 7 天未登入 / 未 check 告警邮箱 | 1. systemd timer + on-boot catchup 让 briefing 在 operator 缺席时仍每日跑 · 2. `pg_dump` 每日落地 + 云盘副本，数据不依赖 operator · 3. 无自动用户 outreach，operator 缺席期间 lab 成员仅无新 feature 推送 · 4. Operator 回来后读 `fetch_runs` + `llm_calls` 审计过去 N 天服务情况 · 5. v0.1 **不**设继任者（C13 明确单人），失联 > 14 天则接受服务暂停 | operator（且没有替代人） |
| BUS-2 | **Operator 本地开发机损坏 · 源码丢失** | L | H | 本地 git working dir 无法恢复 | 源码 push 到 GitHub private repo（不包含 `.env*`）· v0.1 每次 commit 以 Conventional Commits 格式落 git log，出事后可在新机 clone 继续 | operator |
| BUS-3 | **Operator 的邀请机制单点**（只有 operator 知道 invite token 生成路径） | L | L | operator 失联 · 无人能邀请新 seat | 默认无需解决 —— v0.1 只 ≤ 3 seat 不需新增；invite 逻辑写在 `runbook.md`（T031 预留）供任何接手者读 | operator |

---

## 风险响应总览

**必须在 Phase 0 完成前 mitigate**：TECH-1（T001 spike）· DOGFOOD-1（pre-commit 2 名 lab 参与 + sentinel 实现）· BUS-2（源码 GitHub push）

**在每两周 checkpoint 审视**：OPS-1（operator 时间）· DOGFOOD-2（4-action 频率）· COM-3（60 天验证可能性）

**v0.1 刻意不处理**：LEG-1 的完整 GDPR 合规、COM-2 的商业化可扩展、BUS-1 的继任者 —— 这些都是 v1.0 问题，提前做会违反 100h 预算

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · TECH/OPS/SEC/COM/LEG/DOGFOOD/BUS 全类齐 · DOGFOOD-1 和 BUS-1 为强制 |
| 2026-04-23 | 0.2 | R1 adversarial fix：TECH-1 mitigation 补 heuristic fallback 写 paper_summaries；+TECH-8（paper_summaries CHECK 误判）；+TECH-9（operator 凑 skip_why 字数）；SEC-1 mitigation 加 export_log 审计；DOGFOOD-1 sentinel 读 labs.first_day_at/allow_continue_until |
| 2026-04-23 | 0.2.1 | drift 5 · +SEC-10（R1 H6 accepted risk · GET-based invite consume · v0.2 升级 POST）· spec.md v0.2.2 同批 |
| 2026-04-24 | 0.3 | R_final BLOCK fix（G1/G4）· TECH-8 replaced（旧"split CHECK 误判中文"→ 新"count-terminator CHECK 拒绝无终结符文本"，adapter defensive 追加 `。` 兜底）· SEC-10 updated（invite 流从 GET-based 升级为 POST-based `/api/invite/consume` + body token · 原 Caddy `delete query` 缓解失效 · 新缓解用 CSRF + SameSite=Lax + Origin + 一次性 nonce） |
| 2026-04-24 | 0.3.1 | G10 CVE bump 登记 · +SEC-11（nodemailer 6.9.16 保留理由 · v0.1 SMTP 不启用 · Phase 3 前升级触发条件） |
| 2026-04-24 | 0.4.0 | TECH-1 mitigation 改写 · T001 从 Phase 0 强制 gate 降格为 Phase 2 validation · Phase 0/1 默认 fallback heuristic（`LLM_JUDGE_ENABLED=false`）· 加 v0.1 status 行（GLM5.1 首轮 spike 14/20 擦边过 accuracy gate · 但延迟 + 成本两硬 gate fail · 详见 spec.md 0.4.0 changelog 与 DECISIONS-LOG G11） |
