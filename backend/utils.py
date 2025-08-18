import sqlite3

def get_user_latest_preferences(email):
    conn = sqlite3.connect('database/preferences.db')
    c = conn.cursor()
    print(email)
    # remove " from email
    email = email.replace('"', '')
    c.execute('SELECT sports, entertainment, politics, economics, technology FROM preferences WHERE email = ? ORDER BY updt_ts DESC LIMIT 1', (email,))
    row = c.fetchone()
    conn.close()
    return row
