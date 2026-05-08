# Non-goals — 007a-pA

**Version**: 0.2
**Created**: 2026-05-08T13:30:00Z
**Revised**: 2026-05-08T13:55:00Z(R1 fix:加 1.12 Read tool R1 H4 / 加 4.6 -f path 持久化 R1 medium / 加 4.7 friction --reset-state R1 medium)
**Source**: PRD §"Scope OUT" + L2 §5 limits + L3 cross-candidate park 内容 + 工程级追加 + R1 fix follow-up
**用途**:防止 v0.1 scope expansion · 每条都说明"为什么诱人 / 为什么不做 / 何时 revisit"

## 1. PRD-stated non-goals(直接复述,加"何时 revisit")

### 1.1 State machine for adjudication(entry id + status transitions)
- **Tempting because**:形式化的 adjudication 状态(open → acked → resolved)看起来"更工程";entry id 让 tag 与 entry 可追溯绑定不依赖物理位置
- **Why not now**:PRD UX 原则 simplicity > cleverness;operator 已 explicit 同意 markdown tag 即可;state machine 工程量 +3-4h 但不增 trust 价值;C9 不能拼太多时间
- **Revisit when**:operator 在 day-14 trust 答案中明确说"我经常找不到 tag 对应哪条 entry"

### 1.2 Skill placeholder 检测 / 其他 lifecycle hook(C7)
- **Tempting because**:retrospective skill 输出 placeholder 是真实 friction(L2 场景 4),覆盖更全
- **Why not now**:C7 hard;event scope 只 PostToolUseFailure;扩展 hook 注册 + payload schema 学习成本高
- **Revisit when**:v0.2 — `PostToolUse` (success) / `UserPromptSubmit` / `SessionStart` 等 hook 含 placeholder pattern detection。具体由 day-14 verdict 决定优先级

### 1.3 LLM-judge friction signal 判定
- **Tempting because**:LLM 可识别静态规则错过的语义 friction(eg "这个错误信息其实没指明真正问题")
- **Why not now**:静态规则覆盖 80% 真实信号(L2 §6);LLM API 引入 cost/latency/offline 三道工程坎(违 C5 RL-3 offline + C12 stdlib only);LLM 是 disputed 率优化不是 substrate
- **Revisit when**:v0.2 — 若 day-14 verdict = "tighten" 且 disputed 来源是"语义错配"非"白名单太宽"

### 1.4 跨仓 ship(ADP V4 + 其他)
- **Tempting because**:forge 006 路径 2 长期目标包含 ADP V4 dogfood
- **Why not now**:C8 hard;ADP V4 dogfood 4 周等待期不动;hardcoded path D4 是 v0.1 privacy 工具
- **Revisit when**:v0.2 — 4 周等待期结束 + v0.1 day-14 verdict ≠ "pause";跨仓 ship 加 `--scope=v4|v5|adp` flag,设计余地保留(architecture ADR-2)

### 1.5 可配 log 路径
- **Tempting because**:hardcoded 看起来 "不灵活"
- **Why not now**:v0.1 hardcoded 是 privacy promise 工具(D4 / ADR-2);可配引入 default-shared 风险(operator 误配置到 git tracked 公共目录)
- **Revisit when**:v0.2 + 跨仓 ship 同步引入 — 那时 `--scope` flag 比裸路径更受控

### 1.6 Frontend / dashboard / 可视化
- **Tempting because**:metrics 直观展示让 day-14 review 更"专业"
- **Why not now**:C5 RL-4 hard — 不与 enterprise observability(Langfuse / Helicone / Phoenix / Pydantic Logfire / Datadog LLM)正面竞争;markdown 文件 + grep 是 differentiation 不是 limitation
- **Revisit when**:**永不**(这是产品立场,不是工程未尽)。若日后 operator 想要图,自己 grep 后用 `gnuplot` / `qlmanage`,不变成产品功能

### 1.7 团队共享 / multi-reader format / cloud sync / cross-repo aggregation
- **Tempting because**:看起来更"general purpose";吸引更广用户
- **Why not now**:C2 single-operator + C5 RL-3 不接合作上传 + C10 default private;违反 4 条红线之一
- **Revisit when**:v1.0+ 远 vision;且需重新评估 RL-1 / RL-3 是否仍 hold(operator 自决)

### 1.8 自动开 issue / PR / fix
- **Tempting because**:闭环看起来"完整";"agent 报错 → agent 修"是 trending agentic pattern
- **Why not now**:C5 RL-2 hard — 不接追责文化;agent 是 witness 不是 judge(D11);自动 fix 等于 agent 在 operator 不在场时下决定
- **Revisit when**:v1.0+ 且需 operator 显式 opt-in(默认仍 off);agent 是 witness 这一立场不变

