from typing import Dict, Any


def confirm_mappings(proposals: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """
    Human-in-the-loop confirmation for semantic mappings.
    Returns final canonical -> column mapping.
    """
    confirmed = {}

    print("\n=== HUMAN CONFIRMATION REQUIRED ===")

    for canonical_field, info in proposals.items():
        column = info["column"]
        confidence = info["confidence"]
        evidence = ", ".join(info.get("evidence", []))

        print("\n----------------------------------")
        print(f"Canonical field : {canonical_field}")
        print(f"Proposed column : {column}")
        print(f"Confidence      : {confidence}")
        print(f"Evidence        : {evidence}")

        user_input = input(
            "Accept mapping? (y = accept / n = reject / custom = enter column name): "
        ).strip()

        if user_input.lower() == "y":
            confirmed[canonical_field] = column

        elif user_input.lower() == "n":
            print(f"Skipping mapping for '{canonical_field}'.")

        elif user_input:
            confirmed[canonical_field] = user_input
            print(
                f"Custom mapping set: {canonical_field} -> {user_input}"
            )

        else:
            print(f"No input provided. Skipping '{canonical_field}'.")

    return confirmed
