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
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/
source_repo_identity:
  expected_remote_url: "git@github.com:wrong-user/wrong-repo.git"
  repo_marker: "FAKE marker not Idea Incubator"
  git_common_dir_hash: "0000000000000000"
tags:
  - drift
severity: low
created: 2026-05-20T10:30:15Z
---

# Invalid fixture · §6.2.1 约束 3 失败(三模式全 FAIL)

source_repo_identity:
- expected_remote_url 不匹配实际 source_repo 的 remote
- repo_marker 不含 "Idea Incubator"
- git_common_dir_hash 不匹配实际 hash

应 exit 1 + stderr 报 "FAIL · §6.2.1 约束 3 (repo identity check, all 3 modes failed)"
