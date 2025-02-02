from statement_extractor import Statement
from dataclasses import dataclass
from typing import List
from sklearn.cluster import KMeans
import numpy as np
from statement_extractor import extract_statements
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

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
    from openai import OpenAI
    client = OpenAI()

    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding

    statements_text = [statement.text for statement in statements]
    statements_embeddings = [get_embedding(statement.text, model='text-embedding-3-small') for statement in statements]
    

    max_clusters = min(len(statements), 8)
    inertias = []
    
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(statements_embeddings)
        inertias.append(kmeans.inertia_)
    
    # Find elbow point using rate of change
    diffs = np.diff(inertias)
    elbow_point = np.argmin(diffs) + 1
    optimal_clusters = max(2, min(elbow_point + 1, max_clusters))
    
    # Perform final clustering
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(statements_embeddings)
    
    # Project embeddings to 2D using t-SNE
    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(statements_embeddings)
    
    # Plot the clusters
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
                         c=cluster_labels, cmap='viridis',
                         alpha=0.6)
    plt.title('Statement Clusters Visualization')
    plt.colorbar(scatter, label='Cluster')
    
    # Add statement texts as annotations
    for i, txt in enumerate(statements_text):
        plt.annotate(txt[:30] + "...", (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                    fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('statement_clusters.png')
    plt.show()
    # plt.close()
    
    # Aggregate results by cluster
    misinformation_list = []
    for cluster_id in range(optimal_clusters):
        cluster_mask = cluster_labels == cluster_id
        cluster_statements = [s for s, m in zip(statements, cluster_mask) if m]
        cluster_truths = [s for s, m in zip(truth_scores, cluster_mask) if m]
        cluster_severities = [s for s, m in zip(severity_scores, cluster_mask) if m]
        
        cluster_texts = " ".join([s.text for s in cluster_statements])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize these related statements into a concise summary."},
                {"role": "user", "content": cluster_texts}
            ]
        )
        summary = response.choices[0].message.content
        
        misinformation = Misinformation(
            statements=cluster_statements,
            summary=summary,
            severity=sum(cluster_severities) / len(cluster_severities),
            truthiness=sum(cluster_truths) / len(cluster_truths)
        )
        misinformation_list.append(misinformation)
    
    return misinformation_list

if __name__ == "__main__":
    statements = extract_statements("https://www.youtube.com/watch?v=ShRYdYTtIx8")
    print(statements)