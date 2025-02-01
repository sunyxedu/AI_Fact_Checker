from statement_extractor import Statement

from dataclasses import dataclass
from typing import List

@dataclass
class FactCheckedStatement:
    truthiness: float # Score from 0 to 1, could be enum maybe
    statement: str    


def fact_check(video_with_statements: List[Statement]) -> List[FactCheckedStatement]:
    ...
