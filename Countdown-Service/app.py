import time
import os
from flask import Flask, request, redirect

app = Flask(__name__)
sessionState = "inactive"
photoCtToTake = 0
countdownTime = 0
token = ""

@app.route('/')
def hello():

    global sessionState
    global token
    params = sessionState + "|" + token
    html = """
        <script language="javascript">
            respondToMessage = function(e) {
                if((e.origin == 'http://172.16.0.1:5000') ||
                   (e.origin == 'http://172.16.0.1:5001')) {
                    if(e.data == 'sessionState')
                    {
                        e.source.postMessage('""" + params + """', e.origin);
                    }
                }
            }
            window.addEventListener('message', respondToMessage, false);
        </script>
    """

    return html

@app.route('/<path:path>')
def catch_all(path):

    # Get session state
    if path == "session":
        global sessionState
        state = request.args.get("state")
        t = request.args.get("token")
        if state == "":
            return sessionState
        elif state == "active":
            sessionState = "active"
            if t != None:
                global token
                token = t
            return "ACTIVE"
        elif state == "inactive":
            sessionState = "inactive"
            return "INACTIVE"
        else:
            return "invalid"

    # Update adminInfo
    elif path == "adminInfo":
        
        global photoCtToTake
        global countdownTime

        p = request.args.get("photoCtToTake")
        c = request.args.get("countdownTime")

        if p != None:
            photoCtToTake = p
        if c != None:
            countdownTime = c

        return str(photoCtToTake) + ", " + str(countdownTime)

    elif path == "token":

        global token
        return token

    # Request a photo be taken
    elif path == "takePhoto":
        pass
    else:
        return "unknown"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

