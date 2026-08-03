# Forge 001 v6 · P2 · GPT55xHigh

> 篇幅约超 1100 CJK 字符:本轮需回应 Opus 四项修正 + 仓内核查 + SOTA 来源,未做有损压缩。Web searches run: 5. Sources: CVE FAQ / CVE schema / NVD API / Cochrane / BMJ / RFC 7282.

## §1 SOTA 对标

| 面 | 来源 | 对本轮的含义 |
|---|---|---|
| CVE `REJECTED` | CVE FAQ:REJECT record 不被接受,原则上应忽略;CVE schema:Rejected record 留在 List 是让用户知道其无效;NVD API 默认含 Rejected,但提供 `noRejected` 过滤。[CVE FAQ](https://www.cve.org/Resources/Media/Archives/OldWebsite/about/faqs.html) / [schema](https://cveproject.github.io/cve-schema/schema/docs/) / [NVD](https://nvd.nist.gov/developers/vulnerabilities) | 这比“标注/通知”强:无效结论应在消费点可被过滤/拒绝。映射到旧池假 PASS:若池键被证错,受影响 PASS 应进入机器可拒的 invalid/rejected-like 状态,不是只加说明。 |
| CVE `DISPUTED` | CVE/NVD 把 disputed 当 tag:争议存在但记录仍发布,读者应查证;NVD 支持 `cveTag=disputed` 查询。[CVE FAQ](https://www.cve.org/Resources/Media/Archives/OldWebsite/about/faqs.html) / [NVD](https://nvd.nist.gov/developers/vulnerabilities) | reviewer 反对未必等于删除/阻断一切推进;它至少不能被消费为 clean PASS。争议态与无效态要分开。 |
| post-hoc 分组 | Cochrane 允许“sensible and honest” post-hoc subgroup exploration,但须标明;BMJ 系统综述说 retrospective subgroup 可产假设,不应指导实践。[Cochrane](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-10) / [BMJ](https://www.bmj.com/content/344/bmj.e1553) | Opus“先合池后拆方向反了”对 block PASS 成立;但 post-hoc 拆池作为 warn/探索是有正当先例的。故 v5 不是全错,错在把探索性池化出口写成可放行 PASS。 |
| objection 处理 | RFC 7282:rough consensus 要 addressed,不必 accommodated;chair 给 reasoned explanation。[RFC 7282](https://www.rfc-editor.org/rfc/rfc7282.html) | 我同意 Opus 推翻:codex `needs-attention` 不是绝对 veto。缺的是 chair 认定。映射:chair = operator;`/handback-review` 是 chair 的记录/闸点,不是 chair 本身;spec-writer 不能自任 chair。 |

## §2 外部材料消化 + 仓内核查

外部材料给出两条分流:争议未消解可推进,但必须由 chair 判定“已处理”;已证无效则消费点 fail-closed。CVE 还补了 Opus 未取到的面:Rejected 与 Disputed 是不同状态,前者应被过滤/忽略,后者保留给消费方核实。

仓内核查:我搜了 worktree 与主副本 `out/`。真实 `evaluate` 产物只有 `coding-llms-20260802T022608Z.md` 与 `evaluations.jsonl` 一行;二者都明写“非豁免判断 1 条 <3,不得据以判 O2 / §7-P2 PASS”。另有 `a1-selfcheck.jsonl predicate_passed=true`,但那是 T010/T011 解锁自证,不是 O2/P2 PASS。结论:我未发现真实 O2/P2 PASS 被旧池消费;追溯成本目前大概率为零,但应把“零受影响”写成迁移核查结果,不要靠沉默推断。

消费点:当前没有合格消费点。应新增/指定读取 briefing + journal 并产 O2/P2 verdict 的检查器;在它出现前,最近的消费面是 `radar.cli.evaluate` 落盘产物和 `journal record/list` 的 briefing snapshot。fail-closed 应落在这个未来 verifier/consumer 上:读到 `invalid`/`needs-revalidation`/`disputed` 不得给 clean PASS。

## §3 修正后的视角

我 P1 站住:分区键必须前置定义;T021/T040/T041 没有承接 v0.7 三态与池化运行时;产出侧不应逼 judge 凑数。

我 P1 需修正:第 3 行“needs-attention 默认阻断合入”过紧。更准确是:允许 operator-chair override,但 override 必须逐条说明 reviewer concern 如何 addressed,并把状态写给消费点;没有 chair 记录时不得声称 clean PASS。

同意 Opus:追溯不能只靠 `suspended-pass` 标注,必须消费点拒绝。若 v0.8 核查确认零旧 O2/P2 PASS,本轮可把追溯语义先写成“若发现则 rejected-like fail-closed + 重验”,实际迁移表为零项。

同意“≥3 阈值挂账不判”。不裁阈值仍能裁分区键:无论阈值是 2、3、5,集合成员都必须先可比较;阈值的产品价值本轮无视角,只登记为后续产品价值问题。

Opus 四条单方主张表态:§0.1 责任人自批,我 P1 没想到,现认同并并入 chair 缺失;T041 范畴错误,我 P1 只说 file_domain/owner 缺口,现认同更强表述;direction 在去重键抬高计数,我未想到,读 spec 后认同病灶,但修法是否“direction 退出去重键”留 P3;三重不追溯单调性,我未命名但认同,需拆为 fail-closed 不追溯可保留、fail-open PASS 必可撤销。
