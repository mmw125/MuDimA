"""Defines the flask web server app."""

import constants
import database_reader
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
    return json.dumps([source.__dict__ for source in news_fetcher.get_sources(language="en")])


@app.route("/getTopics")
def get_topics():
    """Get the topics."""
    page_number = int(request.args.get("p", 0))
    category = request.args.get("category", None)
    return json.dumps(database_reader.get_topics(page_number=page_number, category=category))


@app.route("/getNumberTopics")
def get_number_pages():
    """Get the number of topics."""
    category = int(request.args.get("category", None))
    items_per_page = int(request.args.get("items_per_page", constants.ARTICLES_PER_PAGE))
    return json.dumps(database_reader.get_number_topics(category=category) / items_per_page)


@app.route("/getStories")
def get_stories_for_topic():
    """Get the stories for a topic id."""
    topic_id = request.args.get("topic_id")
    return json.dumps(database_reader.get_stories_for_topic(topic_id))


if __name__ == "__main__":  # pragma: no cover
    if not database_reader.get_urls():
        # If there is nothing in the database, update it
        print "Nothing in database. Populating..."
        news_fetcher.update_database()
    app.run(host="localhost", port=80)
