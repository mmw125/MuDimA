"""Various utilities for tests."""

import database_utils
import mock
import models
import os
import unittest

SIMILAR_ARTICLES = (
    models.Article("https://www.nytimes.com/2017/09/25/us/politics/obamacare-repeal-susan-collins-dead.html",
                   keywords={u'senators', u'repeal', u'support', u'bill', u'dead', u'gop', u'pivotal', u'health',
                             u'declares', u'opposition', u'mr', u'vote', u'senator', u'republicans', u'republican',
                             u'appears', u'care'}),
    models.Article("http://thehill.com/policy/healthcare/352342-third-gop-senator-opposes-new-obamacare-"
                   "repeal-killing-bill-ahead-of",
                   keywords={u'bill', u'trump', u'republicans', u'obamacare', u'dead', u'hearing', u'appears',
                             u'lastditch',
                             u'vote', u'collins', u'repeal', u'effort', u'gop'}))

DISSIMILAR_ARTICLES = (
    models.Article("https://www.washingtonpost.com/opinions/cassidy-is-sorry-about-the-cassidy-graham-"
                   "process-he-should-be/2017/09/25/0cd234f0-a243-11e7-ade1-76d061d56efa_story.html",
                   keywords={u'cassidygraham', u'votes', u'republicans', u'room', u'process', u'bill', u'hearing',
                             u'cassidy', u'sen', u'sorry', u'public'}),
    models.Article("https://www.cnet.com/au/news/7-things-to-know-before-upgrading-to-macos-high-sierra-10-13/",
                   keywords={
                       u'macos', u'apple', u'things', u'1013', u'upgrading', u'update', u'high', u'photos', u'know',
                       u'file', u'sierra', u'security', u'afs', u'dont'}))


class DatabaseTest(unittest.TestCase):
    """A parent class for the database class that handles mocking out the default database."""

    def setUp(self):
        """Set up the class for the tests."""
        self._database_name_mock = mock.patch("server.database_utils.database_name", return_value="mudima_test.db")
        self._database_name_mock.start()
        self._database_location = database_utils.database_path(database_utils.database_name())
        self._delete_database()
        self.article = models.Article("example.com", title="Example", keywords=["0", "1"])
        self.grouping = models.Grouping(self.article)

    def tearDown(self):
        """Tear down the class for the tests."""
        self._delete_database()
        self._database_name_mock.stop()

    def _delete_database(self):
        if os.path.exists(self._database_location):
            os.remove(self._database_location)
        for article in SIMILAR_ARTICLES:
            article.set_in_database(False)
        for article in DISSIMILAR_ARTICLES:
            article.set_in_database(False)
