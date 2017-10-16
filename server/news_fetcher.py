"""Fetches the news from the api."""

import classifier
import database_reader
import database_utils
import database_writer
import models
import requests

default_language = "en"
news_api_url = "http://beta.newsapi.org/v2/"
news_api_key = "25a1ccdea267479c95010aa442e376e5"


class NewsApiError(Exception):
    """An exception that happens from the news api."""

    pass


def _parse_response(response):
    """Parse the response from the news api."""
    response_dict = response.json()
    if response_dict.get("status") != "ok":
        raise NewsApiError(response_dict.get('message'))
    if response_dict.get("articles"):
        return {article["url"]: models.Article.create_from_dict(article)
                for article in response_dict.get("articles", [])}.values()
    return [models.Source(source) for source in response_dict.get("sources", [])]


def _build_url(endpoint, params=None):
    """Build the url to send to the news api."""
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
    """Get the top headlines from the news api."""
    url = _build_url("top-headlines", {"sources": sources, "q": q, "category": category,
                                       "language": language, "country": country})
    response = requests.get(url)
    return _parse_response(response)


def get_sources(language=default_language, category="", country=""):
    """Get the available sources from the news api."""
    url = _build_url("sources", {"language": language, "category": category, "country": country})
    response = requests.get(url)
    return _parse_response(response)


def update_database():
    """Update the database with all the headlines from get_top_headlines."""
    articles = get_top_headlines()
    urls_in_database = database_reader.get_urls()
    articles = [article for article in articles if article.get_url() not in urls_in_database]
    grouped = classifier.group_articles(articles)
    database_writer.write_topics_to_database(grouped)


if __name__ == "__main__":  # pragma: no cover
    with database_utils.DatabaseConnection(refresh=True):
        pass  # refresh the database
    update_database()
