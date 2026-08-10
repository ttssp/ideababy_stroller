# X batch snapshot · forge 006 v9(权威快照 · Codex 首选阅读源)

> **Provenance**:
> - Part 1 = IDS `discussion/001/handback/HANDBACK-LOG.md` **第 40 条**(2026-08-03T09:34:19Z)
>   与 **第 42 条**(2026-08-04T00:18:06Z)中的实测证据段,均由 IDS consumer 侧**独立真核**
>   产生(非取 hand-back 包自述)。
> - Part 2 = `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/dogfood-backlog.md`
>   四条原文全文(KG-B11 记于 2026-07-17;XD-41/XD-43 记于 2026-07-31;XD-44 记于 2026-08-04)。
> - Part 3 = 现行机制的**代码/协议现场原文**(XenoDev SKILL + lib · IDS SHARED-CONTRACT
>   + handback-review 命令),含精确行号。
>
> **外部路径 Codex 沙箱可能 BLOCK —— 本快照自足,BLOCK 时以本文件为准。**

---

## Part 0 · 本轮审议主体一句话

四条缺口是**同一失败家族的四个面向**,都关于「评审这件事本身的证据」:

| 面向 | 条目 | 一句话 |
|---|---|---|
| **评审跑过了吗** | XD-43 | 门实装了,但没有任何入口调用它 —— 从未被执行过 |
| **评审结论是什么** | **KG-B11** | 评审记录只产 singleton 不产 immutable;**实测更坏:两者皆无** |
| **评审够不够** | XD-44 | 4 轮上限对状态机式协议设计系统性偏低(5 轮 / 11 轮两实例) |
| **评审没跑时会怎样** | XD-41 | 替代路径放行的代码,gate 一恢复就抓出 21 条(11 high) |

**它们共享一个结构**:每一条都是「机制存在 → 但它的执行/证据/充分性没有机器落点 →
于是缺席被静默当作通过」。**「缺席即豁免」是这个家族的通用形状。**

---

## Part 1 · 实测证据(IDS consumer 侧独立真核 · 2026-08-03 / 08-04 两次)

### 1.1 第一次发现(HANDBACK-LOG 第 40 条 · 2026-08-03)

审 hand-back 包 `001-radar-pA-20260802T162313Z`(spec v0.7 amendment)时,IDS 侧读
**codex 原始 log 而非包的转述**,发现三项:

- **① v0.7 五轮在正规 immutable 存储里一条记录都没有**。XenoDev 的 R-Q7 机制
  (`lib/handback-validator/review-log-writer-lib.sh` 的 `write_review_log_immutable`)规定
  immutable 记录写 `.claude/skills/codex-review/real-review/<scope-slug>-<ts-slug>.md`,
  该目录**被 git 追踪**(非 gitignore)。实查:v0.7 五轮 **零条**。
  (注:`review-log/` 是 **gitignored 草稿区**,不是 immutable 存储。)
- **② singleton latest-pointer 是 stale 的,且指向反向结论**。
  `.claude/skills/codex-review/REVIEW-LOG.md` 停在 **v0.6**:`verdict: approve` ·
  `findings_count: 0` · `ts: 2026-07-26T00:10:51Z`。而现实是 v0.7 `needs-attention` 带 2 条 high。
  ⇒ **任何读 latest-pointer 的下游看到的是「approve、零 finding」,与事实恰好相反。**
  **这比"证据丢失"更危险 —— 丢失是空,stale pointer 是错误的正信号。**
- **③ 这直接解释了 hand-back 的 `ids_verdict_evidence:` 块为何缺席**:forge v4 R-Q6 那 7 个
  协议字段**正是从 REVIEW-LOG 派生**。上游没产记录 ⇒ 下游无块可带。
  ⇒ 三项不是三个独立疏漏,**是同一个根因(R-Q7 未被调用)的三个投影**。
- **④ consumer 侧对此完全无感**:precheck 探父键 `ids_verdict_evidence:`,不存在则**整步跳过、
  不 warn**。⇒ **缺块的包比带坏块的包更容易过闸**(缺席即豁免)。

第 40 条当时把 (a)(b)(c) 三问**路由 `/expert-forge 006` 攒批**。

