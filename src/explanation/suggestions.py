from typing import Dict, List


def generate_suggestions(inspection_report: Dict) -> List[str]:
    """
    Generate human-readable suggestions based on data inspection report.
    """
    suggestions = []

    # ---- Missing values ----
    missing = inspection_report.get("missing_values", {})
    columns_with_missing = [
        col for col, stats in missing.items()
        if stats["missing_count"] > 0
    ]

    if columns_with_missing:
        suggestions.append(
            f"Missing values detected in columns: {', '.join(columns_with_missing)}. "
            "Consider handling them before analysis."
        )
    else:
        suggestions.append(
            "No missing values detected. No null handling is required."
        )

    # ---- Duplicates ----
    duplicates = inspection_report.get("duplicates", {})
    total_dupes = duplicates.get("total_duplicate_rows", 0)

    if total_dupes > 0:
        suggestions.append(
            f"{total_dupes} duplicate rows found. Review and remove duplicates if necessary."
        )
    else:
        suggestions.append(
            "No duplicate records detected."
        )

    # ---- Numeric sanity ----
    numeric_checks = inspection_report.get("numeric_checks", {})
    revenue_check = numeric_checks.get("revenue_consistency")

    if revenue_check == "FAIL":
        suggestions.append(
            "Revenue values are inconsistent with units sold and unit price. "
            "Verify revenue calculations."
        )
    elif revenue_check == "PASS":
        suggestions.append(
            "Revenue values are consistent with units sold and unit price."
        )

    # ---- Readiness ----
    if not columns_with_missing and total_dupes == 0 and revenue_check == "PASS":
        suggestions.append(
            "Dataset is clean and ready for analytics. "
            "You can proceed with trend, comparison, or ranking analyses."
        )

    return suggestions
