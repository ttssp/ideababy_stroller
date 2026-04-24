# Idea 001 · L3R1 · Opus 4.7 Max · Scope (no search)

**Timestamp**: 2026-04-23T12:48:20Z
**Inputs read**: L2 report (stage-L2-explore-001.md), L3R0-intake.md, proposals 001, scope-protocol
**Searches used**: NONE in this round
**Visibility**: I did NOT read GPT's L3R1. Verified `discussion/001/L3/` contained only PROTOCOL.md, L3R0-intake.md before writing.

---

## 0. How I read the intake

Human 的 intake 给出了一个**形状清晰但三角冲突**的约束组合：**20h/周 × 先免费 × PI-first 双 persona × Web-first 倾向 × ❓ time + ❓ red lines × ⚠️ Speed+Differentiation+Polish 同时勾选**。我把这个约束组合翻译成三个互相 peer 的候选 —— 每个候选**明确放弃 priorities 三角的其中一角**，诚实地呈现 trade-off。

- **硬约束 honor**：双 persona (PI buyer + senior PhD/postdoc operator)、15-30h/周（以 ~20h 估算）、先免费 + 预留 auth、L2 §6 的 6 条 conditions（data portability / digest-first / hybrid taste / 可剪枝留痕 / buyer+operator 双层 / delegation 假设）全部继承
- **Unknowns 我会给 options**：时间（每个候选带独立估算）、red lines（§5 提 3 条 + 1 条可选第 4 条）
- **Red lines I will honor**：L2 §5 的 8 条 natural limits 作为边界上限；不会提议任何违反"委托 triage ≠ 替代阅读"、"8-15 topic 是护城河"、"不做 graph-first 入口"、"不做公开评分市场"的候选
- **三角冲突的处理**：我**明确拒绝写"三项都满足"的候选**。三个候选各自明确放弃一角 —— A 放弃 Polish、B 放弃 Speed、C 放弃 Differentiation

注意：**三个候选不是"好中差"**。它们服务于**不同类型的 product bet**。human 通过 L3 menu 选哪个候选 fork 进 L4。

---

## 1. Candidate A · "Sharp Digest MVP" （lean Speed + Differentiation，放弃 Polish）

### v0.1 in one paragraph
一个**只做每日 topic-state briefing + 低价值留痕**的极简 Web 工具。8-15 个 topic，每天一份 digest、按"state shift"组织（不是按论文堆叠）；每篇被扫过的论文都有归档痕迹（read / triage / skip-with-breadcrumb / archive）。**不做 taste agent、不做 topology graph view、不做 lab shared view 的多人协作 —— 砍到只剩一个 loop**：每天打开 → 读 briefing → 对每篇标 read/skip/breadcrumb → 系统学习。v0.1 是 PI 自己用的"个人版 lab radar"，operator 作为第二用户能访问同一账户下的数据。**证明"digest-first briefing + 可剪枝留痕"这一条 novelty axis 值不值得花时间**，其他 novelty 留到 v0.2+。

### User persona (sharpened from L2)
**Dr. Chen 类型 PI 为主**（覆盖 8-15 topic、每周要给学生做方向建议、最痛的是"漏看一篇 next week 会被学生问住的文章"）；**Maya 类型 senior PhD/postdoc 作为第二用户共享同一账户数据**。v0.1 不做 invite / 多人协作 —— lab 成员共用 PI 的 login 即可（这是 v0.1 做出的重要 concession）。

### Core user stories (4)
- 作为 PI，我每天早上 8:00 可以打开一个 Web 页，在 10 分钟内看完 8-15 个 topic 的"state briefing"，**确定今天要深入哪 1-2 个 shift**
- 作为 PI，我可以对 briefing 里的每一篇论文做 4 种标注：read now / read later / skip（不留痕）/ breadcrumb（留痕但不读），系统会记住并在下次出现时体现这次标注的影响
- 作为 PI，3 个月后，我可以查"过去 90 天我为哪些 topic 标过 breadcrumb？其中哪些现在被 resurface 了"——形成"过去我标过但可能要重看"的列表
- 作为 senior PhD，我可以用 PI 的登录访问同一 lab 的 radar 数据（不需要独立账户）；briefing 内容对我可用

