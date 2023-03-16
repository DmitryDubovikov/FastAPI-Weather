import smtplib
from celery import Celery
from email.message import EmailMessage
from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://redis:6379/0")


def get_email_last_weather(weather_data, email_to: str):
    email = EmailMessage()
    email["Subject"] = "last weather"
    email["From"] = SMTP_USER
    email["To"] = email_to

    email.set_content(
        weather_data,
    )
    return email


def send_email_last_weather_background_tasks(weather_data, email_to: str):
    send_email_last_weather(weather_data, email_to)


@celery.task
def send_email_last_weather_celery(weather_data, email_to: str):
    send_email_last_weather(weather_data, email_to)


def send_email_last_weather(weather_data, email_to: str):
    email = get_email_last_weather(weather_data, email_to)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
