import time
import os
from flask import Flask, request, redirect, send_from_directory

app = Flask(__name__)

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
