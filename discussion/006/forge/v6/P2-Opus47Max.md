# Forge v6 · P2 · Opus 4.8 Max（参照系评估 · SOTA 对标）

**Phase**: 2（读双方 P1 + 跑 SOTA 搜索 · 用外部锚校准修法方向）
**Reviewer**: Opus 4.8 Max
**Searches run**: 5（12-factor config / git rev-parse repo-root / 版本 pin-vs-glob / uv reproducible env + mirror / hardcode grep-gate CI）
**Read**: `P1-Opus47Max.md`（自己）+ `P1-GPT55xHigh.md`（对方,P2 才读)

---

## §1 · SOTA 对标（表格）

> 每行:一条 SOTA 惯例 → 对本轮哪条 KG 修法给出**有外部依据的方向**（K 要求"修法有外部锚不自创"）。

| # | SOTA 惯例（来源） | 命中的 KG | 对修法的锚定 |
|---|---|---|---|
| 1 | **12-factor §III · config 存环境变量,不存 code**："storing config as constants in code is a violation;config varies across deploys, code does not"（12factor.net/config）。env var 是 **language- & OS-agnostic standard** | KG-26/27 | 硬编码的 mac 路径/版本本质是"把 config 当 constant 塞进 code"。SOTA 明确:**跨机器变化的量 = config = 该出环境或运行期推断,不进模板字面**。这直接支持 P1 判断 |
| 2 | **git rev-parse --show-toplevel 运行期解析仓根**："no matter where you roam, rev-parse --show-toplevel always knows your root;more portable than hardcoding"（git-tower / opensource.com） | KG-26 + X#5 gen-handback | IDS `plan-start` 产 HANDOFF 时,`source_repo`/`build_repo` 该 **运行期 `git rev-parse --show-toplevel` / `realpath` 推断**,不写字面量。gen-handback 的 `to_source_repo`/`workspace.*` 同理。**这是"生成时推断"路线的 SOTA 背书** |
| 3 | **版本:manifest 用 range/glob + lockfile 定,不硬编码 exact 版本号散各处**："hardcoding version numbers everywhere → stale pins;consensus = ranges + lockfile"（vulert / poetry#3747） | KG-27（`1.0.3`） | codex 版本**绝不散写 `1.0.3`**。SOTA = 单一解析点(glob `codex/*/scripts` + `sort -V | tail -1`)。**且 spec-writer 已用此范式** → 推广它,不发明 |
| 4 | **uv:mirror 走 `UV_DEFAULT_INDEX` 环境变量,不进 lockfile;CI 用 `--frozen` 装 as-is** "uv.lock records mirror index config, not ideal for CI/collaborators;UV_DEFAULT_INDEX supports fallback;`uv sync --frozen` never checks pyproject"（astral-sh/uv#9053 #6349 / pydevtools） | KG-28 | **重大发现:backlog 说的"去 --locked"是次优。SOTA 更干净**:mirror 走 `UV_DEFAULT_INDEX` 环境变量(不污染 lock)+ yanked-dep 用 `--frozen`(装 lock as-is 不校 pyproject)。env preflight 该**探 uv/venv/index 可达 + 导出 UV_DEFAULT_INDEX**,而非改 lock |
| 5 | **防漂移:grep/ast-grep/semgrep 做 CI lint gate 拦硬编码**"custom rules detect hardcoded paths;grep-based guard as required status check;lightweight grep-like syntax"（ast-grep / semgrep / autonoma） | 防再漂移（P1 §3③ · Opus 判"最有价值新增"） | **grep-gate 有 SOTA 背书 + 便宜**。一个 `check-no-hardcoded-env.sh`(扫 `/Users/admin`、扫散写版本号)作 pre-commit / 手动 gate。SOTA 支持"轻量 grep 即可",不必上重 CI(契合 K binding④双机非发行) |

---

## §2 · 用户外部材料消化

K 无额外 URL/文件（X 的 5 槽 = 全部一手材料）。但 P1→P2 之间 **Codex 侧 P1 补了一手实证**,须消化:

