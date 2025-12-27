from typing import Dict, Any, List


"""
V4.1 Semantic Mapper

Purpose:
Detect analytics primitives from an unknown dataset.

Canonical primitives:
- measures[]     (numeric, multiple allowed)
- entity         (categorical, optional)
- time           (date, optional)
- dimensions[]   (categorical, optional)

All mappings are PROPOSALS and require human confirmation.
Deterministic, explainable, offline-safe.
"""


# ----------------------------------
# Keyword hints (domain-agnostic)
# ----------------------------------

KEYWORD_HINTS = {
    "measure": [
        "total", "amount", "value", "score", "marks", "points", "count", "sum"
    ],
    "entity": [
        "name", "id", "student", "employee", "customer", "user", "person"
    ],
    "time": [
        "date", "time", "year", "month", "day"
    ],
    "dimension": [
        "region", "category", "type", "subject", "department", "class", "group"
    ],
}


# ----------------------------------
# Scoring helpers
# ----------------------------------

def score_name_match(column_name: str, target: str) -> float:
    name = column_name.lower()
    for kw in KEYWORD_HINTS.get(target, []):
        if kw in name:
            return 0.4
    return 0.0


def score_type_match(column_type: str, target: str) -> float:
    if target == "measure" and column_type == "numeric":
        return 0.4
    if target in ["entity", "dimension"] and column_type == "categorical":
        return 0.3
    if target == "time" and column_type == "date":
        return 0.4
    return 0.0


def score_numeric_behavior(signals: Dict[str, Any]) -> float:
    if not signals:
        return 0.0

    score = 0.0

    if signals.get("unique_count", 0) > 3:
        score += 0.2

    if signals.get("max", 0) > signals.get("mean", 0):
        score += 0.2

    return score


# ----------------------------------
# Proposal initialization
# ----------------------------------

def initialize_proposals() -> Dict[str, Any]:
    return {
        "measures": [],      # ← MULTI-MEASURE
        "entity": None,
        "time": None,
        "dimensions": []
    }


# ----------------------------------
# Core proposal logic
# ----------------------------------

def propose_mappings(schema_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate semantic mapping proposals using deterministic heuristics.
    """
    proposals = initialize_proposals()

    for column, info in schema_report.items():
        col_type = info["type"]
        signals = info.get("signals", {})

        # -----------------------
        # MEASURE (multiple)
        # -----------------------
        if col_type == "numeric":
            score = 0.0
            evidence = []

            s = score_type_match(col_type, "measure")
            if s:
                score += s
                evidence.append("numeric_type")

            s = score_name_match(column, "measure")
            if s:
                score += s
                evidence.append("name_signal")

            s = score_numeric_behavior(signals)
            if s:
                score += s
                evidence.append("numeric_behavior")

            if score >= 0.6:
                proposals["measures"].append({
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": evidence
                })
                continue

        # -----------------------
        # TIME
        # -----------------------
        if col_type == "date" and proposals["time"] is None:
            score = score_type_match(col_type, "time") + score_name_match(column, "time")

            if score >= 0.4:
                proposals["time"] = {
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": ["date_type"]
                }
                continue

        # -----------------------
        # ENTITY
        # -----------------------
        if col_type == "categorical" and proposals["entity"] is None:
            score = score_type_match(col_type, "entity") + score_name_match(column, "entity")

            if score >= 0.4:
                proposals["entity"] = {
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": ["entity_signal"]
                }
                continue

        # -----------------------
        # DIMENSIONS (multiple)
        # -----------------------
        if col_type == "categorical":
            score = score_type_match(col_type, "dimension") + score_name_match(column, "dimension")

            if score >= 0.3:
                proposals["dimensions"].append({
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": ["categorical_dimension"]
                })

    return proposals


# ----------------------------------
# Human confirmation
# ----------------------------------

def confirm_mappings(proposed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Human-in-the-loop confirmation of semantic mappings.
    """
    confirmed = {
        "measures": [],
        "entity": None,
        "time": None,
        "dimensions": []
    }

    print("\n=== HUMAN CONFIRMATION REQUIRED ===\n")

    # -----------------------
    # MEASURES
    # -----------------------
    for m in proposed.get("measures", []):
        print("-" * 40)
        print("Canonical field : measure")
        print(f"Proposed column : {m['column']}")
        print(f"Confidence      : {m['confidence']}")
        print(f"Evidence        : {', '.join(m['evidence'])}")

        decision = input("Accept as measure? (y/n): ").strip().lower()
        if decision == "y":
            confirmed["measures"].append(m["column"])

    # -----------------------
    # ENTITY
    # -----------------------
    if proposed.get("entity"):
        e = proposed["entity"]
        print("-" * 40)
        print("Canonical field : entity")
        print(f"Proposed column : {e['column']}")
        print(f"Confidence      : {e['confidence']}")
        print(f"Evidence        : {', '.join(e['evidence'])}")

        if input("Accept entity? (y/n): ").strip().lower() == "y":
            confirmed["entity"] = e["column"]

    # -----------------------
    # TIME
    # -----------------------
    if proposed.get("time"):
        t = proposed["time"]
        print("-" * 40)
        print("Canonical field : time")
        print(f"Proposed column : {t['column']}")
        print(f"Confidence      : {t['confidence']}")
        print(f"Evidence        : {', '.join(t['evidence'])}")

        if input("Accept time? (y/n): ").strip().lower() == "y":
            confirmed["time"] = t["column"]

    # -----------------------
    # DIMENSIONS
    # -----------------------
    for d in proposed.get("dimensions", []):
        print("-" * 40)
        print("Canonical field : dimension")
        print(f"Proposed column : {d['column']}")
        print(f"Confidence      : {d['confidence']}")
        print(f"Evidence        : {', '.join(d['evidence'])}")

        if input("Accept dimension? (y/n): ").strip().lower() == "y":
            confirmed["dimensions"].append(d["column"])

    return confirmed
