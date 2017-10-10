import sqlite3
import os


def database_name():
    return "mudima.db"


def database_path(name):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), name)


class DatabaseConnection:
    def __init__(self, path=None, refresh=False):
        db_path = database_path(path if path else database_name())
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
        self.cursor.execute("""CREATE TABLE article (name TEXT, link TEXT, keywords TEXT, topic_id TEXT, date DATETIME,
                               FOREIGN KEY(topic_id) REFERENCES topic ON DELETE CASCADE)""")
        self.connection.commit()

    def __enter__(self):
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
