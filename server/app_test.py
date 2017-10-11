import unittest
import app


class RunningTest(unittest.TestCase):
    def test_update_stories(self):
        self.assertIsNone(app.update_stories())

    def test_get_sources(self):
        self.assertIsNotNone(app.get_sources())

    def test_get_topics(self):
        self.assertIsNotNone(app.get_topics())
