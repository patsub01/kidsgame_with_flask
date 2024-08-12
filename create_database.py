# create_database.py
import sqlite3

def create_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