### Scope IN
- Topic 维护：8-15 topic，PI 手动维护（CRUD 接口），每 topic 一个关键词池 + arXiv category + 可选 seed author 列表
- 每日 briefing（Web page）：digest-first，每 topic 一行 state 摘要 + 至多 3 篇触发论文
- 论文级 4-action 标注（read / later / skip / breadcrumb）
- 低价值留痕：breadcrumb 会有"resurfacing" 逻辑 —— 6 周 / 3 个月 / 6 个月被系统 re-surface，带"为什么现在又回来"的上下文
- 简单 auth：PI 一个账户 + lab 成员可用同一 login（预留"将来能分用户"的 schema，不做多租户 UI）
- Data portability：JSON export、所有数据自有 SQLite/PG 可导出

### Scope OUT (explicit non-goals)
- **Taste agent**（PI 不写 "why I disagree"，没有 hybrid 学习闭环）—— 延后到 v0.2
- **Topology graph / topic 关系图**—— 延后；digest-first 本来就不需要 graph 作为主入口
- **Lab shared view / 多用户 UI / 分权**—— 不做（"一账户一 lab" 是 v0.1 明确简化）
- **Paper 二次分析 / novelty 自动评分 / 跨 paper 对比**—— 延后（v0.1 只做 briefing + 留痕）
- **Mobile / CLI / API**—— Web only
- **PDF 全文解析 / 深度 summary**—— v0.1 仅用 abstract + metadata；full-text 延后
- **Onboarding-focused view**（Carol 场景）—— 降级 v0.2

### Success looks like (observable)
- **PI 连续使用 30 天**（日活 ≥ 25/30）—— digest 不是 newsletter 是 ritual 的证据
- **PI 每月 ≥ 5 次 breadcrumb resurface** 被实际点开 —— "低价值留痕" 的价值被用户自己验证
- **PI 可以说出至少 2 个"没这工具会漏看"的真实案例**（30 天后访谈）
- **Senior PhD/postdoc 至少 2 次/周登入 briefing**—— operator 这一层不会死

### Honest time estimate under ~20h/week
- **~4-5 周到 v0.1**（20h/周 × 4.5 = 90 h）
- 关键工时：arXiv 抓取 + LLM 解读 pipeline (20h)、digest 生成 (15h)、Web UI + auth (25h)、breadcrumb 存储与 resurface 逻辑 (15h)、PI 自用联调 (10h)、缓冲 (5h)
- **Confidence: Medium-High**。unknown 在 "LLM 解读质量调优" 可能消耗超过 20h；如果调优失败，briefing 可能退化成 summary list

### UX principles (tradeoff stances)
- **Speed > Polish**：UI 粗糙可接受（表格 + 纯文本 briefing 就行），快先上
- **Differentiation > Polish**："digest-by-state-shift" 和 "breadcrumb resurface" 这两个核心要做对，其他不花心思
- **PI 优先，operator 第二位**：operator 共享 PI 账户这个 compromise 换 4 周 vs 7 周
- **一个视图解决一件事**：首页就是 digest，没有 sidebar、没有 modal，所有其他功能通过 URL 进入

### Biggest risk
**PI 会把 briefing 当成 newsletter 读一周然后放弃** —— 原因是 v0.1 没有 taste agent、breadcrumb 第一个月还没累积足够信号、topology graph 这个 "wow moment" 也不存在。**风险缓解**：30 天必须手动陪 PI 实际用过 ≥10 次（访谈 + 现场使用）来校准；如果 30 天后 PI 还是只看不标注，证明 "4-action loop" 这个 bet 错了，需要回 L2 重新思考。**这个 risk 是所有候选中最高的**，因为它是最 sharp 的 bet。

---

## 2. Candidate B · "Lab Research Editor v0.1"（lean Differentiation + Polish，放弃 Speed）

### v0.1 in one paragraph
一个**完整的 lab 级外置研究编辑部 MVP**：digest + topology explainer + hybrid taste agent + 多用户 lab view + 低价值留痕 + data portability。砍掉的是"研究生产侧" (post-experiment integration loop) 和大量的 onboarding UX，保留 L2 report 里 "Research editor" 的整个核心回路（发现 → 判断 → 归档 → 留痕 → 回看 → SOTA 更新）。**诚实放弃 Speed** —— 这是 2-3 个月的投入，不是几周的 MVP，但完成后外观和内核都有明显差异化，lab 内外都能被说服使用。

### User persona (sharpened from L2)
**Dr. Chen (PI) + Maya (senior PhD/postdoc) 双视角同时 v0.1 就位**：PI 有"lab 级 view"（所有 topic 的集体 state + operator 活动），operator 有"personal view"（自己负责的 topic + 个人标注 + lab 共识对比）。两个 persona 都可以独立登入、查看、标注。**Carol (onboarding) 仍然降级**，但 topic topology view 天然能支持她自己探索。

