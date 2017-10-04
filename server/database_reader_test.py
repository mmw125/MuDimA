import classifier
import database_reader
import database_writer
import news_fetcher
import unittest


class DatabaseReaderTest(unittest.TestCase):
    def test_get_topics(self):
        self.assertEqual({"123abc", "456dfg"}, set([i['id'] for i in database_reader.get_topics()['topics']]))

    def test_get_stories_for_topic(self):
        for val in database_reader.get_topics()['topics']:
            self.assertTrue(database_reader.get_stories_for_topic(val['id']))
