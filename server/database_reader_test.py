
import database_reader
import unittest


class DatabaseReaderTest(unittest.TestCase):
    def test_get_topics(self):
        self.assertEqual({"123abc", "456dfg"}, set(database_reader.get_topics().keys()))

    def test_get_stories_for_topic(self):
        for key in database_reader.get_topics().keys():
            self.assertTrue(database_reader.get_stories_for_topic(key))
