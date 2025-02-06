"""Google analytics constants"""
import os
# from dotenv import load_dotenv
# load_dotenv()


# pylint: disable=too-few-public-methods
class GoogleAnalyticsSettings():
    """Google Analytics Settings"""
    PROPERTY_ID = os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
    CREDENTIALS_DATA = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_DATA")
    CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# pylint: enable=too-few-public-methods
