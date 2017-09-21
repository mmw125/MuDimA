import classifier
import database_reader
import database_writer
import json
import news_fetcher

from flask import Flask, render_template, abort, request

app = Flask(__name__)


@app.route("/updateStories")
def update_stories():
    articles = news_fetcher.get_top_headlines()
    grouped = classifier.group_articles(articles)
    database_writer.write_topics_to_database(grouped)


@app.route("/getSources")
def get_sources():
    return json.dumps([source.__dict__ for source in news_fetcher.get_sources(language="en")])


@app.route("/getTopics")
def get_topics():
    return json.dumps(database_reader.get_topics())


@app.route("/getStories")
def get_stories_for_topic():
    topic_id = request.args.get("topic_id")
    return json.dumps(database_reader.get_stories_for_topic(topic_id))

if __name__ == "__main__": app.run(host="localhost", port=80)
