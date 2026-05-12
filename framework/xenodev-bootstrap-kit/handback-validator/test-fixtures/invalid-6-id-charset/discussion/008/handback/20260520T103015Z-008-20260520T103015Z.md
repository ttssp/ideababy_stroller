---
discussion_id: 008
prd_fork_id: 008/../../etc
handback_id: 008/../../etc-20260520T103015Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/
source_repo_identity:
  expected_remote_url: "git@github.com:ttssp/ideababy_stroller.git"
  repo_marker: "# Idea Incubator"
  git_common_dir_hash: ""
tags:
  - drift
severity: low
created: 2026-05-20T10:30:15Z
---

# Invalid fixture · §6.2.1 约束 6 失败(id 含 / 和 ..)

prd_fork_id = "008/../../etc"
- 含 `/` `..` — path traversal 攻击
- 不匹配 ^[0-9]{3}[a-z]?(-p[A-Z])?$

应 exit 1 + stderr 报 "FAIL · §6.2.1 约束 6 (id charset + filename basename + final-path containment)"
