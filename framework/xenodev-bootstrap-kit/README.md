# XenoDev Bootstrap Kit

> **operator 操作指南** — 如何 bootstrap `/Users/admin/codes/XenoDev` 仓
> **版本**:v0.1(B2.1 落地)
> **依据**:`discussion/006/forge/v2/stage-forge-006-v2.md` §"模块 B" + §"B2 流" M5-M8

## 这是什么

XenoDev 是 ADP-next 的运行时 harness(per forge 006 v2 verdict)。本 kit 是 IDS 仓内的种子文件集合,operator 在 XenoDev session 跑 `bootstrap.sh` 即可一次性 init 完整新仓。

**架构关系**:
- `ideababy_stroller`(IDS)= idea→PRD + 治理仓(SSOT)
- `XenoDev`(本 kit bootstrap 的目标)= L4 build runtime 仓(consume hand-off,produce hand-back)
- `autodev_pipe`(V4)= 历史 build 仓(M2 cutover 后 archive,只 mirror block-dangerous.sh)

## kit 目录结构

```
framework/xenodev-bootstrap-kit/
├── README.md                    # 本文件
├── AGENTS.md                    # XenoDev 顶级 SSOT(参考 IDS 但聚焦 L4)
├── CLAUDE.md                    # XenoDev 项目 constitution
├── README.md.template           # XenoDev 仓 README
├── LICENSE.template             # MIT
├── .gitignore.template          # 通用 + Python + macOS
├── bootstrap.sh                 # operator 跑的 init script
├── safety-floor-1/              # 件 1 凭据隔离(B2.1 Block B 落)
├── safety-floor-2/              # 件 2 不可逆命令 hard block(本 Block A 落,mirror autodev_pipe)
├── safety-floor-3/              # 件 3 备份破坏检测(B2.1 Block C 落)
├── workspace-schema/            # workspace 4 字段 validator(B2.1 Block C 落)
├── eval-event-log/              # Eval 3 类 event 接口(B2.1 Block E 落)
└── handback-validator/          # §6.2.1 6 约束 validator(B2.1 Block F 落)
```

## operator 操作步骤(B2.2 起跑时跑;B2.1 阶段不跑)

```bash
# 1. mkdir XenoDev 仓
mkdir -p /Users/admin/codes/XenoDev
cd /Users/admin/codes/XenoDev

# 2. 跑 bootstrap.sh(自动 git init + cp 全套 + 初始 commit)
bash /Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/bootstrap.sh

# 3. 验证(应输出 5 PASS)
test -f AGENTS.md && echo "PASS · AGENTS.md"
test -f CLAUDE.md && echo "PASS · CLAUDE.md"
test -x .claude/hooks/block-dangerous.sh && echo "PASS · block-dangerous.sh"
test -d lib/handback-validator && echo "PASS · handback-validator"
git log --oneline | head -1 | grep -q 'XenoDev bootstrap' && echo "PASS · initial commit"

# 4. 下一步:起 B2.2 sub-plan(operator 手补 PRD + 跑首个真 PRD ship)
```

## 不在本 kit 范围(per stage doc + B2.1 plan v10 scope OUT)

- ❌ XenoDev 自己的 spec-writer / task-decomposer / parallel-builder skill(由 XenoDev L4 派生,首个真 PRD 起跑时实装)
- ❌ Spec Kit 0.8.7 fork 整 repo(本 kit Block D 仅出评估文档,推荐 adapter 模式;fork 决策延 v0.2 note 1)
- ❌ Eval scoring 算法(本 kit 只产 append-only event log + writer/reader,不算阈值;v0.2 note 2)
- ❌ risk tier verdict / 阈值数字(v0.2 note 3)
- ❌ 跑首个真 PRD(B2.2 sub-plan)
- ❌ XenoDev 复制 forge 机制(forge 永远在 IDS 治理仓)

## 关键 reference

- `framework/SHARED-CONTRACT.md` §6 v2.0 ACTIVE-but-not-battle-tested(协议层 normative)
- `framework/SHARED-CONTRACT.md` §3.1 source_repo_identity(Block F validator 三模式比对依据)
- `discussion/006/forge/v2/stage-forge-006-v2.md`(本 kit 的 verdict source)
- `framework/spec-kit-evaluation.md`(B2.1 Block D 落地后)
- `framework/b2.1-dry-run-validation.md`(B2.1 Block G 落地后,operator 跑 dry-run 的指南)

## 失败回滚

若 bootstrap.sh 跑失败:
1. cd /Users/admin/codes/XenoDev
2. rm -rf .git .claude lib *.md *.template README LICENSE .gitignore  # 谨慎,仅在 XenoDev 空仓
3. 检查 bootstrap.sh 报错 + 报回 IDS

若整个 XenoDev 仓需重建:
1. cd /Users/admin/codes
2. mv XenoDev XenoDev.bak.$(date +%s)  # 不删,移走
3. 重新跑 mkdir + bootstrap.sh
