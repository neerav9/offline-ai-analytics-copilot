import pandas as pd
from src.utils.data_inspector import inspect_dataset
from src.explanation.suggestions import generate_suggestions
from src.explanation.guided_analytics import (
    available_analyses,
    map_choice_to_intent,
)

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
    # V2: Generate AI-assisted suggestions
    suggestions = generate_suggestions(inspection_report)

    print("\n=== AI-ASSISTED SUGGESTIONS ===")
    for s in suggestions:
        print(f"- {s}")
        # V2.3: Guided analytics (loopable)
    while True:
        print("\n=== GUIDED ANALYTICS OPTIONS ===")
        options = available_analyses(inspection_report)

        for idx, text in options:
            print(f"{idx}. {text}")

        print("0. Exit")

        try:
            selected = int(input("\nSelect an option number to proceed: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if selected == 0:
            print("\nExiting guided analytics. Goodbye!")
            break

        selected_text = dict(options).get(selected)
        if not selected_text:
            print("Invalid selection. Please try again.")
            continue

        intent_payload = map_choice_to_intent(selected_text)
        intent = intent_payload["intent"]

        if intent == "SUMMARY":
            analytics_result = run_summary(df)

        elif intent == "TREND":
            analytics_result = run_trend(df)

        elif intent == "COMPARE":
            analytics_result = run_compare(df, intent_payload["dimension"])

        elif intent == "RANK":
            analytics_result = run_rank(df, intent_payload["dimension"])

        else:
            print("Unsupported analysis.")
            continue

        explanation = explain(intent, analytics_result)

        print("\n=== RESULT ===")
        print(analytics_result)

        print("\n=== EXPLANATION ===")
        print(explanation)


if __name__ == "__main__":
    main()