### Core user stories (6)
- 作为 PI，我有一个 Web 首页的 digest-first 视图，可以看到 8-15 topic 的本周 state shift（Candidate A 那套）
- 作为 PI 或 operator，我可以为 topic 里每个 "state claim" 写一句 stance ("lab 相信 X"、"lab 怀疑 Y")，形成 topic-level belief ledger
- 作为 operator，我可以在读某篇论文时调出 topology explainer（"这篇和我们 topic 里哪些工作相关？和哪些工作冲突？"），不是主入口但是二级 view
- 作为 PI / operator，我对任何系统标注可以写一句 "why I disagree"，taste agent 把这条记下、影响下次同类论文的标注 (hybrid explicit-implicit loop)
- 作为 operator，我可以标 read / later / skip / breadcrumb（Candidate A 的 4-action），同时可以在 breadcrumb 上加"为什么留痕"的短注
- 作为 lab 成员（任何人），我可以 export 整个 lab 的数据（JSON + markdown），迁移到他处

### Scope IN
- 所有 Candidate A 的内容 (digest + 4-action + breadcrumb + resurface + data export)
- Topology explainer view：topic 内的 "paper—relation—paper" 二级图，supersedes / derives-from / contradicts；**作为 explainer，不作为入口**
- Hybrid taste agent：operator 每次 explicit disagree 都被记录；系统用 implicit (read time / later→read ratio / breadcrumb hit rate) 补充；每周产出 "lab taste drift" 的简报
- Multi-user lab view：PI invite by email（不是 OAuth，只用简单 token），最多 15 用户；每人有独立账号、独立标注，但所有人共享 topic ledger
- Belief ledger：topic 下可以写 stance 和 stance history
- User-level 权限：PI = admin、operator = member、可以分 read-only / write

### Scope OUT
- 不做公开打分 / 社区 review（Paperstars 失败模式 red line）
- 不做 PDF 全文解析（abstract 够用；full-text 延后 v0.2）
- 不做 post-experiment integration loop（lab 自己的实验数据进 topic 图）
- 不做 Carol-focused onboarding UI / guided tour
- 不做 mobile / CLI
- 不做 cross-lab federation
- 不做原 proposal 里的"最终目标 research agent"（这是 2027+ 的事）

### Success looks like (observable)
- v0.1 上线 60 天内：至少 3 支真实 AI lab 同时在用（≥ PI + 2 operator 活跃）
- 每个活跃 lab 的 "taste drift 简报" 达到 PI 读 30 秒能说 "是的这就是我们 lab 这两个月的变化"
- Belief ledger 非空（每 lab ≥ 20 条 stance）
- Breadcrumb resurface 在 operator 这一层也触发点击 (≥ 30% surface 会被点开)
- **Differentiation 可被 3 分钟 demo 说清楚**：lab PI 看了 demo 能说 "我没见过这样的工具"

### Honest time estimate under ~20h/week
- **~10-12 周到 v0.1**（20h × 11 = 220 h）
- 关键工时：Candidate A 全部 (90h) + topology explainer (25h) + taste agent (35h) + multi-user auth + 权限 (30h) + belief ledger (20h) + 3 lab dogfooding 陪跑 (20h) + 缓冲
- **Confidence: Medium**。风险在 taste agent —— hybrid explicit-implicit loop 在 cold start 期如果 PI 写 disagree 频率太低，agent 学不动；这一段工时可能从 35h 膨胀到 70h。建议**里程碑式拆分**（8 周里程碑 = digest + topology + breadcrumb + multi-user 上线；11 周里程碑 = taste agent 可用）

### UX principles
- **Differentiation > Speed**：10 周换一个有明显辨识度的产品
- **Polish > Speed**：UI 要做到 lab 外的 PI 看了会想用的程度（不是华丽，是清晰 + 可靠）
- **一切服从 "研究编辑部" 的叙事**：每个 feature 都对应 "发现 / 判断 / 归档 / 留痕 / 回看 / SOTA" 中的一个；砍掉不在这 6 件事里的功能
- **Hybrid taste 是核心**，不能砍到只剩 implicit

