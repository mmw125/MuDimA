from flask import Flask, render_template, abort
import json
import news_fetcher

app = Flask(__name__)

@app.route("/getStories")
def getStories():
    return json.dumps([a.__dict__ for a in news_fetcher.get_top_headlines()])

if __name__ == "__main__": app.run(host='localhost', port=80)
