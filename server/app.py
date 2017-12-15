"""Defines the flask web server app."""

import constants
import database_reader
import database_writer
import json
import news_fetcher

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/updateStories")
def update_stories():
    """Update the database."""
    news_fetcher.update_database()


@app.route("/getSources")
def get_sources():
    """Get the sources."""
    return json.dumps([database_reader.get_sources()])


@app.route("/getTopics")
def get_topics():
    """Get the topics."""
    page_number = int(request.args.get("p", 0))
    category = request.args.get("category", None)
    return json.dumps(database_reader.get_topics(page_number=page_number, category=category))


@app.route("/articles")
def get_articles():
    """Get articles with some filter."""
    keyword = request.args.get("kw", None)
    try:
        page = int(request.args.get("p", 0))
    except ValueError:
        page = 0
    try:
        limit = int(request.args.get("limit", constants.ARTICLES_PER_PAGE))
    except ValueError:
        limit = constants.ARTICLES_PER_PAGE
    order_by = request.args.get("limit")
    descending = bool(request.args.get("descending"))
    return json.dumps(database_reader.get_articles(keyword=keyword, page=page, limit=limit,
                                                   order_by=order_by, descending=descending))


@app.route("/getNumberTopics")
def get_number_pages():
    """Get the number of topics."""
    category = int(request.args.get("category", None))
    items_per_page = int(request.args.get("items_per_page", constants.ARTICLES_PER_PAGE))
    return json.dumps(database_reader.get_number_topics(category=category) / items_per_page)


@app.route("/keywords")
def get_top_keywords():
    """Get the most used keywords in the database."""
    num_keywords = int(request.args.get("n", constants.DEFAULT_NUM_KEYWORDS))
    return json.dumps(database_reader.get_top_keywords(num_keywords))


@app.route("/getStories")
def get_stories_for_topic():
    """Get the stories for a topic id."""
    topic_id = request.args.get("topic_id")
    stories = database_reader.get_stories_for_topic(topic_id)
    stories["title"] = stories.get("title", constants.NO_SUCH_TOPIC)
    return json.dumps(database_reader.get_stories_for_topic(topic_id))


@app.route("/userClick", methods=['POST'])
def user_click():
    """Update the popularity when the user clicks on an article."""
    data = json.loads(request.data)
    if "url" in data:
        database_writer.mark_item_as_clicked(data["url"])
    return ""

@app.route("/getTruth")
def get_truth():
    """Get Truth-O-meter verified statements from Politifact API"""
    truth_count = int(request.args.get("n", 10))
    response = news_fetcher.get_truth(truth_count);
    return json.dumps(response.json())

if __name__ == "__main__":  # pragma: no cover
    if not database_reader.get_urls():
        # If there is nothing in the database, update it
        print "Nothing in database. Populating..."
        news_fetcher.update_database()
    app.run(host="localhost", port=80, threaded=True)
