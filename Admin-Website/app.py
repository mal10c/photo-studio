import time
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def hello():

    f = open("index.html", "r")
    html = f.read()
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

