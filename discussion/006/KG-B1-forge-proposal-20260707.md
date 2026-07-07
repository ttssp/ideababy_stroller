# KG-B1 修复方案 · 回 IDS forge 输入(fork-id charset 协议)

> **结论先**:IDS `/plan-start` 铸的「带 idea-slug 中段」fork-id(如 `001-radar-pA`)被 XenoDev hand-back
> validator 约束6 的 charset regex 拒 → 该 fork 所有 hand-back 无法回流。修法 = 把约束6 的 `prd_fork_id`
> regex 从 v0.3 扩到 **v0.4**(接中段 slug),**安全零损**(三层独立防御中 regex 只是第一层,真 path-traversal
> 由 1.5 forbidden-char + §2 basename + §3 realpath-containment 兜)。附带修 gen-handback 多-fork stale HANDOFF 坑。
> **spine cross-repo · 高优先**(每个 001 task 都卡同一门)。**本仓不当场改**(check-6/gen-handback 是
> bootstrap-kit mirror · 走 IDS forge · 与 KG-29 同族同批审)。

---

## 1 · 问题本质(cross-repo 协议漂移)

**两仓对 fork-id 形态的假设不一致**:

| 仓 | 对 fork-id 的约定 |
|---|---|
| **IDS**(`/plan-start` 铸造) | `<disc><a-z?>` + 可选 `-<idea-slug>` + 可选 `-p<Variant>` + 可选 `-v<M>.<m>`。**新增了 idea-slug 中段**(如 `001-radar-pA` 的 `radar` · 见 `discussion/001/001-radar/001-radar-pA/`) |
| **XenoDev**(check-6 约束6 regex) | `^[0-9]{3}[a-z]?(-p[A-Z][a-zA-Z]*)?(-v[0-9]+\.[0-9]+)?$`(v0.3)—— **从没预期中段 slug** |

**实测**(即便 009 分支的 v0.3):
```
001-radar-pA  →  ❌ prd_fork_id not matching  ^[0-9]{3}[a-z]?(-p[A-Z][a-zA-Z]*)?(-v[0-9]+\.[0-9]+)?$
```
v0.3(KG-29)只把 `-p` 后缀放宽为多字符(接 `009-pForge`),**没接中段 slug**。本 001 分支 off main,连 v0.3 都没有(main 停在更窄的 v0.2)。

**撞面**:所有 IDS 用「带 idea-slug 中段」命名的 fork · 通用(不止 001-radar-pA)。

## 2 · 修法:约束6 regex v0.3 → v0.4

```bash
# 旧 v0.3:^[0-9]{3}[a-z]?(-p[A-Z][a-zA-Z]*)?(-v[0-9]+\.[0-9]+)?$
# 新 v0.4:^[0-9]{3}[a-z]?(-[a-z0-9]+)*(-p[A-Z][a-zA-Z]*)?(-v[0-9]+\.[0-9]+)?$
#                        ^^^^^^^^^^^^^ 新增:0+ 个「连字符 + 小写字母数字段」= idea-slug 中段
if ! [[ "$PRD_FORK_ID" =~ ^[0-9]{3}[a-z]?(-[a-z0-9]+)*(-p[A-Z][a-zA-Z]*)?(-v[0-9]+\.[0-9]+)?$ ]]; then
```

**改动 = 在 `[a-z]?` 与 `(-p...)` 之间插 `(-[a-z0-9]+)*`**(中段 idea-slug · 可多词如 `-multi-word-slug`)。

## 3 · 安全论证(约束6 的立法本意 = OWASP path-traversal 防御 · 必须证不削弱)

### 3.1 v0.4 的字符集只含 `{0-9, a-z, A-Z, '-', '.'}` · 无 path-traversal 字符
逐段拆:
| 段 | 字符 |
|---|---|
| `[0-9]{3}` | 数字 |
| `[a-z]?` | 小写字母 |
| `(-[a-z0-9]+)*`(新) | **连字符 + 小写字母数字** —— 不引 `/ \ . 控制字符` |
| `(-p[A-Z][a-zA-Z]*)?` | 连字符 + 字母 |
| `(-v[0-9]+\.[0-9]+)?` | 连字符 + 数字 + 点 |

