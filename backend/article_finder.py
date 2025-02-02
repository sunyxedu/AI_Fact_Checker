from statement_extractor import Statement

from bs4 import BeautifulSoup
from googlesearch import search
from dataclasses import dataclass
import requests
from typing import List

@dataclass
class Article:
    timestamp: str
    contents: str
    name: str
    url: str

def get_date_from_url(url):
    try:
        # Send a request to the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find the date in common meta tags (e.g., 'article:published_time', 'date', 'pubdate')
        date = None
        for meta in soup.find_all('meta'):
            if meta.get('property') == 'article:published_time' or meta.get('name') == 'date' or meta.get('name') == 'pubdate':
                date = meta.get('content')
                break

        # If no date is found in meta tags, look for other possible locations like <time> tag
        if not date:
            time_tag = soup.find('time')
            if time_tag:
                date = time_tag.get('datetime')

        if not date:
            date = 'Date not found'

        return date
    except Exception as e:
        return f"Error retrieving date: {e}"

def find_articles(statement, num_results=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://duckduckgo.com/html/?q={statement}&num={num_results}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.find_all('a', class_='result__a'):
        link = item['href']
        title = item.text
        # date = get_date_from_url(link)  # Extract date from the article link

        results.append((link, title))

    return results
   

if __name__=="__main__":
    find_articles("Testing testing")
