import pandas as pd
from typing import Dict


# -----------------------------
# SUMMARY
# -----------------------------
from typing import TypedDict, List


class SummaryResult(TypedDict):
    total_measure: float
    entity_count: int


class RankResult(TypedDict):
    ranking: dict


class TrendResult(TypedDict):
    trend: dict
class CompareResult(TypedDict):
    comparison: dict


def run_summary(canonical_df: pd.DataFrame) -> SummaryResult:
    """
    Compute summary statistics for the active measure.
    """
    if "measure" not in canonical_df.columns:
        return {}

    result = {
        "total_measure": float(canonical_df["measure"].sum())
    }

    if "entity" in canonical_df.columns:
        result["entity_count"] = canonical_df["entity"].nunique()

    return result


# -----------------------------
# RANK
# -----------------------------

def run_rank(canonical_df: pd.DataFrame) -> RankResult:
    """
    Rank entities by the active measure.
    """
    if "measure" not in canonical_df.columns or "entity" not in canonical_df.columns:
        return {}

    ranking = (
        canonical_df
        .groupby("entity", dropna=False)["measure"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "ranking": ranking.to_dict()
    }


# -----------------------------
# TREND
# -----------------------------

def run_trend(canonical_df: pd.DataFrame) -> TrendResult:
    """
    Compute trend of the active measure over time.
    """
    if "measure" not in canonical_df.columns or "time" not in canonical_df.columns:
        return {}

    trend = (
        canonical_df
        .groupby("time", dropna=False)["measure"]
        .sum()
        .sort_index()
    )

    return {
        "trend": trend.to_dict()
    }


# -----------------------------
# COMPARE
# -----------------------------

def run_compare(canonical_df: pd.DataFrame) -> CompareResult:
    """
    Compare active measure across available dimensions.
    """
    if "measure" not in canonical_df.columns:
        return {}

    dimension_cols = [
        c for c in canonical_df.columns if c.startswith("dimension_")
    ]

    if not dimension_cols:
        return {}

    comparisons = {}

    for dim in dimension_cols:
        grouped = (
            canonical_df
            .groupby(dim, dropna=False)["measure"]
            .sum()
            .sort_values(ascending=False)
        )
        comparisons[dim] = grouped.to_dict()

    return {
        "comparisons": comparisons
    }
