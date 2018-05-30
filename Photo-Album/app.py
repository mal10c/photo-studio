import time
import os
from flask import Flask, request, redirect, send_from_directory
import os.path
import json

app = Flask(__name__)

#@app.after_request
#def add_header(r):
#    """
#    Add headers to both force latest IE rendering engine or Chrome Frame,
#    and also to cache the rendered page for 10 minutes.
#    """
#    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#    r.headers["Pragma"] = "no-cache"
#    r.headers["Expires"] = "0"
#    r.headers['Cache-Control'] = 'public, max-age=0'
#    return r

@app.route('/photos/<path:path>')
def send_photos(path):
    return send_from_directory('/photos', path)

@app.route('/<path:path>')
def catch_all(path):

    result = ""

    if path == "album":
        folder = request.args.get("folder")
        photoPath = "/photos/" + folder
        if os.path.isdir(photoPath):

            dataFileName = os.path.join(photoPath, "data.json")
            if os.path.isfile(dataFileName):
                with open(dataFileName) as f:
                    data = json.load(f)
                    result += "<div id=\"__fnameGreeting1\">Thank you " + data["fname"] + "</div>"
                    result += "<div id=\"__fnameGreeting2\">Your photos are all set to go to: " + data["email"] + "</div>"
                    #result += "<div id=\"__fnameGreeting3\">Press the button below when you're ready to send the photos.</div>"
                    result += "<div id=\"__fname\">" + data["fname"] + "</div>"
                    result += "<div id=\"__lname\">" + data["lname"] + "</div>"
                    result += "<div id=\"__email\">" + data["email"] + "</div>"

            for photo in os.listdir(photoPath):
                if photo.endswith("jpg"):
                    if "_LOGO_" in photo:
                        entirePath = "http://172.16.0.1:5011{}/{}".format(photoPath, photo)
                        result += "<img class=\"customerPhoto\" src=\"{}\" />".format(entirePath)
        else:
            result = "Directory not found"
    else:
        return "Invalid"

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

