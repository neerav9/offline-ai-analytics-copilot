from typing import Dict
import pandas as pd


# --------------------------------------------------
# Step 1: Canonical fact extraction (NO DECISIONS)
# --------------------------------------------------
def extract_canonical_facts(canonical_df: pd.DataFrame) -> Dict[str, bool | int]:
    return {
        "has_measure": "measure" in canonical_df.columns,
        "has_entity": "entity" in canonical_df.columns,
        "has_time": "time" in canonical_df.columns,
        "has_dimensions": any(
            col.startswith("dimension_") for col in canonical_df.columns
        ),
        "time_cardinality": (
            canonical_df["time"].nunique()
            if "time" in canonical_df.columns
            else 0
        ),
    }


# --------------------------------------------------
# Step 2: Explicit capability matrix (RULES ONLY)
# --------------------------------------------------
CAPABILITY_MATRIX = {
    "summary": {
        "required": ["has_measure"],
    },
    "rank": {
        "required": ["has_measure", "has_entity"],
    },
    "trend": {
        "required": ["has_measure", "has_time"],
    },
    "compare": {
        "required": ["has_measure", "has_dimensions"],
    },
}


# --------------------------------------------------
# Step 3: Reasoner (FACTS + RULES → DECISIONS)
# --------------------------------------------------
def reason_about_capabilities(canonical_df: pd.DataFrame, semantic_context):
    """
    Determine which analytics are safe based on the canonical dataframe.

    IMPORTANT:
    - No raw dataframe access
    - No implicit inference
    - All decisions come from CAPABILITY_MATRIX
    """

    facts = extract_canonical_facts(canonical_df)

    enabled = []
    disabled = {}
    assumptions = []
    risks = []

    # -----------------------------
    # Capability evaluation
    # -----------------------------
    for analysis, rules in CAPABILITY_MATRIX.items():
        missing_requirements = [
            req for req in rules["required"]
            if not facts.get(req, False)
        ]

        if missing_requirements:
            disabled[analysis] = (
                f"Missing required canonical features: {missing_requirements}"
            )
        else:
            enabled.append(analysis)

    # -----------------------------
    # Assumptions (explicit)
    # -----------------------------
    if facts["has_measure"]:
        assumptions.append("Measure values are comparable across records")

    # -----------------------------
    # Risks (fact-based, not rules)
    # -----------------------------
    if facts["has_time"] and facts["time_cardinality"] <= 1:
        risks.append("Single time value limits trend depth")

    return {
        "enabled": enabled,
        "disabled": disabled,
        "assumptions": assumptions,
        "risks": risks,
        "facts": facts,   # useful for debugging / UI later
    }
