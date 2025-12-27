import pandas as pd
from typing import Dict, List


class SchemaValidationError(Exception):
    """Raised when canonical schema requirements are violated."""
    pass


def build_canonical_dataframe(
    df: pd.DataFrame,
    confirmed_mappings: Dict[str, any],
    active_measure: str
) -> pd.DataFrame:
    """
    Build a canonical dataframe using a single active measure.

    Canonical columns:
    - measure        (required, exactly one at runtime)
    - entity         (optional)
    - time           (optional)
    - dimension_1..N (optional)

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset
    confirmed_mappings : dict
        Output of human-confirmed semantic mappings
    active_measure : str
        One of the confirmed measure columns to analyze

    Returns
    -------
    pd.DataFrame
        Canonical dataframe
    """

    # -----------------------
    # Validate measures
    # -----------------------
    measures: List[str] = confirmed_mappings.get("measures", [])

    if not measures:
        raise SchemaValidationError(
            "No measures confirmed. At least one numeric measure is required."
        )

    if active_measure not in measures:
        raise SchemaValidationError(
            f"Active measure '{active_measure}' is not in confirmed measures: {measures}"
        )

    # -----------------------
    # Build canonical DF
    # -----------------------
    canonical_df = pd.DataFrame()

    # ---- Measure (required, singular) ----
    canonical_df["measure"] = df[active_measure]

    # ---- Entity (optional) ----
    entity_col = confirmed_mappings.get("entity")
    if entity_col:
        canonical_df["entity"] = df[entity_col]

    # ---- Time (optional) ----
    time_col = confirmed_mappings.get("time")
    if time_col:
        canonical_df["time"] = pd.to_datetime(
            df[time_col], errors="coerce"
        )

    # ---- Dimensions (0..N) ----
    dimensions: List[str] = confirmed_mappings.get("dimensions", [])

    for idx, dim_col in enumerate(dimensions):
        canonical_df[f"dimension_{idx + 1}"] = df[dim_col]

    # -----------------------
    # Final sanity checks
    # -----------------------
    if canonical_df["measure"].isna().all():
        raise SchemaValidationError(
            "Active measure column contains only null values."
        )

    return canonical_df
