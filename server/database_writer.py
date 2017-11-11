"""Functions that write to the database."""

import constants
import database_reader
import database_utils
import models


def write_articles(article_list, debug=False):
    """Write articles in the article list into the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        for i, article in enumerate(article_list):
            if debug:
                print "adding article", i, "out of", len(article_list)
            cursor.execute("""INSERT INTO article (name, link, image_url, keywords, date, article_text) 
                              VALUES (?, ?, ?, ?, ?, ?)""",
                           (article.get_title(), article.get_url(), article.get_url_to_image(),
                            " ".join(article.get_keywords()), article.get_published_at(), article.get_text()))
            connection.commit()


def write_topics(grouping_list):
    """Write groups in the grouping list into the database if they are not already there."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        for grouping in grouping_list:
            if not grouping.in_database():
                cursor.execute("INSERT INTO topic (name, id, image_url, category) VALUES (?, ?, ?, ?)",
                               (grouping.get_title(), grouping.get_uuid(),
                                grouping.get_image_url(), grouping.get_category()))
                grouping.set_in_database(True)
            for article in grouping.get_new_articles():
                cursor.execute("UPDATE article SET topic_id = ? WHERE link = ?",
                               (grouping.get_uuid(), article.get_url()))
            connection.commit()


def write_group_fits(grouping_list):
    with database_utils.DatabaseConnection() as (connection, cursor):
        for grouping in grouping_list:
            if grouping.has_new_articles():
                for article, fit in grouping.calculate_fit():
                    cursor.execute("UPDATE article SET group_fit_x = ?, group_fit_y = ? WHERE link = ?",
                                   (fit[0], fit[1], article.get_url()))


def write_overall_fits(grouping_list=None):
    grouping_list = database_reader.get_grouped_articles() if grouping_list is None else grouping_list
    with database_utils.DatabaseConnection() as (connection, cursor):
        articles = [article for grouping in grouping_list for article in grouping.get_articles()]
        for article, fit in models.calculate_fit(articles):
            cursor.execute("UPDATE article SET fit_x = ?, fit_y = ? WHERE link = ?",
                           (fit[0], fit[1], article.get_url()))
        connection.commit()


def remove_grouping_from_database(grouping):
    """Remove the given grouping from the database with its associated articles."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        _remove_group_ids_from_database(grouping.get_uuid())
        grouping.set_in_database(False)
        for article in grouping.get_articles():
            article.set_in_database(False)
        connection.commit()


def _remove_group_ids_from_database(group_ids):
    """Remove the topics with the given ids from the database with the associated articles."""
    if isinstance(group_ids, (str, unicode)):
        group_ids = [group_ids]
    with database_utils.DatabaseConnection() as (connection, cursor):
        for group_id in group_ids:
            cursor.execute("""DELETE FROM topic WHERE id = ?""", (group_id,))
            cursor.execute("""DELETE FROM article WHERE topic_id = ?""", (group_id,))
        connection.commit()


def mark_item_as_clicked(url):
    """Mark the article as visited by incrementing its popularity."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("UPDATE article SET popularity = popularity + 1 WHERE link = ?", (url,))
        connection.commit()


def clean_database():
    """Remove articles from the database when they are old."""
    groups_to_remove = []
    with database_utils.DatabaseConnection() as (connection, cursor):
        # Remove all of the topics with no topic and
        cursor.execute("DELETE FROM article WHERE article.topic_id IS NULL "
                       "AND julianday(CURRENT_TIMESTAMP) - julianday(article.date) <= ?",
                       (constants.ARTICLE_REPLACEMENT_TIME,))
        connection.commit()

        # Remove all of the topics that only have articles that are over some number of days old
        cursor.execute("SELECT id FROM topic WHERE NOT EXISTS(SELECT 1 FROM article WHERE topic.id = article.topic_id "
                       "AND julianday(CURRENT_TIMESTAMP) - julianday(date) <= ?)",
                       (constants.ARTICLE_REPLACEMENT_TIME,))
        groups_to_remove = [item[0] for item in cursor.fetchall()]
        connection.commit()
    _remove_group_ids_from_database(groups_to_remove)
