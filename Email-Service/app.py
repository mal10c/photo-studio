import time
from time import sleep
import os
from flask import Flask, request, redirect
import logging

from smtplib import SMTP

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import email
from email.mime.application import MIMEApplication
import json

app = Flask(__name__)


MY_ADDRESS = ''
PASSWORD = ''
emailToFname = ''
emailToLname = ''
emailToAddr = ''
emailToPhotos = []

def load_smtp_email_info():

    global MY_ADDRESS
    global PASSWORD

    with open('/share/smtp-email-info.json') as f:
        data = json.load(f)

        MY_ADDRESS = data["address"]
        PASSWORD = data["password"]

        logging.info("SMTP info: " + MY_ADDRESS + ", " + PASSWORD)

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def compose_and_send_email():

    global emailToFname
    global emailToLname
    global emailToAddr
    global emailToPhotos

    message_template = read_template('message.html')

    # set up the SMTP server
    s = SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    
    # Define these once; use them twice!
    strFrom = MY_ADDRESS
    strTo = emailToAddr

    # Create the root message and fill in the from, to, and subject headers
    #msgRoot = MIMEMultipart('related') <-- doesn't show image on ios
    #msgRoot = MIMEMultipart('mixed') <-- shows all images as attachments
    msgRoot = MIMEMultipart('mixed')
    msgRoot['Subject'] = 'Your Photos from St. Joseph Fun Days!'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    body = MIMEMultipart('alternative')

    msgText = MIMEText('This is the alternative plain text message.')
    body.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    message = message_template.substitute(PERSON_NAME=emailToFname)
    msgText = MIMEText(message, 'html')
    body.attach(msgText)

    msgRoot.attach(body)

    # Attach image(s)
    for filename in emailToPhotos:
        filename = filename.replace("http://172.16.0.1:5011", "")
        fp = open(filename, 'rb')
        att = MIMEApplication(fp.read())
        fp.close()
        att.add_header('Content-ID', '<jpg1>') # if no cid, client like MAil.app (only one?) don't show the attachment
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        att.add_header('Content-Disposition', 'inline', filename=filename)
        msgRoot.attach(att)

    # Send the email (this example assumes SMTP authentication is required)
    s.sendmail(strFrom, strTo, msgRoot.as_string())
        
    # Terminate the SMTP session and close the connection
    s.quit()

@app.route('/')
def hello():

    logging.info("Sending email")
    compose_and_send_email()
    return "Woot"

@app.route('/<path:path>')
def catch_all(path):

    if path == "sendEmail":

        global emailToFname
        global emailToLname
        global emailToAddr
        global emailToPhotos

        email = request.args.get("email")
        fname = request.args.get("fname")
        lname = request.args.get("lname")
        photos = request.args.get("images").split(",")

        emailToAddr = ''
        emailToFname = ''
        emailToLname = ''

        if email != None:
            emailToAddr = email
        if fname != None:
            emailToFname = fname
        if lname != None:
            emailToLname = lname

        emailToPhotos = []
        logging.info("Email info: {}, {}, {}".format(email, fname, lname))
        logging.info("Photos:")
        for photo in photos:
            logging.info(photo)
            emailToPhotos.append(photo)
        
        compose_and_send_email()

        return "OK"
    
    return "Invalid"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_smtp_email_info()
    app.run(host="0.0.0.0", debug=True)

