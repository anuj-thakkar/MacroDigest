import json
import os
from datetime import datetime
from utils import get_user_latest_preferences
from flask import Blueprint, request, jsonify
from news_fetcher import fetch_news
from summarizer import summarize_articles_from_urls
import logging
import sqlite3


# List of all categories (updated)
CATEGORIES = [
    'Market Volatility & Options',
    'Equities and Indexes',
    'Macroeconomics',
    'Regulatory & Compliance News',
    'Alternative Assets & Innovation'
]

routes = Blueprint('routes', __name__)
logger = logging.getLogger(__name__)


@routes.route('/preferences', methods=['POST'])
def save_preferences():
    data = request.json
    print('Received data:', data)
    email = data.get('email')
    topics = data.get('topics', [])
    print('Parsed email:', email)
    print('Parsed topics:', topics)
    if not email or not topics:
        print('Missing email or topics')
        return jsonify({'error': 'Email and topics required'}), 400
    # Map topics to indicator fields
    topic_fields = {
        'Market Volatility & Options': 0,
        'Equities and Indexes': 0,
        'Macroeconomics': 0,
        'Regulatory & Compliance News': 0,
        'Alternative Assets & Innovation': 0
    }
    for topic in topics:
        if topic in topic_fields:
            topic_fields[topic] = 1
    print('Topic fields:', topic_fields)
    try:
        conn = sqlite3.connect('database/preferences.db')
        c = conn.cursor()
        print('Inserting into database...')
        c.execute('INSERT INTO preferences (email, market_volatility_options, equities_indexes, macroeconomics, regulatory_compliance, alternative_assets_innovation, updt_ts) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
                  (email, topic_fields['Market Volatility & Options'], topic_fields['Equities and Indexes'], topic_fields['Macroeconomics'], topic_fields['Regulatory & Compliance News'], topic_fields['Alternative Assets & Innovation']))
        conn.commit()
        conn.close()
        print('Preferences saved successfully')
        return jsonify({'message': 'Preferences saved successfully'})
    except Exception as e:
        print('Database error:', e)
        return jsonify({'error': str(e)}), 500

@routes.route('/view_preferences', methods=['GET'])
def view_preferences():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400
    try:
        row = get_user_latest_preferences(email)
        if not row:
            return jsonify({'topics': []})
        topic_map = [
            ('Market Volatility & Options', row[0]),
            ('Equities and Indexes', row[1]),
            ('Macroeconomics', row[2]),
            ('Regulatory & Compliance News', row[3]),
            ('Alternative Assets & Innovation', row[4])
        ]
        selected_topics = [name for name, val in topic_map if val == 1]
        return jsonify({'topics': selected_topics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/fetch_daily_articles', methods=['GET'])
def fetch_daily_articles():
    """
    Fetch top 5 articles for each category and store in a daily JSON file.
    """
    daily_articles = {}
    for category in CATEGORIES:
        articles = fetch_news(category)[:5]
        daily_articles[category] = articles
    # Save to daily file
    today = datetime.now().strftime('%Y%m%d')
    out_dir = os.path.join('database', 'daily_articles')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'articles_{today}.json')
    with open(out_path, 'w') as f:
        json.dump(daily_articles, f, indent=2)
    print(f'Daily articles saved to {out_path}')
    return jsonify({'message': f'Daily articles saved to {out_path}', 'daily_articles': daily_articles})

@routes.route('/generate_topic_summaries', methods=['GET'])
def generate_topic_summaries():
    try:
        today = datetime.now().strftime('%Y%m%d')
        articles_dir = os.path.join('database', 'daily_articles')
        summaries_dir = os.path.join('database', 'daily_summaries')
        os.makedirs(summaries_dir, exist_ok=True)
        articles_path = os.path.join(articles_dir, f'articles_{today}.json')
        if not os.path.exists(articles_path):
            print(f'No daily articles file found: {articles_path}')
            return jsonify({'error': 'No daily articles file found'}), 404
        with open(articles_path, 'r') as f:
            daily_articles = json.load(f)

        topic_summaries = {}
        for topic, articles in daily_articles.items():
            urls = [article.get('link') for article in articles if article.get('link')]
            print('\n',f'Generating summary for topic "{topic}" with {len(urls)} URLs.')
            print('----------------------------------------------------------------')
            if urls:
                result = summarize_articles_from_urls(urls, openai_api_key=os.getenv("OPENAI_API_KEY"), topic=topic)
                topic_summaries[topic] = {
                    'summary': result['summary'],
                    'urls': urls,
                    'articles': result['articles']
                }
            else:
                topic_summaries[topic] = {
                    'summary': "No articles found.",
                    'urls': urls,
                    'articles': []
                }

        # Save to daily_summaries folder
        summaries_path = os.path.join(summaries_dir, f'summaries_{today}.json')
        with open(summaries_path, 'w') as f:
            json.dump(topic_summaries, f, indent=2)
        print(f'Topic summaries saved to {summaries_path}')
        return jsonify({'message': f'Topic summaries saved to {summaries_path}', 'summaries': topic_summaries})
    except Exception as e:
        return jsonify({'error': str(e)}), 500