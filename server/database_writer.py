"""Functions that write to the database."""

import constants
import database_reader
import database_utils
import models
import sqlite3


def _print_status(name, i, out_of):
    if i is 0:
        print "Writing", out_of, name
    print ".",
    if i == out_of - 1:
        print "done"


def _write_article(article, cursor):
    try:
        cursor.execute("INSERT INTO article (name, link, image_url, keywords, date, article_text, source, favicon) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (article.get_title(), article.get_url(), article.get_url_to_image(),
                        " ".join(article.get_keywords()), article.get_published_at(),
                        article.get_text(), article.get_source().get_name(), article.get_favicon()))
    except sqlite3.IntegrityError as e:
        print "Integrity Error", e.message
    article.set_in_database(True)


def write_articles(article_list):
    """Write articles in the article list into the database."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        for i, article in enumerate(article_list):
            _print_status("articles", i, len(article_list))
            _write_article(article, cursor)


def write_groups(grouping_list=None):
    """Write groups in the grouping list into the database if they are not already there."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        for i, grouping in enumerate(grouping_list):
            _print_status("groups", i, len(grouping_list))
            if not grouping.in_database():
                cursor.execute("INSERT INTO topic (name, id, image_url, category) VALUES (?, ?, ?, ?)",
                               (grouping.get_title(), grouping.get_uuid(),
                                grouping.get_image_url(), grouping.get_category()))
                grouping.set_in_database(True)
            for article in grouping.get_new_articles():
                if not article.in_database():
                    _write_article(article, cursor)
                cursor.execute("UPDATE article SET topic_id = ? WHERE link = ?",
                               (grouping.get_uuid(), article.get_url()))


def write_group_fits(grouping_list=None):
    """Write the group fits into the database."""
    if grouping_list is None:
        group_ids = [str(id) for id in database_reader.get_groups_with_unfit_articles()]
        grouping_list = [group for group in database_reader.get_grouped_articles() if group.get_uuid() in group_ids]
    with database_utils.DatabaseConnection() as (connection, cursor):
        for i, grouping in enumerate(grouping_list):
            _print_status("group fits", i, len(grouping_list))
            for article, fit in grouping.calculate_fit():
                cursor.execute("UPDATE article SET group_fit_x = ?, group_fit_y = ? WHERE link = ?",
                               (fit[0], fit[1], article.get_url()))


def write_overall_fits(grouping_list=None):
    """Write overall fits into the database."""
    grouping_list = database_reader.get_grouped_articles() if grouping_list is None else grouping_list
    with database_utils.DatabaseConnection() as (connection, cursor):
        articles = [article for grouping in grouping_list for article in grouping.get_articles()]
        fits = models.calculate_fit(articles, max_iter=500)
        i = 1
        for article, fit in fits:
            _print_status("fits", i, len(fits))
            cursor.execute("UPDATE article SET fit_x = ?, fit_y = ? WHERE link = ?",
                           (fit[0], fit[1], article.get_url()))
            i += 1


def remove_grouping_from_database(grouping):
    """Remove the given grouping from the database with its associated articles."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        _remove_group_ids_from_database(grouping.get_uuid())
        grouping.set_in_database(False)
        for article in grouping.get_articles():
            article.set_in_database(False)


def _remove_group_ids_from_database(group_ids):
    """Remove the topics with the given ids from the database with the associated articles."""
    if isinstance(group_ids, (str, unicode)):
        group_ids = [group_ids]
    with database_utils.DatabaseConnection() as (connection, cursor):
        for group_id in group_ids:
            cursor.execute("""DELETE FROM topic WHERE id = ?""", (group_id,))
            cursor.execute("""DELETE FROM article WHERE topic_id = ?""", (group_id,))


def mark_item_as_clicked(url):
    """Mark the article as visited by incrementing its popularity."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("UPDATE article SET popularity = popularity + 1 WHERE link = ?", (url,))


def update_topic_pictures():
    """Mark the article as visited by incrementing its popularity."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        cursor.execute("SELECT id FROM topic WHERE image_url IS NULL")
        for id in [item[0] for item in cursor.fetchall()]:
            cursor.execute("SELECT image_url FROM article WHERE topic_id = ? AND image_url IS NOT NULL", (id,))
            item = cursor.fetchone()
            if item:
                cursor.execute("UPDATE topic SET image_url = ? WHERE id = ?", (item[0], id))


def clean_database():
    """Remove articles from the database when they are old."""
    with database_utils.DatabaseConnection() as (connection, cursor):
        # Remove all of the topics with no topic and
        cursor.execute("DELETE FROM article WHERE article.topic_id IS NULL "
                       "AND julianday(CURRENT_TIMESTAMP) - julianday(article.date) >= ?",
                       (constants.ARTICLE_REPLACEMENT_TIME,))

        # Remove all of the topics that only have articles that are over some number of days old
        cursor.execute("SELECT id FROM topic WHERE NOT EXISTS(SELECT 1 FROM article WHERE topic.id = article.topic_id "
                       "AND julianday(CURRENT_TIMESTAMP) - julianday(date) <= ?)",
                       (constants.ARTICLE_REPLACEMENT_TIME,))
        groups_to_remove = [item[0] for item in cursor.fetchall()]
        if groups_to_remove:
            print "Removing", len(groups_to_remove), "groups"
    _remove_group_ids_from_database(groups_to_remove)
