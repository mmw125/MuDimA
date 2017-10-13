import constants
import database_utils
import models


def get_urls():
    """Gets all of the urls in articles in the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT link FROM article")
        return set(item[0] for item in cursor.fetchall())


def get_number_topics():
    """Gets just the number of topics from the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT 1 FROM article, topic "
                       "WHERE article.topic_id = topic.id GROUP BY topic.id ORDER BY count(*) DESC;")
        return len(cursor.fetchall())


def get_topics(page_number=0, articles_per_page=constants.ARTICLES_PER_PAGE):
    """Gets the topics for the given page."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        start = page_number * articles_per_page
        end = (page_number + 1) * articles_per_page
        cursor.execute("SELECT topic.name, topic.id, topic.image_url, count(*) FROM article, topic "
                       "WHERE article.topic_id = topic.id GROUP BY topic.id ORDER BY count(*) DESC;")
        return sorted([{"title": item[0], "id": item[1], "image": item[2], "count": item[3]}
                       for item in cursor.fetchall()[start:end]], key=lambda x: -x["count"])


def get_stories_for_topic(topic_id):
    """Gets all of the stories for the topic with the given topic id. Returns empty dict if topic not in database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name FROM topic WHERE id=?", (topic_id,))
        title = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM article WHERE topic_id=?", (topic_id,))
        return {"title": title, "articles": [(item[0], item[1]) for item in cursor.fetchall()]}


def get_grouped_articles():
    """Gets the items in the database and puts them into Article and Grouping objects."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name, keywords, topic_id, link FROM article")
        groups = {}
        for item in cursor.fetchall():
            name, keywords, id, url = item
            article = models.Article(url=url, title=name, in_database=True)
            article.set_keywords(keywords)
            if id in groups:
                groups.get(id).add_article(article)
            else:
                group = models.Grouping(article, in_database=True)
                group.set_uuid(id)
                groups[id] = group
        return list(groups.values())


if __name__ == "__main__":  # pragma: no cover
    print get_topics()
    for topic in get_topics():
        print get_stories_for_topic(topic.get("id"))
