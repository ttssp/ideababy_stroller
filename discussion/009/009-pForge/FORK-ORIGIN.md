# Fork origin

**This fork**: `009-pForge`
**Forked from**: `009` · **forge stage v1 + v2**(非 L3 candidate)
**Source stage docs**:
- `discussion/009/forge/v1/stage-forge-009-v1.md`(verdict + PRD draft 骨架)
- `discussion/009/forge/v2/stage-forge-009-v2.md`(七环节目标态蓝图 + Strangler Fig 分期)
- `discussion/009/ACCEPTED.md`(operator [C] 局部接受固化)
- `discussion/009/M1-price-data-source-research.md`(数据源选型 + M1 表 DDL)

## 这个 fork 是什么

009 是**集合体 idea**(008 采集 + 回测验证 + 004 纪律 + 四条新想法:验证分析师 alpha / 回测 /
时序异质图谱 / 蒸馏技能)。它没走标准 L1→L2→L3,而是 **forge-first**(见
`discussion/009/FORGE-ORIGIN.md`):直接起 forge 双轮审阅收敛。

- **forge v1**(2026-06-30→07-01)答"该不该建 / 怎么建":verdict = 009 = **闭环集成契约规范 +
  共享回测地基(非独立统一壳)**,回测 new-first 按 DSR/PBO 建,图谱 defer,蒸馏末位独立 lane,
  004 端永不权威综合分。
- **forge v2**(2026-07-01)答"最终形态长啥样 / 怎么分期走到那":verdict = **七环节契约化闭环图**
  (不推翻 v1),唯一关键新器官 = **PIT 价格历史层**,Strangler Fig 分期
  M1 数据层→M2 alpha 头→M3 calibration+回流→M4 gated 图谱/蒸馏。

**本 fork = 进 L4 落地 Strangler Fig 前两期(M1 + M2)。**

## Scope 决策(operator 2026-07-01)

- **[C] 局部接受** forge v1+v2 verdict(证据最硬、0 争议部分)。
- **第一个 HANDOFF 放 M1 + M2**(PIT 价格数据层 + alpha 头)。
  - ⚠ **注**:两份 forge stage doc + `ACCEPTED.md` 均推荐**只放 M1**(严守"每期独立可用")。
    operator 明知偏离保守建议、选 M1+M2 一起交 —— 好处 = 一次出"分析师行不行"的第一个价值锚;
    代价 = HANDOFF 更重、M1 数据层未实测就压 M2。已告知并按 M1+M2 落地。
- **PRD-form = phased**,`Phases: [M1, M2]`(SLA/风险按 milestone 分段;不改变建出的代码,
  只让 M1→M2 依赖分段写清楚)。
- **M3 calibration 头 / 统一壳 / 图谱 / 蒸馏全部 defer 到本 fork 之外**(Scope OUT 硬边界)。

## forked-from 血缘说明(与常规 fork 的区别)

常规 fork 是 `/fork <root> from-L3 candidate-X as <id>`(从 L3 scope 菜单选候选)。
**本 fork 无 L3 阶段** —— parent 是 forge stage(v1+v2),不是 L3 candidate。
`/fork-from-forge` 命令尚未落地,故本 fork 按两份 stage doc 的 Decision menu [A] **手工创建**:
PRD.md 骨架 = v1 stage doc §"Next-version PRD draft",叠加 v2 蓝图 M1 契约 + M1 调研表设计。

## 现实缺口(forge 自批判 · L4/build 要盯)

1. **免费源退市覆盖是最大风险**:每个源实测,别信文档(M1 缺口)。
2. **分析师历史样本量可能不足以让 DSR 显著** → M2 可能判不出 alpha,是闭环第一个价值锚,先验证(M2 缺口)。
3. **"beat 80-90% 同行"缺 baseline 样本池**:M2 v0.1 可能只能给 vs 大盘的绝对超额。
4. **港股缺口**:免费源普遍差,港股是重点才评估 EODHD,否则暂缓。
5. **双模型回声室**:v1+v2 是两个 AI 高度收敛的产物,非真实回测数据,可能共享盲点。

## 进入下一层的命令

```
/plan-start 009-pForge
```
→ 产 `discussion/009/009-pForge/L4/HANDOFF.md` → 新开 XenoDev session 真开发。

**⚠ XenoDev 本机路径 = `/home/ys/codes/XenoDev`**(linux;`/plan-start` 模板硬编码的
`/Users/admin/codes/XenoDev` 是陈旧 mac 路径,HANDOFF 已填对真实路径)。

**Forked at**: 2026-07-01T09:04:55Z
**Forked by**: human operator(经 Claude,手工执行 —— `/fork-from-forge` 未落地)

## Related

- `discussion/009/FORGE-ORIGIN.md` — 009 目录 forge-first 启动说明
- `discussion/009/forge/v1/` + `v2/` — 双轮 forge 全套产物(8 份 round + stage doc 各一)
- `framework/SHARED-CONTRACT.md` §6 v2.0 — 两仓分工 / hand-off schema / hand-back 通道
