# Forge v7 · 006 · P2 · Claude · 参照系评估(with search)

**Timestamp**: 2026-07-07T13:05:00Z
**Searches run**: 5, SOTA-benchmark
**Visibility**: 我已读对方 P1。
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 簇1 fallback 制度化(KG-32/37/38) | Circuit breaker 模式(微服务韧性标准件) | 三态机 Closed/Open/Half-Open;失败按**阈值分类**触发跳闸;跳闸期走**预定义 fallback**;恢复期 half-open 试探;observability 必配 | 失效处理是 CLAUDE.md 一段文字 + 三次临场外推;无状态机、无阈值、无预定义降级链。但「codex 恢复后优先补跑作权威确认」恰是自发长出的 half-open | 我们缺的正是 SOTA 的**全部四要素**(分类阈值/显式态/预定义 fallback/可观测);且实践已自发逼近该模式,制度化=套用成熟形状而非发明 | [groundcover](https://www.groundcover.com/learn/performance/circuit-breaker-pattern) · [Aerospike](https://aerospike.com/blog/circuit-breaker-pattern/) |
| KG-38 挂死判死 + 未编号长任务条 | Kubernetes liveness probe / watchdog | 专用心跳信号(healthz,**不查依赖**);`timeoutSeconds` 略高于 P99;`failureThreshold × periodSeconds` = 容忍窗;显式防**假阳性**(负载慢≠挂死) | companion 无任何 liveness 概念,status 恒 running;调用侧人肉数分钟;未编号条目的 `ps\|grep` 误判起 3 进程 = **坏 probe 设计的活例**(查进程表而非查心跳/产物) | 判死要素 SOTA 全有现成公式:心跳源(job log 末次活动)+ 阈值(N×period)+ 假阳性防护;probe 声明在 workload、执行在平台(kubelet)——映射:阈值声明在 SKILL、执行该在 companion | [k8s probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/) · [避免假阳性](https://oneuptime.com/blog/post/2026-02-09-liveness-probes-avoid-false-positives/view) |
| KG-B1 跨仓 fork-id 契约(+KG-29 史) | Schema Registry 兼容规则 + Pact 消费者驱动契约测试 | schema 有**单一规范定义源**+版本化;registry 在 CI 期强制兼容规则(producer 改动不许破 consumer);consumer 生成契约、producer 对**每个 consumer 的期望**独立验证 | fork-id 语法无规范定义:IDS 铸(plan-start 惯例)、XenoDev 验(check-6 regex),两边各自演化;修法=逐例放宽 regex,已断两次(KG-29→KG-B1) | 「每种新命名再断一次」= 教科书级**缺契约测试**症状。SOTA 解法形状:fork-id 语法进 SHARED-CONTRACT 作单一规范 + 双仓各自跑同一 fixture 语料的契约测试(IDS 铸造测 + XenoDev 接受测) | [Pact](https://docs.pact.io/) · [schema versioning](https://www.datasops.com/blog/data-contracts-versioning) |
| 强 review gate 卡死(簇1 总体) | GitHub required status checks 生态 | 卡 pending/Expected 是**业界地方病**(路径过滤跳过/并发取消/名称不匹配全会卡死 merge);生态答案=显式重跑路径 + 命名契约对齐,而非取消强 gate | 我们的强 hook 同构:KG-38 卡死无重跑路径;KG-22(gate 读 top-level、spec 报 per-phase)与「required check 期望名 X、matrix 报名 Y」**同构** | 强 gate 卡死不丢人,丢人的是没有显式脱困路径;KG-22 本质是 status 命名契约不匹配,与簇1 可共用「契约对齐」框架 | [GitHub 讨论](https://github.com/orgs/community/discussions/26698) · [troubleshooting docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks) |
| fallback 的越权风险(设计边界) | CODEOWNERS bypass vs merge queue | bypass 是 all-or-nothing,与 merge queue 交互直接坏掉(bypass 生效则 queue 被整个跳过);结论=**降级必须一等公民设计,补丁式 bypass 破坏不变量** | operator 决议的 fallback 惯例(标 subagent-fallback 不冒充 codex)恰好避开了"冒充"这个坑,方向对 | 印证 P3 该做的是把 fallback 做成 SKILL 决策表的显式分支(带审计标注),不是加一个"跳过 review"的口子 | [codenote 验证](https://codenote.net/en/posts/github-codeowners-bypass-merge-queue-verification/) |

**本轮活体证据**:Codex 写它自己的 P1 时又撞 bwrap loopback(outbox 自述,靠提权重写文件脱困)——KG-37 家族在 forge 审它自己的过程中第三次复现,"间歇性环境失效"板上钉钉。

## 2. 用户外部材料消化

n/a——K 未给外部链接/文件(Z=对标 SOTA,已在 §1 消化)。

## 3. 修正后的视角

- P1 判断「失效分支制度化进 SKILL 决策表」→ **站住且升级**:不是自创机制,是套 circuit breaker 的标准四要素(失效分类阈值 / 显式状态 / 预定义降级链 / 可观测);实践已自发长出 half-open(codex 恢复补跑),制度化只是把已验证行为写进态机。
- P1 判断「判死阈值 = 静默 N 分钟」→ **站住但被 SOTA 精化**:心跳源要选对(job log 末次活动,不是 pid 存活——status 恒 running 正是查错了心跳源),阈值公式 = threshold × period,且必须防假阳性(未编号条目的 ps|grep 误判是反面教材,它查的是进程表不是产物/心跳)。我 P1 不确定点 2(判死放哪层)得到部分解答:**k8s 把 probe 声明与执行分离**——阈值声明在 SKILL/config,执行属于拥有 job 生命周期的 companion;companion 改不动时 SKILL 侧轮询判死是过渡。
- P1 判断「new 跨仓 fork-id 规范单点,拒绝第三次逐例放宽」→ **站住并获得具体形状**:SHARED-CONTRACT 收编 fork-id 语法(单一规范源)+ 双仓契约测试(同一 fixture 语料:IDS 铸造侧全过 + XenoDev 接受侧全过),这是 schema-registry + Pact 的标准组合,直接回答 GPT P1 不确定点 2 的"两难"——**不是二选一,是把语法定义权收到契约层,两边都变 consumer**。
- GPT P1 判断「codex 有真实发现价值,不 cut」→ **被 SOTA 加固**:circuit breaker 的存在意义就是"安全地继续使用有价值但不可靠的依赖",cut 是错误答案,裸奔也是。
- P1 不确定点 3(KG-23 branch-scope 最对 vs KG-37 branch-mode 恰是沙箱重灾区)→ **搜索未解,升级为 P3 必裁**:GitHub 生态的启示只有"给强 gate 显式脱困路径 + scope 语义当契约审"(KG-23 是文档-实现契约违约),两条 KG 的修法交互仍需 P3 把簇1 当系统收敛。
