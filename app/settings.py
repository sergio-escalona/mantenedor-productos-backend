import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")


def get_db_url(env: str) -> str:
    if env == "production":
        return os.getenv("DATABASE_URL_PROD")

    return os.getenv("DATABASE_URL_DEV")


DATABASE_URL = get_db_url(ENV)
API_URL = os.getenv("API_URL")
SECRET_KEY = os.getenv("SECURITY_SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_SECRET_KEY")
RECOVERY_KEY = os.getenv("RECOVERY_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES"))
RECOVERY_TOKEN_EXPIRE_MINUTES = int(os.getenv("RECOVERY_ACCESS_TOKEN_EXPIRE_MINUTES"))
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
