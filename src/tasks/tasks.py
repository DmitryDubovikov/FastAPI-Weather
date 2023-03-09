import smtplib
from email.message import EmailMessage
from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_lowest_temperatures():
    email = EmailMessage()
    email["Subject"] = "lowest temperatures"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        """data""",
    )
    return email


def send_email_lowest_temperatures():
    email = get_email_lowest_temperatures()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
