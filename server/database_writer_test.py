import classifier
import database_reader
import database_writer
import models
import test_utils


class DatabaseWriterTest(test_utils.DatabaseTest):
    def test_write_topics_to_database_grouping_in_database(self):
        self.grouping.set_in_database(True)
        for article in self.grouping.get_articles():
            article.set_in_database(True)
        database_writer.write_topics_to_database([self.grouping])
        self.assertTrue(self.grouping.in_database())
        self.assertEqual(0, len(database_reader.get_urls()))

    def test_remove_grouping_from_database(self):
        database_writer.write_topics_to_database([self.grouping])
        self.assertTrue(self.grouping.in_database())
        self.assertEqual(1, len(database_reader.get_urls()))
        database_writer.remove_grouping_from_database(self.grouping)
        self.assertFalse(self.grouping.in_database())
        self.assertEqual(0, len(database_reader.get_urls()))
