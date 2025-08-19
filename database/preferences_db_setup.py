import sqlite3

def init_db():
    conn = sqlite3.connect('database/preferences.db')
    c = conn.cursor()
    c.execute('''
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    market_volatility_options INTEGER DEFAULT 0,
    equities_indexes INTEGER DEFAULT 0,
    macroeconomics INTEGER DEFAULT 0,
    regulatory_compliance INTEGER DEFAULT 0,
    alternative_assets_innovation INTEGER DEFAULT 0,
    updt_ts TIMESTAMP
)
''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
