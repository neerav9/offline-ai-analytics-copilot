from typing import Dict


def reason_about_capabilities(canonical_df) -> Dict[str, any]:
    """
    Determine which analytics are safe based on canonical dataframe.
    """
    columns = set(canonical_df.columns)

    capabilities = {
        "summary": "measure" in columns,
        "rank": "measure" in columns and "entity" in columns,
        "trend": "measure" in columns and "time" in columns,
        "compare": any(col.startswith("dimension_") for col in columns),
    }

    explanation = {
        "enabled": [],
        "disabled": {},
        "assumptions": [],
        "risks": []
    }

    for k, v in capabilities.items():
        if v:
            explanation["enabled"].append(k)
        else:
            explanation["disabled"][k] = "Required canonical fields missing"

    if canonical_df["measure"].nunique() < 3:
        explanation["risks"].append(
            "Low variance in measure may reduce analytical insight"
        )

    if "time" in columns and canonical_df["time"].nunique() == 1:
        explanation["risks"].append(
            "Single time value limits trend depth"
        )

    return explanation
