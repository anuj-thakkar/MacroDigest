
import requests
topic = 'chicago bulls'
NEWS_API_KEY = 'a023b2284ef942298d6013c283a16477'
url = f"https://newsapi.org/v2/top-headlines?q={topic}&apiKey={NEWS_API_KEY}"

response = requests.get(url)
if response.status_code == 200:

    articles = response.json().get("articles")
    print(articles)
else:
    print(f"Error: {response.status_code}")