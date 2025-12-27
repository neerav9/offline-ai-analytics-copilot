# src/explanation/explainer.py
from typing import Dict, Any


def explain(intent: str, result: Dict[str, Any]) -> str:
    """
    Generate a domain-agnostic explanation for analytics results.

    This explainer is V4-compatible:
    - No sales-specific language
    - Uses measure/entity/time abstractions
    - Safe for unknown datasets
    """

    intent = intent.upper()

    # -------------------------
    # SUMMARY
    # -------------------------
    if intent == "SUMMARY":
        parts = []

        total = result.get("total_measure")
        count = result.get("entity_count")

        if total is not None:
            parts.append(
                f"The total value of the selected measure across all records is {total:.2f}."
            )

        if count is not None:
            parts.append(
                f"The analysis includes {count} distinct entities."
            )

        if not parts:
            return "A summary was computed, but no interpretable metrics were available."

        return " ".join(parts)

    # -------------------------
    # RANK
    # -------------------------
    if intent == "RANK":
        ranking = result.get("ranking")

        if not ranking:
            return "Ranking could not be generated due to insufficient data."

        top_entity = next(iter(ranking))
        top_value = ranking[top_entity]

        return (
            f"Entities were ranked by the selected measure. "
            f"The top-ranked entity is {top_entity} with a value of {top_value}."
        )

    # -------------------------
    # TREND
    # -------------------------
    if intent == "TREND":
        trend = result.get("trend")

        if not trend:
            return "Trend analysis was attempted, but no time-based variation was available."

        time_points = len(trend)

        if time_points == 1:
            return (
                "The trend shows a single time point. "
                "This limits trend interpretation, but the aggregated value was computed safely."
            )

        return (
            f"Trend analysis was performed across {time_points} time points, "
            "showing how the selected measure evolves over time."
        )

    # -------------------------
    # COMPARE
    # -------------------------
    if intent == "COMPARE":
        comparisons = result.get("comparison")

        if not comparisons:
            return (
                "Comparison analysis could not be completed because "
                "no valid categorical dimensions were available."
            )

        return (
            "The measure was compared across different categories, "
            "highlighting relative differences between groups."
        )

    # -------------------------
    # FALLBACK
    # -------------------------
    return (
        "The analysis completed successfully, "
        "but no detailed explanation is available for this operation."
    )
