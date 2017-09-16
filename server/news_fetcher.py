import newspaper
import requests

news_api_url = "http://beta.newsapi.org/v2/"
news_api_key = "25a1ccdea267479c95010aa442e376e5"


class Article:
    def __init__(self, article):
        self._description = article.get("description")
        self._title = article.get("title")
        self._url = article.get("url")
        self._author = article.get("author")
        self._publishedAt = article.get("publishedAt")
        self._source = article.get("source")
        self._urlToImage = article.get("urlToImage")
        self._text = None

    def get_description(self):
        return self._description

    def get_title(self):
        return self._title

    def get_url(self):
        return self._url

    def get_author(self):
        return self._author

    def get_published_at(self):
        return self._publishedAt

    def get_source(self):
        return self._source

    def get_url_to_image(self):
        return self._urlToImage

    def get_text(self):
        if self._text is None:
            article = newspaper.Article(self.get_url())
            article.download()
            article.parse()
            self._text = article.text
        return self._text


    def __str__(self):
        return " ".join((self._title, self._url)).encode("utf-8")


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
        return [Article(article) for article in response_dict.get("articles", [])]
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


def get_top_headlines(sources=list(), q=list(), category="", language="en", country=""):
    url = _build_url("top-headlines", {"sources": sources, "q": q, "category": category,
                                       "language": language, "country": country})
    response = requests.get(url)
    return _parse_response(response)


def get_everything(sources=list(), domains=list(), q=list(), category="", language="en", sort_by="", page=0):
    url = _build_url("everything", {"sources": sources, "domains": domains, "q": q, "category": category,
                                       "language": language, "sortBy": sort_by, "page": page})
    response = requests.get(url)
    return _parse_response(response)


def get_sources(language="", category="", country=""):
    url = _build_url("sources", {"language": language, "category": category, "country": country})
    response = requests.get(url)
    return _parse_response(response)

if __name__ == "__main__":
    articles = get_top_headlines()
    for article in articles[:5]:
        print(article)
    for source in get_sources()[:5]:
        print(source)
    print articles[0].get_url()
    print articles[0].get_text()
    print "-----------------"
    print articles[1].get_url()
    print articles[1].get_text()
    print "-----------------"
    print articles[2].get_url()
    print articles[2].get_text()
