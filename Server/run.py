from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods = ["GET"])
def root():
    return render_template("index.html")


def run(debug : bool):
    app.run(port = 48879, debug = debug)