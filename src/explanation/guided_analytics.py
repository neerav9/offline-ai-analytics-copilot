from typing import Dict, List, Tuple


def available_analyses(reasoning: Dict) -> List[Tuple[int, str]]:
    """
    Return a numbered list of analytics options
    based purely on system reasoning output.
    """
    options = []
    option_id = 1

    enabled = reasoning.get("enabled", [])

    if "summary" in enabled:
        options.append((option_id, "View summary"))
        option_id += 1

    if "trend" in enabled:
        options.append((option_id, "Analyze trend over time"))
        option_id += 1

    if "compare" in enabled:
        options.append((option_id, "Compare across dimensions"))
        option_id += 1

    if "rank" in enabled:
        options.append((option_id, "Rank entities"))
        option_id += 1

    return options


def map_choice_to_intent(choice_text: str) -> Dict:
    """
    Map a guided analytics choice to an intent descriptor.
    No execution happens here.
    """
    text = choice_text.lower()

    if "summary" in text:
        return {"intent": "summary"}

    if "trend" in text:
        return {"intent": "trend"}

    if "compare" in text:
        return {"intent": "compare"}

    if "rank" in text:
        return {"intent": "rank"}

    raise ValueError("Unsupported guided analytics choice")
