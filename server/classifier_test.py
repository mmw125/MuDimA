"""Tests for the classifier."""

import classifier
import database_writer
import models
import test_utils
import unittest
import news_fetcher
import mock
import database_utils
import os

class ClassifierTest(test_utils.DatabaseTest):
    """Classifier tests."""

    def test_similar_urls(self):
        """Test that similar urls get grouped together."""
        self.assertEqual(1, len(classifier.group_articles(test_utils.SIMILAR_ARTICLES)))

    def test_similar_urls_one_in_database(self):
        """Test that similar urls get grouped together when one is already in the database."""
        groupings = classifier.group_articles([test_utils.SIMILAR_ARTICLES[0]])
        database_writer.write_topics_to_database(groupings)
        self.assertEqual(1, len(classifier.group_articles([test_utils.SIMILAR_ARTICLES[1]])))

    def test_dissimilar_urls(self):
        dissimilar = [news_fetcher.Article(url) for url in test_utils.DISSIMILAR_URLS]
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_URLS)))


class RigerousClassifierTest(unittest.TestCase):

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

    def test_classifier_grouping(self):
        self.hurricane_harvy_urls = ["https://www.usnews.com/news/best-states/texas/articles/2017-10-03/"
                                     "hurricane-harvey-floods-hundreds-of-safe-deposit-boxes",
                                     "http://www.chron.com/business/energy/article/Hurricane-Harvey-cost"
                                     "-Occidental-Petroleum-some-12248946.php",
                                     "https://www.curbed.com/2017/10/2/16393922/houston-hurricane-harvey-recovery"]
        self.tom_petty_urls = ["https://www.nytimes.com/2017/10/03/arts/music/tom-petty-dead.html",
                               "http://www.rollingstone.com/music/news/tom-petty-rock-iconoclast-who-led-the-"
                               "heartbreakers-dead-at-66-w506651",
                               "https://www.cbsnews.com/news/tom-petty-dead-at-66-rocker-tom-petty-and-heartbreakers/",
                               "http://www.cnn.com/2017/10/03/entertainment/tom-petty-obit/index.html"]
        self.las_vegas_urls = ["https://www.nytimes.com/2017/10/03/us/las-vegas-shooting-live-updates.html",
                               "http://abcnews.go.com/US/las-vegas-massacre/story?id=50246458",
                               "http://www.foxnews.com/us/2017/10/03/las-vegas-shooter-installed-cameras"
                               "-in-and-out-hotel-room-ahead-premeditated-attack.html",
                               "http://www.chicagotribune.com/news/columnists/kass/ct-met-las-vegas-"
                               "shooting-kass-1004-story.html"]
        self.concat_articles = self.hurricane_harvy_urls + self.tom_petty_urls + self.las_vegas_urls
        self.assertEqual(3, len(classifier.group_articles(self.concat_articles)))


class FindURLErrorTest(unittest.TestCase):
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

    def test_parsing_issue(self):
        self.url = ["https://www.techwyse.com/blog/online-innovation/introducing-the-world's"
                    "-first-lorem-ipsum-website-checker/"]
        self.assertEqual(1, len(classifier.group_articles(self.url)))
        """Test that dissimilar urls do not get grouped together."""
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_ARTICLES)))

    def test_keywordless_articles(self):
        self.url = ["https://www.techwyse.com/blog/online-innovation/introducing-the-world's"
                    "-first-lorem-ipsum-website-checker/"]
        """Tests that keywordless articles are put into a separate grouping."""
        articles = [models.Article(url="example.com", keywords=[]), models.Article(url="test.com", keywords=[])]
        articles.extend(test_utils.SIMILAR_ARTICLES)
        groups = classifier.group_articles(articles)
        self.assertEqual(2, len(groups))
        for group in groups:
            if len(group.get_articles()[0].get_keywords()) == 0:
                self.assertTrue(group.in_database())
