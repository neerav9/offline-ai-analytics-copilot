import pandas as pd
from typing import List

# -----------------------------
# V3 (signals only)
# -----------------------------
from src.v3.schema_extractor import extract_schema

# -----------------------------
# V4 core
# -----------------------------
from src.v4.semantic_mapper import propose_mappings, confirm_mappings
from src.v4.schema_adapter import build_canonical_dataframe, SchemaValidationError
from src.v4.system_reasoner import reason_about_capabilities
from src.v4.analytics_engine import (
    run_summary,
    run_rank,
    run_trend,
    run_compare,
)

from src.explanation.explainer import explain


# --------------------------------------------------
# Utility
# --------------------------------------------------

def print_header(title: str):
    print("\n" + "=" * 50)
    print(title.upper())
    print("=" * 50)


def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def select_active_measure(measures: List[str]) -> str:
    """
    Let user choose the active measure at runtime.
    """
    print_header("SELECT ACTIVE MEASURE")

    for idx, m in enumerate(measures, start=1):
        print(f"{idx}. {m}")

    while True:
        try:
            choice = int(input("\nChoose measure number: "))
            if 1 <= choice <= len(measures):
                return measures[choice - 1]
        except ValueError:
            pass

        print("Invalid selection. Try again.")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    """
    Offline AI Analytics Copilot — V4.2
    Runtime measure switching without re-confirmation.
    """

    # -----------------------------
    # Load dataset
    # -----------------------------
    dataset_path = "data/curated/student_marks.csv"
    df = load_dataset(dataset_path)

    # -----------------------------
    # Schema extraction (signals)
    # -----------------------------
    schema_report = extract_schema(df)

    print_header("DATASET SCHEMA SIGNALS")
    for col, info in schema_report.items():
        print(f"{col}: {info}")

    # -----------------------------
    # Semantic mapping (ONCE)
    # -----------------------------
    proposals = propose_mappings(schema_report)

    print_header("SEMANTIC MAPPING PROPOSALS")
    for k, v in proposals.items():
        print(f"{k} -> {v}")

    # -----------------------------
    # Human confirmation (ONCE)
    # -----------------------------
    confirmed = confirm_mappings(proposals)

    # -----------------------------
    # Active measure selection
    # -----------------------------
    measures = confirmed.get("measures", [])
    if not measures:
        print_header("SCHEMA VALIDATION ERROR")
        print("No valid measure candidates confirmed.")
        return

    active_measure = select_active_measure(measures)
    confirmed["active_measure"] = active_measure

    print_header("ACTIVE MEASURE SELECTED")
    print(active_measure)

    # -----------------------------
    # Canonical dataframe build
    # -----------------------------
    try:
        canonical_df = build_canonical_dataframe(
            df,
            confirmed,
            active_measure=active_measure
        )
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
    # Guided analytics loop
    # -----------------------------
    while True:
        print_header("AVAILABLE ANALYSES")

        enabled = capabilities["enabled"]
        options = {i + 1: name for i, name in enumerate(enabled)}

        for idx, name in options.items():
            print(f"{idx}. {name}")

        print("9. Switch measure")
        print("0. Exit")

        try:
            choice = int(input("\nSelect an option: "))
        except ValueError:
            print("Invalid input.")
            continue

        # Exit
        if choice == 0:
            print("\nExiting. Goodbye.")
            break

        # Runtime measure switch (NO reconfirmation)
        if choice == 9:
            active_measure = select_active_measure(measures)
            confirmed["active_measure"] = active_measure

            canonical_df = build_canonical_dataframe(
                df,
                confirmed,
                active_measure=active_measure
            )

            capabilities = reason_about_capabilities(canonical_df)

            print_header("MEASURE SWITCHED")
            print(f"Active measure: {active_measure}")
            continue

        intent = options.get(choice)
        if not intent:
            print("Invalid choice.")
            continue

        # -----------------------------
        # Execute analytics
        # -----------------------------
        if intent == "summary":
            result = run_summary(canonical_df)
        elif intent == "rank":
            result = run_rank(canonical_df)
        elif intent == "trend":
            result = run_trend(canonical_df)
        elif intent == "compare":
            result = run_compare(canonical_df)
        else:
            print("Unsupported analysis.")
            continue

        explanation = explain(intent.upper(), result)

        print_header("RESULT")
        print(result)

        print_header("EXPLANATION")
        print(explanation)


if __name__ == "__main__":
    main()