### 1.9 完整 2 周 pilot 协议(L3 Candidate B 完整体)
- **Tempting because**:industry-aligned baseline(BugBug / ClawStaff / DigitalApplied)
- **Why not now**:工程量 14-18h + operator self-interview 30-60 min × 2 = 接近 2 周上限;catch-all C9 反向压力;塌方风险高(L3 Candidate B "biggest risk")
- **Revisit when**:v0.2 — 若 v0.1 day-14 hybrid 答案是"想要 evidence-based 决策"而 hybrid 1 题不够。**v0.1 hybrid 1 题就是 B 的 lite hedge**

### 1.10 完整 weekly review ritual(L3 Candidate C 完整体)
- **Tempting because**:解决"file too trustworthy weakly opened"风险更彻底
- **Why not now**:Reflct/Mindsera 类工具有 prompts/summaries/history/pattern surfacing 4 件套,v0.1 1-2 周 budget 只够 1-2 件;scope-reality 警告 thin prompt 是 underbuilt 风险;ritual prompt 调优是隐藏成本
- **Revisit when**:v0.2 — 若 day-14 hybrid 答案明确表达"我 historically 不主动 review,需要 cadence forcing function";那时投资 4 件套 scaffolding

### 1.11 跨 dogfood 周期聚合 / shared immune memory
- **Tempting because**:V4 / V5 / V6 多周期 friction 趋势能给整体改进方向
- **Why not now**:v1.0+ 远 vision;v0.1 单周期都没跑通,谈聚合过早
- **Revisit when**:v1.0+;且需先有跨仓基础(1.4 解决后)

### 1.12 `Read` tool failure 进 v0.1 静态规则白名单(R1 H4 修订)
- **Tempting because**:Read 失败有时是真实 friction(权限错 / 文件不存在 → operator 在调试)
- **Why not now**:R1 H4:超出 PRD §"Open questions" L137 OQ-E 候选范围(候选仅 `Bash / Edit / Write 失败 + Claude Code lifecycle hook block 信号`,**Read 不在内**);Read failure 普遍较 noisy(operator 主动 cat 不存在文件等都触发);PRD 文本未 explicit 拥抱
- **Revisit when**:v0.2 — 在 v0.1 真实 dogfood 数据下评估 Read failure 是否能 H/M/L 合理分类;若真要加,必须给 Read 加 stderr-pattern 强信号过滤(防 noisy)

## 2. L2 §5 自然限制(产品立场,加细节)

### 2.1 不是全知监控(L2 §5)
- **Tempting because**:"agent 多说一点"看起来更聪明
- **Why not now**:agent 是 witness 不是心理医生 / 管理者 / 裁判(D11);electronic monitoring meta-analysis 警告小但显著负面效应
- **Revisit when**:**永不**(产品立场)

### 2.2 不吞掉 human entry(双声部 archive)
- **Tempting because**:agent 自动覆盖率高时人工 entry 显得多余
- **Why not now**:CLI fallback `friction <msg>` 是 right-of-reply,L2 §5 + PRD §"Core user stories" #3 都 explicit 列;subjective 体感 agent 看不到
- **Revisit when**:**永不**(双声部是产品定义)

### 2.3 不记录一切(信号噪声)
- **Tempting because**:全 lifecycle hook 看起来 capture 完整
- **Why not now**:quantified-self 弃用研究"effortless capture is not enough" — 信号噪声比 > capture 成本;C7 + C11 precision > recall
- **Revisit when**:v0.2 — 若 day-14 verdict 是 "miss too much",但优先调 threshold 而非扩 hook 范围

### 2.4 不适合追责文化
- **Tempting because**:量化"问题来源"看起来高效
- **Why not now**:C5 RL-2 hard;single-operator 场景"追责"无对象,但 v1.0 multi-user 时刻起这条 surface
- **Revisit when**:**永不**(产品立场;若 multi-user 转出版本必须 explicit 加 guardrail)

### 2.5 不替代 operator 主观感受
- **Tempting because**:agent 看到全部 stderr 看起来"信息更全"
- **Why not now**:agent 看不到"我心里觉得这流程不对";CLI 是 right-of-reply
- **Revisit when**:**永不**(双声部)

### 2.6 不追求 100% recall / precision
- **Tempting because**:工程师本能想要 metric 都满分
- **Why not now**:false positive 成本 = trust loss,远大于 miss 成本(C11);静态规则边界清晰即够
- **Revisit when**:**永不**(C11 决策已锁)

### 2.7 不与 enterprise observability 平台竞争
- **Tempting because**:技术栈相似(都是 LLM 行为日志)
- **Why not now**:C5 RL-4 hard;single-operator dogfood + friction-as-relational-artifact 是 narrow slice;正面比是输的
- **Revisit when**:**永不**(产品立场)

