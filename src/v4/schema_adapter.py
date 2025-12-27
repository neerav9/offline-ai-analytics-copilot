import pandas as pd
from typing import Dict, List


class SchemaValidationError(Exception):
    """Raised when required canonical fields are missing or invalid."""
    pass


def build_canonical_dataframe(
    df: pd.DataFrame,
    confirmed_mappings: Dict,
    active_measure: str
) -> pd.DataFrame:
    """
    Build canonical dataframe using a runtime-selected active measure.

    Canonical columns:
    - measure        (required, selected at runtime)
    - entity         (optional)
    - time           (optional)
    - dimension_1..N (optional)

    Parameters:
        df: original dataframe
        confirmed_mappings: output of semantic mapper (measures, entity, time, dimensions)
        active_measure: selected measure column name

    Returns:
        Canonical pandas DataFrame
    """

    measures: List[str] = confirmed_mappings.get("measures", [])

    if not measures:
        raise SchemaValidationError("No measures confirmed.")

    if active_measure not in measures:
        raise SchemaValidationError(
            f"Active measure '{active_measure}' not in confirmed measures: {measures}"
        )

    canonical_df = pd.DataFrame()

    # -----------------------
    # Measure (required)
    # -----------------------
    canonical_df["measure"] = df[active_measure]

    # -----------------------
    # Entity (optional)
    # -----------------------
    if confirmed_mappings.get("entity"):
        canonical_df["entity"] = df[confirmed_mappings["entity"]]

    # -----------------------
    # Time (optional)
    # -----------------------
    if confirmed_mappings.get("time"):
        canonical_df["time"] = pd.to_datetime(
            df[confirmed_mappings["time"]],
            errors="coerce"
        )

    # -----------------------
    # Dimensions (0..N)
    # -----------------------
    dimensions = confirmed_mappings.get("dimensions", [])

    for idx, dim in enumerate(dimensions, start=1):
        canonical_df[f"dimension_{idx}"] = df[dim]

    return canonical_df
