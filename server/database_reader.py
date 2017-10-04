import database_utils as utils


def get_topics():
    with utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT * FROM topic")
        return [{"title": item[0], "id": item[1], "image": item[2]} for item in cursor.fetchall()]


def get_stories_for_topic(topic_id):
    with utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT * FROM article WHERE Topic_id=?", topic_id)
        return cursor.fetchall()

if __name__ == "__main__":
    print get_topics()
    for topic in get_topics():
        print get_stories_for_topic(topic.get("id"))