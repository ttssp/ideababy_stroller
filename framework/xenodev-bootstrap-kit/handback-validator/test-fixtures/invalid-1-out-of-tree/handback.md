---
discussion_id: 008
prd_fork_id: 008a-pA
handback_id: 008a-pA-20260520T103015Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /tmp/whatever/handback/
source_repo_identity:
  expected_remote_url: ""
  repo_marker: "# Idea Incubator"
  git_common_dir_hash: ""
tags:
  - drift
severity: low
created: 2026-05-20T10:30:15Z
---

# Invalid fixture · §6.2.1 约束 1 失败

handback_target 指向 /tmp/whatever/handback/(不在 source_repo/discussion/008/handback/ 之下)

应 exit 1 + stderr 报 "FAIL · §6.2.1 约束 1 (canonical-path containment)"
