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
percent = "0.4"
email = ""
fname = ""
lname = ""
masterCt = 0

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
        e = request.args.get("email")
        fn = request.args.get("fname")
        ln = request.args.get("lname")
        if state == None:
            return sessionState
        elif state == "active":
            sessionState = "active"
            if t != None:
                global token
                token = t
            if e != None:
                global email
                email = e
            if fn != None:
                global fname
                fname = fn
            if ln != None:
                global lname
                lname = ln
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
        global percent

        p = request.args.get("photoCtToTake")
        c = request.args.get("countdownTime")
        per = request.args.get("percent")

        if p != None:
            photoCtToTake = p
        if c != None:
            countdownTime = c
        if per != None:
            percent = per

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
        global percent
        global email
        global fname
        global lname
        global masterCt

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
            takePhotoUrl = "http://172.16.0.1:5002/takePhoto?token=" + token + "&ct=" + str(ct) + "-" + str(masterCt) + "&p=" + percent + "&email=" + email + "&fname=" + fname + "&lname=" + lname
            masterCt += 1
            logging.info("URL: " + takePhotoUrl)
            contents = urllib2.urlopen(takePhotoUrl).read()

        logging.info("Received new photos from album!")
        photoPath = contents
        photoCountdown = "No"
        return photoPath

    else:
        return "unknown"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", debug=True)

