import sqlite3
import os

DB_NAME = "mudima.db"


class DatabaseConnection:
    def __init__(self, path=DB_NAME, refresh=False):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        exists = os.path.exists(db_path)
        if exists and refresh:
            os.remove(db_path)
            exists = False
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        if not exists:
            self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE topic (name TEXT, id TEXT PRIMARY KEY, image_url TEXT)""")
        self.cursor.execute("""CREATE TABLE article (name TEXT, link TEXT, keywords TEXT, topic_id TEXT,
                               FOREIGN KEY(topic_id) REFERENCES topic)""")
        self.connection.commit()

    def __enter__(self):
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
