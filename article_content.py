import json
import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime, timedelta

# Keywords [Financial & Reputation]
keywords = [
    "financial", "earnings", "profit", "loss", "investment", "market", 
    "stock", "revenue", "debt", "rating", "credit", "scandal", "reputation", 
    "audit", "keuangan", "pendapatan", "laba", "rugi", "investasi", "pasar", 
    "saham", "pendapatan", "hutang", "peringkat", "kredit", "skandal", 
    "reputasi", "audit", "bisnis", "rencana"
]

def getNewsData(search_query, limit=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    search_url = f"https://www.google.com/search?q={search_query}&gl=id&tbm=nws&num={limit}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []

    for el in soup.select("div.SoaBEf"):
        title_elem = el.select_one("div.MBeuO")
        link_elem = el.find("a")
        snippet_elem = el.select_one(".GI74Re")
        source_elem = el.select_one(".NUnG9d span")
        date_str_elem = el.select_one(".LfVVr")

        title = title_elem.get_text() if title_elem else "No Title"
        link = link_elem["href"] if link_elem else "No Link"
        snippet = snippet_elem.get_text() if snippet_elem else "No Snippet"
        source = source_elem.get_text() if source_elem else "No Source"
        date_str = date_str_elem.get_text() if date_str_elem else None

        published_date = date_str and dateparser.parse(date_str, languages=['id'])
        published_iso = published_date and published_date.isoformat()

        # Check if the published date is within the last week
        if published_date and published_date >= datetime.now() - timedelta(days=7):
            # Fetch news article
            try:
                article_response = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(article_response.content, "html.parser")
                article_content = ' '.join([p.get_text() for p in article_soup.find_all('p')])

                # Filter news by keywords
                if any(keyword in article_content.lower() for keyword in keywords):
                    news_results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet,
                        "source": source,
                        "published_at": published_iso,
                        "content": article_content  # Include article content
                    })
            except Exception as e:
                print(f"Error fetching article content: {e}")

        if len(news_results) >= limit:
            break

    return news_results

search_query = "Bulog"
latest_news = getNewsData(search_query, limit=10)

for idx, news in enumerate(latest_news, start=1):
    print(f"News {idx}:")
    print(f"Title: {news['title']}")
    print(f"Link: {news['link']}")
    print(f"Snippet: {news['snippet']}")
    print(f"Source: {news['source']}")
    print(f"Published At: {news['published_at']}")
    print(f"Content: {news['content']}")
    print("-" * 50)
