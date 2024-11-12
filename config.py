import os

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("DB_HOST", "host.docker.internal")
    MYSQL_USER = os.getenv("DB_USERNAME", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "myrootpassword")
    MYSQL_DB = os.getenv("DB_NAME", "0ce")
    MYSQL_CURSORCLASS = "DictCursor"
