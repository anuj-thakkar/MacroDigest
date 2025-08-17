import requests
NEWS_API_KEY = "your_api_key"

def fetch_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return [a["title"] + " " + a["description"] for a in articles[:5]]
