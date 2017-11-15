"""Tests for the database reader."""

import classifier
import database_reader
import database_utils
import database_writer
import test_utils


class DatabaseReaderTest(test_utils.DatabaseTest):
    """Test database reader."""

    def test_write_read_similar(self):
        """Test writing then reading similar articles."""
        self.assertEqual(0, database_reader.get_number_topics())
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_groups(groups)
        stories = database_reader.get_stories_for_topic(groups[0].get_uuid())
        stories = set(a.get('link') for a in stories.get('articles'))
        self.assertEqual(stories, set(model.get_url() for model in test_utils.SIMILAR_ARTICLES))
        self.assertEqual(1, database_reader.get_number_topics())

    def test_get_urls(self):
        """Test getting urls from the database."""
        self.assertEqual(set(database_reader.get_urls()), set())
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_groups(groups)
        self.assertEqual(set(database_reader.get_urls()), set(model.get_url() for model in test_utils.SIMILAR_ARTICLES))

    def test_get_topics(self):
        """Test getting topics from the database."""
        self.assertEqual(0, database_reader.get_number_topics())
        self.assertEqual(set(database_reader.get_topics()), set())
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_groups(groups)
        self.assertEqual(database_reader.get_topics()[0]["title"], groups[0].get_title())

    def test_get_grouped_articles(self):
        """Test getting grouped articles from the database."""
        self.assertEqual(database_reader.get_grouped_articles(), [])
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_groups(groups)
        self.assertEqual(database_reader.get_grouped_articles()[0], groups[0])

    def test_populate_keywords(self):
        """Test writing and retrieving the keywords for an article."""
        article = test_utils.SIMILAR_ARTICLES[0]
        database_writer.write_articles([article])
        with database_utils.DatabaseConnection() as (connection, cursor):
            self.assertEqual(article.get_keywords(), database_reader._get_article_keywords(article.get_url(), cursor))
