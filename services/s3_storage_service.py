"""S3 Storage Service"""
import os
from botocore.exceptions import ClientError
from base_classes.aws_client_base import AwsClientBase
from helpers.file_helper import FileHelper
from services.s3_progress_percentage import S3ProgressPercentage
from settings.aws_settings import AwsSettings


class S3StorageService(AwsClientBase):
    """S3 Storage class"""

    def __init__(self) -> None:
        super().__init__("s3")
        self.file_helper = FileHelper()

    def create_bucket(self, bucket_name: str):
        """Create an S3 bucket"""
        self.string_helper.validate_null_or_empty(bucket_name, "bucket_name")
        location = {'LocationConstraint': AwsSettings.REGION_NAME}
        try:
            self.client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location)
            print(f"Bucket created successfully. Name={bucket_name}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print("Bucket exists")
            else:
                raise e

    def list_buckets(self):
        """List buckets available"""
        response = self.client.list_buckets()
        buckets = response.get("Buckets")
        if not buckets:
            return []

        return [bucket["Name"] for bucket in buckets]

    def delete_bucket(self, bucket_name: str):
        """Delete a bucket"""
        self.string_helper.validate_null_or_empty(bucket_name, "bucket_name")

        # delete bucket contents
        self.resource.Bucket(bucket_name).objects.all().delete()

        # Delete bucket
        self.client.delete_bucket(Bucket=bucket_name)

    def upload_file(self, bucket: str, file_name: str,  object_name=None):
        """upload a file to S3
        bucket: bucket name in S3 to store
        file_name: file to read in the local machine
        object_name: name of the file at S3
        """
        self.string_helper.validate_null_or_empty(bucket, "bucket")
        self.string_helper.validate_null_or_empty(file_name, "file_name")

        if not self.file_helper.does_file_exist(file_name):
            raise FileNotFoundError(f"File doesnot exist. {file_name}")

        if self.string_helper.is_null_or_whitespace(object_name):
            object_name = os.path.basename(file_name)

        self.client.upload_file(file_name, bucket, object_name,
                                Callback=S3ProgressPercentage(file_name))

    def download_file(self, bucket: str, object_name: str, file_name: str):
        """Download file from S3
            bucket: S3 bucket name
            object_name: file name in S3 to download
            file_name: file name to save in the local machine
        """
        self.string_helper.validate_null_or_empty(bucket, "bucket")
        self.string_helper.validate_null_or_empty(object_name, "object_name")
        self.string_helper.validate_null_or_empty(file_name, "file_name")
        self.file_helper.make_directories_from_file_path(file_name)
        self.client.download_file(bucket, object_name, file_name)

    def create_presigned_url(self, bucket: str, object_name: str, expiration=3600):
        """
            Generate a presigned URL to share an S3 object
        """
        return self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket,
                "Key": object_name
            },
            ExpiresIn=expiration
        )
