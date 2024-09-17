import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Protocol, TypeVar, Dict

from jinja2 import FileSystemLoader, Environment

from models import CurrencyModel
from portfolio_formatter import Formatter

T = TypeVar("T")


class Sender(Protocol):
    def send(self, data: T):
        ...


def send_message(msg, sender_email, server):
    receiver_email = os.getenv('receiver_email')
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print(f"Email sent to {receiver_email}!")


def login_smtp(server):
    sender_email = os.getenv('sender_email')
    password = os.getenv('password')
    server.login(sender_email, password)
    return sender_email


def fill_template(data):
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("email_template.html")
    output = template.render(data)
    return output


def compose_message(formatted_data):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('sender_email')
    msg['To'] = os.getenv('receiver_email')
    msg['Subject'] = os.getenv('subject')

    output = fill_template(formatted_data)
    msg.attach(MIMEText(output, 'html'))

    return msg


class EmailSender(Sender):
    def __init__(self, formatter: Formatter):
        self.formatter = formatter

    def send(self, data: Dict[str, CurrencyModel]):
        formatted_data = self.formatter.format(data)

        msg = compose_message(formatted_data)

        smtp_server = os.getenv('smtp_server')
        port = int(os.getenv('smtp_port'))

        server = smtplib.SMTP(smtp_server, port)
        try:
            server.starttls()

            sender_email = login_smtp(server)

            send_message(msg, sender_email, server)

        except Exception as e:
            print(f"Failed to send email: {str(e)}")

        finally:
            # Terminate the SMTP session
            server.quit()
