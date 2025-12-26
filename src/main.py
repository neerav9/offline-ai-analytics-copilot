import pandas as pd
from src.utils.data_inspector import inspect_dataset

from src.core.analytics_engine import (
    run_summary,
    run_trend,
    run_compare,
    run_rank,
    run_why,
)

from src.explanation.explainer import explain


def load_dataset(path: str) -> pd.DataFrame:
    """
    Load the curated dataset.
    """
    return pd.read_csv(path)


def handle_intent(intent: str, df: pd.DataFrame) -> dict:
    """
    Route the intent to the correct analytics logic.
    """
    intent = intent.upper()

    if intent == "SUMMARY":
        return run_summary(df)

    if intent == "TREND":
        return run_trend(df)

    if intent == "COMPARE":
        return run_compare(df, dimension="region")

    if intent == "RANK":
        return run_rank(df, dimension="salesperson")

    raise ValueError("Unsupported intent")


def main():
    """
    Entry point for the Offline AI Analytics Copilot (V1).
    """
    # --- Temporary placeholders (V1) ---
    dataset_path = "data/curated/sales_data.csv"
    user_intent = "SUMMARY"  # will be dynamic later

    # Load data
    df = load_dataset(dataset_path)

    # Run analytics
    analytics_result = handle_intent(user_intent, df)

    # Generate explanation
    explanation = explain(user_intent, analytics_result)

    # Output
    print("=== ANALYTICS RESULT ===")
    print(analytics_result)

    print("\n=== EXPLANATION ===")
    print(explanation)
    # V2: Inspect dataset
    inspection_report = inspect_dataset(df, key_column="order_id")

    print("\n=== DATA INSPECTION REPORT ===")
    print(inspection_report)


if __name__ == "__main__":
    main()