### 1.2 第二次发现(HANDBACK-LOG 第 42 条 · 2026-08-04)· **原样复发**

审下一个 hand-back 包 `001-radar-pA-20260803T171809Z`(spec v0.8 amendment · codex 跑了
**11 轮**)时,IDS 侧再次独立真核:

- **immutable 存储对 v0.8 十一轮仍零条记录**。`real-review/` 最新文件仍是
  `working-tree-spec-v0.6-o2-low-confidence-exemption--2026-07-26T001051Z.md`
  ⇒ **v0.7 五轮 + v0.8 十一轮 = 16 轮 review,immutable 存储里一条都没有**。
- **latest-pointer 仍停在 v0.6 那条 `approve` / `findings_count: 0`**
  ⇒ **stale 跨度从 5 轮扩到 16 轮**,期间无任何机器信号。
- **raw log 只存 2/11 轮**(`review-log/001-radar-pA-spec-v08/` 仅 round1 / round5),
  且 `review-log/` 命中 `.gitignore:72`,`git ls-files` 该目录 **0 条**。
- **`ids_verdict_evidence:` 父键连续第 2 个包缺席,consumer precheck 连续第 2 次静默跳过。**
- **spec 的自我披露本身也没跟磁盘核对**:`spec.md:100` 称「未逐轮存档为独立文件…仅
  round-9/10/11 保留在会话记录中」,而磁盘上实际存在 round1/round5 两份文件 ——
  **方向相反的不准确**。记为「披露未经真核」的又一实例:**诚实的意图 ≠ 核过的事实**。

⇒ 第 40 条的路由**已下达但零落地**,下一个包**原样复发**。第 42 条据此**升级为阻断级议题**,
升级依据 = **复发计数**,不是新论证:**证明单靠 forge 路由而无 enforcement,该缺陷会稳定复发。**

### 1.3 ⭐ 一项**比 KG-B11 更坏**的精确化(本轮新增 · 请 reviewer 重点核)

KG-B11(2026-07-17)描述的失败模式是:**spec-writer 流只写 singleton、不产 immutable**
(ship-flow 双写 vs spec-writer 单写的**不对称**)。

**但实测显示的是第三态:v0.7/v0.8 连 singleton 都没写。**

判据:
- v0.6(2026-07-26)**双写齐全** —— singleton `REVIEW-LOG.md` 是 v0.6 内容,且
  `real-review/working-tree-spec-v0.6-...--2026-07-26T001051Z.md` immutable 记录存在
  ⇒ v0.6 走的是**完整双写路径**。
- v0.7 / v0.8 **两者皆无** —— singleton 仍是 v0.6 那份(未被覆盖),immutable 也无新记录。

⇒ 若只是 KG-B11 描述的「spec-writer 单写」,singleton 应该**已被 v0.8 覆盖**。它没有。
⇒ **真实故障不是「写得不对称」,是「整个 REVIEW-LOG 写入步骤根本没被执行」。**
⇒ **这意味着按 KG-B11 的建议修(让 spec-writer 也 source 那个 lib)大概率修不好这个 bug**
——因为问题不在「调了哪个写法」,在「压根没调」。**请 reviewer 独立验证这一推断,
不要因它来自 IDS 侧就采信**(判据:`real-review/` 目录 ls + `REVIEW-LOG.md` frontmatter `ts`)。

---

## Part 2 · 四条 dogfood-backlog 原文

### KG-B11 · spec-writer SKILL §3.2.1 写 REVIEW-LOG 只产 singleton 不产 immutable = R-Q7 协议债

- 日期: 2026-07-17T00:50:00Z
- 类型: 框架缺陷(SKILL 不对称 · schema-gap)
- 严重度: medium(不丢数据但丢 **working-tree 可见性** + 老 hand-back `review_log_sha256`
  binding 被下次 review 静默 invalidate · R-Q7 协议债 codex-review SKILL §3.6.4 明列为 anti-pattern)
