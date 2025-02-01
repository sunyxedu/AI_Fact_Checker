import openai
from dotenv import load_dotenv
import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def correlation_graph(check, data):
    # [['2024-xxxxxx','Fox new Trump said ....'], ['2025-1-1', 'Trump xxxxx']]
    # Data Type: timestamp + info
    # Sort data by timestamp
    data = sorted(data, key=lambda x: x[0])
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Define severity colors
    severity_colors = {
        1: '#90EE90',  # Light green - minimal misinformation
        2: '#FFFF99',  # Light yellow
        3: '#FFB366',  # Light orange
        4: '#FF8080',  # Light red
        5: '#FF0000'   # Bright red - severe misinformation
    }
    
    # Add nodes with publisher names and severity levels
    node_colors = []
    for i in range(len(data)):
        # Extract publisher and analyze severity using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing misinformation."},
                {"role": "user", "content": f"""Analyze this text: {data[i][1]}
                1. Extract the publisher name
                2. Rate the severity of misinformation on a scale of 1-5 where:
                   1 = Factual/No misinformation
                   2 = Slight inaccuracies
                   3 = Moderate misinformation
                   4 = Significant misinformation
                   5 = Severe misinformation/Complete fabrication
                Respond in format: 'Publisher|SeverityLevel'"""}
            ]
        )
        
        publisher, severity = response.choices[0].message.content.strip().split('|')
        severity = int(severity)
        
        G.add_node(i, label=publisher, severity=severity)
        node_colors.append(severity_colors[severity])
    
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
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=1500, arrowsize=20)
    
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels)
    
    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=color, label=f'Level {level}',
                                 markersize=10)
                      for level, color in severity_colors.items()]
    plt.legend(handles=legend_elements, title='Misinformation Severity',
              loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.title(f"Correlation Graph for {check}")
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    correlation_graph("bitcoin", [[]])