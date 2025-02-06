"""Base class for AWS Client"""
import boto3
from helpers.string_helper import StringHelper
from settings.aws_settings import AwsSettings

# pylint: disable=too-few-public-methods

class AwsClientBase():
    """Base class for AWS Client boto3"""
    def __init__(self, service_name) -> None:
        self.string_helper = StringHelper()
        self.string_helper.validate_null_or_empty(service_name, "service_name")
        self.string_helper.validate_null_or_empty(
            AwsSettings.REGION_NAME, "AwsSettings.REGION_NAME")
        self.string_helper.validate_null_or_empty(
            AwsSettings.ACCESS_KEY_ID, "AwsSettings.ACCESS_KEY_ID")
        self.string_helper.validate_null_or_empty(
            AwsSettings.SECRET_ACCESS_KEY, "AwsSettings.SECRET_ACCESS_KEY")

        self.client = boto3.client(
            service_name=service_name,
            region_name=AwsSettings.REGION_NAME,
            aws_access_key_id=AwsSettings.ACCESS_KEY_ID,
            aws_secret_access_key=AwsSettings.SECRET_ACCESS_KEY)

        self.resource = boto3.resource(service_name=service_name,
                                       region_name=AwsSettings.REGION_NAME,
                                       aws_access_key_id=AwsSettings.ACCESS_KEY_ID,
                                       aws_secret_access_key=AwsSettings.SECRET_ACCESS_KEY)


# pylint: disable=too-few-public-methods
