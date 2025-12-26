import pandas as pd
from typing import Dict, Any


def infer_column_type(series: pd.Series) -> str:
    """
    Infer high-level data type of a column.
    Includes safe detection of date-like strings.
    """
    # Already datetime
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    # Numeric
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    # Try parsing strings as dates (SAFE check)
    if series.dtype == object:
        parsed = pd.to_datetime(series, errors="coerce")
        non_null_ratio = parsed.notna().mean()

        # If most values parse correctly, treat as date
        if non_null_ratio > 0.8:
            return "date"

    return "categorical"



def numeric_signals(series: pd.Series) -> Dict[str, Any]:
    """
    Extract behavioral signals for numeric columns.
    """
    clean = series.dropna()

    return {
        "min": float(clean.min()),
        "max": float(clean.max()),
        "mean": float(clean.mean()),
        "is_integer_like": bool((clean % 1 == 0).all()),
        "unique_count": int(clean.nunique())
    }


def categorical_signals(series: pd.Series) -> Dict[str, Any]:
    """
    Extract behavioral signals for categorical columns.
    """
    clean = series.dropna()

    return {
        "unique_count": int(clean.nunique()),
        "sample_values": clean.unique()[:5].tolist()
    }


def extract_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract dataset schema with behavioral signals.
    """
    schema = {}

    for column in df.columns:
        series = df[column]
        col_type = infer_column_type(series)

        entry = {
            "type": col_type,
            "missing_count": int(series.isna().sum())
        }

        if col_type == "numeric":
            entry["signals"] = numeric_signals(series)

        elif col_type == "categorical":
            entry["signals"] = categorical_signals(series)

        schema[column] = entry

    return schema
