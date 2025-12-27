import pandas as pd
from typing import Dict, Any, List


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

def run_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute a safe summary over the active measure.
    """
    result = {}

    if "measure" not in df.columns:
        return result

    result["total_measure"] = float(df["measure"].sum())

    if "entity" in df.columns:
        result["entity_count"] = df["entity"].nunique()

    return result


# --------------------------------------------------
# RANK
# --------------------------------------------------

def run_rank(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Rank entities by the active measure.
    """
    if "entity" not in df.columns:
        raise ValueError("Ranking requires an entity column.")

    ranking = (
        df.groupby("entity")["measure"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    return {"ranking": ranking}


# --------------------------------------------------
# TREND
# --------------------------------------------------

def run_trend(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Aggregate measure over time.
    """
    if "time" not in df.columns:
        raise ValueError("Trend analysis requires a time column.")

    trend = (
        df.groupby("time")["measure"]
        .sum()
        .sort_index()
        .to_dict()
    )

    return {"trend": trend}


# --------------------------------------------------
# COMPARE
# --------------------------------------------------

def run_compare(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compare measure across all available dimensions.
    """
    dimensions: List[str] = [
        c for c in df.columns if c.startswith("dimension_")
    ]

    if not dimensions:
        raise ValueError("Comparison requires at least one dimension.")

    comparisons = {}

    for dim in dimensions:
        comparisons[dim] = (
            df.groupby(dim)["measure"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )

    return {"comparison": comparisons}
