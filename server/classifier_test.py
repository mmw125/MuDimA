"""Tests for the classifier."""

import classifier
import test_utils
import unittest


class ClassifierTest(unittest.TestCase):
    """Classifier tests."""

    def test_similar_urls(self):
        """Test that similar urls get grouped together."""
        self.assertEqual(1, len(classifier.group_articles(test_utils.SIMILAR_ARTICLES)))

    def test_dissimilar_urls(self):
        """Test that dissimilar urls do not get grouped together."""
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_ARTICLES)))
