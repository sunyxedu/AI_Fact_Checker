from statement_extractor import Statement

from dataclasses import dataclass
from typing import List


"""
We take a list of Statements from the YouTube video and compute
truthiness scores for all of them using a mixture of methods.

For simple cases, we can rely on an LLM to determine truthiness. If it
determines that the issue is controversial or confusing we can
fall back to Wikipedia and Google Fact Check API.

Outputs should be normalised floats between 0 and 1.
"""
def fact_check(statements: List[Statement]) -> List[float]:
    ...
