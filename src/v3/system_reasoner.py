from typing import Dict, List


def reason_about_system(canonical_df, confirmed_mappings: Dict) -> Dict:
    columns = set(canonical_df.columns)

    reasoning = {
        "dataset_shape": None,
        "enabled_analyses": [],
        "disabled_analyses": {},
        "assumptions": [],
        "risks": [],
    }

    # ---- Dataset shape detection ----
    has_entity = "entity_name" in columns
    has_metric = "revenue" in columns
    has_time = "order_date" in columns
    has_category = "category" in columns

    if has_entity and has_metric and has_time:
        reasoning["dataset_shape"] = "Entity–Metric–Time"
    elif has_entity and has_metric:
        reasoning["dataset_shape"] = "Entity–Metric"
    elif has_metric and has_time:
        reasoning["dataset_shape"] = "Metric–Time"
    elif has_metric:
        reasoning["dataset_shape"] = "Metric-only"
    else:
        reasoning["dataset_shape"] = "Unsupported"

    # ---- Enabled / disabled analytics ----
    if has_metric:
        reasoning["enabled_analyses"].append("Summary")
    else:
        reasoning["disabled_analyses"]["Summary"] = "Primary metric not available"

    if has_entity and has_metric:
        reasoning["enabled_analyses"].append("Ranking")
    else:
        reasoning["disabled_analyses"]["Ranking"] = "Entity or metric missing"

    if has_category and has_metric:
        reasoning["enabled_analyses"].append("Comparison")
    else:
        reasoning["disabled_analyses"]["Comparison"] = "Category not mapped"

    if has_time and has_metric:
        reasoning["enabled_analyses"].append("Trend")
    else:
        reasoning["disabled_analyses"]["Trend"] = "Time field not available"

    # ---- Assumptions ----
    if has_metric:
        reasoning["assumptions"].append(
            "Metric values are comparable across records"
        )

    if has_category:
        reasoning["assumptions"].append(
            "Categories are mutually exclusive"
        )

    # ---- Risks ----
    if has_metric and canonical_df["revenue"].nunique() < 5:
        reasoning["risks"].append(
            "Low metric variance may reduce ranking reliability"
        )

    if has_time and canonical_df["order_date"].nunique() == 1:
        reasoning["risks"].append(
            "Single time value limits trend analysis depth"
        )

    return reasoning
