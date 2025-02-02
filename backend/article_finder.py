import argparse
import requests
from datetime import datetime

def find_articles(statement, num_results=10, before_date=None):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': "AIzaSyCcLt-9ysm5wwQvNAR_eFgpJs7Lrfb5xyo",
        'cx': "f7daf3352d60240f2",
        'q': statement,
        'num': num_results
    }
    
    # Add date filter if provided
    if before_date:
        # Calculate days between today and before_date to get maximum article age
        today = datetime.now().date()
        days_diff = (today - before_date).days
        # Use dateRestrict to find articles OLDER than this date
        params['sort'] = 'date:r:1970:' + before_date.strftime('%Y%m%d')
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json()
        
        articles = []
        if 'items' in results:
            for item in results['items']:
                article = {
                    'title': item.get('title', 'No title'),
                    'link': item.get('link', '#'),
                    'snippet': item.get('snippet', 'No description')
                }
                articles.append(article)
        return articles
    except Exception as e:
        print(f"Error searching articles: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Find relevant articles for a statement')
    parser.add_argument('statement', type=str, help='Statement to research')
    parser.add_argument('--before', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                       help='Filter articles by date (format: YYYY-MM-DD)')
    args = parser.parse_args()
    
    articles = find_articles(args.statement, before_date=args.before)
    
    print(f"\nFound {len(articles)} results for: '{args.statement}'\n")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   URL: {article['link']}")
        print(f"   Description: {article['snippet']}\n")

if __name__ == "__main__":
    main()