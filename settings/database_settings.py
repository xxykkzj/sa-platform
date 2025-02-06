"""Database settings module"""
import os

# pylint: disable=too-few-public-methods


class DatabaseSettings():
    """Database Settings class"""
    DB_URL= os.getenv("DB_URL")
    # DB_TYPE = os.getenv("DB_TYPE")
    # DB_HOST = os.getenv("DB_HOST")
    # DB_PORT = os.getenv("DB_PORT")
    # DB_NAME = os.getenv("DB_NAME", "data-analytics")
    # DB_USER = os.getenv("DB_USER")
    # DB_PASSWORD = os.getenv("DB_PASSWORD")

# pylint: enable=too-few-public-methods
