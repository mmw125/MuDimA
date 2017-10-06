import classifier
import database_utils
import database_writer
import requests

default_language = "en"
news_api_url = "http://beta.newsapi.org/v2/"
news_api_key = "25a1ccdea267479c95010aa442e376e5"


class NewsApiError(Exception):
    pass


def _parse_response(response):
    response_dict = response.json()
    if response_dict.get("status") != "ok":
        raise NewsApiError(response_dict.get('message'))
    if response_dict.get("articles"):
        return [database_utils.Article.create_from_dict(article) for article in response_dict.get("articles", [])]
    return [database_utils.Source(source) for source in response_dict.get("sources", [])]


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


def get_sources(language=default_language, category="", country=""):
    url = _build_url("sources", {"language": language, "category": category, "country": country})
    response = requests.get(url)
    return _parse_response(response)


def update_database():
    articles = get_top_headlines()[:100]
    grouped = classifier.group_articles(articles)
    database_writer.write_topics_to_database(grouped)

if __name__ == "__main__":  # pragma: no cover
    import database_utils
    with database_utils.DatabaseConnection(refresh=True):
        pass  # refresh the database
    update_database()
    import database_reader
    print database_reader.get_topics()
