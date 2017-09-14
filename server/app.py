from flask import Flask, render_template, abort
import json

app = Flask(__name__)

@app.route("/getStories")
def getStories():
    return json.dumps({"value": "hi"})

if __name__ == "__main__": app.run(host='0.0.0.0', port=80)
