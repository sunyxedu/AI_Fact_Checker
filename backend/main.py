from statement_extractor import extract_statements, Statement
from fact_checker import fact_check
from severity_checker import check_severity
from article_finder import find_articles, Article
from statement_aggregator import aggregate_statements, Misinformation

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class AppData:
    url: str

    article_dagraph: List[dict] # List of Article DAGs
    statement_graphs: List[dict] # List of Graph of Statements
    misinformation_graph: dict # List of Misinformation as JSON


# "https://www.youtube.com/watch?v=ShRYdYTtIx8"

def get_app_data(youtube_url: str) -> AppData:
    mg, sgs, adgs = analyse_video(youtube_url)

    return AppData(
        url=youtube_url,
        misinformation_graph=mg,
        statement_graphs=sgs,
        article_dagraph=adgs
    )


def analyse_video(youtube_url: str):
    statements = extract_statements(youtube_url)
    truth_scores = fact_check(statements)

    # Filter for low-truth statements (fixing the iteration over indices)
    low_truth = [statements[i] for i in range(len(truth_scores)) if truth_scores[i] < 0.4]
    low_truth_truth_scores = [score for score in truth_scores if score < 0.4]

    # Retrieve articles for each low-truth statement
    articles = [find_articles(statement) for statement in low_truth] # 1:1 with statement

    # Use articles to assess severity of low-truth statements
    severity = check_severity(low_truth, articles)
    severity_scores, article_dags = zip(*severity) # 1:1 with statements

    for i, low_truth_s in enumerate(low_truth):
        low_truth_s.severity = severity_scores[i]
        low_truth_s.truthiness = low_truth_truth_scores[i]

    # Aggregate misinformation into large categories
    misinformation = aggregate_statements(low_truth, low_truth_truth_scores, severity_scores)

    misinformation_graph = misinformation_to_graph(misinformation)
    statement_graphs = []
    for m in misinformation:
        statement_graphs.append(statement_to_graph(m.statements, ))

    return misinformation_graph, statement_graphs, article_dags


def misinformation_to_graph(misinformation: List[Misinformation]) -> dict:
    n = len(misinformation)
    nodes = range(n)
    names = map(lambda x: x.summary, misinformation)
    severities = map(lambda x: x.severity, misinformation)
    truthiness = map(lambda x: x.truthiness, misinformation)
    edges = []

    return {
        "nodes": nodes,
        "names": names,
        "severities": severities,
        "truthiness": truthiness,
        "edges": edges
    }


def statement_to_graph(statements: List[Statement]) -> dict:
    n = len(statements)
    nodes = range(n)
    text = map(lambda x: x.text, statements)
    dates = map(lambda x: x.timestamp, statements)
    truthiness = map(lambda x: x.truthiness, statements)
    severity = map(lambda x: x.severity, statements)
    edges = []

    return {
        "nodes": nodes,
        "text": text,
        "dates": dates,
        "edges": edges
    }
