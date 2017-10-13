import database_reader
import json
import news_fetcher

from flask import Flask, render_template, abort, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/updateStories")
def update_stories():
    news_fetcher.update_database()


@app.route("/getSources")
def get_sources():
    return json.dumps([source.__dict__ for source in news_fetcher.get_sources(language="en")])


@app.route("/getTopics")
def get_topics():
    page_number = int(request.args.get("p", 0))
    return json.dumps(database_reader.get_topics(page_number=page_number))


@app.route("/getStories")
def get_stories_for_topic():
    topic_id = request.args.get("topic_id")
    return json.dumps(database_reader.get_stories_for_topic(topic_id))

if __name__ == "__main__":  # pragma: no cover
    app.run(host="localhost", port=80)
