import pandas as pd

from src.v3.human_confirmation import confirm_mappings



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
)
from src.explanation.explainer import explain

# V3 imports
from src.v3.schema_extractor import extract_schema
from src.v3.semantic_mapper import propose_mappings


def print_header(title: str):
    print("\n" + "=" * 50)
    print(title.upper())
    print("=" * 50)


def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def main():
    """
    Entry point for the Offline AI Analytics Copilot (V3).
    """

    # -----------------------------
    # Load dataset
    # -----------------------------
    dataset_path = "data/curated/sales_data.csv"
    df = load_dataset(dataset_path)

    # -----------------------------
    # V3.2: Extract dataset schema
    # -----------------------------
    schema_report = extract_schema(df)

    print_header("V3 DATASET SCHEMA SIGNALS")
    for col, info in schema_report.items():
        print(f"{col}: {info}")

    # -----------------------------
    # V3.3: Semantic mapping
    # -----------------------------
    mappings = propose_mappings(schema_report)

    print_header("V3 SEMANTIC MAPPING PROPOSALS")
    for field, info in mappings.items():
        print(f"{field} -> {info}")
    # -----------------------------
    # V3.4: Human confirmation
    # -----------------------------
    final_mapping = confirm_mappings(mappings)

    print_header("V3 CONFIRMED MAPPINGS")
    for k, v in final_mapping.items():
        print(f"{k} -> {v}")

    # -----------------------------
    # V2.1: Data inspection
    # -----------------------------
    inspection_report = inspect_dataset(df, key_column="order_id")

    print_header("DATA INSPECTION REPORT")
    print(inspection_report)

    # -----------------------------
    # V2.2: AI-assisted suggestions
    # -----------------------------
    suggestions = generate_suggestions(inspection_report)

    print_header("AI-ASSISTED SUGGESTIONS")
    for s in suggestions:
        print(f"- {s}")

    # -----------------------------
    # V2.3: Guided analytics
    # -----------------------------
    while True:
        print_header("GUIDED ANALYTICS OPTIONS")

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

        print_header("RESULT")
        print(analytics_result)

        print_header("EXPLANATION")
        print(explanation)


if __name__ == "__main__":
    main()