**全字符集无 `/`、`\`、控制字符、绝对路径前缀。**

### 3.2 `..` 结构上不可能
`.` 只在 `-v[0-9]+\.[0-9]+` 出现 —— **点前后强制是数字**,故两点相邻(`..`)无法匹配。实测:`001-v1..2`/`001-v..2`/`001.radar` 全被拒。

### 3.3 关键:regex 只是三层独立防御的第一层(即便全放开也挡真 traversal)
约束6 有 **4 道独立检查**,charset regex(1.2)只是第一道:
| 检查 | 作用 | 本次是否动 |
|---|---|---|
| **1.2 charset regex** | shape 白名单 | ✅ 本次扩(接中段 slug) |
| **1.5 forbidden-char** | 独立查 `/ \ .. 绝对前缀 控制字符`(regex 之外二次挡) | ❌ 不动 |
| **§2 basename** | filename 不含 separator | ❌ 不动 |
| **§3 realpath containment** | 最终路径必 resolve 在 `discussion/<id>/handback` 下(真 traversal 挡) | ❌ 不动 |

**即便把 regex 完全放开,1.5 + §2 + §3 仍挡任何真 path-traversal**(realpath -m 二次归一后必须在 prefix 下)。故扩 shape 白名单 = **零安全损失** —— 这与 KG-29 v0.3 的安全论证同构(v0.3 注释原话:「仅在 -p 段追加 [a-zA-Z]*(不引入 / \ . .. 控制字符),path-traversal 防线(basename + realpath containment)不变」)。

## 4 · 测试向量(forge 审 + 回归用)

### 应接受(真实 IDS fork-id · 全过 v0.4)
```
001-radar-pA           ✅  (本次触发 · 中段 radar)
009-pForge             ✅  (KG-29 · -p 多字符)
008-pB                 ✅  (-p 单字符)
006a-pM  006a-pM-v0.2  ✅  (老形态 · 兼容)
007                    ✅  (裸 3 位)
001-pA                 ✅  (无中段 · 直接 -p)
012-multi-word-slug-pX ✅  (多词中段)
003a-foo-pM-v1.5       ✅  (中段 + -p + -v 全组合)
```

### 必须拒绝(path-traversal / 危险 · 全被 v0.4 拒)
```
001/etc          001..radar        001-radar/../x    ../../../etc   → path-traversal(/ 或 ..)
001-RADAR-pA     001.radar                                         → 大写中段 / 裸点
006a-pM-V0.2     006a-pM-v0        001-radar-pA-v0.2.3             → 版本格式错(大写V/缺minor/三段)
```

### 已知语义松弛(非安全问题 · forge 决是否收紧)
```
009-pforge   001-radar-pa   →  v0.4 接受(-pforge/-pa 被当中段 idea-slug · 非 -p<Uppercase>Variant)
```
**说明**:中段 slug 泛化后,regex 无法区分「合法 idea-slug」与「小写 -p 变体拼错」。这**不是安全问题**(无危险字符 · 三层防御仍挡 traversal),是**命名规范松弛**。取舍:
- 接受松弛(简单 · 拼错的 fork-id 本就不该被 IDS 铸出来 · IDS 侧铸造是 SSOT)· 或
- forge 决定加更强约束(如中段 slug 与 `-p` 变体的分隔用不同规则)—— 但会显著增 regex 复杂度。
**建议**:接受松弛(SSOT 在 IDS 铸造侧 · validator 是 char-safety 门非命名规范门)· 但 forge 拍板。

## 5 · 附带修:gen-handback 多-fork stale HANDOFF 坑(同 KG-B1 记录)

**问题**:`gen-handback.sh` 强读 `$REPO_ROOT/HANDOFF.md` 的 `prd_fork_id`(防绕 SSOT · 不接受 `--feature` override)。但 operator 同时开多 fork(008/009/001)时,仓根 HANDOFF **只能是一个** → 为 fork B 产 hand-back 时静默用 fork A 的 stale id(本次差点把 001 的 hand-back 产成 `008-pB`)。workflow 隐含假设「一时刻一活跃 fork」,多 fork 并行下漏。

**修法建议**(forge 决):
- (a) gen-handback 加 `--handoff <path>` 显式指定 HANDOFF(仍跑 identity 校验 · 不绕 SSOT · 只是不假设根)· 或
- (b) 多-fork workflow 规约明确「切 fork 必先 `cp <fork>/HANDOFF.md` 进根」(文档级 · 但易漏)· 或
- (c) gen-handback 从 `--feature` 反查 `discussion/<id>/<slug>/<fork>/L4/HANDOFF.md`(约定路径 · 免手 cp)。
**推荐 (a)+(c)**:显式 flag 兜 + 约定路径自动找。

### 4.1 现有 validator test-fixtures 回归(v0.4 全对)
对 bootstrap-kit 自带 fixture 的 fork-id 跑 v0.4:
```
008a-pA          ✅ 接受(valid fixture)
999z-pZ          ✅ 接受(valid fixture · 边界:9 开头 + z + -pZ)
008/../../etc    ✅ 拒绝(invalid-6-id-charset fixture · path-traversal 攻击 · 正确拒)
{{PRD_FORK_ID}}  ✅ 拒绝(模板占位符 · 正确拒)
```
→ v0.4 对既有 fixture **零回归**:合法的接受 · 攻击/占位的仍拒。**佐证安全**:即便 regex 扩了,`008/../../etc` 这种真攻击 fixture 仍被 v0.4 的字符集(不含 `/`)+ 1.5 forbidden-char 双挡。

## 6 · 落地路径(bootstrap-kit mirror 同步)

1. IDS forge 审本方案(与 KG-29 同族 · 一并审 fork-id charset 协议全貌 + 命名松弛取舍)。
2. 改 IDS `bootstrap-kit` 的 `check-6-id-charset-and-final-path.sh`(v0.4 regex)+ `gen-handback.sh`(HANDOFF 处理)。
3. 同步回 XenoDev(bootstrap-kit mirror · 本仓 `lib/handback-validator/` 是只读镜像)。
4. XenoDev 补发**已 blocked 的 hand-back**:001-radar-pA T001(rationale 已备 · 见 `specs/001-radar-pA/followup-log.md` FU-T001-handback-deferred + REVIEW-LOG T001 段)+ 后续 T002+。

## 7 · Provenance
- 触发:001-radar-pA T001 ship · §4.1 hand-back producer 阶段(2026-07-07)
- 相关:KG-B1(`dogfood-backlog.md`)· KG-29(009 分支 v0.3 · 同族前修)· `check-6-id-charset-and-final-path.sh` · IDS `/plan-start` fork-id 铸造(SSOT)
- 安全论证同构 KG-29 v0.3 注释(regex 是纵深第一层 · realpath containment 是真 traversal 门)
