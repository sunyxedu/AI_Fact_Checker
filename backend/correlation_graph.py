from article_finder import Article

import openai
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from typing import List

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def correlation_graph(check, data: List[Article]):
    # Sort articles by timestamp
    data = sorted(data, key=lambda x: x.timestamp)
    
    # Initialize result structure
    result = {
        "nodes": [],
        "nodename": [],
        "severity": [],
        "urls": [],
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
                {"role": "user", "content": f"Analyze this text: {data[i].text}"}
            ],
            functions=[{
                "name": "analyze_misinformation", 
                "description": "Analyzes text for publisher and misinformation severity",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "severity": {
                            "type": "integer", 
                            "description": "Misinformation severity rating from 1-5",
                            "enum": [1, 2, 3, 4, 5]
                        },
                        "summary": {
                            "type": "string",
                            "description": "A 3-6 word summary of the misinformation in the article"
                        }
                    },
                    "required": ["publisher", "severity", "summary"]
                }
            }],
            function_call={"name": "analyze_misinformation"}
        )
        # Parse the function call response
        function_call_response = response.choices[0].message.function_call.arguments
        result_analysis = json.loads(function_call_response)
        summary = result_analysis["summary"]
        print(summary)
        severity = int(result_analysis["severity"])
        
        result["nodes"].append(i)
        result["nodename"].append(f"{summary}\n{data[i].timestamp}")
        result["urls"].append(data[i].url)
        result["severity"].append(severity)
    
    # Find correlations and build edge relationships
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            # Extract info for items i and j
            info_i = data[i].text
            info_j = data[j].text
            
            # Calculate correlation using OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a correlation analyzer."},
                    {"role": "user", "content": f"Is there a correlation between these two articles about {check}? First article: {info_i}, Second article: {info_j}. Respond with only 'yes' or 'no'. Be open minded and appreciative of small links between them."}
                ]
            )
            
            correlation = response.choices[0].message.content.strip().lower()
            
            if correlation == "yes":
                result["edge"].append([i, j])
    # print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class Article:
        timestamp: str
        text: str

    result = correlation_graph("bitcoin is a scam", [
        Article("2024-01-01", "CNN Bitcoin price surges past $50,000 for first time since 2021"),
        Article("2024-01-02", "Reuters Bitcoin miners struggle with rising energy costs"),
        Article("2024-01-03", "Bloomberg Major investment firm launches Bitcoin ETF"),
        Article("2024-01-04", "Cryptocurrency market sees increased volatility")
    ])
    # print(json.dumps(result, indent=2))