from typing import Dict, Any, List


"""
V4 Semantic Mapper

Purpose:
Map dataset schema signals to domain-agnostic analytics primitives.

Canonical primitives:
- measure        (numeric, required)
- dimensions[]   (categorical, optional, multiple)
- entity         (categorical, optional)
- time           (date, optional)

All mappings are proposals and MUST be human-confirmed.
Deterministic, explainable, offline-safe.
"""


# -------------------------------
# Keyword hints (domain-agnostic)
# -------------------------------

KEYWORD_HINTS = {
    "measure": [
        "total", "amount", "score", "marks", "value", "sum", "points"
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


# -------------------------------
# Helper scoring functions
# -------------------------------

def score_name_match(column_name: str, target: str) -> float:
    """
    Score column name against keyword hints.
    """
    name = column_name.lower()
    for kw in KEYWORD_HINTS.get(target, []):
        if kw in name:
            return 0.4
    return 0.0


def score_type_match(column_type: str, target: str) -> float:
    """
    Score based on inferred column type.
    """
    if target == "measure" and column_type == "numeric":
        return 0.4
    if target in ["entity", "dimension"] and column_type == "categorical":
        return 0.3
    if target == "time" and column_type == "date":
        return 0.4
    return 0.0


def score_numeric_behavior(signals: Dict[str, Any]) -> float:
    """
    Score numeric behavior suitable for a measure.
    """
    if not signals:
        return 0.0

    score = 0.0

    if signals.get("max", 0) > signals.get("mean", 0):
        score += 0.2

    if signals.get("unique_count", 0) > 3:
        score += 0.2

    return score


# -------------------------------
# Output structure
# -------------------------------

def initialize_mapping_output() -> Dict[str, Any]:
    return {
        "measure": None,
        "dimensions": [],
        "entity": None,
        "time": None
    }


# -------------------------------
# Core proposal logic
# -------------------------------

def propose_mappings(schema_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose semantic mappings using deterministic heuristics.
    """
    mappings = initialize_mapping_output()

    for column, info in schema_report.items():
        col_type = info["type"]
        signals = info.get("signals", {})
        col_name = column.lower()

        # ---- Measure ----
        if col_type == "numeric" and mappings["measure"] is None:
            score = 0.0
            evidence = []

            s = score_name_match(column, "measure")
            if s:
                score += s
                evidence.append("name_signal")

            s = score_type_match(col_type, "measure")
            if s:
                score += s
                evidence.append("type_match")

            s = score_numeric_behavior(signals)
            if s:
                score += s
                evidence.append("numeric_behavior")

            if score >= 0.6:
                mappings["measure"] = {
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": evidence
                }
                continue

        # ---- Time ----
        if col_type == "date" and mappings["time"] is None:
            score = score_type_match(col_type, "time") + score_name_match(column, "time")

            if score >= 0.4:
                mappings["time"] = {
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": ["date_type"]
                }
                continue

        # ---- Entity ----
        if col_type == "categorical" and mappings["entity"] is None:
            score = score_name_match(column, "entity") + score_type_match(col_type, "entity")

            if score >= 0.4:
                mappings["entity"] = {
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": ["entity_name_signal"]
                }
                continue

        # ---- Dimension (plural) ----
        if col_type == "categorical":
            score = score_name_match(column, "dimension") + score_type_match(col_type, "dimension")

            if score >= 0.3:
                mappings["dimensions"].append({
                    "column": column,
                    "confidence": round(score, 2),
                    "evidence": ["categorical_grouping"]
                })

    return mappings


# -------------------------------
# Human confirmation (critical)
# -------------------------------

def confirm_mappings(proposed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Human-in-the-loop confirmation of proposed mappings.
    """
    confirmed = {
        "measure": None,
        "dimensions": [],
        "entity": None,
        "time": None
    }

    print("\n=== HUMAN CONFIRMATION REQUIRED ===\n")

    for key in ["measure", "entity", "time"]:
        proposal = proposed.get(key)
        if not proposal:
            continue

        print("-" * 40)
        print(f"Canonical field : {key}")
        print(f"Proposed column : {proposal['column']}")
        print(f"Confidence      : {proposal['confidence']}")
        print(f"Evidence        : {', '.join(proposal['evidence'])}")

        decision = input("Accept mapping? (y/n): ").strip().lower()
        if decision == "y":
            confirmed[key] = proposal["column"]

    for dim in proposed.get("dimensions", []):
        print("-" * 40)
        print("Canonical field : dimension")
        print(f"Proposed column : {dim['column']}")
        print(f"Confidence      : {dim['confidence']}")
        print(f"Evidence        : {', '.join(dim['evidence'])}")

        decision = input("Accept as dimension? (y/n): ").strip().lower()
        if decision == "y":
            confirmed["dimensions"].append(dim["column"])

    return confirmed
