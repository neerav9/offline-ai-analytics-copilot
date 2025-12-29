from dataclasses import dataclass
from typing import List, Dict


@dataclass
class InterpretationPlan:
    intent: str
    steps: List[str]
    assumptions: List[str]
    requires_user_input: Dict[str, str]
