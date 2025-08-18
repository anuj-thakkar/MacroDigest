# Daily Digest

**TL;DR for news.**

## Overview
Daily Digest is a full-stack web app that delivers concise news summaries based on your selected topics. Users can subscribe to topics and receive daily digests tailored to their preferences.

## Features
- Select your preferred news topics (Sports, Entertainment / Pop Culture, Politics, Economics, Technology, Business)
- View and update your preferences
- Get daily news digests

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
2. Set up the database:
	```sh
	python ../database/preferences_db_setup.py
	```
3. Run the backend server:
	```sh
	flask run
	```

### Frontend
1. Install dependencies:
	```sh
	cd frontend
	npm install
	```
2. Start the frontend:
	```sh
	npm start
	```

## Usage
- Go to `http://localhost:3000` to view and manage your preferences.
- Go to `/settings` to update your selected topics.

## API Endpoints
- `POST /preferences` — Save preferences
- `GET /view_preferences?email=...` — View preferences for an email
- `POST /digest` — Get news digest for a topic