- 复现场景: XenoDev 落地 forge 001 v2 · spec-writer 落 frozen DAG 结构改跑完 codex review 后,
  按 codex-review SKILL §3.6.2 用 `write_review_log_immutable` lib 写 REVIEW-LOG(产 singleton +
  immutable 双写)· 但发现**上一条 singleton(老 gate.py T004-A1 14 轮 review · 2026-07-13 ·
  由 prior session 走 spec-writer SKILL §3.2.1 写)只有 singleton 无独立 immutable 记录** ——
  本次 lib 覆盖 singleton 时,老 review 的 296 行详细 body 从 working-tree 消失(git 历史仍在 ·
  但 working-tree 丢 + 任何绑该 singleton sha256 的 hand-back binding 被 invalidate)。已从 git
  `227baeb~1` 恢复并保全为 immutable 记录 `real-review/T004-A1-gate-py-14rounds-2026-07-13T060950Z.md`。
- 根因: **spec-writer SKILL §3.2.1(line 137)用裸 `cat > .claude/skills/codex-review/REVIEW-LOG.md <<EOF`
  只覆盖 singleton** · 未调 codex-review SKILL §3.6.2 的 `write_review_log_immutable` lib。
  ship-flow 与 spec-writer-flow **不对称**:前者双写、后者 singleton-only。
- 为什么是框架级: 修好后受益的是**所有走 spec-writer SKILL 产 spec/amendment 并跑 codex review
  的项目** · 是 SKILL 层不对称,不是 001 单项目 bug。
- 关联: `spec-writer/SKILL.md` §3.2.1(line 137 裸 cat 覆盖) · `codex-review/SKILL.md` §3.6.2
  (`write_review_log_immutable` lib 双写范式)+ §3.6.4(R-Q7 anti-pattern 明列) ·
  `lib/handback-validator/review-log-writer-lib.sh`
- 可能的框架侧解法(留 forge 议): ① spec-writer SKILL §3.2.1 改调 `write_review_log_immutable` lib;
  ② 或把「写 REVIEW-LOG 必产 immutable」抽成两 SKILL 共用的单点。
- operator 确认: <留空 · SKILL 层不对称修复归 IDS forge>

> **⚠ v9 补注(见 Part 1.3)**:本条的诊断可能**不足以解释实测现象** —— v0.7/v0.8 连 singleton
> 都没被覆盖,指向「步骤未被调用」而非「调了错的写法」。**forge 须先判定真实故障态,再定修法。**

### XD-41 · 六批「替代路径评审」放行的代码,codex 一恢复就 4 轮抓出 21 条(其中 11 条 high)

- 日期: 2026-07-31 · 类型: 框架缺陷(review gate 的强度差 · 替代路径的可信边界)· 严重度: **high**
- 关联: KG-20(codex 配额墙)· KG-28(沙箱拦死 review gate)· KG-B12(后端强制新模型致 CLI 不可用)
  —— 前三条都记的是「gate 不可用怎么办」,**本条记的是「用了替代路径之后欠了多少债」**

**复现场景**:配额墙期间(2026-07-27 ~ 08-02),8 个 task-unit **连续 6 批**走「独立子代理评审」
替代路径 merge。每批当时都做了红绿日志 / mutation 验牙 / 双子代理评审 / verdict ≠ BLOCK。
配额恢复后补跑 codex,scope 取「最后一个真过 codex 的 commit → HEAD」的**累积区间**,
**4 轮共 21 条 finding,11 条 high**,多条属「产物能说谎」:
- 非 dry-run 路径接受注入的 fake ⇒ briefing 表头照写「全链真跑 · PPV P2 终点产物」;
- 公共 renderer 的来源声明是个默认 False 的布尔 ⇒ **什么都不做**就等于声称真跑;
- journal record 只校验「可读 + 非空」⇒ README 能成为 O5/O7 journal 行;
- 两个仓级 shell 门此前**零测试覆盖**。

**为什么是框架级 —— 两条路径的强度差有结构性成因**:
1. **子代理与被审代码同源同上下文**。它读的是同一批文件、同一套注释,而那些注释正是作者的自述。
   codex 是另一个模型 + 另一条 harness,不继承作者的叙事。
2. **子代理不跨 task-unit 看**。6 批分别评审,而最贵的几条恰恰**跨批次**才看得见。
3. **「verdict ≠ BLOCK」这个判据在替代路径上偏松**。6 批全是 needs-attention 而非 approve,
   按当时规则照样 merge —— **于是 needs-attention 事实上等价于放行。**

