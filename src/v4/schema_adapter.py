import pandas as pd
from typing import Dict, List


class SchemaValidationError(Exception):
    """Raised when required canonical fields are missing."""
    pass


def build_canonical_dataframe(
    df: pd.DataFrame,
    confirmed_mappings: Dict[str, any]
) -> pd.DataFrame:
    """
    Build a canonical dataframe based on confirmed semantic mappings.

    Canonical columns:
    - measure        (required)
    - dimensions[]   (optional)
    - entity         (optional)
    - time           (optional)

    Returns:
        pd.DataFrame with renamed canonical columns
    """

    # -----------------------
    # Validate required field
    # -----------------------
    if not confirmed_mappings.get("measure"):
        raise SchemaValidationError(
            "Missing required canonical field: measure"
        )

    canonical_df = pd.DataFrame()

    # -----------------------
    # Measure (required)
    # -----------------------
    measure_col = confirmed_mappings["measure"]
    canonical_df["measure"] = df[measure_col]

    # -----------------------
    # Entity (optional)
    # -----------------------
    if confirmed_mappings.get("entity"):
        entity_col = confirmed_mappings["entity"]
        canonical_df["entity"] = df[entity_col]

    # -----------------------
    # Time (optional)
    # -----------------------
    if confirmed_mappings.get("time"):
        time_col = confirmed_mappings["time"]
        canonical_df["time"] = pd.to_datetime(df[time_col], errors="coerce")

    # -----------------------
    # Dimensions (0..N)
    # -----------------------
    dimensions: List[str] = confirmed_mappings.get("dimensions", [])

    for idx, dim_col in enumerate(dimensions):
        canonical_df[f"dimension_{idx+1}"] = df[dim_col]

    return canonical_df
