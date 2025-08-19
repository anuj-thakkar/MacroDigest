import sqlite3

def get_user_latest_preferences(email):
    conn = sqlite3.connect('database/preferences.db')
    c = conn.cursor()
    print(email)
    # remove " from email
    email = email.replace('"', '')
    c.execute('SELECT market_volatility_options, equities_indexes, macroeconomics, regulatory_compliance, alternative_assets_innovation FROM preferences WHERE email = ? ORDER BY updt_ts DESC LIMIT 1', (email,))
    row = c.fetchone()
    conn.close()
    return row

def save_user_preferences(email, topic_fields):
    conn = sqlite3.connect('database/preferences.db')
    c = conn.cursor()
    c.execute(
        '''INSERT INTO preferences (
            email, market_volatility_options, equities_indexes, macroeconomics,
            regulatory_compliance, alternative_assets_innovation, updt_ts
        ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
        (
            email,
            topic_fields['Market Volatility & Options'],
            topic_fields['Equities and Indexes'],
            topic_fields['Macroeconomics'],
            topic_fields['Regulatory & Compliance News'],
            topic_fields['Alternative Assets & Innovation']
        )
    )
    conn.commit()
    conn.close()
    return True