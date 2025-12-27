# src/v4/canonical_schema.py

CANONICAL_SCHEMA = {
    "measure": {
        "type": "numeric",
        "required": True,
        "description": "Primary numeric value to aggregate"
    },
    "dimensions": {
        "type": "categorical",
        "required": False,
        "multiple": True,
        "description": "One or more categorical grouping attributes"
    },
    "entity": {
        "type": "categorical",
        "required": False,
        "description": "Primary actor (special dimension)"
    },
    "time": {
        "type": "date",
        "required": False,
        "description": "Temporal reference"
    },
    "identifier": {
        "type": "categorical",
        "required": False,
        "description": "Unique row identifier"
    }
}


def get_canonical_fields():
    return list(CANONICAL_SCHEMA.keys())
