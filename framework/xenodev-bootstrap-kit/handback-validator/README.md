# §6.2.1 6 约束 hand-back validator

per `framework/SHARED-CONTRACT.md` §6.2.1 + §3.1。

## 这是什么

M2 Block D `/handback-review.md` 命令骨架引用 §6.2.1 6 约束作为 normative source(M2 contract-only)。本 Block F 落实 **可调 validator code**(producer + consumer 双端共用)。

XenoDev 端(producer)写 hand-back 包前必跑;IDS 端(consumer)读 hand-back 包前必跑。任一约束失败 → hard-fail(不写 / 不读 / 只 stderr)。

## 6 约束清单

| # | 约束 | check script |
|---|---|---|
| 1 | canonical-path containment | check-1-canonical-path.sh |
| 2 | symlink reject | check-2-symlink-reject.sh |
| 3 | repo identity check(三模式 remote / no-remote / hash-only) | check-3-repo-identity.sh |
| 4 | hard-fail 行为 | (行为约定,无独立 script;由 validate-handback.sh 主入口实施) |
| 5 | id consistency check(三处 id 严格一致) | check-5-id-consistency.sh |
| 6 | id 字符集 + filename basename + final-path containment | check-6-id-charset-and-final-path.sh |

## 文件清单

- `README.md`(本文件)
- `validate-handback.sh` — 主入口(producer + consumer 共用)
- `check-1-canonical-path.sh`
- `check-2-symlink-reject.sh`
- `check-3-repo-identity.sh`
- `check-5-id-consistency.sh`
- `check-6-id-charset-and-final-path.sh`
- `test-fixtures/`:
  - `valid/` — 6 约束全过的 hand-back 包样本
  - `invalid-1-out-of-tree/` — 路径逃逸(handback_target 在 source_repo 之外)
  - `invalid-2-symlink/` — symlink 攻击(路径段含 symlink)
  - `invalid-3-repo-mismatch/` — 三模式全 FAIL(IDS 副本 / test clone)
  - `invalid-5-id-mismatch/` — 三处 id 不一致(corruption-of-corpus)
  - `invalid-6-id-charset/` — id 含 `/ \ ..`(path traversal 攻击)

## 装机(XenoDev 端,operator bootstrap.sh 后)

bootstrap.sh 已自动 cp 到 `lib/handback-validator/`。

XenoDev parallel-builder 在产 hand-back 包时调:
```bash
bash lib/handback-validator/validate-handback.sh \
  /tmp/draft-handback.md \
  /Users/admin/codes/ideababy_stroller
# exit 0 → 写到 source_repo/discussion/<id>/handback/
# exit 1 → drop,stderr 报哪条约束 + handback_id
```

IDS 端 `/handback-review` 命令在读 hand-back 包前调同一脚本。

## 单元测试

```bash
# valid → exit 0
bash framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh \
  framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/valid/handback.md \
  /Users/admin/codes/ideababy_stroller

# 5 invalid → 各 exit 1 + stderr 报对应约束
for i in 1-out-of-tree 2-symlink 3-repo-mismatch 5-id-mismatch 6-id-charset; do
  echo "=== invalid-$i ==="
  bash framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh \
    framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/invalid-$i/handback.md \
    /Users/admin/codes/ideababy_stroller 2>&1
done
```

## 与 §3.1 source_repo_identity 的关系

约束 3(repo identity check)的三模式比对依据 hand-off 包 frontmatter `source_repo_identity:` 块(M2 Block E + plan-start v3.0 实装)。

- remote 模式:`expected_remote_url` 字段
- no-remote 模式:`repo_marker` 字段
- hash-only 模式:`git_common_dir_hash` 字段

任一非空 → 用对应模式;任一 PASS → 约束 3 PASS;**全 N/A → 约束 3 FAIL**(per §3.1 normative)。

## 已知限制

- `realpath -m`(macOS):若不可用,fallback python3 `os.path.normpath(os.path.abspath())`(单人 dev 环境兼容)
- `shasum -a 256`(macOS):用 `sha256sum`(linux)alternate;script 中默认 `shasum`(operator macOS)
- `grep -P` / Perl regex 在某些 grep 实现不可用 — check-6 中用作控制字符检测

## OQ

- **OQ-validator-1**:fixtures 中 invalid-2-symlink 创建需要 mkdir + ln -s;在 git 中 symlink 是否能 cp 跨 repo — bootstrap.sh cp -r 应保留 symlink,B2.2 跑后看
- **OQ-validator-2**:windows 环境(operator 是否会用)— v0.2 决,v0.1 假设 macOS / linux
- **OQ-validator-3**:check-3 的 normalize() 函数处理 git@ vs https:// 边界用 case 匹配,可能漏 ssh:// 边界 — B2.2 跑真 git remote 时验