**建议(归 IDS forge)**:① 替代路径 merge 的代码必须挂「补审债」标记,gate 恢复后强制补跑,
范围取**累积区间**;② 替代路径下放行判据收紧一档(needs-attention 须**两个独立子代理都无 high**);
③ hand-back schema 加机器可读字段(如 `review_path: codex | fallback`),让 IDS 一眼看出哪些 ship 欠债。

### XD-43 · 「preflight runner 已实装但无任何流程强制调用」

- 日期: 2026-07-31 · 类型: 框架缺陷(gate 接线)· 严重度: **high**
- 关联: XD-42 · **KG-B4**(「机器道 STOP 必须真 wire 成退出码」同型)

**复现场景**:task-preflight 脚本是 IDS `/handback-review 001`(HANDBACK-LOG 第 29 条)要的
机器可读落点:task 起跑前置写进 frontmatter 的 preflight 声明,由该脚本逐条真跑,任一非 0 → hard-block。
本轮把解析器从 fail-open 改到 fail-closed(R1/R2/R3 三轮逐步收紧),但 codex **每一轮都同时指出**:
即使解析器完全正确,**也没有任何入口强制调用它** —— parallel-builder SKILL 的 preflight 清单里
没有这一行。**于是 task 可以直接起、直接 ship,这道门从未被执行过**,它宣称的 hard-block 保证不成立。
脚本自己的头部注释也如实承认了这一点。

**建议(归 IDS forge)**:① parallel-builder preflight 清单加一行:起 task 前必跑该脚本,非 0 即 hard-block;
② **ship 门也要验**:交付时校验存在一条与当前 task/spec **内容绑定**的成功执行记录(task id +
commit + 命令 + 退出码 + 内容摘要),缺失/过期/摘要不符则拒 —— 否则「起跑时跑过」与「ship 的是
同一份内容」之间仍有缝;③ 与 KG-B4 并案:那条讲「gate 必须真 wire」,本条讲「wire 了但没人调用」
—— **是同一条链上前后两段**。

### XD-44 · codex-review SKILL 的「4 轮上限」对状态机式协议设计类改动系统性偏低

- 日期: 2026-08-04 · 类型: 框架缺陷(SKILL 判据校准)· 严重度: medium
- **复现场景**: v0.8 amendment 跑到 **round-11** 才把 verdict 收到「两条 high 已修但未经下一轮
  确认」,过程中 **round 4/5/6/7/9/10/11(共 7 轮)都至少命中一条 `[high]`** —— 不是「前几轮抓大
  问题、后面抓小 typo」的常见收敛曲线,而是持续暴露真实设计缺口:退出码与既有前置错误码撞车(r9)、
  消费点 verifier 定义了却没接线(r9)、接线方案本身循环依赖(r10)、dry-run 产物无法与真产物区分
  (r10)、消费点信任自报字段未做跨字段自洽校验(r11)、验证命令在新协议下会误停(r10/r11 各修一次)
  —— **这是同一个「多状态字段协同设计」任务不断长出新维度,不是同一个 finding 反复被重新表述**。
  `codex-review` SKILL §4.2 明写「round 4+ 仍 needs-attention 需 operator 决策」,但本仓自己的
  v0.7 amendment 就已需破例到 5 轮,v0.8 进一步到 11 轮 —— **「4 轮上限对这一类任务系统性偏低」
  的第 2 个独立实例**,不是一次性异常。
- **建议(归 IDS forge)**:
  1. **区分任务类别再定轮次上限**:两次破例都发生在「一次性定义多个互相依赖的状态字段/协议」
     这类任务上,其搜索空间是**组合式**的(N 个字段两两/多方一致性),轮次需求天然高一个数量级。
     建议按 `risk_level: high` **且**改动涉及「新增枚举/状态机/跨文件字段绑定」时把默认上限提到
     8-10,而不是每次靠 operator 临场「再破一次例」。
  2. **收敛信号应该是「finding 类别是否重复」,不是「轮次计数」**:本轮 7/11 轮命中 high 但没有
     一条是同一 finding 换措辞重报。**重复出现同一类 finding 才是真正该 hard-stop 的信号。**
  3. **v0.7 与 v0.8 是否该合并计数**留给 forge 判断:两次都是同一份 spec 的 amendment 序列,
     只是 `--base` 不同 —— 若属「同一份 spec 的持续演化」,**5+11=16 轮这个总量本身值得被看见**。

