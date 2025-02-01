from severity_checker import CheckedStatement
from statement_extractor import Statement

from dataclasses import dataclass
from typing import List

@dataclass
class Misinformation:
    statements: List[Statement]
    summary: str
    severity: float
    truthiness: float


def aggregate_statements(truth_scores: List[float], severity_scores: List[float]) -> List[Misinformation]:
    ...
