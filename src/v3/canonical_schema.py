from typing import Dict


CANONICAL_SCHEMA: Dict[str, Dict[str, str]] = {
    "required": {
        "revenue": "numeric"
    },
    "semi_required": {
        "order_date": "date",
        "category": "categorical"
    },
    "optional": {
        "units_sold": "numeric",
        "unit_price": "numeric",
        "entity_name": "categorical"
    }
}


def get_required_fields() -> Dict[str, str]:
    return CANONICAL_SCHEMA["required"]


def get_semi_required_fields() -> Dict[str, str]:
    return CANONICAL_SCHEMA["semi_required"]


def get_optional_fields() -> Dict[str, str]:
    return CANONICAL_SCHEMA["optional"]


def get_all_fields() -> Dict[str, str]:
    all_fields = {}
    all_fields.update(get_required_fields())
    all_fields.update(get_semi_required_fields())
    all_fields.update(get_optional_fields())
    return all_fields
