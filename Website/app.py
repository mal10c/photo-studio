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

    # Thoughts on how I could make this all work:
    #   * Create stand alone html pages that are loaded by this function
    #
    #   * website:
    #       - [X] sends countdown time, number of photos, email, first/last name to countdown-service
    #       - [X] also works with the countdown-service to display a smaller countdown
    #       - works with photo-album to retrieve list of photos, then shows them
    #       - user selects best photos
    #       - sends best photos to email-service
    #   * countdown-service
    #       - countdown-website page(s) will pull from this for the countdown time
    #       - [X] this will send a request to camera-controller to take the photo
    #       - [X] event if countdown timer is zero, still goes through this service
    #       - [X] knows how many pictures should be taken (and does the countdown for each one)
    #       - sends unique id to camera-controller so photos can be organized, and we know what's what
    #   * camera-controller:
    #       - [X] saves the photos in /share
    #       - [X] sends request to photo-mod to insert logo
    #   * photo-mod:
    #       - [X] places logo in corner
    #   * photo-album:
    #       - rename photos to this
    #       - returns list of photos that match a key
    #   * email-service:
    #       - emails photos as attachments
    #       - compiles rich text email from local file template

    html = """
        {}
        <form action="http://{}:5002" method="get" target="dummyframe">
            <input type="submit" value="Take Picture"/>
        </form>
        """.format(iframe, name)

    return html + '\nWoot hi!\n' + request.url_root

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

