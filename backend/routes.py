from flask import Blueprint, request, jsonify
from news_fetcher import fetch_news
from summarizer import summarize_articles

routes = Blueprint('routes', __name__)

@routes.route("/digest", methods=["POST"])
def get_digest():
    data = request.json
    topic = data.get("topic")
    articles = fetch_news(topic)
    digest = summarize_articles(articles)
    return jsonify({"digest": digest})
