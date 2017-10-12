import classifier
import test_utils
import unittest


class ClassifierTest(unittest.TestCase):
    def test_similar_urls(self):
        self.assertEqual(1, len(classifier.group_articles(test_utils.SIMILAR_ARTICLES)))

    def test_dissimilar_urls(self):
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_ARTICLES)))
