import news_fetcher
import unittest


class NewsFetcherTest(unittest.TestCase):
    @staticmethod
    def test_get_top_headlines():
        news_fetcher.get_top_headlines()

    @staticmethod
    def test_get_sources():
        news_fetcher.get_sources()