### Biggest risk
**10 周跑完 20h/周 = 一个 quarter 的全部 side-project 精力**。风险不在代码，在 **"10 周之前的任何一次验收都只是半成品"**—— PI 可能在第 6 周拿到 digest + multi-user 但没有 taste agent 的版本觉得"和 newsletter 没区别"而失去耐心。**风险缓解**：第 5 周必须有一次 PI 陪用 checkpoint；如果那时 PI 的反馈不亮，**允许快速 pivot 到 Candidate A 的 scope**（digest + breadcrumb 已完成、砍掉后续）。

---

## 3. Candidate C · "Polished Personal Lab Radar"（lean Speed + Polish，放弃 Differentiation）

### v0.1 in one paragraph
一个**好看、好用、容易上手的个人版研究 radar**：每日 topic briefing + 简洁的 paper 管理界面 + 智能 summary + search + 基础 personal knowledge base。**功能组合和现有工具（Elicit, ResearchRabbit, Undermind）有相当重叠**，但执行得比任何单一工具都细腻：UI 讲究、响应快、多端同步、移动端 PWA 可用。**放弃 differentiation** 意味着不做 "digest-by-state-shift" 和 "breadcrumb resurface" 这两个未经验证的 novelty bet，也不做 lab shared view。**走的是"我做得比现有工具都精致"这条产品主义路线**。

### User persona (sharpened from L2)
**Dr. Chen (PI) 个人用**，**Maya (operator)** 是"同一套工具被 PI 推荐给学生"的次级传播场景（v0.1 不做专门的 operator 视角）。这是**回到"个人工具"假设**的候选，违背 L2 里的 buyer/operator split 但作为一条 sober 的 baseline 值得摆出来。

### Core user stories (4)
- 作为 PI，我可以维护一个 8-15 topic 的关注列表，系统每天为每个 topic 生成一份 digest
- 作为 PI，我可以搜索 / 过滤 / 收藏 / 加 tag 我关注的论文，UI 比 Zotero 更现代
- 作为 PI，我可以对收藏的论文写 notes，系统生成简单 summary + 相似度推荐
- 作为 PI，我可以在 iPad / 手机上用 PWA 版本快速扫 digest + 标注

### Scope IN
- Daily digest（不做 state-shift 组织，做传统 paper-list 组织）
- Paper 管理（搜索 / 过滤 / 标签 / 收藏 / notes）
- 简单 summary 生成（LLM 摘要 + 关键词）
- 相似度推荐（基于 embedding）
- 多端：Web + PWA (iPad / 手机)
- 简单 auth
- 数据导出

### Scope OUT
- 所有 Candidate A 的 state-shift / breadcrumb / resurface（这些都是**Differentiation bet**，放弃）
- 所有 Candidate B 的 lab view / taste agent / belief ledger
- Topology view

### Success looks like (observable)
- 30 天：PI 日活 ≥ 25/30
- PI 收藏 ≥ 100 篇论文，有 ≥ 20 篇有 notes
- PI 愿意把它推荐给学生
- 但**不会有**"没见过这样的工具"的震撼反馈 —— 它是 Better version of Elicit，不是 new thing

### Honest time estimate under ~20h/week
- **~6-7 周到 v0.1**（20h × 6.5 = 130 h）
- 关键工时：arXiv 抓取 + digest 生成 (15h) + UI (40h，因为 polish) + PWA + 多端同步 (25h) + auth (10h) + summary + recommendation (20h) + 数据模型 + export (10h) + 调试打磨 (10h)
- **Confidence: High**。所有组件都是成熟路径，风险在"打磨耗时"而不是 unknown；超时概率低但超时范围小（最多 +2 周）

### UX principles
- **Polish > Speed > Differentiation**：慢 2 周换更打磨，但不冒 Differentiation 的风险
- **保守但可靠**：每个 feature 都在已知 pattern 内
- **PI 是唯一真实用户**：operator 是次级、lab view 不做

### Biggest risk
**它竞争不过一个 well-funded 的现有工具**。Elicit 在 2025-2026 持续迭代（L2R2 验证），ResearchRabbit 被 Litmaps 收购进入整合期 —— 如果你 v0.1 用 6 周追上他们的功能，他们用 12 个月的工程资源可以保持领先。**除非你的执行质量真的能 dominate，否则 Candidate C 会陷入 "功能 parity + 差不多好用"的无人区**。这是所有候选中"失败但不痛"的候选 —— 不会塌但也不会赢。

---

## 4. Options for the human's ❓ items

