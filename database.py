import sqlite3

from config import DATABASE_FILE


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(
            DATABASE_FILE,
            check_same_thread=False
        )

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS register_current (
            register INTEGER PRIMARY KEY,
            raw INTEGER,
            signed INTEGER,
            scaled REAL,
            updated TEXT
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS register_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            register INTEGER,
            raw INTEGER,
            signed INTEGER,
            scaled REAL
        )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()