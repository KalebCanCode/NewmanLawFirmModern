import os
from dotenv import load_dotenv
from flask import Flask, request
import smtplib

path_to_env_file = './.env'
load_dotenv(path_to_env_file)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

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
