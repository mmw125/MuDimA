import database_utils
import mock
import os
import unittest

SIMILAR_URLS = ("https://www.nytimes.com/2017/09/25/us/politics/obamacare-repeal-susan-collins-dead.html",
                "http://thehill.com/policy/healthcare/352342-third-gop-senator-opposes-new-obamacare-"
                "repeal-killing-bill-ahead-of")

DISSIMILAR_URLS = (
    "https://www.washingtonpost.com/opinions/cassidy-is-sorry-about-the-cassidy-graham-"
    "process-he-should-be/2017/09/25/0cd234f0-a243-11e7-ade1-76d061d56efa_story.html",
    "https://www.cnet.com/au/news/7-things-to-know-before-upgrading-to-macos-high-sierra-10-13/")


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self._database_name_mock = mock.patch("server.database_utils.database_name", return_value="mudima_test.db")
        self._database_name_mock.start()
        self._database_location = database_utils.database_path(database_utils.database_name())
        self._delete_database()

    def tearDown(self):
        self._delete_database()
        self._database_name_mock.stop()

    def _delete_database(self):
        if os.path.exists(self._database_location):
            os.remove(self._database_location)
