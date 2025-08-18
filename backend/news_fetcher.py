from apify_client import ApifyClient
import os

def fetch_news(topic="AAPL"):
    # Initialize the ApifyClient with your Apify API token
    APIIFY_CLIENT_TOKEN = os.getenv("APIFY_CLIENT_TOKEN")
    client = ApifyClient(APIIFY_CLIENT_TOKEN)

    # Prepare the Actor input
    run_input = {
        "query": topic,
        "language": "US:en",
        "maxItems": 5,
        "proxyConfiguration": { "useApifyProxy": True },
    }

    # Run the Actor and wait for it to finish
    run = client.actor("lhotanova/google-news-scraper").call(run_input=run_input)

    # Fetch Actor results from the run's dataset (if there are any)
    articles = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        articles.append(item.get("title", "") + " " + item.get("description", ""))
    return articles
