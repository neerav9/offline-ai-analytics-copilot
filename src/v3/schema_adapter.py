from typing import Dict
import pandas as pd
from src.v3.canonical_schema import (
    get_required_fields,
    get_semi_required_fields,
    get_optional_fields,
)


class SchemaValidationError(Exception):
    """Raised when required canonical fields are missing."""
    pass


def validate_mappings(final_mapping: Dict[str, str]) -> None:
    """
    Ensure all required canonical fields are mapped.
    """
    required = set(get_required_fields().keys())
    mapped = set(final_mapping.keys())

    missing = required - mapped
    if missing:
        raise SchemaValidationError(
            f"Missing required canonical fields: {', '.join(missing)}"
        )


def adapt_dataframe(
    df: pd.DataFrame,
    final_mapping: Dict[str, str]
) -> pd.DataFrame:
    """
    Rename dataframe columns to canonical schema and
    return a canonical dataframe.
    """
    # Validate required mappings
    validate_mappings(final_mapping)

    # Rename columns
    rename_map = {v: k for k, v in final_mapping.items()}
    canonical_df = df.rename(columns=rename_map)

    # Keep only canonical columns that exist
    allowed_fields = (
        set(get_required_fields().keys())
        | set(get_semi_required_fields().keys())
        | set(get_optional_fields().keys())
    )

    canonical_columns = [
        col for col in canonical_df.columns if col in allowed_fields
    ]

    return canonical_df[canonical_columns]
