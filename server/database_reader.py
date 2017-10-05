import database_utils as utils


def get_topics():
    with utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT topic.name, topic.id, topic.image_url, count(*) FROM article, topic "
                       "WHERE article.topic_id = topic.id GROUP BY topic.id;")
        return sorted([{"title": item[0], "id": item[1], "image": item[2], "count": item[3]}
                       for item in cursor.fetchall()], key=lambda x: -x["count"])


def get_stories_for_topic(topic_id):
    with utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name FROM topic WHERE id=?", (topic_id,))
        title = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM article WHERE topic_id=?", (topic_id,))
        return {"title": title, "articles": [(item[0], item[1]) for item in cursor.fetchall()]}

if __name__ == "__main__":
    print get_topics()
    for topic in get_topics():
        print get_stories_for_topic(topic.get("id"))
