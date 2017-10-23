"""All of the models that are used throughout the program."""

import collections
import newspaper
import uuid

from datetime import date
from dateutil import parser

from lxml import etree


class Article:
    """Represents an article."""

    @staticmethod
    def create_from_dict(article_dict, **kwargs):
        """Create an article from a dict."""
        article_dict.update(kwargs)
        return Article(**article_dict)

    def __init__(self, url, description="", title="", author="", publishedAt="", source={}, urlToImage="",
                 text=None, in_database=False, keywords=None, category=None):
        self.description = description
        self.title = title
        self.url = url
        self.author = author
        if publishedAt:
            try:
                self.publishedAt = parser.parse(publishedAt)
            except AttributeError:
                self.publishedAt = date.today()
        else:
            self.publishedAt = date.today()
        self.source = source
        self.urlToImage = urlToImage
        self.text = text
        self.article = None
        self.keywords = None
        self.set_keywords(keywords)
        self._in_database = in_database
        self.category = category

    def get_description(self):
        """Get description."""
        return self.description

    def get_title(self):
        """Get title."""
        return self.title

    def get_url(self):
        """Get url."""
        return self.url

    def get_author(self):
        """Get author's name."""
        return self.author

    def get_published_at(self):
        """Get published date and time."""
        return self.publishedAt

    def get_source(self):
        """Get the source for the article."""
        return Source(self.source)

    def get_url_to_image(self):
        """Get description."""
        return self.urlToImage

    def _init_article(self):
        if self.article is None:
            self.article = newspaper.Article(self.get_url())
            self.article.download()
            try:
                self.article.parse()
            except etree.XMLSyntaxError:
                pass

    def get_text(self):
        """Get the text of the article."""
        if self.article is None:
            self._init_article()
        return self.article.text

    def set_keywords(self, keywords):
        """Set the keywords for the article."""
        if keywords is None:
            return
        if isinstance(keywords, (str, unicode)):
            keywords = keywords.split(" ")
        self.keywords = set(keywords)

    def get_keywords(self):
        """Get the keywords for the article."""
        if self.keywords is not None:
            return self.keywords
        if self.article is None:
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
        """Get the sum of all of the lengths of the keywords."""
        return sum(len(i) for i in self.get_keywords())

    def keyword_similarity(self, other_article):
        """Get the similarity of the articles keywords."""
        similar = float(sum(len(title) for title in other_article.get_keywords().intersection(self.get_keywords())))
        return 0 if similar == 0 else similar / min([other_article.get_keyword_length(), self.get_keyword_length()])

    def in_database(self):
        """Get if the article is in the database."""
        return self._in_database

    def set_in_database(self, in_database):
        """Set if the article thinks it is in the database."""
        self._in_database = in_database

    def get_category(self):
        """Get the category of the article."""
        return self.category

    def __str__(self):  # pragma: no cover
        return " ".join((self.title, self.url)).encode("utf-8")

    def __eq__(self, other):
        return other.get_url() == self.get_url() if isinstance(other, Article) else False


class Source:
    """Represents a source that has articles."""

    def __init__(self, source):
        self._id = source.get("id")
        self._name = source.get("name")
        self._description = source.get("description")
        self._url = source.get("url")
        self._category = source.get("category")
        self._language = source.get("language")
        self._country = source.get("country")

    def get_id(self):
        """Get source id."""
        return self._id

    def get_name(self):
        """Get source name."""
        return self._name

    def get_description(self):
        """Get source description."""
        return self._description

    def get_url(self):
        """Get source url."""
        return self._url

    def get_category(self):
        """Get source category."""
        return self._category

    def get_language(self):
        """Get source language."""
        return self._language

    def get_country(self):
        """Get source country."""
        return self._country

    def __str__(self):  # pragma: no cover
        return " ".join((self._name, self._url)).encode("utf-8")


class Grouping(object):
    """Represents a set of articles that should be about the same topic."""

    def __init__(self, article, in_database=False):
        assert isinstance(article, Article)
        self._articles = [article]
        self._uuid = None
        self._in_database = in_database
        self._has_uuid = False

    def add_article(self, article):
        """Add the new article from the list."""
        assert isinstance(article, Article)
        self._articles.append(article)

    def get_articles(self):
        """Get the article in the grouping."""
        return self._articles

    def combine_group(self, group):
        """Absorb the items from the other group."""
        self._articles.extend(group.get_articles())

    def best_similarity(self, article):
        """Get the keyword similarity of the most similar article."""
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
        """Get the image url."""
        for article in self._articles:
            if article.get_url_to_image():
                return article.get_url_to_image()
        return None

    def set_uuid(self, uuid):
        """Set the uuid."""
        self._uuid = uuid
        self._has_uuid = True

    def get_uuid(self):
        """Get the uuid."""
        if not self._has_uuid:
            self._uuid = uuid.uuid4()
            self._has_uuid = True
        return str(self._uuid)

    def in_database(self):
        """Get if the group is in the database."""
        return self._in_database

    def set_in_database(self, in_database):
        """Set if group in database."""
        self._in_database = in_database

    def get_category(self):
        """Get group's category."""
        categories = collections.defaultdict(int)
        for article in self._articles:
            categories[article.get_category()] += 1
        largest_key, largest_value = 0, None
        for key, value in categories.iteritems():
            if value > largest_value:
                largest_key = key
        return largest_key

    def __str__(self):  # pragma: no cover
        return '\n'.join([str(art) for art in self._articles])

    def __eq__(self, other):
        return other.get_articles() == self.get_articles() if isinstance(other, Grouping) else False
