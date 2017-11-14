"""Functions for reading from the database."""

import constants
import database_utils
import models


def get_urls():
    """Get all of the urls in articles in the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT link FROM article")
        return set(item[0] for item in cursor.fetchall())


def get_number_topics(category=None):
    """Get just the number of topics from the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        if category is None:
            cursor.execute("SELECT 1 FROM article, topic WHERE article.topic_id = topic.id AND "
                           "article.topic_id IS NOT NULL GROUP BY topic.id ORDER BY count(*) DESC;")
        else:
            cursor.execute("SELECT 1 FROM article, topic WHERE article.topic_id = topic.id AND article.category = ? AND"
                           " article.topic_id IS NOT NULL GROUP BY topic.id ORDER BY count(*) DESC;", (category,))
        return len(cursor.fetchall())


def get_topics(category=None, page_number=0, articles_per_page=constants.ARTICLES_PER_PAGE):
    """Get the topics for the given page."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        start = page_number * articles_per_page
        end = (page_number + 1) * articles_per_page
        if category is None:
            cursor.execute("SELECT topic.name, topic.id, topic.image_url, topic.category, count(*) FROM article, topic "
                           "WHERE article.topic_id = topic.id GROUP BY topic.id ORDER BY count(*) DESC;")
        else:
            cursor.execute("SELECT topic.name, topic.id, topic.image_url, topic.category, count(*) FROM article, topic "
                           "WHERE article.topic_id = topic.id AND topic.category = ? "
                           "GROUP BY topic.id ORDER BY count(*) DESC;", (category,))
        return sorted([{"title": item[0], "id": item[1], "image": item[2], "category": item[3], "count": item[4]}
                       for item in cursor.fetchall()[start:end]], key=lambda x: -x["count"])


def get_sources():
    """Get all of the stories for the topic with the given topic id. Returns empty dict if topic not in database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT source, count(1) FROM article GROUP BY source")
        return cursor.fetchall()


def get_stories_for_topic(topic_id):
    """Get all of the stories for the topic with the given topic id. Returns empty dict if topic not in database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name FROM topic WHERE id=?", (topic_id,))
        title = cursor.fetchone()[0]
        cursor.execute("SELECT name, link, image_url, fit_x, fit_y, popularity, source FROM article WHERE topic_id=?",
                       (topic_id,))
        return {"title": title, "articles": [{"name": item[0], "link": item[1], "image": item[2], "x": item[3],
                                              "y": item[4], "popularity": item[5], "source": item[6]}
                                             for item in cursor.fetchall()]}


def get_grouped_articles():
    """Get the items in the database and puts them into Article and Grouping objects."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name, keywords, topic_id, link, article_text FROM article")
        groups = {}
        for item in cursor.fetchall():
            name, keywords, id, url, article_text = item
            article = models.Article(url=url, title=name, in_database=True, text=article_text)
            article.set_keywords(keywords)
            if id in groups:
                groups.get(id).add_article(article)
            else:
                group = models.Grouping(article, in_database=True)
                group.set_uuid(id)
                groups[id] = group
        return list(groups.values())
