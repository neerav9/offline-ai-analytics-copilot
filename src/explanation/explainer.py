from typing import Dict


def explain(intent: str, analytics_result: dict) -> str:
    intent = intent.upper()

    if intent == "SUMMARY":
        parts = []

        if "total_revenue" in analytics_result:
            parts.append(
                f"Overall, total value is {analytics_result['total_revenue']:.2f}."
            )

        if "total_units_sold" in analytics_result:
            parts.append(
                f"Total units counted: {analytics_result['total_units_sold']}."
            )

        if "revenue_by_category" in analytics_result:
            top_category = max(
                analytics_result["revenue_by_category"],
                key=analytics_result["revenue_by_category"].get
            )
            parts.append(
                f"The highest contributing category is {top_category}."
            )

        return " ".join(parts) if parts else "No summary metrics available."

    if intent == "RANK":
        top_key = next(iter(analytics_result))
        top_entity = max(analytics_result[top_key], key=analytics_result[top_key].get)
        return f"The top performer is {top_entity}."

    if intent == "COMPARE":
        top_key = next(iter(analytics_result))
        top_category = max(analytics_result[top_key], key=analytics_result[top_key].get)
        return f"{top_category} has the highest contribution in this comparison."

    if intent == "TREND":
        return "Trend analysis completed over the available time range."

    return "Explanation not available for this analysis."


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
