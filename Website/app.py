import time
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def hello():

    iframe = """
        <iframe width="0" height="0" border="0" name="dummyframe" id="dummyframe"></iframe>
        """

    host = request.host
    hostParts = host.split(":")
    if len(hostParts) == 2:
        name = hostParts[0]
    else:
        name = "0.0.0.0"

    html = """
        {}
        <form action="http://{}:5002" method="get" target="dummyframe">
            <input type="submit" value="Take Picture"/>
        </form>
        """.format(iframe, name)

    return html + '\nWoot hi!\n' + request.url_root

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

