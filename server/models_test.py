"""Tests the classes in the models.py file."""

import mock
import models
import test_utils
import unittest


class ArticleTest(unittest.TestCase):
    """Tests for the article class in the models file."""

    def test_get_keywords(self):
        """Check that it is able to parse example.com."""
        article = models.Article("http://www.example.com/")
        self.assertNotEqual(0, len(article.get_keywords()))
        self.assertIn("Example Domain", article.get_text())

    def test_get_keywords_bad_url(self):
        """Check that it does not error out when the url is bad."""
        article = models.Article("")
        with mock.patch("traceback.print_exc"):
            self.assertEqual(0, len(article.get_keywords()))
            self.assertEqual("", article.get_text())


class GroupingTest(unittest.TestCase):
    """Tests for the grouping class in the models file."""

    def test_combine_group(self):
        g0 = models.Grouping(test_utils.SIMILAR_ARTICLES[0])
        g1 = models.Grouping(test_utils.SIMILAR_ARTICLES[1])
        g0.combine_group(g1)
        self.assertEqual(list(test_utils.SIMILAR_ARTICLES[0:2]), list(g0.get_articles()))
