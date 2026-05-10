# Safety Floor 件 2 · 不可逆命令 hard block(mirror from autodev_pipe)

per `framework/SHARED-CONTRACT.md` §1 第 2 件 + §2 件 2 + stage-forge-006-v2.md §"模块 B" step 2:
> **cp `block-dangerous.sh` from V4(纯工业共识,无定制)**

## 文件清单

- `block-dangerous.sh` — Claude Code PreToolUse hook(mirror from autodev_pipe)

## Mirror provenance

- **源**:`/Users/admin/codes/autodev_pipe/.claude/hooks/block-dangerous.sh`(autodev_pipe v3.1 §6 实装)
- **镜像时间**:2026-05-10(B2.1 Block A)
- **改动**:与源完全一致(byte-for-byte)
- **同步策略**:本 mirror 始终保持与 autodev_pipe 同步;未来若需 XenoDev 定制 dangerous patterns,在 XenoDev 仓内 fork 后修改,不要改本 mirror

## 阻断的 24 类危险命令(grep -E 正则模式)

| 类别 | 模式举例 | 现实威胁场景 |
|---|---|---|
| 删根/删 home | `rm -rf /` `rm -rf ~` `rm -rf $HOME` | Cursor + Claude 9 秒删库案例 |
| 删父目录 | `rm -rf ..` | 跳出当前目录误删 |
| force push 主分支 | `git push --force.*main` `git push -f.*master` | 覆盖远程主分支 |
| 丢弃未推送提交 | `git reset --hard.*origin` | 本地工作丢失 |
| 强制清理 | `git clean -fxd` 类 | 误删未追踪文件 |
| SQL 破坏 | `DROP DATABASE` `DROP TABLE` `TRUNCATE TABLE` | 数据库删库 |
| 云资源破坏 | `aws s3 rm --recursive production` `aws s3 rb --force` | S3 桶删除 |
| K8s 破坏 | `kubectl delete namespace` | 命名空间整删 |
| IaC 破坏 | `terraform destroy` | 基础设施整删 |
| fork bomb | `:(){ :\|:& };:` | 资源耗尽 |
| 设备写入 | `dd if=...of=/dev/...` | 裸设备覆写 |
| 格式化 | `mkfs.` | 文件系统重建 |
| 远程执行 | `curl ... \| bash` `wget ... \| sh` | 远程恶意脚本 |
| 权限放开 | `chmod -R 777 /` | 全系统权限开放 |

## 装机方式(operator 跑 bootstrap.sh 后)

bootstrap.sh 自动 cp 本文件到 XenoDev `.claude/hooks/block-dangerous.sh` + chmod +x。

XenoDev `.claude/settings.json` 必须含:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-dangerous.sh"
      }]
    }]
  }
}
```

## 失败案例参考(为何此 hook 必装)

- **Cursor + Claude 9 秒删库**(tomshardware 2025) — `rm -rf` 类未阻断,9 秒内删除生产 DB
- **MSR 2026 33k agentic PR 失败研究** — 部分失败源于不可逆操作未拦
- **autodev_pipe V4 dogfood** — 该 hook 在 V4 12 周 dogfood 跑过(虽 V4 整体 archive,本 hook 是工业共识保留)

## 与 §6.5 第 8-9 项的关系

- §6.5 第 8-9 项已勾(M3 commit d3194a0)— 4 fork specs/ DEPRECATED
- 本 hook 不依赖 specs/(纯命令拦截层)
- M2 cutover 后 IDS 不再 build,本 hook 不在 IDS 跑;但 mirror 保留作 XenoDev bootstrap source
