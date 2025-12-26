from typing import Dict


def explain(intent: str, analytics_result: Dict) -> str:
    """
    Generate a human-readable explanation based on intent and analytics output.
    """
    intent = intent.upper()

    if intent == "SUMMARY":
        return explain_summary(analytics_result)

    if intent == "TREND":
        return explain_trend(analytics_result)

    if intent == "COMPARE":
        return explain_compare(analytics_result)

    if intent == "RANK":
        return explain_rank(analytics_result)

    if intent == "WHY":
        return explain_why(analytics_result)

    return "This question type is not supported."


def explain_summary(result: Dict) -> str:
    total_revenue = result.get("total_revenue")
    total_units = result.get("total_units_sold")
    revenue_by_region = result.get("revenue_by_region", {})

    top_region = max(revenue_by_region, key=revenue_by_region.get, default=None)

    return (
        f"Overall, total revenue is {total_revenue:.2f} "
        f"with {total_units} units sold. "
        f"The highest contributing region is {top_region}."
    )


def explain_trend(result: Dict) -> str:
    revenue_over_time = result.get("revenue_over_time", {})

    if not revenue_over_time:
        return "No trend data is available."

    values = list(revenue_over_time.values())
    direction = "increased" if values[-1] > values[0] else "decreased"

    return f"Revenue has {direction} over the selected time period."


def explain_compare(result: Dict) -> str:
    key = next(iter(result))
    comparison = result[key]

    if not comparison:
        return "No comparison data available."

    best = max(comparison, key=comparison.get)

    return f"{best} has the highest revenue in this comparison."


def explain_rank(result: Dict) -> str:
    key = next(iter(result))
    ranking = result[key]

    if not ranking:
        return "No ranking data available."

    top_entity = next(iter(ranking))

    return f"The top performer is {top_entity}."


def explain_why(result: Dict) -> str:
    change = result.get("change_percent")
    delta_by_region = result.get("delta_by_region", {})

    if change is None or not delta_by_region:
        return "Insufficient data to explain the change."

    main_driver = min(delta_by_region, key=delta_by_region.get)

    direction = "declined" if change < 0 else "increased"

    return (
        f"Sales have {direction} by {abs(change):.1f}%. "
        f"The primary contributor to this change is the {main_driver} region."
    )
