"""Tests the news fetcher."""

import models
import news_fetcher
import unittest


class NewsFetcherTest(unittest.TestCase):
    """Tests the news fetcher."""

    def test_get_top_headlines(self):
        """Ensure that the get top headlines doesn't crash."""
        headlines = news_fetcher.get_top_headlines()
        self.assertIsInstance(headlines, list)
        for headline in headlines:
            self.assertIsInstance(headline, models.Article)

    def test_get_sources(self):
        """Ensure that the get top headlines doesn't crash."""
        sources = news_fetcher.get_sources()
        self.assertIsInstance(sources, list)
        for source in sources:
            self.assertIsInstance(source, models.Source)

    def test_parse_response_error(self):
        """Test parse_response with an error message."""
        response = {"status": "error", "message": "error_message"}
        with self.assertRaises(news_fetcher.NewsApiError):
            news_fetcher._parse_response(response)
