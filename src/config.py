import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_AUTH = os.environ.get("SECRET_AUTH")

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")

API_KEY = os.environ.get("API_KEY")
