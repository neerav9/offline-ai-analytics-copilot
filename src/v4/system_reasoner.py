from typing import Dict, List
import pandas as pd


def reason_about_capabilities(canonical_df: pd.DataFrame) -> Dict[str, any]:
    """
    Determine which analytics are safe to run based on the canonical dataframe.

    This function is:
    - Stateless
    - Deterministic
    - Measure-agnostic

    Returns:
        {
            enabled: List[str],
            disabled: Dict[str, str],
            assumptions: List[str],
            risks: List[str],
        }
    """

    enabled: List[str] = []
    disabled: Dict[str, str] = {}
    assumptions: List[str] = []
    risks: List[str] = []

    columns = set(canonical_df.columns)

    has_measure = "measure" in columns
    has_entity = "entity" in columns
    has_time = "time" in columns
    has_dimension = any(c.startswith("dimension_") for c in columns)

    # -----------------------------
    # SUMMARY
    # -----------------------------
    if has_measure:
        enabled.append("summary")
    else:
        disabled["summary"] = "Required canonical field missing: measure"

    # -----------------------------
    # RANK
    # -----------------------------
    if has_measure and has_entity:
        enabled.append("rank")
    else:
        disabled["rank"] = "Requires both measure and entity"

    # -----------------------------
    # TREND
    # -----------------------------
    if has_measure and has_time:
        enabled.append("trend")

        unique_times = canonical_df["time"].nunique(dropna=True)
        if unique_times <= 1:
            risks.append(
                "Single time value limits trend depth"
            )
    else:
        disabled["trend"] = "Requires both measure and time"

    # -----------------------------
    # COMPARE
    # -----------------------------
    if has_measure and has_dimension:
        enabled.append("compare")
    else:
        disabled["compare"] = "Requires measure and at least one dimension"

    # -----------------------------
    # Assumptions
    # -----------------------------
    if has_measure:
        assumptions.append(
            "Measure values are comparable across records"
        )

    if has_entity:
        assumptions.append(
            "Each entity represents a distinct comparable unit"
        )

    # -----------------------------
    # Data quality risks
    # -----------------------------
    if has_measure:
        variance = canonical_df["measure"].var()
        if variance is not None and variance == 0:
            risks.append(
                "Zero variance in measure reduces analytical usefulness"
            )

    return {
        "enabled": enabled,
        "disabled": disabled,
        "assumptions": assumptions,
        "risks": risks,
    }
