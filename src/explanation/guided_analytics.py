from typing import Dict, List, Tuple


def available_analyses(inspection_report: Dict) -> List[Tuple[int, str]]:
    """
    Return a numbered list of valid analytics options based on inspection report.
    """
    options = []
    option_id = 1

    # Dataset shape must exist
    shape = inspection_report.get("shape", {})
    if shape.get("rows", 0) > 0:
        options.append((option_id, "View summary"))
        option_id += 1

    # Trend requires a date column
    missing = inspection_report.get("missing_values", {})
    if "order_date" in missing:
        options.append((option_id, "Analyze revenue trend over time"))
        option_id += 1

    # Compare requires a categorical dimension
    for dim in ["region", "salesperson", "product"]:
        if dim in missing:
            options.append((option_id, f"Compare revenue by {dim}"))
            option_id += 1

    # Rank requires a categorical dimension
    for dim in ["salesperson", "product", "region"]:
        if dim in missing:
            options.append((option_id, f"Rank top performers by {dim}"))
            option_id += 1

    return options


def map_choice_to_intent(choice_text: str) -> Dict:
    """
    Map a chosen option text to intent and parameters.
    """
    text = choice_text.lower()

    if "summary" in text:
        return {"intent": "SUMMARY"}

    if "trend" in text:
        return {"intent": "TREND"}

    if "compare" in text:
        for dim in ["region", "salesperson", "product"]:
            if dim in text:
                return {"intent": "COMPARE", "dimension": dim}

    if "rank" in text:
        for dim in ["region", "salesperson", "product"]:
            if dim in text:
                return {"intent": "RANK", "dimension": dim}

    raise ValueError("Unsupported guided analytics choice")
