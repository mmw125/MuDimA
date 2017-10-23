"""Tests the news fetcher."""

import models
import news_fetcher
import unittest
import mock
import requests
import database_utils
import os


# This method will be used by the mock to replace requests.get
def mocked_sources_get(*args, **kwargs):
    file_object = open("server/api_sources.json", "r")
    response = requests.Response()
    response.raw = file_object
    return response


# This method will be used by the mock to replace requests.get
def mocked_top_sources_get(*args, **kwargs):
    file_object = open("server/api_top_headlines.json", "r")
    response = requests.Response()
    response.raw = file_object
    return response


class NewsFetcherTest(unittest.TestCase):

    def setUp(self):
        """Set up the class for the tests."""
        self._database_name_mock = mock.patch("server.database_utils.database_name", return_value="mudima_test.db")
        self._database_name_mock.start()
        self._database_location = database_utils.database_path(database_utils.database_name())
        self._delete_database()

    def tearDown(self):
            """Tear down the class for the tests."""
            self._delete_database()
            self._database_name_mock.stop()

    def _delete_database(self):
            if os.path.exists(self._database_location):
                os.remove(self._database_location)

    @mock.patch('requests.get', side_effect=mocked_sources_get)
    def test_get_sources(self, mock_get):
        self.source = news_fetcher.get_sources()[0]
        self.assertEqual(self.source.get_id(), "test")
        self.assertEqual(self.source.get_name(), "test")
        self.assertEqual(self.source.get_description(), "test")
        self.assertEqual(self.source.get_url(), "http://test.test.test")
        self.assertEqual(self.source.get_category(), "general")
        self.assertEqual(self.source.get_language(), "en")
        self.assertEqual(self.source.get_country(), "us")

    @mock.patch('requests.get', side_effect=mocked_top_sources_get)
    def test_get_top_headlines(self, mock_get):
        self.top_headline = news_fetcher.get_top_headlines()[0]
        # {"id": "usa-today", "name": "USA Today"}, "author":"Mason", "title":"'Stealthing' is sexual assault
        # and Congress
        # should address it, lawmakers say", "description":"Removing a condom without consent can lead to unplanned
        # pregnancies and STIs.", "url":"https://www.usatoday.com/story/news/politics/onpolitics/2017/10/04/
        # lawmakers-stealthing-sexual-assault-and-congress-should-address/731654001/", "urlToImage":
        # "https://www.gannett-cdn.com/-mm-/db62a81b840494f0b0e56270aad022e81a5517e8/
        # c=0-305-6000-3695&r=x1683&c=3200x1680/local/-/media/2017/10/04/USATODAY/
        # USATODAY/636427300339395388-GettyImages-623210788.jpg", "publishedAt":"2017-10-04T19:30:15Z"}

        self.assertEqual(self.top_headline.get_source().get_id(), "usa-today")
        self.assertEqual(self.top_headline.get_source().get_name(), "USA Today")
        self.assertEqual(self.top_headline.get_author(), "Mason")
        self.assertEqual(self.top_headline.get_title(), "'Stealthing' is sexual assault and "
                                                        "Congress should address it, lawmakers say")
        self.assertEqual(self.top_headline.get_description(), "Removing a condom without consent can lead to "
                                                              "unplanned pregnancies and STIs.")
        self.assertEqual(self.top_headline.get_url(), "https://www.usatoday.com/story/news/politics/"
                                                      "onpolitics/2017/10/04/lawmakers-stealthing-"
                                                      "sexual-assault-and-congress-should-address/731654001/")
        self.assertEqual(self.top_headline.get_url_to_image(), "https://www.gannett-cdn.com/-mm-/"
                                                               "db62a81b840494f0b0e56270aad022e81a5517e8/c=0-305-6000"
                                                               "-3695&r=x1683&c=3200x1680/local/-/media/2017/10/04/"
                                                               "USATODAY/USATODAY/636427300339395388-GettyImages-"
                                                               "623210788.jpg")
        self.assertEqual(self.top_headline.get_published_at(), "2017-10-04T19:30:15Z")
        self.assertIsNotNone(self.top_headline.get_text())

    @mock.patch('requests.get', side_effect=mocked_top_sources_get)
    def test_get_top_headlines_null(self, mock_get):
        self.top_headline = news_fetcher.get_top_headlines()[1]

        self.assertEqual(self.top_headline.get_source().get_id(), None)
        self.assertEqual(self.top_headline.get_source().get_name(), None)
        self.assertEqual(self.top_headline.get_author(), None)
        self.assertEqual(self.top_headline.get_title(), None)
        self.assertEqual(self.top_headline.get_description(), None)
        self.assertEqual(self.top_headline.get_url(), None)
        self.assertEqual(self.top_headline.get_url_to_image(), None)
        self.assertEqual(self.top_headline.get_published_at(), None)
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
