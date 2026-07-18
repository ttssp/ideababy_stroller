"""extraction/gold_layer1.py — T007 · 009-pM3prime E1 · 金标 Layer-1 span 验收。

结论(先):两层金标第一层(O7)—— 疑似信号语句**有没有被找到**。产 Krippendorff α(标注者间一致性)+
  span P/R/F1(vs 金标 span)真数值 vs 预注册门槛 · 过/STOP。写 gold_layer1_result 表真行。

pure-math(不引 scipy · echo alpha/deflate.py 范式:只用 stdlib)· 第二标注源 + 分歧仲裁留痕(C9)。

核心红线:
  1. **门槛预注册**(OQ-1):α/P/R 下限先写下再跑(evaluate 入参 · SLA 冻结表)· 不过 = STOP 不谈回测(§5)。
  2. **echo-chamber known-gap**(E1-R2):Layer-1 第二源可 LLM+人混,但若都 LLM → α 虚高须记 known-gap(C9)。
  3. **operator 不单独终审**(C9):需第二标注源 + 分歧仲裁流程留痕(second_annotator + arbitration_note 列)。

边界:只做 Layer-1 span 验收。不做 Layer-2 映射(T008)· 不做 gate(T009)· 不建表(T002)。
"""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping, Sequence

from pydantic import BaseModel, ConfigDict

# span 三元组:(source_id, span_start, span_end)
Span = tuple[str, int, int]


class Layer1Result(BaseModel):
    """Layer-1 验收结果(α/P/R/F1 + 过否)。"""

    model_config = ConfigDict(frozen=True)

    krippendorff_alpha: float
    span_precision: float
    span_recall: float
    span_f1: float
    passed: bool


def krippendorff_alpha(annotations: Mapping[str, Mapping[str, int]]) -> float:
    """Krippendorff α(nominal · pure-math · 不引 scipy)。

    结论:α = 1 - D_o / D_e(观察不一致 / 期望不一致)· 完全一致 → 1.0 · 系统反向 → ≤0。
    细节(nominal 度量 · 处理缺失):
      - 按 unit 聚合各标注者的值 · 只用被 ≥2 标注者标的 unit(pairable)。
      - D_o = 单元内不一致对占比;D_e = 全局按值分布期望不一致。
      - echo deflate.py:只用 stdlib(无 numpy/scipy)· 手算配对不一致。
    """
    # 按 unit 收各标注者值
    units: dict[str, list[int]] = {}
    for _annotator, coding in annotations.items():
        for unit, value in coding.items():
            units.setdefault(unit, []).append(value)

    # 只保留 ≥2 标注的 unit(可配对)
    pairable = {u: vals for u, vals in units.items() if len(vals) >= 2}
    if not pairable:
        # ⚠ review 修:无可配对数据 **不能**读作 α=1.0(完美一致)—— 那会让空标注集伪装成满分过门槛。
        #   无证据 = 无一致性可言 → 返 0.0(最保守 · 配合 evaluate_layer1 门槛必然 STOP · fail-closed)。
        raise ValueError(
            "Krippendorff α:无可配对标注单元(需 ≥1 个被 ≥2 标注者标的 unit)· "
            "空标注集不产一致性数字(fail-closed · 不伪装满分)"
        )

    # 观察不一致 D_o:各 unit 内所有有序对中 value 不同的比例(nominal metric)
    obs_disagree = 0
    obs_pairs = 0
    value_counts: dict[int, int] = {}
    total_values = 0
    for vals in pairable.values():
        m = len(vals)
        obs_pairs += m * (m - 1)
        for i in range(m):
            value_counts[vals[i]] = value_counts.get(vals[i], 0) + 1
            total_values += 1
            for j in range(m):
                if i != j and vals[i] != vals[j]:
                    obs_disagree += 1
    d_o = obs_disagree / obs_pairs if obs_pairs else 0.0

    # 期望不一致 D_e:按全局值分布,随机两值不同的概率
    exp_disagree = 0
    exp_pairs = total_values * (total_values - 1)
    for va, ca in value_counts.items():
        for vb, cb in value_counts.items():
            if va != vb:
                exp_disagree += ca * cb
    d_e = exp_disagree / exp_pairs if exp_pairs else 0.0

    if d_e == 0.0:
        return 1.0  # 无期望分歧(全同值)· 约定 α=1
    return 1.0 - (d_o / d_e)


def span_prf(*, gold: Sequence[Span], pred: Sequence[Span]) -> tuple[float, float, float]:
    """span 级 precision / recall / F1(exact-match 集合口径)。

    结论:tp = |gold ∩ pred| · precision = tp/|pred| · recall = tp/|gold| · F1 = 调和平均。
    细节:span 完全一致(source_id+start+end 全等)才算命中(exact match · 严口径 · 反宽松放水)。
      空 pred → P=0/R=0(不除零)· 空 gold → R 约定 0(无金标可召回)。
    """
    gold_set = set(gold)
    pred_set = set(pred)
    tp = len(gold_set & pred_set)
    precision = tp / len(pred_set) if pred_set else 0.0
    recall = tp / len(gold_set) if gold_set else 0.0
    if precision + recall == 0.0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def evaluate_layer1(
    caliber_version: str,
    *,
    conn: sqlite3.Connection,
    annotations: Mapping[str, Mapping[str, int]],
    gold_spans: Sequence[Span],
    pred_spans: Sequence[Span],
    alpha_threshold: float,
    prf_threshold: float,
    second_annotator: str,
    arbitration_note: str = "",
) -> Layer1Result:
    """Layer-1 验收:算 α + span P/R/F1 → vs 预注册门槛 → 过/STOP → 写 gold_layer1_result 行。

    结论:α ≥ alpha_threshold 且 span_precision/recall ≥ prf_threshold → passed;否则 STOP(不谈回测)。
    细节:门槛是**入参**(预注册 · SLA 冻结表 · OQ-1)· 第二标注源 + 仲裁留痕(C9 · operator 不单独终审)。
    """
    alpha = krippendorff_alpha(annotations)
    precision, recall, f1 = span_prf(gold=gold_spans, pred=pred_spans)

    passed = (
        alpha >= alpha_threshold
        and precision >= prf_threshold
        and recall >= prf_threshold
    )

    now = conn.execute("SELECT strftime('%Y-%m-%dT%H:%M:%SZ','now')").fetchone()[0]
    conn.execute(
        "INSERT INTO gold_layer1_result "
        "(krippendorff_alpha, span_precision, span_recall, span_f1, passed, "
        "second_annotator, arbitration_note, caliber_version, created_at) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (
            alpha, precision, recall, f1, 1 if passed else 0,
            second_annotator, arbitration_note, caliber_version, now,
        ),
    )

    return Layer1Result(
        krippendorff_alpha=alpha,
        span_precision=precision,
        span_recall=recall,
        span_f1=f1,
        passed=passed,
    )
