import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Protocol


class Sender(Protocol):
    def send(self, data: str):
        ...

class EmailSender(Sender):
    def send(self, data: str):
        msg = MIMEMultipart()
        msg['From'] = os.getenv('sender_email')
        msg['To'] = os.getenv('receiver_email')
        msg['Subject'] = os.getenv('subject')

        msg.attach(MIMEText(data, 'plain'))

        smtp_server = os.getenv('smtp_server')
        port = int(os.getenv('smtp_port'))

        server = smtplib.SMTP(smtp_server, port)
        try:
            server.starttls()

            sender_email = os.getenv('sender_email')
            password = os.getenv('password')
            server.login(sender_email, password)

            receiver_email = os.getenv('receiver_email')
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Email sent to {receiver_email}!")

        except Exception as e:
            print(f"Failed to send email: {str(e)}")

        finally:
            # Terminate the SMTP session
            server.quit()