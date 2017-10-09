import database_utils as utils


def write_topics_to_database(grouping_list):
    with utils.DatabaseConnection() as (connection, cursor):
        for grouping in grouping_list:
            if not grouping.in_database():
                cursor.execute("""INSERT INTO topic (name, id, image_url) VALUES (?, ?, ?)""",
                               (grouping.get_title(), grouping.get_uuid(), grouping.get_image_url()))
                grouping.set_in_database(True)
            for article in grouping.get_articles():
                if not article.in_database():
                    cursor.execute("""INSERT INTO article (name, link, keywords, date, topic_id)
                                   VALUES (?, ?, ?, ?, ?)""", (article.get_title(), article.get_url(),
                                                               " ".join(article.get_keywords()),
                                                               article.get_published_at(),
                                                               grouping.get_uuid()))
                    article.set_in_database(True)
        connection.commit()


def remove_grouping_from_database(grouping):
    with utils.DatabaseConnection() as (connection, cursor):
        if not grouping.get_in_database():
            cursor.execute("""DELETE FROM topic WHERE id = ?""", (grouping.get_uuid(),))
            grouping.set_in_database(False)
        for article in grouping.get_articles():
            article.set_in_database(False)
        connection.commit()
