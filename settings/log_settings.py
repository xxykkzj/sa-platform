"""Log Settings"""
import os
# from dotenv import load_dotenv
# load_dotenv()

# pylint: disable=too-few-public-methods


class LogSettings():
    """Log Settings clas"""
    NAME = os.getenv("LOG_NAME", "data-analytics")
    FILE_NAME = os.getenv("LOG_FILE_NAME", "app.log")
    BASE_DIRECTORY = os.getenv("LOG_BASE_DIRECTORY", ".")
    FOLDER = os.getenv("LOG_FOLDER", "logs")
    ROTATION_TIME = os.getenv("LOG_ROTATION_TIME", "midnight")
    ENCODING = os.getenv("LOG_ENCODING", "utf-8")
    BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "10"))
    LOG_FILE_PATH = os.path.join(BASE_DIRECTORY, FOLDER)

# pylint: disable=too-few-public-methods
