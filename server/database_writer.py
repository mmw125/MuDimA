import database_utils as utils


def write_topics_to_database(grouping_list):
    with utils.DatabaseConnection() as (connection, cursor):
        for grouping in grouping_list:
            cursor.execute("""INSERT INTO topic (name, id, image_url) VALUES (?, ?, ?)""",
                           (grouping.get_title(), grouping.get_uuid(), grouping.get_image_url()))
            for article in grouping.get_articles():
                cursor.execute("""INSERT INTO article (name, link, keywords, topic_id)
                               VALUES (?, ?, ?, ?)""", (article.get_title(), article.get_url(),
                                                        " ".join(article.get_keywords()), grouping.get_uuid()))
        connection.commit()
