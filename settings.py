import os
from dotenv import load_dotenv
from flask import Flask, request
import smtplib
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64




path_to_env_file = './.env'
load_dotenv(path_to_env_file)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

with open('client_secret_640267311334-kv6hobqs9eb9phhrv63bckg218oga5vi.apps.googleusercontent.com.json') as json_file:
    client_secret = json.load(json_file)

creds = Credentials.from_authorized_user_info(info=client_secret)

# Build the Gmail API client
gmail_service = build('gmail', 'v1', credentials=creds)

# Handle the form submission
def send_email(request):
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Validate the input
        if not name or not email or not message:
            return 'Please fill out all fields'

        # Send the email
        try:
            message = MIMEMultipart()
            text = MIMEText(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
            message.attach(text)
            message['to'] = 'Kalebnemwan2@gmail.com'
            message['subject'] = 'New Contact Form Submission'
            message['from'] = email
            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            send_message = (gmail_service.users().messages().send(userId="me", body=create_message).execute())
            return 'Email sent successfully'
        except Exception as error:
            return 'An error occurred: {}'.format(error)
    return 'Invalid request'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD")

        # Send the email
        to = EMAIL_HOST_USER
        subject = "Contact Form Submission"
        body = "Name: " + name + "\nEmail: " + email+ "\nNumber: " + phone + "\nMessage: " + message
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(email, to, msg)

        # Close the SMTP server
        server.quit()

        return "Thank you for your message!"
    else:
        return """
            <form method="post">
                <input type="text" name="name" placeholder="Name">
                <input type="email" name="email" placeholder="Email">
                <textarea name="message" placeholder="Message"></textarea>
                <input type="submit" value="Send">
            </form>
        """

if __name__ == '__main__':
    app.run()