### 2.8 非 dogfood 模式不应自动 emit
- **Tempting because**:"always-on capture" 看起来更工程
- **Why not now**:L2 §5 末段 — 非 dogfood 模式 agent 自动 emit 没读者,变日志膨胀;D15 default off / opt-in
- **Revisit when**:**永不**(D15 锁;`friction --on` 是 dogfood 起点仪式)

## 3. Hybrid 增量边界(D14)

### 3.1 hybrid self-interview ≠ Candidate B 的 6 题协议
- **Tempting because**:6 题更结构化;industry pilot baseline 更 robust
- **Why not now**:C9 catch-all 反向压力;hybrid 增量 < 1h 工程是 v0.1 通过的关键;6 题在 day-14 那一天压力大易塌方(L3 Candidate B biggest risk)
- **Revisit when**:v0.2 — 若 day-14 hybrid 答案明确表达"想要更 structured evidence",fork v0.2 candidate B

### 3.2 hybrid 1 题不替代 Candidate C 的 weekly cadence
- **Tempting because**:把 hybrid 改成 weekly forcing function 看起来更对症 PROD-1
- **Why not now**:weekly ritual 工程量更高(prompt/summary/pattern scaffolding 4 件套 thin 风险);hybrid 是 day-14 一次性 hedge,不是 weekly cadence 替代
- **Revisit when**:v0.2 candidate C(若 day-14 verdict = "want cadence")

## 4. 工程级 non-goals(spec 阶段追加)

### 4.1 完整安装包 / Homebrew formula
- **Tempting because**:`brew install friction-tap` 看起来更专业
- **Why not now**:C2 single-operator + C12 stdlib only;`bash scripts/install.sh` 已够;Homebrew formula 是 v1.0 公开发布时的事
- **Revisit when**:v1.0(若决定公开 release)

### 4.2 配置 schema 校验框架(jsonschema / pydantic)
- **Tempting because**:state.json 字段类型校验更"安全"
- **Why not now**:C12 stdlib only;state.json 4 个字段,手写 isinstance 校验已够
- **Revisit when**:v0.2 — 若 schema 字段数 > 10

### 4.3 多语言 / i18n
- **Tempting because**:trust report 输出可能想中英双语
- **Why not now**:single-operator(Yashu)双语都行;固定 prompt 文案中英混用即可(D14 prompt 是英文,中文 README)
- **Revisit when**:v1.0 多 user 时

### 4.4 可视化 entry timeline / 图表
- **Tempting because**:day-14 mini-summary 加图看起来直观
- **Why not now**:C5 RL-4 + 1.6 反向;markdown 表格已够 review
- **Revisit when**:**永不**(产品立场)

### 4.5 实时 entry 推送 / desktop notification
- **Tempting because**:operator 即时知道 hook 在工作
- **Why not now**:C2 single-operator + 不打扰 task 心流(L2 §1 核心 use case);默默 capture 是设计

### 4.6 `-f path` 持久化为 default(R1 medium 修订)
- **Tempting because**:operator 跨多 dogfood 周期 / 跨仓时,持久 -f 比每次显式更省事
- **Why not now**:`-f` 仅"explicit one-shot 路径 override",per-call ephemeral,不写入 state.json(D6 + R1 medium 修订);持久化等于绕开 D4 hardcoded path 的 privacy promise(可配路径会让 operator 误配置到 git tracked 公共目录,违 C10);config-driven path 留 v0.2 跨仓 ship 时一起加 `--scope=v4|v5|adp` flag
- **Revisit when**:v0.2 跨仓 ship(C8 4 周等待期结束)同步引入

### 4.7 `friction --reset-state` 一键修复 corrupted state.json(R1 medium 修订)
- **Tempting because**:state.py 抛 StateError 时 operator 不知道修复路径;recovery flag 看起来体贴
- **Why not now**:v0.1 时间预算紧;StateError 是罕见情况(operator 手编辑 state.json 才会触发);v0.1 已通过 README 教 manual `rm ~/.config/friction-tap/state.json` 后 `friction --status` 自动重建默认值
- **Revisit when**:v0.2 — 若 v0.1 dogfood 期间 ≥ 1 次 operator 报告 StateError 困惑,加 `--reset-state` 一键 reset

## 5. summary

| Category | 条数 | 是否永不 revisit |
|---|---|---|
| 1.x PRD scope OUT(R1 H4 加 1.12 Read) | **12** | 部分(1.6 / 1.7 / 1.8 永不;其他可 v0.2 / v1.0+) |
| 2.x L2 自然限制 | 8 | 大多永不(产品立场) |
| 3.x hybrid 边界 | 2 | v0.2 可 revisit |
| 4.x 工程级(R1 medium 加 4.6 -f 持久化 + 4.7 reset-state) | **7** | 4.1 / 4.2 / 4.3 / 4.6 / 4.7 v0.2 / v1.0 可 revisit;4.4 / 4.5 永不 |
| **Total** | **29** | — |

非空 ✓ ;每条带 tempting / why not / revisit 三段。
