"""AWS Settings"""
import os

# pylint: disable=too-few-public-methods


class AwsSettings():
    """AWS Settings"""
    REGION_NAME = os.getenv("AWS_REGION_NAME")
    ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# pylint: disable=too-few-public-methods
