"""Tests for the classifier."""

import classifier
import database_writer
import models
import test_utils


class ClassifierTest(test_utils.DatabaseTest):
    """Classifier tests."""

    def test_similar_urls(self):
        """Test that similar urls get grouped together."""
        self.assertEqual(1, len(classifier.group_articles(test_utils.SIMILAR_ARTICLES)))

    def test_similar_urls_one_in_database(self):
        """Test that similar urls get grouped together when one is already in the database."""
        groupings = classifier.group_articles([test_utils.SIMILAR_ARTICLES[0]])
        database_writer.write_groups(groupings)
        self.assertEqual(1, len(classifier.group_articles([test_utils.SIMILAR_ARTICLES[1]])))

    def test_dissimilar_urls(self):
        """Test that dissimilar urls do not get grouped together."""
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_ARTICLES)))

    def test_keywordless_articles(self):
        """Tests that keywordless articles are put into a separate grouping."""
        articles = [models.Article(url="example.com", keywords=[]), models.Article(url="test.com", keywords=[])]
        articles.extend(test_utils.SIMILAR_ARTICLES)
        groups = classifier.group_articles(articles)
        self.assertEqual(2, len(groups))
        for group in groups:
            if len(group.get_articles()[0].get_keywords()) == 0:
                self.assertTrue(group.in_database())
