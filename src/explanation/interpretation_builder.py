from src.core.interpretation_plan import InterpretationPlan


def build_interpretation(intent: str, capabilities: dict) -> InterpretationPlan:
    steps = []
    assumptions = capabilities.get("assumptions", [])
    missing_inputs = {}

    if intent == "summary":
        steps.append("Aggregate the selected measure across all records")

    elif intent == "rank":
        steps.append("Group records by entity")
        steps.append("Sort entities by the selected measure")

    elif intent == "trend":
        steps.append("Group records by time")
        steps.append("Aggregate the selected measure over time")

    elif intent == "compare":
        steps.append("Group records by categorical dimension")
        steps.append("Compare aggregated measure values across groups")

    else:
        steps.append("Unknown analysis type")

    return InterpretationPlan(
        intent=intent,
        steps=steps,
        assumptions=assumptions,
        requires_user_input=missing_inputs
    )
