import newspaper
import requests

default_language = "en"
news_api_url = "http://beta.newsapi.org/v2/"
news_api_key = "25a1ccdea267479c95010aa442e376e5"


class Article:
    @staticmethod
    def create_from_dict(article_dict):
        return Article(**article_dict)

    def __init__(self, url, description="", title="", author="",
                 publishedAt="", source="", urlToImage="", text=None):
        self.description = description
        self.title = title
        self.url = url
        self.author = author
        self.publishedAt = publishedAt
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
        return self.source

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

    def get_keywords(self):
        if self.keywords is None:
            self._init_article()
            self.article.nlp()
            self.keywords = set(self.article.keywords)
        return self.keywords

    def keyword_similarity(self, other_article):
        similar = float(len(other_article.get_keywords().intersection(self.get_keywords())))
        return similar / min([len(other_article.get_keywords()), len(self.get_keywords())])

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


class NewsApiError(Exception):
    pass


def _parse_response(response):
    response_dict = response.json()
    if response_dict.get("status") != "ok":
        raise NewsApiError(response_dict.get('message'))
    if response_dict.get("articles"):
        return [Article.create_from_dict(article) for article in response_dict.get("articles", [])]
    return [Source(source) for source in response_dict.get("sources", [])]


def _build_url(endpoint, params=None):
    if params is None:
        params = dict()
    params["apiKey"] = news_api_key
    param_list = []
    for key, value in params.items():
        if not value:
            continue
        if isinstance(value, (list, tuple)):
            value = ','.join(value)
        param_list.append(str(key) + "=" + value)
    return news_api_url + endpoint + "?" + "&".join(param_list)


def get_top_headlines(sources=list(), q=list(), category="", language=default_language, country=""):
    url = _build_url("top-headlines", {"sources": sources, "q": q, "category": category,
                                       "language": language, "country": country})
    response = requests.get(url)
    return _parse_response(response)


# def get_everything(sources=list(), domains=list(), q=list(), category="",
#                    language=default_language, sort_by="", page=0):
#     url = _build_url("everything", {"sources": sources, "domains": domains, "q": q, "category": category,
#                                     "language": language, "sortBy": sort_by, "page": page})
#     print url
#     response = requests.get(url)
#     return _parse_response(response)


def get_sources(language=default_language, category="", country=""):
    url = _build_url("sources", {"language": language, "category": category, "country": country})
    response = requests.get(url)
    return _parse_response(response)

if __name__ == "__main__":
    articles = get_top_headlines()
    for article in articles[:5]:
        print(article)
    for source in get_sources()[:5]:
        print(source)
    for article in articles[:10]:
        article.get_url()
        article.get_text()
        print "-----------------"
