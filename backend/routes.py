from flask import Blueprint, request, jsonify
from news_fetcher import fetch_news
from summarizer import summarize_articles
import logging
import sqlite3

routes = Blueprint('routes', __name__)

logger = logging.getLogger(__name__)

@routes.route("/digest", methods=["POST"])
def get_digest():
    logger.info("/digest route called")
    print("Request data:", request.json)
    data = request.json
    topic = data.get("topic")
    articles = fetch_news(topic)
    print("Fetched articles:", articles)
    #digest = summarize_articles(articles)
    #print("Digest:", digest)
    #return jsonify({"digest": digest})
    return jsonify({"digest": articles})


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
        'Sports': 0,
        'Entertainment / Pop Culture': 0,
        'Politics': 0,
        'Economics': 0,
        'Technology': 0
    }
    for topic in topics:
        if topic in topic_fields:
            topic_fields[topic] = 1
    print('Topic fields:', topic_fields)
    try:
        conn = sqlite3.connect('database/preferences.db')
        c = conn.cursor()
        print('Inserting into database...')
        c.execute('INSERT INTO preferences (email, sports, entertainment, politics, economics, technology) VALUES (?, ?, ?, ?, ?, ?)',
                  (email, topic_fields['Sports'], topic_fields['Entertainment / Pop Culture'], topic_fields['Politics'], topic_fields['Economics'], topic_fields['Technology']))
        conn.commit()
        conn.close()
        print('Preferences saved successfully')
        return jsonify({'message': 'Preferences saved successfully'})
    except Exception as e:
        print('Database error:', e)
        return jsonify({'error': str(e)}), 500