> **⚠ v9 数据更正(IDS HANDBACK-LOG 第 42 条 (A))**:XD-44 若引用了 v0.8 的 commit 数,
> 须用 **15**(11 `fix` + 1 `test` + 3 `docs`,`8eda692..HEAD` 实测)。hand-back 包 §1/§2
> 自述的「6 个 commit」**是错的**(形状照抄了 v0.7 那轮的真实 6 commits 未重算)。
> **成本数错 9 个 fix commit ⇒ 会系统性低估「11 轮复核有多贵」,而这正是本条要 forge 判的输入。**

---

## Part 3 · 现行机制现场原文(带行号 · 供 reviewer 直接核)

### 3.1 XenoDev `codex-review/SKILL.md` —— R-Q7 双写范式与 anti-pattern(**机制侧已写对**)

```
:279   # R-Q7 · immutable per-review 记录 + singleton latest-pointer(idea 006 forge v4 · 策略 A 两者并存)
:281   # 动机:老单点 cat > 覆盖会 invalidate 老 hand-back 的 review_log_sha256 binding(R-Q7 协议债)。
:288   RR_FILE=$(write_review_log_immutable \
:314   - ❌ 覆盖已存在的 immutable 记录(`real-review/<scope>-<ts>.md` 一旦写成不可变 · noclobber 守 · R-Q7)
:315   - ❌ 只写 singleton 不产 immutable 记录(老 hand-back 的 review_log_sha256 binding 会被下次 review 覆盖 invalidate · R-Q7 协议债)
:317   > R-Q7 策略 A 两者并存(idea 006 forge v4):singleton latest-pointer 可覆盖;immutable per-review
:317     记录绝不可覆盖。hand-back 的 review_log_path 可绑 singleton(latest)或具体 immutable 记录;
:317     绑 immutable 记录则 sha256 binding 永久稳定。
```

⇒ **协议文本是对的、anti-pattern 是点名了的、lib 是存在的。缺的是「谁保证它被调用」。**

### 3.2 XenoDev `spec-writer/SKILL.md` —— KG-B11 指的裸 cat(**至今未改**)

```
:137   cat > .claude/skills/codex-review/REVIEW-LOG.md <<EOF
```

⇒ 与 3.1 的 `write_review_log_immutable` **不对称**,即 KG-B11 的诊断。
⚠ 但见 Part 1.3:实测现象是「两者皆无」,指向更上游的「步骤未被调用」。

### 3.3 XenoDev `codex-review/SKILL.md` —— 4 轮上限(XD-44 的标的)

```
:339   | Verdict: needs-attention | 不进下游 · 按 finding 改 impl → 重跑(最多 4 轮)|
:421   ### §4.2 4 轮上限(同 spec-writer SKILL §3.2)
:466   5. review needs-attention 后强 ship(不修 finding)→ 拒 · 必回上游改 · 4 轮上限触顶才 hard-stop
:488   | 4 轮 needs-attention | hard-stop · operator 决(同 spec-writer §3.2)|
:547   - 4 轮上限 + fail closed 派生自 spec-writer SKILL §3.2 + parallel-builder round-3 codex F1
```

### 3.4 IDS `framework/SHARED-CONTRACT.md` §6 B-4-IDS —— consumer 校验深度 < producer(**缺席即豁免的协议根**)

