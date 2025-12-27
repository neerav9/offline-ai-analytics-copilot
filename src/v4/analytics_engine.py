import pandas as pd
from typing import List, Dict


# -----------------------
# Core analytics
# -----------------------

def run_summary(df: pd.DataFrame) -> Dict[str, float]:
    """
    Summary over canonical measure.
    """
    result = {
        "total_measure": float(df["measure"].sum())
    }

    if "entity" in df.columns:
        result["entity_count"] = int(df["entity"].nunique())

    return result


def run_rank(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Rank entities by measure.
    """
    if "entity" not in df.columns:
        raise ValueError("Ranking requires entity column")

    ranked = (
        df.groupby("entity")["measure"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "ranking": ranked.to_dict()
    }


def run_compare(df: pd.DataFrame, dimensions: List[str]) -> Dict[str, Dict]:
    """
    Compare measure across one or more dimensions.
    """
    if not dimensions:
        raise ValueError("Comparison requires at least one dimension")

    grouped = (
        df.groupby(dimensions)["measure"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "comparison": grouped.to_dict()
    }


def run_trend(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Trend of measure over time.
    """
    if "time" not in df.columns:
        raise ValueError("Trend requires time column")

    trend = (
        df.groupby("time")["measure"]
        .sum()
        .sort_index()
    )

    return {
        "trend": trend.to_dict()
    }
