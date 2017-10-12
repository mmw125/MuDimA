import classifier
import database_reader
import database_writer
import test_utils


class DatabaseReaderTest(test_utils.DatabaseTest):
    def test_write_read_similar(self):
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_topics_to_database(groups)
        stories = database_reader.get_stories_for_topic(groups[0].get_uuid())
        stories = set(a[1] for a in stories.get('articles'))
        self.assertEqual(stories, set(model.get_url() for model in test_utils.SIMILAR_ARTICLES))

    def test_get_urls(self):
        self.assertEqual(set(database_reader.get_urls()), set())
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_topics_to_database(groups)
        self.assertEqual(set(database_reader.get_urls()), set(model.get_url() for model in test_utils.SIMILAR_ARTICLES))

    def test_get_topics(self):
        self.assertEqual(set(database_reader.get_topics()), set())
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_topics_to_database(groups)
        self.assertEqual(database_reader.get_topics()[0]["title"], groups[0].get_title())

    def test_get_grouped_articles(self):
        self.assertEqual(database_reader.get_grouped_articles(), [])
        groups = classifier.group_articles(test_utils.SIMILAR_ARTICLES)
        database_writer.write_topics_to_database(groups)
        print database_reader.get_grouped_articles()
        self.assertEqual(database_reader.get_grouped_articles()[0], groups[0])