```
:911   ### B-4-IDS Verdict evidence consumer contract(v0.2 协议补段 · 2026-05-29)
:918   - IDS consumer 端(/handback-review skill)读 hand-back · 核对 frontmatter ids_verdict_evidence
         与本地 REVIEW-LOG 一致 → ACCEPT;否则 REJECT(防伪造 verdict)
:947   hand-back frontmatter ids_verdict_evidence: 父键(透传契约 · immutable evidence binding)
:949   producer 从 REVIEW-LOG 读 7 字段 · 透传到下一 task hand-back frontmatter。
         **任一字段缺 = consumer REJECT**(防伪造 verdict / stale verdict 流入下一 task)
:984-990  逐条严格相等校验(verdict / findings_count / review_log_path / review_log_sha256 /
           target_file / ts / codex_model)
:993   ⚠️ [known-gap · P0 forge v4 · 2026-05-31] …… review_log_path 是 XenoDev repo-relative ·
         IDS 仓本地不存在该文件 · 字面实装会对每个合法 hand-back REJECT(已一手验证)。
         故 consumer 走 shallow:只校验 7 字段齐全 + verdict enum + findings_count 整数 ·
         不跑可达/rehash。即 **consumer 校验深度 < producer 校验深度**。
```

🔴 **注意 `:949` 与实际行为的落差**:协议明写「**任一字段缺 = consumer REJECT**」。
但实际实装是「**父键整个不存在 ⇒ 整步跳过、不 warn、不 REJECT**」。
⇒ **协议说的是「缺字段要拒」,实装做的是「缺整块就免检」。** 连续 2 个包由此过闸。

### 3.5 IDS `.claude/commands/handback-review.md` Step 4.3 —— precheck 的实际条件(现场)

```bash
# 先探父键(无则跳过本步 · 老 hand-back / 非 build-ship 包无此块属正常)
if grep -q '^ids_verdict_evidence:' "$HANDBACK_DIR/<file>.md"; then
  bash .../validate-verdict-evidence.sh "$HANDBACK_DIR/<file>.md" --mode=consumer
fi
```

⇒ **「无则跳过」的豁免理由写的是「老 hand-back / 非 build-ship 包无此块属正常」。**
这个豁免是**按包的年代/类型**设计的,但实装用的判据是**父键在不在** —— 两者不等价:
一个**声称跑了 11 轮 review 的 2026-08 build-ship 包**同样只要不写这个块就免检。

---

## Part 4 · 给 reviewer 的四个待判问题(不预设答案)

1. **真实故障态判定**(Part 1.3):KG-B11 的「不对称」诊断 vs 实测的「两者皆无」——
   哪个是真的?按哪个修?**若按 KG-B11 修而真因是「未被调用」,会修出一个假的完成感。**
2. **「缺席即豁免」的通用解**:XD-43(门没人调)、KG-B11(记录没人写)、3.5(块没人带)
   是同一形状的三个实例。**存在一个通用机制,还是必须逐点接线?**
   ⚠ 注意 3.4 的 known-gap 说明了为什么不能简单「缺块就 REJECT」——
   老包 / 非 build-ship 包会被误拒。**需要的是「该带而未带」的判据,不是「未带就拒」。**
3. **stale pointer 的检测判据**:latest-pointer 可长期指向早已不是 latest 的 verdict,零机器信号,
   且**指向反向结论比指向空更危险**。判据怎么定才不误报?
4. **轮次上限 vs 收敛信号**(XD-44):固定轮次数 vs「finding 类别是否重复」——
   后者更准但更难机器判定。**在本仓的真实条件下(codex 单向无回路、finding 文本不结构化),
   哪个可落地?** 并请判 5+11 是否该合并计为 16。

---

## Part 5 · 本快照自身的诚实边界

- Part 1 的实测由 **IDS consumer 侧的 AI agent 执行**,未经第三方人工复核。判据均已给出
  (目录 ls / frontmatter ts / git ls-files / .gitignore 行号),**可被独立证伪**。
- Part 2 四条 backlog 原文摘自 **001-radar-pA worktree** 的 `dogfood-backlog.md`(不是 XenoDev
  main checkout —— main 的那份没有 XD-41..44,它们只在 worktree 分支上)。**这本身也是一个
  可能的证据可见性问题,但不在本轮 X 范围内,记此备查。**
- Part 3 行号取自 2026-08-04 的工作树状态,**未来会漂**。
- **本快照不含 KG-B8 / B9 / B10 / B12 / XD-42** —— operator 本轮选「中 · 证据完整性家族」,
  这五条**显式留在批次外**,不是遗漏。
