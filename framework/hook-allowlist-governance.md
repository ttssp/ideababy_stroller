# Hook 白名单治理规则 (forge 006 v8 · 簇④ B6 · 2026-07-13)

> **定位**:credential / dangerous-command 等 Safety Floor hook 的**白名单如何组织与回审**的
> 治理纪律。本文档是 **IDS 治理层**产物(白名单**怎么组织**、多久回审);hook 本体的**误报面
> 实装**改动(scan-credentials.sh / pre-commit-credential.sh 具体豁免逻辑)的 SSOT 在 XenoDev
> bootstrap-kit mirror,走**授权条目**下发(见 `discussion/006/forge/v8/AUTHORIZATION-BRIEF-v8.md`),
> 不在本文档内改脚本。
>
> **不动的地位**:Safety Floor 件 1(credential-isolation)/ 件 2(block-dangerous)的
> **non-overridable** 地位不动;fail-closed 姿态不动。本规约动的**只是误报面的组织方式**。

## 1 · 根因(KG-B6 · 为什么需要治理纪律)

credential hook 对三类**合法写法**误报 fail-closed,且与 `parallel-builder` SKILL §6.1
明写的 `mktemp` 私有 dir 范式**直接冲突**——每个 ship 都可能撞:

- **heredoc 类**:commit message / 文档里用 heredoc 写含 `prod://` 样式的示例文本被当真凭据
- **变量拼路径类**:`$SECRETS_DIR/prod` 这类运行时拼接被静态扫误判
- **`$()` 命令替换类**:`$(get-token)` 这类动态求值被当字面凭据

**病灶不是"漏报",是"误报逐例加白"**:现有 `SKIP_PATHS` 是**精确仓根相对路径**列表
(见 `safety-floor-1/pre-commit-credential.sh` L70-82 · 有意不允许 suffix 通配,防误 skip
vendor/lib/AGENTS.md)。这个设计对"跳过特定文件"是对的,但如果**每撞一个新误报点就往
SKIP_PATHS 塞一条精确路径 / 往扫描逻辑塞一个 case**,就重演 **KG-B1**「逐例放宽 regex」的
同构路径病(fork-id charset 每出一种新命名就断一次、逐例补)——**逐例加白 = 教科书级缺
分类治理症状**。

## 2 · 治理不变量(三条)

### 不变量 1 · 按模式类收敛,不按撞一次加一条

新增豁免**必须先归入一个命名的模式类**,不允许直接塞一条无归类的精确路径 / 一次性 case。
当前已识别的模式类(可扩,扩时也必须命名):

| 模式类 | 覆盖的误报形态 | 豁免的正确层次 |
|---|---|---|
| **heredoc-commit-message 类** | commit message / 文档 heredoc 里的凭据样式示例文本 | 扫描逻辑识别 heredoc 上下文,非逐个文件加白 |
| **mktemp 私有 dir 类** | `parallel-builder` §6.1 mktemp scratchpad 路径 | 与 §6.1 协调(见 §3)· 固定路径模式豁免,非逐 ship 加白 |
| **变量拼路径 / `$()` 类** | `$SECRETS_DIR/prod` / `$(get-token)` 动态求值 | 扫描逻辑区分「字面凭据」与「运行时拼接」,非逐变量加白 |

**加白决策树**:撞到新误报 → 它属于上表某个模式类吗?
- **是** → 确认该类的豁免机制已覆盖它(通常无需改白名单,是机制没识别到);若机制确有盲区,
  改的是**该模式类的识别逻辑**(授权条目下发 XenoDev),不是加一条精确路径。
- **否** → 它是**新模式类** → 先在本表**命名并登记这个新类** + 写清它的豁免层次,再实装。
  **禁止**:「先加一条精确路径把 ship 放过去,类以后再说」——这就是逐例加白。

### 不变量 2 · 每条白名单是一条待回审承诺

`SKIP_PATHS` 里每一条精确路径(以及每个模式类的豁免实装)都是**对"这里确实不含真凭据"的
承诺**,承诺会 stale(文件内容会变)。故:

- 每条豁免条目必须带**登记理由**(为什么豁免、属哪个模式类、谁批准、何时批准)。
- 无理由的裸豁免条目 = 回审时默认候选删除。

### 不变量 3 · 定期回审入纪律

- **回审频率**:每次起 `/expert-forge 006`(框架体检)时,**必须**把 hook 白名单全表过一遍
  作为 forge intake 的固定检查项;或 operator 主动触发时。
- **回审动作**:逐条问「这条豁免今天还成立吗?对应文件还在吗?模式类归类还对吗?」——
  不成立的删,归类错的重归类,精确路径能上升为模式类识别的**上升**(减少精确路径条数)。
- **健康度指标**:精确路径条数**只减不增**是健康信号;若某模式类下精确路径持续累加,
  说明该类的识别逻辑有盲区,应改识别逻辑而非继续堆路径。

## 3 · 与 parallel-builder §6.1 的冲突协调(必改其一)

credential hook 误报 `mktemp` 私有 dir,与 `parallel-builder` SKILL §6.1 明写的 mktemp
scratchpad 范式**直接冲突**——SKILL 让你用 mktemp,hook 又拦它。**二者必改其一**
(授权条目下发 XenoDev 择一实装):

- **选项 A**:固定 scratchpad 路径 → SKILL §6.1 改用一个 hook 已知放行的固定路径前缀
  (mktemp 私有 dir 类模式豁免锚定该前缀)。
- **选项 B**:hook 放行 mktemp → scan/pre-commit 识别 `mktemp -d` 产生的路径模式并放行。

选项由 XenoDev 侧按实装代价定,但**决策必须登记**(属"mktemp 私有 dir 类"模式的落地形态)。

## 4 · 落地状态(v8 · 2026-07-13)

- ✅ **本治理规则(IDS 治理层)**:三不变量 + 模式类表 + §6.1 冲突协调框架 · 直接落地。
- ⏳ **scan-credentials.sh / pre-commit-credential.sh 误报面实装**:mirror 件 · SSOT 在
  XenoDev bootstrap-kit · **本轮不当场改** · 授权条目下发(AUTHORIZATION-BRIEF-v8 簇④):
  按三模式类实装豁免识别 + §6.1 冲突择一 + 每条 SKIP_PATHS 补登记理由。
- ⏳ **回审入 forge intake 固定项**:下次 `/expert-forge 006` 起时把白名单全表过一遍。

## 5 · 关联

- 根因缺口:KG-B6(credential hook 误报 fail-closed · XenoDev dogfood-backlog)
- 同构风险先例:KG-B1(fork-id charset 逐例放宽 regex · 见 SHARED-CONTRACT §7.1)
- Safety Floor 件 1/2 定义:SHARED-CONTRACT §2
- 冲突对象:`framework/xenodev-bootstrap-kit/skills/parallel-builder/SKILL.md` §6.1
- forge verdict:`discussion/006/forge/v8/stage-forge-006-v8.md` 簇④
