import smtplib
from celery import Celery
from email.message import EmailMessage
from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://redis:6379/0")


def get_email_lowest_temperatures(email_to: str):
    # TODO: refactor in one function
    email = EmailMessage()
    email["Subject"] = "lowest temperatures"
    email["From"] = SMTP_USER
    email["To"] = email_to

    email.set_content(
        """data""",
    )
    return email


def get_email_highest_temperatures():
    # TODO: refactor in one function
    email = EmailMessage()
    email["Subject"] = "highest temperatures"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        """data""",
    )
    return email


def send_email_lowest_temperatures(email_to: str):
    email = get_email_lowest_temperatures(email_to)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_email_highest_temperatures():
    email = get_email_highest_temperatures()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
