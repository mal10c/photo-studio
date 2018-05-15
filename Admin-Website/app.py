import time
import os
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def hello():

    f = open("index.html", "r")
    html = f.read()
    return html

@app.route('/<path:path>')
def catch_all(path):
    if os.path.isfile(path):
        f = open(path, "r")
        html = f.read()
        return html
    else:
        return '404'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

