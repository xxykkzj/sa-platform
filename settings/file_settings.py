"""File constants"""
import os
# from dotenv import load_dotenv
# load_dotenv()

# pylint: disable=too-few-public-methods


class FileSettings():
    """File Settings"""
    ROOT_PATH = os.getenv("ROOT_PATH", ".")
    DATA_ROOT_PATH = os.getenv(
        "DATA_ROOT_PATH", os.path.join(ROOT_PATH, "data"))
    EXPORT_EXCEL_ROOT_PATH = os.getenv(
        "EXPORT_EXCEL_ROOT_PATH", os.path.join(DATA_ROOT_PATH, "export"))
    URL_STATUS_EXPORT_PATH = os.getenv("URL_STATUS_EXPORT_PATH",
                                       os.path.join(DATA_ROOT_PATH, "export", "url_status"))

# pylint: enable=too-few-public-methods
