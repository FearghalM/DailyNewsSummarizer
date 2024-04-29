import os
import smtplib
import ssl
from email.message import EmailMessage
import csv

def send_email(subject, message, receiver_email, attachment_path=None):
    sender_email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')

    if not sender_email or not password:
        print("Email credentials not provided.")
        return

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(message)

    if attachment_path:
        with open(attachment_path, 'rb') as file:
            attachment_data = file.read()
        attachment_filename = os.path.basename(attachment_path)
        msg.add_attachment(attachment_data, maintype='application', subtype='octet-stream', filename=attachment_filename)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Example usage
subject = 'CSV File Email'
message = 'Please find the attached CSV file.'
receiver_email = 'femcmorrow@gmail.com'  # Update with the recipient's email address
csv_file_path = 'Articles/Ireland_articles.csv'  # Update with the path to your CSV file
send_email(subject, message, receiver_email, csv_file_path)
