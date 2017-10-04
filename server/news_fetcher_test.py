import news_fetcher
import unittest
import mock
import requests

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    file_object = open("../test/api_top_headlines.json", "r")
    response = requests.Response()
    response.raw = file_object
    return response

class NewsFetcherTest(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):
        self.source =  news_fetcher.get_top_headlines()[0]
        self.assertEqual(self.source.get_id(), "test")
        self.assertEqual(self.source.get_name(), "test")
        self.assertEqual(self.source.get_description(), "test")
        self.assertEqual(self.source.get_url(), "http://test.test.test")
        self.assertEqual(self.source.get_category(), "general")
        self.assertEqual(self.source.get_language(), "en")
        self.assertEqual(self.source.get_country(), "us")

    @staticmethod
    def test_get_sources():
        news_fetcher.get_sources()
