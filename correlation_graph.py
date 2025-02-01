import openai
from dotenv import load_dotenv
import os
import networkx as nx
import matplotlib.pyplot as plt

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def correlation_graph(check, data):
    # [['2024-xxxxxx','Fox new Trump said ....'], ['2025-1-1', 'Trump xxxxx']]
    # Data Type: timestamp + info
    # Sort data by timestamp
    data = sorted(data, key=lambda x: x[0])
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes with publisher names
    for i in range(len(data)):
        # Extract publisher from info using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract the publisher name from this text."},
                {"role": "user", "content": f"Extract just the publisher name from this text: {data[i][1]}. Respond with only the publisher name."}
            ]
        )
        publisher = response.choices[0].message.content.strip()
        G.add_node(i, label=publisher)
    
    # Add edges for correlations
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            # Extract info for items i and j
            info_i = data[i][1]
            info_j = data[j][1]
            
            # Calculate correlation using OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a correlation analyzer."},
                    {"role": "user", "content": f"Is there a correlation between these two articles about {check}? First article: {info_i}, Second article: {info_j}. Respond with only 'yes' or 'no'."}
                ]
            )
            
            correlation = response.choices[0].message.content.strip().lower()
            
            if correlation == "yes":
                G.add_edge(i, j)
                
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12,8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, arrowsize=20)
    
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels)
    
    plt.title(f"Correlation Graph for {check}")
    plt.show()
    
if __name__ == "__main__":
    correlation_graph("bitcoin", [[]])