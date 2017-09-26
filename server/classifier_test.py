import classifier
import unittest


class ClassifierTest(unittest.TestCase):
    def setUp(self):
        self.similar_urls = ["https://www.nytimes.com/2017/09/25/us/politics/obamacare-repeal-susan-collins-dead.html",
                             "http://thehill.com/policy/healthcare/352342-third-gop-senator-opposes-new-obamacare-"
                             "repeal-killing-bill-ahead-of",
                             "https://www.washingtonpost.com/opinions/cassidy-is-sorry-about-the-cassidy-graham-"
                             "process-he-should-be/2017/09/25/0cd234f0-a243-11e7-ade1-76d061d56efa_story.html"]
        self.dissimilar_urls = [
            "https://www.washingtonpost.com/opinions/cassidy-is-sorry-about-the-cassidy-graham-"
            "process-he-should-be/2017/09/25/0cd234f0-a243-11e7-ade1-76d061d56efa_story.html",
            "https://www.cnet.com/au/news/7-things-to-know-before-upgrading-to-macos-high-sierra-10-13/"]

    def test_similar_urls(self):
        self.assertEqual(1, len(classifier.group_articles(self.similar_urls)))

    def test_dissimilar_urls(self):
        self.assertEqual(2, len(classifier.group_articles(self.dissimilar_urls)))
