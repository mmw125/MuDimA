"""Tests the news fetcher."""

import news_fetcher
import unittest


class NewsFetcherTest(unittest.TestCase):
    """Tests the news fetcher."""

    @staticmethod
    def test_get_top_headlines():
        """Ensure that the get top headlines doesn't crash."""
        news_fetcher.get_top_headlines()

    @staticmethod
    def test_get_sources():
        """Ensure that the get top headlines doesn't crash."""
        news_fetcher.get_sources()
