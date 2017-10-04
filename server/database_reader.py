import database_utils as utils


def get_topics():
    with utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT * FROM topic")
        return cursor.fetchall()


def get_stories_for_topic(topic_id):
    with utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT * FROM article WHERE Topic_id=?", topic_id)
        return cursor.fetchall()
