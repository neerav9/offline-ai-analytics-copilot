from typing import Dict, Any, List
from src.v3.canonical_schema import get_all_fields


# --- keyword hints (deterministic, explainable) ---
KEYWORD_HINTS = {
    "revenue": ["revenue", "sales", "amount", "total"],
    "units_sold": ["units", "qty", "quantity", "count"],
    "unit_price": ["price", "cost", "rate"],
    "order_date": ["date", "time"],
    "category": ["region", "area", "category", "segment"],
    "entity_name": ["product", "item", "salesperson", "rep", "agent"]
}


def score_column_name(column: str, canonical_field: str) -> float:
    """
    Score based on keyword presence in column name.
    """
    column_lower = column.lower()
    keywords = KEYWORD_HINTS.get(canonical_field, [])

    for kw in keywords:
        if kw in column_lower:
            return 0.6  # strong signal

    return 0.0


def score_type_match(column_type: str, expected_type: str) -> float:
    """
    Score if inferred type matches canonical expectation.
    """
    return 0.2 if column_type == expected_type else 0.0


def score_numeric_behavior(signals: Dict[str, Any], canonical_field: str) -> float:
    """
    Score numeric behavior patterns.
    """
    if not signals:
        return 0.0

    score = 0.0

    if canonical_field == "units_sold":
        if signals.get("is_integer_like") and signals.get("max", 0) < 1000:
            score += 0.3

    if canonical_field == "unit_price":
        if signals.get("max", 0) > 10:
            score += 0.3

    if canonical_field == "revenue":
        if signals.get("max", 0) > 100:
            score += 0.3

    return score


def propose_mappings(schema_report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Propose canonical field mappings with confidence scores.
    """
    proposals = {}
    canonical_fields = get_all_fields()

    for canonical_field, expected_type in canonical_fields.items():
        best_candidate = None
        best_score = 0.0
        evidence: List[str] = []

        for column, info in schema_report.items():
            score = 0.0
            signals = info.get("signals", {})

            # Layer 1: column name
            name_score = score_column_name(column, canonical_field)
            if name_score > 0:
                score += name_score
                evidence.append("column_name_match")

            # Layer 2: type match
            type_score = score_type_match(info["type"], expected_type)
            if type_score > 0:
                score += type_score
                evidence.append("type_match")

            # Layer 3: numeric behavior
            behavior_score = score_numeric_behavior(signals, canonical_field)
            if behavior_score > 0:
                score += behavior_score
                evidence.append("numeric_behavior")

            if score > best_score:
                best_score = score
                best_candidate = column

        if best_candidate and best_score > 0:
            proposals[canonical_field] = {
                "column": best_candidate,
                "confidence": round(min(best_score, 1.0), 2),
                "evidence": list(set(evidence))
            }

    return proposals
