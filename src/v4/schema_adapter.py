import pandas as pd
from typing import Dict, List, Optional


class SchemaValidationError(Exception):
    """Raised when canonical schema requirements are violated."""
    pass


def build_canonical_dataframe(
    df: pd.DataFrame,
    confirmed_mappings: Dict[str, any],
    active_measure: str,
) -> pd.DataFrame:
    """
    Build a canonical dataframe using a runtime-selected active measure.

    This function is:
    - Stateless
    - Deterministic
    - Safe to call multiple times

    Canonical columns produced:
    - measure        (required, runtime-selected)
    - entity         (optional)
    - time           (optional)
    - dimension_1..N (optional)
    """

    # -----------------------------
    # Validate inputs
    # -----------------------------

    if not active_measure:
        raise SchemaValidationError("Active measure is not specified.")

    measures: List[str] = confirmed_mappings.get("measures", [])
    if active_measure not in measures:
        raise SchemaValidationError(
            f"Active measure '{active_measure}' was not confirmed earlier."
        )

    if active_measure not in df.columns:
        raise SchemaValidationError(
            f"Active measure column '{active_measure}' does not exist in dataset."
        )

    # -----------------------------
    # Build canonical dataframe
    # -----------------------------

    canonical_df = pd.DataFrame()

    # ---- Measure (required) ----
    canonical_df["measure"] = df[active_measure]

    # ---- Entity (optional) ----
    entity_col: Optional[str] = confirmed_mappings.get("entity")
    if entity_col:
        if entity_col not in df.columns:
            raise SchemaValidationError(
                f"Entity column '{entity_col}' not found in dataset."
            )
        canonical_df["entity"] = df[entity_col]

    # ---- Time (optional) ----
    time_col: Optional[str] = confirmed_mappings.get("time")
    if time_col:
        if time_col not in df.columns:
            raise SchemaValidationError(
                f"Time column '{time_col}' not found in dataset."
            )
        canonical_df["time"] = pd.to_datetime(
            df[time_col], errors="coerce"
        )

    # ---- Dimensions (0..N) ----
    dimensions: List[str] = confirmed_mappings.get("dimensions", [])

    for idx, dim_col in enumerate(dimensions):
        if dim_col not in df.columns:
            raise SchemaValidationError(
                f"Dimension column '{dim_col}' not found in dataset."
            )
        canonical_df[f"dimension_{idx + 1}"] = df[dim_col]

    return canonical_df
