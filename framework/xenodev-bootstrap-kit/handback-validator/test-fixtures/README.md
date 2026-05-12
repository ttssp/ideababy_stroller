# handback-validator test-fixtures

per `framework/SHARED-CONTRACT.md` §6.2.1,本目录是 hand-back validator 自测语料 · 模拟真实 dir 结构 `discussion/<X>/handback/<file>.md`(B 件 2.3 重构 · 2026-05-12)。

## 重构动机(plan v0.2-global 件 2.3 · F5)

旧结构:`test-fixtures/<category>/<file>.md`(平铺 · 不含 `discussion/<X>/handback/` 段)
- check-5 path discussion_id 提取要求路径含 `discussion/<X>/handback/` 段(regex `^(.*/)?discussion/([^/]+)/handback/.*`)
- 旧路径 fixture 跑 valid 时 check-5 path 段 FAIL · invalid-5/6 也撞 check-5 path FAIL · **真因被掩盖**

新结构(本次重构):`test-fixtures/<category>/discussion/008/handback/<file>.md`
- valid fixture exit 0 PASS(6 约束全过)
- invalid 各自撞**真因 FAIL**(check-1 / check-3 / check-5 真因)

Evidence:`discussion/006/b2-2/B2-2-RETROSPECTIVE.md` §1.7 L97-102(check-5 regex fix commit `a57972a`)+ §4.3 F5 L172(fixture 物理位置独立必须项)。

## 当前结构(2026-05-12 v2)

```
test-fixtures/
├── valid/
│   └── discussion/008/handback/
│       └── 20260520T103015Z-008a-pA-20260520T103015Z.md  ← exit 0 PASS · 6 约束全过
│
├── invalid-1-out-of-tree/
│   └── discussion/008/handback/
│       └── 20260520T103015Z-008a-pA-20260520T103015Z.md  ← check-1 FAIL(handback_target=/tmp/whatever)
│
├── invalid-2-symlink/
│   └── README.md  ← 不是 fixture · symlink 测动态构造(本 README 说明)
│
├── invalid-3-repo-mismatch/
│   └── discussion/008/handback/
│       └── 20260520T103015Z-008a-pA-20260520T103015Z.md  ← check-3 FAIL(source_repo_identity 三模式全不匹配)
│
├── invalid-5-id-mismatch/
│   └── discussion/008/handback/
│       └── 20260520T103015Z-999z-pZ-20260520T103015Z.md  ← check-5 真因(discussion_id=008 vs prd_fork_id 前缀 999)
│
├── invalid-6-id-charset/
│   └── discussion/008/handback/
│       └── 20260520T103015Z-008-20260520T103015Z.md  ← check-5 mismatch · OWASP defense in depth(见 §invalid-6 注)
│
└── test-check-3-host-binding.sh  ← 独立 host binding test(non-fixture)
```

## 跑 validator dry-run(operator 跑)

### 全 fixture 一遍跑

```bash
# 1. valid · 应 exit 0
bash framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh \
  framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/valid/discussion/008/handback/20260520T103015Z-008a-pA-20260520T103015Z.md \
  "$(realpath /Users/admin/codes/ideababy_stroller)" \
  --mode=consumer

# 2. 4 invalid · 应 exit 1 真因 stderr 显形
for f in framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/invalid-*/discussion/008/handback/*.md; do
  echo "=== $f ==="
  bash framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh "$f" "$(realpath /Users/admin/codes/ideababy_stroller)" --mode=consumer 2>&1 | head -4
done
```

### 预期 stderr verbatim

| fixture | exit | stderr 第一行 |
|---|---|---|
| valid | 0 | `✓ all 6 constraints PASS for 008a-pA-20260520T103015Z` |
| invalid-1-out-of-tree | 1 | `FAIL · §6.2.1 约束 1 (canonical-path containment)` |
| invalid-3-repo-mismatch | 1 | `FAIL · §6.2.1 约束 3 (remote 模式锁定 mismatch · 不允许 fall through)` |
| invalid-5-id-mismatch | 1 | `FAIL · §6.2.1 约束 5 (id consistency check)` · "frontmatter prd_fork_id prefix (999 from 999z-pZ) != frontmatter discussion_id (008)" |
| invalid-6-id-charset | 1 | `FAIL · §6.2.1 约束 5 (id consistency check)` · "filename handback_id (008-...) != frontmatter handback_id (008/../../etc-...)" |

## §invalid-6 注 · 设计权衡(OWASP defense in depth)

invalid-6 frontmatter `handback_id: 008/../../etc-20260520T103015Z` 含 `/` `..` 是 path traversal 攻击载荷 · 设计目标:撞 check-6 charset(regex 不允许 `/` `..` 等)。

**但 filename 不能含 `/`**(OS 限制) · 所以 filename 用合法 token `20260520T103015Z-008-20260520T103015Z.md`(handback_id token = `008-20260520T103015Z`)。

跑 validator 时:
- **check-5 先撞**:filename handback_id (`008-20260520T103015Z`) ≠ frontmatter handback_id (`008/../../etc-20260520T103015Z`)
- check-6 charset **没机会跑**(check-5 已先 fail)

**这不是 regression** · 是 OWASP defense in depth 真展示:
- 攻击场景:producer 端 frontmatter 被注入恶意 handback_id · 即使 attacker 控制 filename 用合法 token 伪装 · check-5 三处一致校验 先撞
- 真世界 producer 写文件时 filename 是从 frontmatter handback_id 算出来的(`<ts>-<handback_id>.md`) · 若 handback_id 含 `/` 立马撞 OS filename 限制 · 写入即 fail
- check-5 是 input shape validation 第一道防线 · check-6 是 charset regex 第二道防线 · 两道并存 · 本 fixture 撞第一道是正确行为

测试覆盖意义:invalid-6 fixture 已经在 fixture corpus 里 · 演示 "frontmatter 注入 + filename 不一致" 攻击仍被挡 · check-6 charset 单独测试可走 `test-check-3-host-binding.sh` 模式动态构造(若 v0.3 需要)。

## 与协议演化的关系

- **v2.0 ACTIVE**(2026-05-11):6 约束 schema 落地 · 当前 fixture corpus 测 1-3 + 5 真因(check-6 charset 真因测延 future · 见 §invalid-6 注)
- **v2.2**(2026-05-12 · plan 件 2.5+2.2 合):§6.3 加 RECOMMENDED 字段 + §6.4.1 闭环责任段 · 不影响 6 约束 schema · fixture corpus 不需 backfill
- **v0.3+ trigger**:若 check-6 charset 真因需独立 fixture 演示 · 可加 invalid-6b(动态构造模式)· 仿 invalid-2-symlink

## 变更日志

- **2026-05-12 v2**(plan-rosy-naur v12 B 件 4):重构 5 fixture 路径含 `discussion/008/handback/` 段 · 删早期 simple `valid/handback.md` · 加本 README.md · valid 1 PASS + invalid 4 真因 FAIL(invalid-6 撞 check-5 mismatch 见 §invalid-6 注)
- **2026-05-10 v1**(B2.2 Block A):初版 fixture corpus(6 fixtures · 平铺结构 · `valid/<file>.md` + `invalid-*/<file>.md`)
