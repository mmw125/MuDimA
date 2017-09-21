import news_fetcher
import unittest

class NewsFetcherTest(unittest.TestCase):
    def test_get_top_headlines(self):
        news_fetcher.get_top_headlines()

    def test_get_sources(self):
        news_fetcher.get_sources()
