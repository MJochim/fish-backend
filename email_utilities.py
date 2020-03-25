import smtplib
from email.message import EmailMessage

import config


def send_email(sender, to, cc, subject, text):
    message = EmailMessage()
    message.set_content(text)

    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to
    message['Cc'] = cc

    smtp_connection = smtplib.SMTP(host = config.smtp_host, local_hostname = smtp_local_hostname)
    smtp_connection.starttls()
    smtp_connection.login(smtp_username, smtp_password)
    smtp_connection.send_message(message)
    smtp_connection.quit()
