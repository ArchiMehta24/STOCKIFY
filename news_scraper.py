#news_scraper.py
import requests
import os

def fetch_news(stock_name):
    """
    Fetches news related to the given stock name using SerpApi.
    Returns a list of news articles.
    """
    API_KEY = os.getenv("SERPAPI_KEY")  # Use API key from environment variables
    search_query = f"{stock_name} stock market news"

    params = {
        "q": search_query,
        "api_key": API_KEY,
        "tbm": "nws",  # News search
        "num": 5
    }

    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code != 200:
        return []

    news_data = response.json().get("news_results", [])

    articles = []
    for article in news_data:
        articles.append({
            "title": article["title"],
            "link": article["link"],
            "source": article["source"],
            "published": article["date"]
        })

    return articles
