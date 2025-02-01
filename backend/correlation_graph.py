import openai
from dotenv import load_dotenv
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from openai import OpenAI

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
        # Initialize the client
        client = OpenAI()
        
        # Extract publisher and analyze severity using OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing misinformation."},
                {"role": "user", "content": f"Analyze this text: {data[i][1]}"}
            ],
            functions=[{
                "name": "analyze_misinformation", 
                "description": "Analyzes text for publisher and misinformation severity",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "publisher": {
                            "type": "string",
                            "description": "The publisher name (Unknown if not found)"
                        },
                        "severity": {
                            "type": "integer", 
                            "description": "Misinformation severity rating from 1-5",
                            "enum": [1, 2, 3, 4, 5]
                        }
                    },
                    "required": ["publisher", "severity"]
                }
            }],
            function_call={"name": "analyze_misinformation"}
        )
        # Parse the function call response
        function_call_response = response.choices[0].message.function_call.arguments
        result = json.loads(function_call_response)
        publisher = result["publisher"]
        print(publisher)
        severity = int(result["severity"])
        
        G.add_node(i, label=f"{publisher}\n{data[i][0]}", severity=severity)
        node_colors.append(severity_colors[severity])
    
    # Add edges for correlations
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            # Extract info for items i and j
            info_i = data[i][1]
            info_j = data[j][1]
            
            # Calculate correlation using OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
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
            node_size=2000, arrowsize=20)
    
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
    return G
    
if __name__ == "__main__":
    correlation_graph("bitcoin is a scam", [
        [0, "CNN Bitcoin price surges past $50,000 for first time since 2021"],
        [1, "Reuters Bitcoin miners struggle with rising energy costs"],
        [2, "Bloomberg Major investment firm launches Bitcoin ETF"],
        [3, "Cryptocurrency market sees increased volatility"]
    ])