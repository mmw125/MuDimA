import classifier
import news_fetcher
import test_utils
import unittest


class ClassifierTest(unittest.TestCase):
    def test_similar_urls(self):
        similar = [news_fetcher.Article(url) for url in test_utils.SIMILAR_URLS]
        self.assertEqual(1, len(classifier.group_articles(test_utils.SIMILAR_URLS)))

    def test_dissimilar_urls(self):
        dissimilar = [news_fetcher.Article(url) for url in test_utils.DISSIMILAR_URLS]
        self.assertEqual(2, len(classifier.group_articles(test_utils.DISSIMILAR_URLS)))


class RigerousClassifierTest(unittest.TestCase):
    def setUp(self):
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

    def test_classifier_grouping(self):
        self.concat_articles = self.hurricane_harvy_urls + self.tom_petty_urls + self.las_vegas_urls
        self.assertEqual(3, len(classifier.group_articles(self.concat_articles)))


class FindURLErrorTest(unittest.TestCase):
    def setUp(self):
        self.url = ["https://www.techwyse.com/blog/online-innovation/introducing-the-world's"
                    "-first-lorem-ipsum-website-checker/"]

    def test_parsing_issue(self) :
        self.assertEqual(1, len(classifier.group_articles(self.url)))