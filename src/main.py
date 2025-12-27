import pandas as pd

from src.v3.schema_extractor import extract_schema

from src.v4.semantic_mapper import propose_mappings, confirm_mappings
from src.v4.schema_adapter import build_canonical_dataframe, SchemaValidationError
from src.v4.system_reasoner import reason_about_capabilities
from src.v4.analytics_engine import (
    run_summary,
    run_rank,
    run_compare,
    run_trend,
)

from src.explanation.explainer import explain


# -----------------------------
# V4 Intent Adapter
# -----------------------------
INTENT_MAP = {
    "summary": "SUMMARY",
    "rank": "RANK",
    "trend": "TREND",
    "compare": "COMPARE",
}


# -----------------------------
# Utilities
# -----------------------------
def print_header(title: str):
    print("\n" + "=" * 50)
    print(title.upper())
    print("=" * 50)


def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# -----------------------------
# Main
# -----------------------------
def main():
    """
    Offline AI Analytics Copilot — V4
    Schema-driven, capability-gated analytics.
    """

    # -----------------------------
    # Load dataset
    # -----------------------------
    dataset_path = "data/curated/student_marks.csv"
    df = load_dataset(dataset_path)

    # -----------------------------
    # Schema extraction
    # -----------------------------
    schema_report = extract_schema(df)

    print_header("DATASET SCHEMA SIGNALS")
    for col, info in schema_report.items():
        print(f"{col}: {info}")

    # -----------------------------
    # Semantic mapping
    # -----------------------------
    proposals = propose_mappings(schema_report)

    print_header("SEMANTIC MAPPING PROPOSALS")
    for k, v in proposals.items():
        print(f"{k} -> {v}")

    # -----------------------------
    # Human confirmation
    # -----------------------------
    confirmed_mappings = confirm_mappings(proposals)

    print_header("CONFIRMED MAPPINGS")
    for k, v in confirmed_mappings.items():
        print(f"{k} -> {v}")

    # -----------------------------
    # Canonical dataframe
    # -----------------------------
    try:
        canonical_df = build_canonical_dataframe(df, confirmed_mappings)
    except SchemaValidationError as e:
        print_header("SCHEMA VALIDATION ERROR")
        print(str(e))
        return

    print_header("CANONICAL DATAFRAME")
    print(canonical_df.head())

    # -----------------------------
    # Capability reasoning
    # -----------------------------
    capabilities = reason_about_capabilities(canonical_df)

    print_header("SYSTEM REASONING")
    print(f"Dataset shape: {canonical_df.shape}")

    print("\nEnabled analyses:")
    for a in capabilities["enabled"]:
        print(f"✓ {a}")

    print("\nDisabled analyses:")
    for a, reason in capabilities["disabled"].items():
        print(f"✗ {a} — {reason}")

    print("\nAssumptions:")
    for a in capabilities["assumptions"]:
        print(f"• {a}")

    print("\nRisks:")
    for r in capabilities["risks"]:
        print(f"⚠ {r}")

    # -----------------------------
    # Guided analytics (capability-gated)
    # -----------------------------
    while True:
        print_header("AVAILABLE ANALYSES")

        enabled = capabilities["enabled"]
        options = {i + 1: name for i, name in enumerate(enabled)}

        for idx, name in options.items():
            print(f"{idx}. {name}")

        print("0. Exit")

        try:
            choice = int(input("\nSelect an option: "))
        except ValueError:
            print("Invalid input.")
            continue

        if choice == 0:
            print("\nExiting. Goodbye.")
            break

        selected = options.get(choice)
        if not selected:
            print("Invalid choice.")
            continue

        # 🔑 CRITICAL FIX: map to engine intent
        intent = INTENT_MAP.get(selected)

        if not intent:
            print("Unsupported analysis.")
            continue

        # -----------------------------
        # Execute analytics
        # -----------------------------
        if intent == "SUMMARY":
            result = run_summary(canonical_df)

        elif intent == "RANK":
            result = run_rank(canonical_df)

        elif intent == "TREND":
            result = run_trend(canonical_df)

        elif intent == "COMPARE":
            result = run_compare(
                canonical_df,
                [c for c in canonical_df.columns if c.startswith("dimension_")]
            )

        else:
            print("Unsupported analysis.")
            continue

        explanation = explain(intent, result)

        print_header("RESULT")
        print(result)

        print_header("EXPLANATION")
        print(explanation)


if __name__ == "__main__":
    main()
