import time
import os
from flask import Flask, request, redirect

app = Flask(__name__)
sessionState = "inactive"

@app.route('/')
def hello():

    global sessionState
    html = """
        <script language="javascript">
            respondToMessage = function(e) {
                if((e.origin == 'http://132.250.60.1:5000') ||
                   (e.origin == 'http://132.250.60.1:5001')) {
                    if(e.data == 'sessionState')
                    {
                        e.source.postMessage('""" + sessionState + """', e.origin);
                    }
                }
            }
            window.addEventListener('message', respondToMessage, false);
        </script>
    """

    return html + "woo"

@app.route('/<path:path>')
def catch_all(path):
    if path == "session":
        global sessionState
        state = request.args.get("state")
        if state == "":
            return sessionState
        elif state == "active":
            sessionState = "active"
            return "ACTIVE"
        elif state == "inactive":
            sessionState = "inactive"
            return "INACTIVE"
        else:
            return "invalid"
    else:
        return "unknown"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

