from flask import Flask, render_template, abort, request
import json
import news_fetcher

app = Flask(__name__)


@app.route("/getStories")
def getStories():
    return json.dumps([a.__dict__ for a in news_fetcher.get_top_headlines()])


@app.route("/getStoryText")
def getStoryText():
    url = request.args.get("url")
    text = news_fetcher.Article(url=url).get_text()
    return json.dumps(text)

if __name__ == "__main__": app.run(host="localhost", port=80)
