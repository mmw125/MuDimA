import classifier
import database_utils
import news_fetcher
import test_utils
import unittest


class ClassifierTest(unittest.TestCase):
    def test_similar_urls(self):
        similar = [database_utils.Article(url) for url in test_utils.SIMILAR_URLS]
        self.assertEqual(1, len(classifier.group_articles(test_utils.SIMILAR_URLS)))

    def test_dissimilar_urls(self):
        dissimilar = [database_utils.Article(url) for url in test_utils.DISSIMILAR_URLS]
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_URLS)))
