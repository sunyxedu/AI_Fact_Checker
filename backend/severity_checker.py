from statement_extractor import Statement

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class OriginWebsite:
    name: str
    url: str
    summary: str


@dataclass
class OriginDAG: # This is a graph of Websites that are the provenance
    nodes: List[int]
    node_websites: List[OriginWebsite] # Extend to include article URL etc.
    severity: List[float]
    edge: List[Tuple[int, int]]


"""
Given our list of Statements from a YouTube video, we need to extract
the severity of each statement in terms of impact score.

PRE-CONDITION: The statement has low truthiness

We need to assess downstraem impact of the low-truth statement.

We return a normalised float between 0 and 1.
"""
def check_severity(fact_checked_statements: List[Statement]) -> List[Tuple[float, OriginDAG]]:
    ...
    # for each statement:
    #   Compute DAG of Articles for Statement <- where we got the statement from
    #   return float
