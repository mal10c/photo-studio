import time
from time import sleep
import os
from flask import Flask, request, redirect
import logging
import urllib2

app = Flask(__name__)

sessionState = "inactive"
photoCtToTake = 1
countdownTime = 0
token = ""
photoCountdown = "No"
ctTimeLeft = 0
photoPath = ""

@app.route('/')
def hello():

    global sessionState
    global token
    global photoPath
    params = sessionState + "|" + token + "|" + photoCountdown + "|" + str(ctTimeLeft) + "|"
    if photoPath != "":
        fp = urllib2.urlopen("http://172.16.0.1:5011/album?folder=" + str(token))
        photoURLs = fp.read()
        photoURLs = photoURLs.decode("utf8")
        fp.close()
        params += photoURLs
        
    html = """
        <script language="javascript">
            respondToMessage = function(e) {
                if((e.origin == 'http://172.16.0.1:5000') ||
                   (e.origin == 'http://172.16.0.1:5001')) 
                {
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
        if state == None:
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
        
        global token
        global photoCtToTake
        global countdownTime
        global sessionState
        global photoCountdown
        global ctTimeLeft
        global photoPath

        countdownTime = int(countdownTime)
        ctTimeLeft = countdownTime

        contents = ""

        photoCountdown = "Yes"
        for ct in range(0, int(photoCtToTake)):
            for ctOffset in range(0, countdownTime + 1):
                ctTimeLeft = countdownTime - ctOffset
                logging.info("Countdown: " + str(ctTimeLeft))
                sleep(1)

            logging.info("Taking picture...")
            contents = urllib2.urlopen("http://172.16.0.1:5002/takePhoto?token=" + token + "&ct=" + str(ct)).read()

        logging.info("Received new photos from album!")
        photoPath = contents
        return photoPath

    else:
        return "unknown"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", debug=True)

