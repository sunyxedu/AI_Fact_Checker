from dataclasses import dataclass
from typing import List

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
def extract_statements(youtube_video_url: str) -> List[Statement]:
    ...
