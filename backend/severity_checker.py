from article_finder import Article

from statement_extractor import Statement
from dataclasses import dataclass
from typing import List, Tuple
from openai import OpenAI
import json
from correlation_graph import correlation_graph


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
def Agent(text: str) -> float:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at analyzing the severity and impact of misinformation."},
            {"role": "user", "content": f"Analyze the severity and potential impact of this statement. Consider factors like reach, harm potential, and how misleading it is: {text}"}
        ],
        functions=[{
            "name": "analyze_severity",
            "description": "Analyzes the severity and impact of a statement",
            "parameters": {
                "type": "object", 
                "properties": {
                    "severity": {
                        "type": "number",
                        "description": "Severity score between 0 and 1, where 1 is most severe",
                        "minimum": 0,
                        "maximum": 1
                    }
                },
                "required": ["severity"]
            }
        }],
        function_call={"name": "analyze_severity"}
    )
    
    function_call_response = response.choices[0].message.function_call.arguments
    result = json.loads(function_call_response)
    return result["severity"]
    
def check_severity(fact_checked_statements: List[Statement], article: List[List[Article]]) -> List[Tuple[float, OriginDAG]]:
    res = []
    for i, statement in enumerate(fact_checked_statements):
        severity = Agent(statement.text)
        dag = correlation_graph(statement.text, article[i])
        res.append((severity, dag))
    return res
    # for each statement:
    #   Compute DAG of Articles for Statement <- where we got the statement from
    #   return float
