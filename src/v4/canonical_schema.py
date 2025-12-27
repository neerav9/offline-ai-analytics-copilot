# src/v4/canonical_schema.py
from typing import Dict, List


def get_canonical_schema() -> Dict[str, Dict]:
    """
    Defines the canonical analytical schema for V4.

    Required:
    - measure: numeric metric being analyzed

    Optional (but capability-enabling):
    - entity: who / what the measure belongs to
    - time: temporal reference
    - dimensions: grouping attributes (can be many)
    """

    return {
        "measure": {
            "type": "numeric",
            "required": True,
            "multiple": True,
        },
        "entity": {
            "type": "categorical",
            "required": False,
            "multiple": False,
        },
        "time": {
            "type": "date",
            "required": False,
            "multiple": False,
        },
        "dimensions": {
            "type": "categorical",
            "required": False,
            "multiple": True,
        },
    }


def required_fields() -> List[str]:
    return [
        k for k, v in get_canonical_schema().items() if v["required"]
    ]
