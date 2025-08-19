# Daily Digest

**TL;DR for news.**

## Overview
Daily Digest is a full-stack web app that delivers concise news summaries based on your selected topics. Users can subscribe to topics and receive daily digests tailored to their preferences.

## Features
- Select your preferred news topics (choose from: Market Volatility & Options, Equities and Indexes, Macroeconomics, Regulatory & Compliance News, Alternative Assets & Innovation)
- View and update your topic preferences easily
- Receive personalized daily news digests via email
- Access concise summaries for each selected topic
- Stay informed with up-to-date articles tailored to your interests

## Project Structure
- `backend/` — Flask API, SQLite database, news fetching and summarization
- `frontend/` — React app for user interface
- `database/` — Database setup scripts

## Setup Instructions

### Backend
1. Install dependencies:
	```sh
	cd backend
	pip install -r requirements.txt
	```
2. Create database (if .db file does not exist in /database):
	```sh
	python ../database/preferences_db_setup.py
	```
3. Kick off the backend server:
	```sh
	python backend/app.py
	```

### Frontend
1. Install dependencies:
	```sh
	cd frontend
	npm install
	```
2. Start the frontend:
	```sh
	cd frontend && npm start
	```

## API Endpoints
| Method | Path                        | Description                                   |
|--------|-----------------------------|-----------------------------------------------|
| POST   | `/preferences`              | Set/Update user news topic preferences        |
| GET    | `/view_preferences`         | Retrieve current user topic preferences       |
| GET    | `/fetch_daily_articles`     | Fetch daily news articles for all topics      |
| GET    | `/generate_topic_summaries` | Generate summaries with articles passed in    |
| POST   | `/send_digest_now`          | Send the daily digest email immediately       |
| GET    | `/`                         | Welcome endpoint                              |

Each endpoint is designed to support the core features of Daily Digest, including managing preferences, fetching news, generating summaries, and sending digests.

## Environment Variables

The following environment variables are used throughout the codebase:

- `OPENAI_API_KEY`: Your OpenAI API key for generating summaries (used in backend/summarizer.py).
- `APIFY_CLIENT_TOKEN`: Your Apify API token for news scraping ([text](https://apify.com/pricing), [text](https://apify.com/store) ).
- `DAILY_DIGEST_GMAIL_USER`: Gmail address used to send digests (used in backend/send_daily_digest.py).
- `DAILY_DIGEST_GMAIL_PASS`: Gmail App Password for sending digests (used in backend/send_daily_digest.py).

Set these in your shell or `.env` file before running the backend:

```sh
export OPENAI_API_KEY=your_openai_key
export APIFY_CLIENT_TOKEN=your_apify_token
export DAILY_DIGEST_GMAIL_USER=youraddress@gmail.com
export DAILY_DIGEST_GMAIL_PASS="your_app_password"
```

**Note:** Gmail requires an App Password for SMTP. See Google Account security settings to generate one.
How to get Google App Password: [Google Support Guide](https://support.google.com/mail/answer/185833?hl=en)