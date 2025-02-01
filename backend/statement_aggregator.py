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


"""
We take in our list of truth scores and severity scores and statements and produce a aggregate misinformation list.
This should embed the statements into some sort of space and then use maybe a cosine similarity metric to associate
them with each other. We can then cluster them using KNN for example, and produce a final aggregate set of Misinformation(s).

The final truthiness' and Severity scores should be aggregated by doing batch averages over the clusters.
Summaries can be generated using an LLM.
"""
def aggregate_statements(statements: List[Statement], truth_scores: List[float], severity_scores: List[float]) -> List[Misinformation]:
    # We correspond statements, truth scores and severity scores by indices
    # Embed the list of statements into some embedding space
    # Perform KNN over the statements to then
    
    # Average over the severity and truthiness in each Statement
