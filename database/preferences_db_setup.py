import sqlite3

def init_db():
    conn = sqlite3.connect('database/preferences.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            sports INTEGER DEFAULT 0,
            entertainment INTEGER DEFAULT 0,
            politics INTEGER DEFAULT 0,
            economics INTEGER DEFAULT 0,
            technology INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
