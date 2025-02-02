from article_finder import find_articles
from fact_checker import fact_check
from severity_checker import check_severity

from statement_extractor import Statement, extract_statements
from dataclasses import dataclass
from typing import List
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import torch  # Using PyTorch for tensor operations

@dataclass
class Misinformation:
    statements: List[Statement]
    summary: str
    severity: float
    truthiness: float

"""
We take in our list of truth scores and severity scores and statements and produce an aggregate misinformation list.
This should embed the statements into some sort of space and then use maybe a cosine similarity metric to associate
them with each other. We can then cluster them using KMeans for example, and produce a final aggregate set of Misinformation(s).

The final truthiness and severity scores should be aggregated by doing batch averages over the clusters.
Summaries can be generated using an LLM.
"""
def aggregate_statements(statements: List[Statement],
                         truth_scores: List[float],
                         severity_scores: List[float]) -> List[Misinformation]:
    # Import your OpenAI client (assuming it is correctly set up)
    from openai import OpenAI
    client = OpenAI()

    # Update get_embedding to return a torch tensor instead of a list
    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        response = client.embeddings.create(input=[text], model=model)
        # Convert the embedding list to a torch tensor
        embedding = torch.tensor(response.data[0].embedding, dtype=torch.float)
        return embedding

    # Extract texts from statements
    statements_text = [statement.text for statement in statements]

    # Get embeddings as a list of tensors and then stack them into one tensor
    embeddings_list = [get_embedding(statement.text, model='text-embedding-3-small') for statement in statements]
    # Shape: (n_statements, embedding_dim)
    embeddings_tensor = torch.stack(embeddings_list)

    # Convert embeddings tensor to a NumPy array for scikit-learn usage
    embeddings_np = embeddings_tensor.detach().cpu().numpy()

    # Determine number of clusters (using elbow method)
    max_clusters = min(len(statements), 8)
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(embeddings_np)
        inertias.append(kmeans.inertia_)

    # Find elbow point using the rate of change (first difference)
    diffs = np.diff(inertias)
    elbow_point = np.argmin(diffs) + 1  # adding 1 because np.diff reduces length by 1
    optimal_clusters = max(2, min(elbow_point + 1, max_clusters))

    # Perform final clustering
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    cluster_labels_np = kmeans.fit_predict(embeddings_np)
    # Convert cluster labels to a tensor for subsequent operations
    cluster_labels = torch.tensor(cluster_labels_np)

    # Project embeddings to 2D using t-SNE for visualization
    tsne = TSNE(n_components=2, random_state=42, perplexity=1)
    embeddings_2d = tsne.fit_transform(embeddings_np)

    # Plot the clusters
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1],
                          c=cluster_labels_np, cmap='viridis',
                          alpha=0.6)
    plt.title('Statement Clusters Visualization')
    plt.colorbar(scatter, label='Cluster')
    # Annotate each point with a snippet of the statement text
    for i, txt in enumerate(statements_text):
        plt.annotate(txt[:30] + "...", (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                     fontsize=8, alpha=0.7)
    plt.tight_layout()
    plt.savefig('statement_clusters.png')
    plt.show()

    # Convert truth_scores and severity_scores to tensors for tensor-based averaging
    truth_scores_tensor = torch.tensor(truth_scores, dtype=torch.float)
    severity_scores_tensor = torch.tensor(severity_scores, dtype=torch.float)

    # Aggregate results by cluster
    misinformation_list = []
    for cluster_id in range(optimal_clusters):
        # Create a boolean mask for the current cluster
        cluster_mask = (cluster_labels == cluster_id)
        # Filter statements based on cluster membership
        cluster_statements = [s for s, m in zip(statements, cluster_mask.tolist()) if m]
        # Filter the truth and severity scores and compute the averages using tensors
        cluster_truths = truth_scores_tensor[cluster_mask]
        cluster_severities = severity_scores_tensor[cluster_mask]

        # Combine texts from the statements in the current cluster for summarization
        cluster_texts = " ".join([s.text for s in cluster_statements])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize these related statements into a concise 3-6 word summary."},
                {"role": "user", "content": cluster_texts}
            ]
        )
        summary = response.choices[0].message.content

        misinformation = Misinformation(
            statements=cluster_statements,
            summary=summary,
            severity=(cluster_severities.mean().item() if cluster_severities.numel() > 0 else 0.0),
            truthiness=(cluster_truths.mean().item() if cluster_truths.numel() > 0 else 0.0)
        )
        misinformation_list.append(misinformation)

    return misinformation_list

if __name__ == "__main__":
    # Extract statements from a source URL
    statements = extract_statements("https://www.youtube.com/watch?v=ShRYdYTtIx8")
    truth_scores = fact_check(statements)

    # Filter for low-truth statements (fixing the iteration over indices)
    low_truth = [statements[i] for i in range(len(truth_scores)) if truth_scores[i] < 0.4]
    low_truth_truth_scores = [score for score in truth_scores if score < 0.4]

    # Retrieve articles for each low-truth statement
    articles = [find_articles(statement) for statement in low_truth]
    severity = check_severity(low_truth, articles)
    print(severity)
    severity_scores, dags = zip(*severity)
    print("dags")
    print(dags)
    aggregated = aggregate_statements(low_truth, low_truth_truth_scores, severity_scores)
    print("aggregated")
    print(aggregated)