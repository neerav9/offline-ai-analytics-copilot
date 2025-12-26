import pandas as pd
from typing import Dict, Any

from src.core.metrics import (
    total_revenue,
    total_units_sold,
    revenue_by_dimension,
    revenue_over_time,
    revenue_change,
    delta_by_dimension,
)


def run_summary(df):
    result = {}

    if "revenue" in df.columns:
        result["total_revenue"] = df["revenue"].sum()

    if "units_sold" in df.columns:
        result["total_units_sold"] = df["units_sold"].sum()

    if "category" in df.columns and "revenue" in df.columns:
        result["revenue_by_category"] = (
            df.groupby("category")["revenue"].sum().to_dict()
        )

    return result



def run_trend(df: pd.DataFrame, freq: str = "M") -> Dict[str, Any]:
    """
    Handle TREND intent.
    """
    return {
        "revenue_over_time": revenue_over_time(df, freq).to_dict()
    }


def run_compare(df: pd.DataFrame, dimension: str) -> Dict[str, Any]:
    """
    Handle COMPARE intent.
    """
    return {
        f"revenue_by_{dimension}": revenue_by_dimension(df, dimension).to_dict()
    }


def run_rank(df: pd.DataFrame, dimension: str, top_n: int = 5) -> Dict[str, Any]:
    """
    Handle RANK intent.
    """
    ranked = revenue_by_dimension(df, dimension)
    return {
        f"top_{top_n}_{dimension}": ranked.head(top_n).to_dict()
    }


def run_why(
    current_period_df: pd.DataFrame,
    previous_period_df: pd.DataFrame,
    dimension: str = "region",
) -> Dict[str, Any]:
    """
    Handle WHY intent using contribution (delta) analysis.
    """
    current_revenue = total_revenue(current_period_df)
    previous_revenue = total_revenue(previous_period_df)

    change_percent = revenue_change(current_revenue, previous_revenue)

    delta_contribution = delta_by_dimension(
        current_period_df,
        previous_period_df,
        dimension
    ).to_dict()

    return {
        "current_revenue": current_revenue,
        "previous_revenue": previous_revenue,
        "change_percent": change_percent,
        f"delta_by_{dimension}": delta_contribution,
    }