- **Codex 独立跑了 KG-29 对抗样例**:`009-pForge` PASS / `006a-pM-v0.2` PASS / **`009-pv0.2` FAIL** / `008/../../etc` 四层全拒。这**正面回答了我 P1 §3① 的不确定**(我担心 `-p`/`-v` 段解析歧义 → `009-pv0.2` 会不会 false-pass)。答案:**不会**,`009-pv0.2` 被正确拒（`-p` 段要求首字符 `[A-Z]`,`v0.2` 的 `v` 是小写 → 不匹配 `-p[A-Z]`,整串 FAIL）。→ **KG-29 追认的安全性,现在有双方独立实证,不再是"只信 Opus 说防线没动"。**
- **Codex 抓到一个我漏的 X#5 细节**:gen-handback **有 `IDS_ROOT` fallback**,但 **template 的 `to_source_repo`/`workspace.source_repo` 仍是 mac 字面量**。即 gen-handback 逻辑层已部分可移植,病灶在它引的 **template 文件**。→ 修 X#5 要精确到 template,不是整个 gen-handback 逻辑。

---

## §3 · 修正后的视角（P1 哪些站住 / 哪些被 SOTA 推翻或深化）

**站住的（SOTA 加固）**:
- ✅ "5 条同根 = 环境形态硬编码成默认" → 被 12-factor §III 直接命名（config-as-constant 反模式）。**双方 P1 + SOTA 三方同判**。
- ✅ "KG-27 正确范式同仓已存在(spec-writer glob),推广即可" → SOTA #3 背书 glob+lockfile 路线。**几乎机械修**。
- ✅ "防再漂移守卫是最有价值新增" → SOTA #5 背书 grep-gate 且判它便宜。**双方 P1 都没把它列进 5 条 KG（它是 KG 之外的元问题）,但我 P1 §2 提了、SOTA 撑了 → 应进 verdict 作"新增"**。
- ✅ KG-29 keep（追认）→ 双方独立实证安全。

**被 SOTA 深化/修正的**:
- 🔧 **KG-28 修法方向变了**。P1 我含糊说"加 env preflight",backlog 说"去 --locked"。SOTA #4 给了**更干净的解**:mirror 走 `UV_DEFAULT_INDEX` **环境变量**(不污染 lockfile —— 这恰恰又是 12-factor:index 是 config,该出环境)+ yanked-dep 用 `--frozen`(而非去 --locked,后者会让 CI 能重写 lock)。→ **KG-28 不只是"加检查",是"把 index config 从 lock 挪到环境变量" + preflight 探可达性**。这比 backlog 的处置更对。
- 🔧 **"环境假设住哪层"这个核心岔口,SOTA 给了分层答案（不是单选）**:
  - **路径** → 运行期推断（SOTA #2 `git rev-parse`/`realpath`）——不进模板字面。
  - **版本** → 单一解析点 glob+sort（SOTA #3）——不散写。
  - **index/env config** → 环境变量（SOTA #1/#4 `UV_DEFAULT_INDEX`）——不进 lock/code。
  - **防漂移** → grep-gate（SOTA #5）。
  - → 即我 P1 §3② 倾向的"混合"**被 SOTA 证成**:三类硬编码性质不同,分别用推断/glob/env,不硬套一种。**这应是 verdict 的骨架。**

**残留待 P3 收敛（给双方定论）**:
1. **SSOT 半同步窗口**（KG-29 现状 + shared-lib-drift）:修法两仓落地顺序 + 能否消除"IDS 先落 XenoDev 后补"的窗口。SOTA 未直接覆盖(这是本项目双仓 mirror 特有),需 P3 从工程纪律角度定。
2. **KG-30 log 是否必须随 commit**（双方 P1 §3 都列为不确定）:落仓根绝对路径 vs verifier 降级为"留证即可"。SOTA #2 支持"路径运行期解析"（log 落点用 `rev-parse --show-toplevel` 锚仓根）—— 但"必须随 commit"这条纪律要不要保,需 P3 定。
3. **grep-gate 放哪 + 会不会自己成为下一个机器假设**（Opus P1 §3③ 未决）:IDS/XenoDev/两边;`check-no-hardcoded-env.sh` 自己用 `rev-parse` 定位就不会重蹈。P3 定归属。

---

**P2 自评**:5 搜索全落地到具体 KG,无泛泛而谈。**最大增量 = KG-28 的 `UV_DEFAULT_INDEX`+`--frozen` 比 backlog 处置更干净（SOTA #4），且"环境假设分层住"(路径→推断/版本→glob/env→环境变量/防漂移→grep-gate)被 SOTA 证成为 verdict 骨架**。双方 P1 高度收敛(5/5 评分一致 + §3 near-identical),SOTA 未推翻任何一条,只深化 KG-28 + 证成分层修法。P3R1 预计只需定 3 条残留(半同步窗口 / log 随commit / grep-gate 归属)。字数约 1350。
