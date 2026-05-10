# invalid-2-symlink fixture

symlink 攻击 fixture 需要在测试时**动态构造**(不能用普通 .md fixture):

```bash
# 测试时构造:
SOURCE_FAKE="$(mktemp -d)"
mkdir -p "$SOURCE_FAKE/discussion/008/"
ln -s /tmp/evil "$SOURCE_FAKE/discussion/008/handback"   # handback 段是 symlink

# 写一个 hand-back fixture handback_target 指向该 symlink
cat > "$SOURCE_FAKE/discussion/008/handback/handback.md" <<'EOF'
---
workspace:
  source_repo: $SOURCE_FAKE
  handback_target: $SOURCE_FAKE/discussion/008/handback/
...
EOF

# 跑 check-2 应 exit 1
bash check-2-symlink-reject.sh $SOURCE_FAKE/discussion/008/handback/ $SOURCE_FAKE
```

valid fixture(.md)无 symlink 创建能力(普通 git checkout 在某些 OS 不保留 symlink),
所以 invalid-2 单独用动态构造的方式测试,不进 git fixtures。

测试脚本在 README 单元测试节中给出。
