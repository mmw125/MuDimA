import classifier
import database_reader
import database_utils
import database_writer
import test_utils
import unittest


class DatabaseReaderTest(unittest.TestCase):
    def setUp(self):
        with database_utils.DatabaseConnection(refresh=True):
            # clean the database
            pass

    def test_write_read_similar(self):
        groups = classifier.group_articles(test_utils.SIMILAR_URLS)
        database_writer.write_topics_to_database(groups)
        stories = database_reader.get_stories_for_topic(groups[0].get_uuid())
        stories = set(a[1] for a in stories.get('articles'))
        self.assertEqual(stories, set(test_utils.SIMILAR_URLS))
