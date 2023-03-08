import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_AUTH = os.environ.get("SECRET_AUTH")
