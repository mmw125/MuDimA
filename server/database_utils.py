import newspaper
import sqlite3
import os
import uuid

from datetime import date
from dateutil import parser


class Article:
    @staticmethod
    def create_from_dict(article_dict):
        return Article(**article_dict)

    def __init__(self, url, description="", title="", author="",
                 publishedAt="", source={}, urlToImage="", text=None):
        self.description = description
        self.title = title
        self.url = url
        self.author = author
        try:
            self.publishedAt = parser.parse(publishedAt)
        except AttributeError:
            self.publishedAt = date.today()
        print type(self.publishedAt)
        self.source = source
        self.urlToImage = urlToImage
        self.text = text
        self.article = None
        self.keywords = None

    def get_description(self):
        return self.description

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_author(self):
        return self.author

    def get_published_at(self):
        return self.publishedAt

    def get_source(self):
        return Source(self.source)

    def get_url_to_image(self):
        return self.urlToImage

    def _init_article(self):
        if self.article is None:
            self.article = newspaper.Article(self.get_url())
            self.article.download()
            self.article.parse()

    def get_text(self):
        if self.text is None:
            self._init_article()
            self.text = self.article.text
        return self.text

    def set_keywords(self, keywords):
        if isinstance(keywords, (str, unicode)):
            keywords = keywords.split(" ")
        self.keywords = keywords

    def get_keywords(self):
        if self.keywords is None:
            print self.get_url()
            self._init_article()
            if self.article.text:
                try:
                    self.article.nlp()
                    self.keywords = set(self.article.keywords)
                except newspaper.article.ArticleException:
                    self.keywords = set()
            else:
                self.keywords = set()
        return self.keywords

    def get_keyword_length(self):
        """Gets the sum of all of the lengths of the keywords."""
        return sum(len(i) for i in self.get_keywords())

    def keyword_similarity(self, other_article):
        similar = float(sum(len(title) for title in other_article.get_keywords().intersection(self.get_keywords())))
        return 0 if similar == 0 else similar / min([other_article.get_keyword_length(), self.get_keyword_length()])

    def __str__(self):
        return " ".join((self.title, self.url)).encode("utf-8")


class Source:
    def __init__(self, source):
        self._id = source.get("id")
        self._name = source.get("name")
        self._description = source.get("description")
        self._url = source.get("url")
        self._category = source.get("category")
        self._language = source.get("language")
        self._country = source.get("country")

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_url(self):
        return self._url

    def get_category(self):
        return self._category

    def get_language(self):
        return self._language

    def get_country(self):
        return self._country

    def __str__(self):
        return " ".join((self._name, self._url)).encode("utf-8")


class Grouping(object):
    """Represents a set of articles that should be about the same topic."""
    def __init__(self, article):
        self._articles = [article]
        self._uuid = None

    def add_article(self, article):
        self._articles.append(article)

    def get_articles(self):
        return self._articles

    def combine_group(self, group):
        self._articles.extend(group.get_articles())

    def best_similarity(self, article):
        return max(article.keyword_similarity(group_article) for group_article in self._articles)

    def get_title(self):
        """Find the title that has the most in common with the other titles."""
        if len(self._articles) == 1:
            return self._articles[0].get_title()
        best = None
        best_similarity = 0
        for article in self._articles:
            article_set = set(article.get_title().split(' '))
            similarities = []
            for other in self._articles:
                if article != other:
                    other_set = set(other.get_title().split(' '))
                    similar = float(len(other_set.intersection(article_set)))
                    similar = 0 if similar == 0 else similar / min((len(article_set), len(other_set)))
                    similarities.append(similar)
            similarity = sum(similarities) / max(len(similarities), 1)
            if similarity >= best_similarity:
                best_similarity = similarity
                best = article
        return best.get_title()

    def get_image_url(self):
        for article in self._articles:
            if article.get_url_to_image():
                return article.get_url_to_image()
        return None

    def set_uuid(self, uuid):
        self._uuid = uuid

    def get_uuid(self):
        if self._uuid is None:
            self._uuid = uuid.uuid4()
        return str(self._uuid)

    def __str__(self):
        return '\n'.join([str(art) for art in self._articles])


def database_name():
    return "mudima.db"


def database_path(name):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), name)


class DatabaseConnection:
    def __init__(self, path=None, refresh=False):
        db_path = database_path(path if path else database_name())
        exists = os.path.exists(db_path)
        if exists and refresh:
            os.remove(db_path)
            exists = False
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        if not exists:
            self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE topic (name TEXT, id TEXT PRIMARY KEY, image_url TEXT)""")
        self.cursor.execute("""CREATE TABLE article (name TEXT, link TEXT, keywords TEXT, topic_id TEXT, date DATETIME,
                               FOREIGN KEY(topic_id) REFERENCES topic)""")
        self.connection.commit()

    def __enter__(self):
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
