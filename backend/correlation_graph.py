import openai
from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def correlation_graph(check, data):
    # [['2024-xxxxxx','Fox new Trump said ....'], ['2025-1-1', 'Trump xxxxx']]
    # Data Type: timestamp + info
    # Sort data by timestamp
    data = sorted(data, key=lambda x: x[0])
    
    # Initialize result structure
    result = {
        "nodes": [],
        "nodename": [],
        "severity": [],
        "edge": []
    }
    
    # Process nodes and get severity/publisher info
    for i in range(len(data)):
        # Initialize the client
        client = OpenAI()
        
        # Extract publisher and analyze severity using OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
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
        result_analysis = json.loads(function_call_response)
        publisher = result_analysis["publisher"]
        print(publisher)
        severity = int(result_analysis["severity"])
        
        result["nodes"].append(i)
        result["nodename"].append(f"{publisher}\n{data[i][0]}")
        result["severity"].append(severity)
    
    # Find correlations and build edge relationships
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            # Extract info for items i and j
            info_i = data[i][1]
            info_j = data[j][1]
            
            # Calculate correlation using OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a correlation analyzer."},
                    {"role": "user", "content": f"Is there a correlation between these two articles about {check}? First article: {info_i}, Second article: {info_j}. Respond with only 'yes' or 'no'."}
                ]
            )
            
            correlation = response.choices[0].message.content.strip().lower()
            
            if correlation == "yes":
                result["edge"].append([i, j])
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    result = correlation_graph("bitcoin is a scam", [
        [0, "CNN Bitcoin price surges past $50,000 for first time since 2021"],
        [1, "Reuters Bitcoin miners struggle with rising energy costs"],
        [2, "Bloomberg Major investment firm launches Bitcoin ETF"],
        [3, "Cryptocurrency market sees increased volatility"]
    ])
    print(json.dumps(result, indent=2))