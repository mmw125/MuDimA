"""Test database writer."""

import database_reader
import database_writer
import models
import test_utils


class DatabaseWriterTest(test_utils.DatabaseTest):
    """Test database writer."""

    def test_write_topics_to_database_grouping_in_database(self):
        """Test remove grouping from database."""
        self.grouping.set_in_database(True)
        for article in self.grouping.get_articles():
            article.set_in_database(True)
        database_writer.write_groups([self.grouping])
        self.assertTrue(self.grouping.in_database())
        self.assertEqual(0, len(database_reader.get_urls()))

    def test_remove_grouping_from_database(self):
        """Test remove grouping from database."""
        database_writer.write_groups([self.grouping])
        self.assertTrue(self.grouping.in_database())
        self.assertEqual(1, len(database_reader.get_urls()))
        database_writer.remove_grouping_from_database(self.grouping)
        self.assertFalse(self.grouping.in_database())
        self.assertEqual(0, len(database_reader.get_urls()))

    def test_clean_database(self):
        """Test clean database."""
        database_writer.write_groups([self.grouping])
        self.assertEqual(1, len(database_reader.get_urls()))
        database_writer.clean_database()
        self.assertEqual(1, len(database_reader.get_urls()))
        grouping = models.Grouping(models.Article(url="google.com", publishedAt="2016-10-11T23:41:34Z", keywords=["a"]))
        database_writer.write_groups([grouping])
        self.assertEqual(2, len(database_reader.get_urls()))
        database_writer.clean_database()
        self.assertEqual(1, len(database_reader.get_urls()))
