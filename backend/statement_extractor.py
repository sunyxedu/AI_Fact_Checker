from dataclasses import dataclass
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import re
import json

@dataclass
class Statement:
    text: str
    timestamp: str


"""
Given YouTube video, extract Statements. We want to extract meaningful
blocks of information from the video. For example:

"I like cats and I like dogs" -> "I like cats", "I like dogs"

We should request the transcript with timestamps, and maintain them in the
final statements.
"""
def video(video_id):
    # Fetch transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([entry["text"] for entry in transcript])
    # Process transcript: separate sentences & keep timestamps

    data = []

    for entry in transcript:
        text = entry["text"]
        timestamp = entry["start"]
        time = str(int(timestamp // 60)) + ":" + str(round(timestamp % 60))
        data.append((time, text))
    # print(data)
    return data

def extract_statements(youtube_video_url: str) -> List[Statement]:
    video_id = youtube_video_url.split("v=")[1]
    ls = video(video_id)
    print(ls)
    print("-------")
    str = ""
    for i in range(len(ls)):
        str = str + ls[i][1] + " "
    print(str)
    print("-------")
    # Use LLM to extract factual statements

    # Initialize LLM
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at extracting factual statements from text."},
            {"role": "user", "content": f"Extract factual statements from this transcript. Return them exactly as written (Same case, same symbol), one per line. For example, given the transcript:\n\n1. 'xxxxxx'\n2. 'yyyyyy'\n\nNow extract statements from this transcript: {str}"}
        ],
        functions=[{
            "name": "extract_statements",
            "description": "Extracts factual statements from text",
            "parameters": {
                "type": "object",
                "properties": {
                    "statements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of extracted factual statements"
                    }
                },
                "required": ["statements"]
            }
        }],
        function_call={"name": "extract_statements"}
    )
    # Get statements from LLM response
    function_call_response = response.choices[0].message.function_call.arguments
    result = json.loads(function_call_response)
    statements_text = result["statements"]
    print(statements_text)
    print("-------")
    sentences = statements_text

    # print("-------SENTENCES-------")
    # for sentence in sentences:
    #     print(sentence)

    seen = set()
    unique_statements = []
    statements_with_positions = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            unique_statements.append(s)
            pos = str.find(s)
            if pos != -1:
                statements_with_positions.append((s, pos))
    
    # Sort statements by position
    print(unique_statements)
    statements_with_positions.sort(key=lambda x: x[1])
    print(statements_with_positions)
    # unique_statements = [s[0] for s in statements_with_positions]
    
    
    acc = ""
    id = 0
    for QwQ in ls:
        acc = acc + QwQ[1] + " "
        if (len(acc) > statements_with_positions[id]):
            
    # return statements
    # return ls

if __name__ == "__main__":
    extract_statements("https://www.youtube.com/watch?v=ShRYdYTtIx8")
