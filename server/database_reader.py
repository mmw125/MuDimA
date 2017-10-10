import database_utils


def get_urls():
    """Gets all of the urls in articles in the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT link FROM article")
        return set(item[0] for item in cursor.fetchall())


def get_topics():
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT topic.name, topic.id, topic.image_url, count(*) FROM article, topic "
                       "WHERE article.topic_id = topic.id GROUP BY topic.id;")
        return sorted([{"title": item[0], "id": item[1], "image": item[2], "count": item[3]}
                       for item in cursor.fetchall()], key=lambda x: -x["count"])


def get_stories_for_topic(topic_id):
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name FROM topic WHERE id=?", (topic_id,))
        title = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM article WHERE topic_id=?", (topic_id,))
        return {"title": title, "articles": [(item[0], item[1]) for item in cursor.fetchall()]}


def get_grouped_articles():
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name, keywords, id, url FROM article")
        groups = {}
        for item in cursor.fetchall():
            name, keywords, id, url = item
            article = database_utils.Article(url=url, title=name, in_database=True)
            article.set_keywords(keywords)
            if id in groups:
                groups.get(id).add_article(article)
            else:
                group = database_utils.Grouping(article, in_database=True)
                group.set_uuid(id)
        return groups.values()


if __name__ == "__main__":  # pragma: no cover
    print get_topics()
    for topic in get_topics():
        print get_stories_for_topic(topic.get("id"))