### ❓ Target delivery 时长
基于上面三个候选，human 在 L3 menu 阶段实际是在选**"时间由 scope 决定后的时长"**：
- **Option 时长-1**：选 Candidate A → 4-5 周 → **~1 个月能拿出原型**
- **Option 时长-2**：选 Candidate C → 6-7 周 → **~1.5 个月能拿出打磨好的工具**
- **Option 时长-3**：选 Candidate B → 10-12 周 → **~1 个 quarter 能拿出差异化产品**

**我的建议**：如果 human 的心理时长是"想看看这能不能 work"，选 Candidate A（可快速 kill / pivot）；如果心理时长是"我要做一个能向外部推的产品"，选 Candidate B（接受 3 个月）；Candidate C 是"保守后备"。

### ❓ Red lines
见 §5 下面。我会提 3 条主 + 1 条可选，human 在 L3 menu 阶段确认。

---

## 5. Red lines I'd propose (basis: L2 §5 + product cultural risks)

### Red line 1 (strongly recommended)： **v0.1 不强吃 long-tail topic**
- **内容**：topic 数量硬上限 20（v0.1 推荐 8-15）。超出会退化成 "扫描" 而不是 "深入"。
- **依据**：L2 §5 明确 "8-15 topic 是护城河"；扩到 50 topic 会让 topology 深度变浅、taste agent 学不动
- **影响候选**：三个候选都会被这条约束

### Red line 2 (strongly recommended)：**v0.1 不替代第一手阅读**
- **内容**：系统的输出永远是 "建议读 / 不读 / 留痕"，不是 "替你读了"；summary 长度硬上限 ≤ 3 句、不给完整 digest；所有 "skip" 决策都有"为什么这么判"的可追溯 link
- **依据**：L2 §5 明确 "终点是让 operator 知道要读什么，不是不读"；否则品味退化
- **影响候选**：对 Candidate B/C 的 LLM summary 生成有硬约束

### Red line 3 (strongly recommended)：**v0.1 不做公开打分 / 社区 review / 公共排行榜**
- **内容**：所有 taste / belief / stance 数据只在 lab 内部，不跨 lab 公开
- **依据**：L2 §5 + L1R2 搜索 ("Paperstars 稀薄 review 密度"、Research Stock Market 的公开计分风险)；lab 信任结构不能被表演场所绑架
- **影响候选**：Candidate B 的 "lab taste drift 简报" 必须严格 lab-scoped

### (Optional) Red line 4：**v0.1 不做 mobile app (iOS/Android native)**
- **内容**：Web + PWA 是 OK 的（Candidate C），但不做 native app
- **依据**：移动端 sprint 会吃掉 20-30% 的工时，与 15-30h/周 不兼容；mobile 价值对 PI 的日常使用而言是 nice-to-have
- **影响候选**：Candidate C 的 PWA 边界清晰化；如果 human reject 这条，Candidate C 会再加 2-3 周

---

## 6. Questions that need real user interviews (L3 can't answer)

即便 human 说 "不需要访谈"，这些问题在 v0.1 之前通过"自用 + 快速 kill"可以被 cheap 地回答，但**它们不会被 L3R1/R2 本身解决**：

1. **L2 report §7 Q1 的实质选择**：PI-first vs operator-first。intake 答 "PI 优先、operator 次选"已经给出方向；但 Candidate A 的 "operator 共享 PI 账户"这种极端压缩是否 survive 真实 lab 的政治和权限需求？—— **只有 30 天自用后 operator 的反馈能答**
2. **Candidate A 的 core bet** "digest-by-state-shift + breadcrumb resurface" 是否真的有 differentiation 价值 —— **只有 30 天后 PI 能不能说出具体 aha 案例能答**
3. **Candidate B 的 core bet** "hybrid taste agent" 在 cold start 期（前 4 周）是否足够 PI 愿意持续写 "why I disagree"—— **只有 4 周实际试用能答**；如果不愿意，整个 taste agent 投入打水漂
4. **数据 portability 承诺的形态**：self-host / export / open format 哪个最能让 lab 信任？—— 这是 L4 细节，但 L3 决策时需要一个初步 stance（建议先做 "JSON export + 自己 host Postgres / SQLite" 最轻量）

---

**Word count**: ~2400 中英混合词等价（约 1350-1450 英文词），在 800-1500 范围内。三个候选**严格 peer**、诚实放弃三角冲突的一角、时间估算独立、risk section 都具体。没有 tech/architecture/stack 细节（只有产品级决策如 "Web-first / PWA OK / 不做 native"）。
