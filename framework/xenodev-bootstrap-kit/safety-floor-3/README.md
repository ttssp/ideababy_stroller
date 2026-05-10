# Safety Floor 件 3 · 备份破坏检测 kit

per `framework/SHARED-CONTRACT.md` §1 第 3 件 + §2 件 3 + stage-forge-006-v2.md §"模块 B" step 4。

## 原理

**snapshot + diff 模式**:周期性取 snapshot,在下一次 snapshot 时与本次 diff,警告 backup destruction patterns(同一 credential 被 grant 删主存 + 备份的权限 / backup 文件突然消失 / 防御配置弱化等)。

灵感来源:Cursor + Claude 9 秒删库案例(tomshardware 2025) — 该事件中 same credential 同时有删主存 + 删 backup 权限,本件 3 检测此类配置漂移。

## v0.1 简化范围

单人本地 dev 场景 v0.1 简化检测:
- `.git/config`(remote URL / push policy 变化)
- `.claude/settings.json`(permissions.deny 减少 = 防御能力弱化)
- `*.backup` / `*.bak` / `*.snapshot` 文件路径(突然消失警报)
- snapshot 间隔(> 30 天报警)

**真正生产级 backup config**(IAM rules / cloud restore policies)v0.2 加 — per stage doc OUT-2 v0.1 不实装阈值算法。

## 文件清单

- `README.md`(本文件)
- `snapshot.sh` — 取 snapshot,写入 `<output-dir>/snapshot-<ISO ts>.json`
- `diff-snapshot.sh` — 比对两 snapshot,4 类破坏模式检测
- `test-fixtures/snapshot-{a,b}.json` — 测试 fixtures(B 模拟 backup 消失 + permissions.deny 减少)

## 装机(XenoDev 端,operator bootstrap.sh 后)

bootstrap.sh 已自动 cp 到 `.claude/safety-floor/backup-detection/`。建议 operator:

1. 周期性 snapshot(per dev 节奏,推荐每周一次):
   ```bash
   bash .claude/safety-floor/backup-detection/snapshot.sh .snapshots/
   ```

2. 取新 snapshot 后立即 diff vs 上一个:
   ```bash
   ls -t .snapshots/snapshot-*.json | head -2 | tac | xargs bash .claude/safety-floor/backup-detection/diff-snapshot.sh
   ```

3. 自动化(可选):lefthook.yml 或 cron 触发

## 4 类检测模式

| # | 模式 | 严重度 | exit |
|---|---|---|---|
| 1 | backup 文件突然全消失 | CRITICAL | exit 1 |
| 2 | `.git/config` push policy 变宽松(加 force push)| WARNING | exit 0 + stderr |
| 3 | `.claude/settings.json` permissions.deny 减少 | WARNING | exit 0 + stderr |
| 4 | snapshot 间隔 > 30 天 | INFO | exit 0 + stderr |

## 单元测试

```bash
# 测试 1: snapshot 跑当前目录(应 exit 0,产 snapshot 文件)
bash framework/xenodev-bootstrap-kit/safety-floor-3/snapshot.sh /tmp/test-snap/
test -f /tmp/test-snap/snapshot-*.json && echo PASS
rm -rf /tmp/test-snap/

# 测试 2: diff 两 fixture(b 模拟 backup 消失)— 应 exit 1
bash framework/xenodev-bootstrap-kit/safety-floor-3/diff-snapshot.sh \
  framework/xenodev-bootstrap-kit/safety-floor-3/test-fixtures/snapshot-a.json \
  framework/xenodev-bootstrap-kit/safety-floor-3/test-fixtures/snapshot-b.json
# 应 exit 1 + stderr 报 CRITICAL

# 测试 3: diff 同一 fixture(无变化)— 应 exit 0
bash framework/xenodev-bootstrap-kit/safety-floor-3/diff-snapshot.sh \
  framework/xenodev-bootstrap-kit/safety-floor-3/test-fixtures/snapshot-a.json \
  framework/xenodev-bootstrap-kit/safety-floor-3/test-fixtures/snapshot-a.json
# 应 exit 0
```

## OQ

- **OQ-backup-1**:cloud IAM 配置 snapshot(AWS S3 / GCS bucket policy)— v0.2,XenoDev 真用云时加
- **OQ-backup-2**:snapshot 频率默认值(每周?每月?)— v0.2 由 operator 实践决
- **OQ-backup-3**:diff 阈值(permissions.deny 减少多少 entry 才警报)— 当前任何减少都报警,可能 noisy
