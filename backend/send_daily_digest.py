import sqlite3
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import markdown2
import time

# CONFIGURATION
GMAIL_USER = os.getenv('DAILY_DIGEST_GMAIL_USER')  # e.g. 'youraddress@gmail.com'
GMAIL_PASS = os.getenv('DAILY_DIGEST_GMAIL_PASS')  # App password
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'preferences.db'))
SUMMARIES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'daily_summaries'))
print(DB_PATH)
print(SUMMARIES_DIR)

# Helper: get all users and their topic preferences
def get_all_user_preferences():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT email, market_volatility_options, equities_indexes, macroeconomics, regulatory_compliance, alternative_assets_innovation FROM preferences')
    users = {}
    for row in c.fetchall():
        email = row[0]
        topics = []
        if row[1]: topics.append('Market Volatility & Options')
        if row[2]: topics.append('Equities and Indexes')
        if row[3]: topics.append('Macroeconomics')
        if row[4]: topics.append('Regulatory & Compliance News')
        if row[5]: topics.append('Alternative Assets & Innovation')
        users[email] = topics
    conn.close()
    return users

# Helper: get today's summaries
def get_today_summaries():
    today = datetime.now().strftime('%Y%m%d')
    summaries_path = os.path.join(SUMMARIES_DIR, f'summaries_{today}.json')
    if not os.path.exists(summaries_path):
        return None
    with open(summaries_path, 'r') as f:
        return json.load(f)

# Helper: format email body for a user
def format_email_body(user_topics, summaries):
    body = ""
    for topic in user_topics:
        if topic in summaries:
            summary_md = summaries[topic]['summary']
            summary_html = markdown2.markdown(summary_md)
            urls = summaries[topic]['urls']
            body += summary_html
            body += "<ul>"
            for url in urls:
                body += f'<li><a href="{url}">{url}</a></li>'
            body += "</ul>"
    return body

# Send email via Gmail SMTP
def send_email(to_email, subject, html_body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        print(f"Sent digest to {to_email} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Failed to send to {to_email}: {e}")

if __name__ == "__main__":
    users = get_all_user_preferences()
    summaries = get_today_summaries()
    if not summaries:
        print("No summaries found for today.")
        exit(1)
    for email, topics in users.items():
        if not topics:
            continue
        body = format_email_body(topics, summaries)
        send_email(email, "Your Daily Digest", body)

    print(f"All digests sent at {time.strftime('%Y-%m-%d %H:%M:%S')}.")
