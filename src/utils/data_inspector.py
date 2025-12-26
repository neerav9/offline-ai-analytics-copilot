import pandas as pd
from typing import Dict, Any


def inspect_shape(df: pd.DataFrame) -> Dict[str, int]:
    """
    Inspect dataset shape.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
    }


def inspect_missing_values(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Inspect missing values per column.
    """
    report = {}

    total_rows = len(df)

    for column in df.columns:
        missing_count = df[column].isna().sum()
        missing_percent = (missing_count / total_rows) * 100 if total_rows > 0 else 0

        report[column] = {
            "missing_count": int(missing_count),
            "missing_percent": round(missing_percent, 2),
        }

    return report


def inspect_duplicates(df: pd.DataFrame, key_column: str = None) -> Dict[str, Any]:
    """
    Inspect duplicate rows and optional key-based duplicates.
    """
    report = {
        "total_duplicate_rows": int(df.duplicated().sum())
    }

    if key_column and key_column in df.columns:
        report["duplicate_by_key"] = int(df[key_column].duplicated().sum())
    else:
        report["duplicate_by_key"] = None

    return report


def inspect_numeric_sanity(df: pd.DataFrame) -> Dict[str, str]:
    """
    Perform basic numeric sanity checks.
    """
    checks = {}

    # Check revenue consistency if required columns exist
    required_cols = {"units_sold", "unit_price", "revenue"}

    if required_cols.issubset(df.columns):
        calculated_revenue = df["units_sold"] * df["unit_price"]
        difference = (df["revenue"] - calculated_revenue).abs()

        if (difference > 0.01).any():
            checks["revenue_consistency"] = "FAIL"
        else:
            checks["revenue_consistency"] = "PASS"
    else:
        checks["revenue_consistency"] = "NOT_APPLICABLE"

    return checks


def inspect_dataset(df: pd.DataFrame, key_column: str = None) -> Dict[str, Any]:
    """
    Run full dataset inspection and return structured report.
    """
    return {
        "shape": inspect_shape(df),
        "missing_values": inspect_missing_values(df),
        "duplicates": inspect_duplicates(df, key_column),
        "numeric_checks": inspect_numeric_sanity(df),
    }
