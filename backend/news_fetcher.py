from apify_client import ApifyClient
import os

def fetch_news(topic="AAPL"):
    APIIFY_CLIENT_TOKEN = os.getenv("APIFY_CLIENT_TOKEN")
    client = ApifyClient(APIIFY_CLIENT_TOKEN)
    print("Apify Client initialized.")
    run_input = {
        "query": topic,
        "language": "US:en",
        "maxItems": 5,
        "proxyConfiguration": { "useApifyProxy": True },
    }
    print(f"Fetching news for topic: {topic}...",'\n','-----------------------------------------------------')
    try:
        run = client.actor("lhotanova/google-news-scraper").call(run_input=run_input)
        articles = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            url = item.get("url", "")
            if "news.google.com" in url:
                continue
            articles.append(item)
        print(f"Fetched {len(articles)} articles for topic: {topic}")
    except Exception as e:
        print("Error fetching articles:", e)
        return []
    return articles
