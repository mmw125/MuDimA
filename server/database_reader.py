"""Functions for reading from the database."""

import constants
import database_utils
import models


def get_urls():
    """Get all of the urls in articles in the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT link FROM article;")
        urls = set(item[0] for item in cursor.fetchall())
        cursor.execute("SELECT link FROM bad_article;")
        return urls.union(item[0] for item in cursor.fetchall())


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
        total_items = get_number_topics()
        if category is None:
            cursor.execute("SELECT topic.name, topic.id, topic.image_url, topic.category, count(*) FROM article, topic "
                           "WHERE article.topic_id = topic.id AND article.topic_id IS NOT NULL "
                           "GROUP BY topic.id ORDER BY count(*) DESC;")
        else:
            cursor.execute("SELECT topic.name, topic.id, topic.image_url, topic.category, count(*) FROM article, topic "
                           "WHERE article.topic_id = topic.id AND topic.category = ? AND article.topic_id IS NOT NULL "
                           "GROUP BY topic.id ORDER BY count(*) DESC;", (category,))
        return sorted([{"total_items": total_items, "title": item[0], "id": item[1],
                        "image": item[2], "category": item[3], "count": item[4]}
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
        cursor.execute("SELECT name, link, image_url, fit_x, fit_y, popularity, source, favicon "
                       "FROM article WHERE topic_id=?",
                       (topic_id,))
        return {"title": title, "articles": [{"name": item[0], "link": item[1], "image": item[2], "x": item[3],
                                              "y": item[4], "popularity": item[5], "source": item[6], "favicon": item[7]
                                              } for item in cursor.fetchall()]}


def get_ungrouped_articles():
    """Get the items in the database and puts them into Article and Grouping objects."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name, link, article_text FROM article "
                       "WHERE article_text != '' AND topic_id IS NULL;")
        articles = []
        for item in cursor.fetchall():
            name, url, article_text = item
            articles.append(models.Article(url=url, title=name, text=article_text, in_database=True,
                                           keywords=_get_article_keywords(url, cursor)))
        return articles


def get_top_keywords(num=constants.DEFAULT_NUM_KEYWORDS):
    """Get the top keywords used in the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT keyword, COUNT(1) AS c FROM keyword GROUP BY keyword ORDER BY c DESC LIMIT ?;", (num,))
        return [item[0] for item in cursor.fetchall()]


def get_groups_with_unfit_articles():
    """Get the ids of the groups in the database that have articles that are not fit."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT topic_id FROM article WHERE group_fit_x IS NULL AND topic_id IS NOT NULL "
                       "GROUP BY topic_id;")
        return [i[0] for i in cursor.fetchall()]


def get_number_articles_without_overall_fit():
    """Get the number of articles in the database without an overall fit."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT topic_id FROM article WHERE group_fit_x IS NULL AND topic_id IS NOT NULL;")
        return len(cursor.fetchall())


def _get_article_keywords(article_url, cursor):
    """Get the keywords for the given article."""
    cursor.execute("SELECT keyword FROM keyword WHERE article_link = ?;", (article_url,))
    return set(item[0] for item in cursor.fetchall())


def get_grouped_articles():
    """Get the items in the database and puts them into Article and Grouping objects."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT name, topic_id, link, article_text, image_url FROM article "
                       "WHERE article_text != '' AND topic_id IS NOT NULL;")
        groups = {}
        for item in cursor.fetchall():
            name, id, url, article_text, image_url = item
            article = models.Article(url=url, title=name, text=article_text, urlToImage=image_url, in_database=True)
            article.set_keywords(_get_article_keywords(url, cursor))
            if id in groups:
                groups.get(id).add_article(article, new_article=False)
            else:
                groups[id] = models.Grouping(article, uuid=id, in_database=True, has_new_articles=False)
        return list(groups.values())

def get_articles(keyword, limit=10):
    """Get the items in the database and puts them into Article and Grouping objects."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT article_link FROM keyword JOIN article ON keyword.article_link = article.link "
                       "WHERE keyword = ? GROUP BY article_link ORDER BY date DESC;", (keyword, limit))
        cursor.fetchall()
