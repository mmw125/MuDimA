
import database_reader
import unittest


class DatabaseReaderTest(unittest.TestCase):
    def get_topics_test(self):
        self.assertListEqual(["123abc", "456dfg"], database_reader.get_topics().keys())

    def get_stories_for_topic_test(self):
        for key in database_reader.get_topics().keys():
            self.assertTrue(database_reader.get_stories_for_topic(key))
