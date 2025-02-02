import argparse
import requests
import re
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Article:
    url: str
    text: str
    title: str
    timestamp: str  # Publication date (if available)

def extract_date_from_snippet(snippet):
    """
    Extracts a date from the snippet.

    First, it checks if the snippet starts with a date in the format 'Oct 7, 2023'. 
    If that fails, it looks for a date following the 'Description:' keyword.
    """
    # Attempt to match a date at the very beginning of the snippet.
    match = re.match(r"^\s*([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})", snippet)
    if match:
        return match.group(1)
    
    # Fallback: attempt to extract a date following 'Description: '
    match = re.search(r"Description:\s*([A-Za-z]+ \d{1,2}, \d{4})", snippet)
    if match:
        return match.group(1)
    
    return ""

def find_articles(statement, num_results=20, before_date=None):
    base_url = "https://www.googleapis.com/customsearch/v1"
    articles = []
    results_per_page = 10  # Google's max per request
    total_pages = min(num_results // results_per_page + 1, 5)  # Max 5 pages (50 results)

    for page in range(total_pages):
        params = {
            'key': "AIzaSyCcLt-9ysm5wwQvNAR_eFgpJs7Lrfb5xyo",
            'cx': "f7daf3352d60240f2",
            'q': statement,
            'num': results_per_page,
            'start': page * results_per_page + 1  # Google starts at 1
        }
        
        if before_date:
            params['sort'] = 'date:r:1970:' + before_date.strftime('%Y%m%d')
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            results = response.json()
            
            if 'items' in results:
                for item in results['items']:
                    title = item.get('title', 'No title')
                    link = item.get('link', '#')
                    snippet = item.get('snippet', 'No description')
                    timestamp = ""

                    # Try to extract publication date from metadata.
                    pagemap = item.get('pagemap', {})
                    metatags = pagemap.get('metatags', [])
                    if metatags:
                        meta = metatags[0]
                        timestamp = meta.get('article:published_time') or meta.get('og:pubdate') or meta.get('pubdate') or ""

                    # If no metadata timestamp, try extracting from the snippet text.
                    if not timestamp:
                        timestamp = extract_date_from_snippet(snippet)
                    else:
                        timestamp = timestamp[:10]
                    
                    articles.append(Article(url=link, text=snippet, title=title, timestamp=timestamp))
                
                if len(articles) >= num_results:
                    break
                    
        except Exception as e:
            print(f"Error on page {page+1}: {e}")
            break
    
    return list(filter(lambda x: x.timestamp != "", articles))[:num_results]

def main():
    parser = argparse.ArgumentParser(description='Find relevant articles for a statement')
    parser.add_argument('statement', type=str, help='Statement to research')
    parser.add_argument('--before', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                        help='Filter articles by date (format: YYYY-MM-DD)')
    parser.add_argument('--num', type=int, default=50,
                        help='Number of results to return (max 50)')
    args = parser.parse_args()
    
    articles = find_articles(args.statement, num_results=args.num, before_date=args.before)
    
    print(f"\nFound {len(articles)} results for: '{args.statement}'\n")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article.title}")
        print(f"   URL: {article.url}")
        print(f"   Description: {article.text}")
        if article.timestamp:
            print(f"   Published Time: {article.timestamp}")
        print()

if __name__ == "__main__":
    main()