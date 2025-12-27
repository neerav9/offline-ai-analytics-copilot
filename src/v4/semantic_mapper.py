from typing import Dict, Any, List

from src.v4.semantic_advisor import semantic_hint


"""
V4.3 Semantic Mapper (HF-Augmented)

Purpose:
- Detect multiple candidate measures
- Detect entity, time, dimensions
- Use HF as an advisory signal ONLY
- Keep system deterministic + explainable
"""


# -------------------------------
# Thresholds (explicit + safe)
# -------------------------------

MEASURE_SCORE_THRESHOLD = 0.6
ENTITY_SCORE_THRESHOLD = 0.4
TIME_SCORE_THRESHOLD = 0.4
DIMENSION_SCORE_THRESHOLD = 0.3


# -------------------------------
# Deterministic scorers
# -------------------------------

def score_numeric_measure(info: Dict[str, Any]) -> float:
    score = 0.0

    if info["type"] == "numeric":
        score += 0.4

    signals = info.get("signals", {})
    if signals.get("unique_count", 0) > 3:
        score += 0.2

    if signals.get("max", 0) > signals.get("mean", 0):
        score += 0.2

    return round(score, 2)


def score_entity(column: str, info: Dict[str, Any]) -> float:
    score = 0.0
    name = column.lower()

    if info["type"] == "categorical":
        score += 0.3

    if any(k in name for k in ["name", "student", "user", "employee", "person"]):
        score += 0.3

    return round(score, 2)


def score_time(column: str, info: Dict[str, Any]) -> float:
    score = 0.0
    name = column.lower()

    if info["type"] == "date":
        score += 0.4

    if any(k in name for k in ["date", "time", "year", "month"]):
        score += 0.2

    return round(score, 2)


def score_dimension(column: str, info: Dict[str, Any]) -> float:
    score = 0.0
    name = column.lower()

    if info["type"] == "categorical":
        score += 0.2

    if any(k in name for k in ["category", "subject", "region", "type", "group"]):
        score += 0.2

    return round(score, 2)


# -------------------------------
# Proposal generation
# -------------------------------

def propose_mappings(schema_report: Dict[str, Any]) -> Dict[str, Any]:
    proposals = {
        "measures": [],
        "entity": None,
        "time": None,
        "dimensions": [],
    }

    for column, info in schema_report.items():

        # ---- Measure candidates ----
        m_score = score_numeric_measure(info)
        if m_score >= MEASURE_SCORE_THRESHOLD:
            hf = semantic_hint(column)
            proposals["measures"].append({
                "column": column,
                "confidence": m_score,
                "evidence": ["numeric_type", "numeric_behavior"],
                "hf_hint": hf
            })

        # ---- Entity ----
        if proposals["entity"] is None:
            e_score = score_entity(column, info)
            if e_score >= ENTITY_SCORE_THRESHOLD:
                hf = semantic_hint(column)
                proposals["entity"] = {
                    "column": column,
                    "confidence": e_score,
                    "evidence": ["entity_signal"],
                    "hf_hint": hf
                }

        # ---- Time ----
        if proposals["time"] is None:
            t_score = score_time(column, info)
            if t_score >= TIME_SCORE_THRESHOLD:
                hf = semantic_hint(column)
                proposals["time"] = {
                    "column": column,
                    "confidence": t_score,
                    "evidence": ["date_type"],
                    "hf_hint": hf
                }

        # ---- Dimensions ----
        d_score = score_dimension(column, info)
        if d_score >= DIMENSION_SCORE_THRESHOLD:
            hf = semantic_hint(column)
            proposals["dimensions"].append({
                "column": column,
                "confidence": d_score,
                "evidence": ["categorical_grouping"],
                "hf_hint": hf
            })
        # ----------------------------------
        # HF-aware ranking of measure candidates
        # ----------------------------------

        def ranking_score(m):
            hf_conf = 0.0
            if m.get("hf_hint") and m["hf_hint"].get("confidence") is not None:
                hf_conf = m["hf_hint"]["confidence"]

            return round(
                (m["confidence"] * 0.7) + (hf_conf * 0.3),
                3
            )

        proposals["measures"] = sorted(
            proposals["measures"],
            key=ranking_score,
            reverse=True
        )

    return proposals


# -------------------------------
# Human confirmation
# -------------------------------

def confirm_mappings(proposed: Dict[str, Any]) -> Dict[str, Any]:
    confirmed = {
        "measures": [],
        "entity": None,
        "time": None,
        "dimensions": [],
    }

    print("\n=== HUMAN CONFIRMATION REQUIRED ===\n")

    # ---- Measures ----
    for m in proposed.get("measures", []):
        print("-" * 40)
        print("Canonical field : measure")
        print(f"Proposed column : {m['column']}")
        print(f"Confidence      : {m['confidence']}")
        print(f"Evidence        : {', '.join(m['evidence'])}")

        hf = m.get("hf_hint", {})
        if hf.get("suggestion"):
            print(f"HF suggestion   : {hf['suggestion']} (confidence: {hf['confidence']})")

        decision = input("Accept as measure? (y/n): ").strip().lower()
        if decision == "y":
            confirmed["measures"].append(m["column"])

    # ---- Entity ----
    if proposed.get("entity"):
        e = proposed["entity"]
        print("-" * 40)
        print("Canonical field : entity")
        print(f"Proposed column : {e['column']}")
        print(f"Confidence      : {e['confidence']}")
        print(f"Evidence        : {', '.join(e['evidence'])}")

        hf = e.get("hf_hint", {})
        if hf.get("suggestion"):
            print(f"HF suggestion   : {hf['suggestion']} (confidence: {hf['confidence']})")

        if input("Accept entity? (y/n): ").strip().lower() == "y":
            confirmed["entity"] = e["column"]

    # ---- Time ----
    if proposed.get("time"):
        t = proposed["time"]
        print("-" * 40)
        print("Canonical field : time")
        print(f"Proposed column : {t['column']}")
        print(f"Confidence      : {t['confidence']}")
        print(f"Evidence        : {', '.join(t['evidence'])}")

        hf = t.get("hf_hint", {})
        if hf.get("suggestion"):
            print(f"HF suggestion   : {hf['suggestion']} (confidence: {hf['confidence']})")

        if input("Accept time? (y/n): ").strip().lower() == "y":
            confirmed["time"] = t["column"]

    # ---- Dimensions ----
    for d in proposed.get("dimensions", []):
        print("-" * 40)
        print("Canonical field : dimension")
        print(f"Proposed column : {d['column']}")
        print(f"Confidence      : {d['confidence']}")
        print(f"Evidence        : {', '.join(d['evidence'])}")

        hf = d.get("hf_hint", {})
        if hf.get("suggestion"):
            print(f"HF suggestion   : {hf['suggestion']} (confidence: {hf['confidence']})")

        if input("Accept as dimension? (y/n): ").strip().lower() == "y":
            confirmed["dimensions"].append(d["column"])

    return confirmed
