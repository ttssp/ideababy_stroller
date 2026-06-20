# Forge v2 · 008 · P3R1 · Opus 4.7 Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-06-16T09:30:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

读完双方 P1+P2,这件事的样子已经很清楚,且**双盲下高度收敛**。核心结论三层:

**产品价值层**:把 Obsidian 定为 US8(三形态统一时间线 + 已看/未看)的实现载体——双方都判 `new`,且 SOTA 双向印证(我:SQLite Explorer 的 snapshot embedding;Codex:Readwise/Logseq「采集→本地知识图谱」是成熟形态)。US8 目标 PRD 早已立,缺的只是载体,Obsidian 的 Calendar/Bases/双链/`reviewed` 字段正好落地。这不是新开 scope,是给已有 story 选实现。

**数据流层**:②单向 exporter(SQLite SSOT 不漂,vault 只读衍生)是 binding 底线,双方判 `new` 且站住。Omnivore 云端退场(Codex §1)反证「可重建的人读导出层」比把权威源交给 PKM 工具更稳。三道护栏全部复用 v0.1 既有(`_assert_c5_safe_out_dir` + allowlist + 单向不回写)。

**C5 边界层**:这是 v2 的真焦点。我的 SOTA(iCloud 同步整个 vault 目录、不读 .gitignore)+ Codex 的 SOTA(Readwise full-text export 是成熟产品里的显式开关)**双重坐实**:vault git-ignored 不足以守 C5,原内容进 vault 会被云同步传播出去,且「原文导出」很容易被当便利功能加回来。故 vault 放原文 = `cut`(双方一致,证据加固)。

## 2. 我的初步 verdict(草案)

**我倾向 GO + refactor-C5,不 redesign,且 v0.2 立即可启动 PRD/spec 增量决议(正式 build 前先收口验收边界)**。理由:(1) US8=Obsidian 载体双盲一致 + SOTA 双向印证,产品价值站得住,非过度工程;(2) ②单向 exporter 保住 v0.1 全部护栏,冲击面小,是成熟形态;(3) C5 必须 refactor 已被双方 SOTA 坐实(git-ignore ≠ 不传播),但**改法**要精准。关键不确定点 = **C5 怎么改**(全局扩措辞 vs 局部钉 v0.2 scope),若 R2 收敛不了会拖累 next-PRD 的 C5 草案。

## 3. 关键分歧清单

- **分歧 1**:C5 改法 —— 全局扩措辞 vs 局部钉 + 收窄表述
  - 我的立场:倾向「C5 扩措辞(增补传播渠道原则)+ vault 只放指针摘要」双保险,根因修复更干净。
  - 对方立场(Codex P2,≤15w):"PRD C5 增补传播渠道原则 + v0.2 exporter 明确原文不进 vault"。
  - 我希望 R2 怎么收敛:其实双方已经很近 —— 都要「传播渠道原则」+「exporter 原文不进 vault」。真正待定的是**全局 C5 措辞改动会不会反向误伤 v0.1 已 ship 落点**(PRD Phase-transition 提到落点含云/手机微信)。R2 应明确:C5 增补一句「自用不传播」的渠道中性原则(covers git + 云同步 + 任何传播渠道),但**用「采集落点」与「衍生导出层」分别处置**避免误伤——v0.1 采集落点合规性不变(operator 已负责),新增约束只针对 vault 这类衍生导出层。即:扩原则 + 不溯及既有落点。

- **分歧 2**(非对立,是 Codex 的真增量,我 R1 主动纳入):Dataview JS 脚本边界
  - 我的立场:P2 我只说「选 Bases 而非 Dataview 是 L4 细节」,**低估了**这条。
  - 对方立场(Codex P2,≤15w):"别把任意脚本能力纳入可信路径"(Dataview JS 能写文件/联网)。
  - 我希望 R2 怎么收敛:接受为 verdict 的一条**验收约束**——v0.2 验收只要求 frontmatter 可被 Bases/普通查询消费,**不依赖**能写文件/联网的脚本(Dataview JS)。这与 v0.1「vault 只读衍生」一致:查询层也必须只读,不能从查询插件开出新写路径/旁路。

## 4. 与 K 的对齐性自检

- K 第 1 条「US8 价值能否兑现 vs 过度工程」→ ✅ verdict GO 基于双盲一致 + SOTA 印证;维护成本风险(stale/silent-loss)已落为「exporter 幂等 + drift 可检」验收项,非否决。
- K 第 2 条「数据流护栏守得住」→ ✅ ②单向 exporter 三护栏复用 v0.1 既有;新增 Dataview-JS 只读约束进一步收紧。
- K 第 3 条「C5 边界怎么画」→ ✅(待 R2 精化)分歧 1 给了「扩原则 + 不溯及既有落点 + vault 只放指针摘要」方向。
- K 第 4 条「v0.2 该不该现在启动 + 与 US7 排序」→ ✅ verdict = 现在可启动 PRD/spec 增量决议,exporter 作 US8 bounded scope,**不替代 US7**(双方一致);正式 build 优先级留 next-PRD 摆。
- K binding(C5 法律定性 operator 负责 / SSOT 不漂 / ①③出局 / v0.1 不重审)→ ✅ 全程遵守,P2 无任何法律检索,①③仅作防回潮记录。

无漂离 K 项。R2 重点 = 精化分歧 1 的 C5 措辞 + 把分歧 2 固化为验收约束 + 给 W 三件套草稿建议。
