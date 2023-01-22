import os
import json
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart


# Your credentials should be in a json file and should be loaded
# You can download the credentials from the google developer console
with open("/Users/kalebnewman/Desktop/newmanlawmodern/NewmanLawFirmModern/client_secret_640267311334-cilbp288u7hafcaedhgmuhins1p9am9i.apps.googleusercontent.com.json", "r") as f:
    credentials = json.load(f)

# Build the credentials object
from google.oauth2.credentials import Credentials
creds = Credentials.from_authorized_user_info(info=credentials)

def send_email(to_email, name, email, phone, message):
    try:
        # Create a Gmail client
        service = build('gmail', 'v1', credentials=creds)

        # Create the message
        message = MIMEMultipart()
        text = MIMEText(f"{message}\n\n Name: {name}\n Email: {email}\n Phone: {phone}")
        message.attach(text)

        # Send the message
        message['to'] = to_email
        message['subject'] = 'Contact Form Submission'
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {to_email} Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

# handle the post request here
def handle_request(request):
    data = request.form
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")
    to_email = "Kalebnewman2@gmail.com"

    send_email(to_email, name, email, phone, message)