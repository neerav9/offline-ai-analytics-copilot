from enum import Enum
from dataclasses import dataclass


class SemanticMode(Enum):
    SINGLE_MEASURE = "single_measure"
    CATEGORICAL_MEASURE = "categorical_measure"


@dataclass(frozen=True)
class SemanticContext:
    mode: SemanticMode

    def is_single_measure(self) -> bool:
        return self.mode == SemanticMode.SINGLE_MEASURE

    def is_categorical_measure(self) -> bool:
        return self.mode == SemanticMode.CATEGORICAL_MEASURE
