from typing import Dict
import pandas as pd


def reason_about_capabilities(canonical_df, semantic_context):

    """
    Determine which analytics are safe based on the canonical dataframe.
    Canonical truth:
    - 'measure' column = active numeric measure
    - 'entity' optional
    - 'time' optional
    - 'dimension_*' optional
    """

    enabled = []
    disabled = {}
    assumptions = []
    risks = []

    # -----------------------------
    # Measure existence (CRITICAL)
    # -----------------------------
    if "measure" not in canonical_df.columns:
        disabled["summary"] = "No active measure selected"
        disabled["rank"] = "No active measure selected"
        disabled["trend"] = "No active measure selected"
        disabled["compare"] = "No active measure selected"
        risks.append("No measurable numeric field available")
        return {
            "enabled": enabled,
            "disabled": disabled,
            "assumptions": assumptions,
            "risks": risks,
        }

    # -----------------------------
    # SUMMARY
    # -----------------------------
    enabled.append("summary")

    # -----------------------------
    # RANK
    # -----------------------------
    if "entity" in canonical_df.columns:
        enabled.append("rank")
    else:
        disabled["rank"] = "Entity field not available"

    # -----------------------------
    # TREND
    # -----------------------------
    if "time" in canonical_df.columns:
        enabled.append("trend")

        if canonical_df["time"].nunique() <= 1:
            risks.append("Single time value limits trend depth")
    else:
        disabled["trend"] = "Time field not available"

    # -----------------------------
    # COMPARE
    # -----------------------------
    dimension_cols = [c for c in canonical_df.columns if c.startswith("dimension_")]

    if dimension_cols:
        enabled.append("compare")
    else:
        disabled["compare"] = "No categorical dimensions available"

    # -----------------------------
    # Assumptions
    # -----------------------------
    assumptions.append("Measure values are comparable across records")

    return {
        "enabled": enabled,
        "disabled": disabled,
        "assumptions": assumptions,
        "risks": risks,
    }
