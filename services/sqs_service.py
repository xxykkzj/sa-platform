"""SQS implementation"""

import json
import logging
from base_classes.aws_client_base import AwsClientBase
from dtos.message_queue_dto import MessageQueueDto
from dtos.sqs_message_dto import SqsMessageDto
from settings.sqs_settings import SqsSettings


class SqsService(AwsClientBase):
    """SQS Service class"""

    def __init__(self, queue_name: str) -> None:
        super().__init__("sqs")
        self.logger = logging.getLogger(__name__)
        self.string_helper.validate_null_or_empty(queue_name, "queue_name")
        self.queue_name = queue_name
        self.create_queue(queue_name)

    def list_queues(self):
        """list SQS queues"""
        response = self.client.list_queues()
        return response.get("QueueUrls", [])

    def create_queue(self, queue_name: str):
        """Create SQS Queue"""
        self.logger.info("create_queue queue_name:%s", queue_name)
        self.string_helper.validate_null_or_empty(queue_name, "queue_name")

        response = self.client.create_queue(
            QueueName=queue_name,
            Attributes={
                "DelaySeconds": SqsSettings.QUEUE_DELAY_SECONDS,
                "MessageRetentionPeriod": SqsSettings.MESSAGE_RETENTION_PERIOD
            })

        return response.get("QueueUrl")

    def get_queue_url(self, queue_name: str):
        """Get queue url"""
        self.logger.info("get_queue_url queue_name:%s", queue_name)
        self.string_helper.validate_null_or_empty(queue_name, "queue_name")

        response = self.client.get_queue_url(QueueName=queue_name)
        return response.get("QueueUrl")

    def delete_queue(self, queue_url: str):
        """delete queue by it's url"""
        self.logger.info("delete_queue queue_url:%s", queue_url)
        self.string_helper.validate_null_or_empty(queue_url, "queue_url")

        self.client.delete_queue(QueueUrl=queue_url)

    def send_message(self,
                     message_queue_dto: MessageQueueDto,
                     delay_seconds=SqsSettings.SEND_MESSAGE_DELAY_SECONDS):
        """Send message to the SQS queue"""
        queue_url = self.get_queue_url(self.queue_name)
        self.logger.info(
            "send_message queue_url: %s, message: %s", queue_url, message_queue_dto)
        self.string_helper.validate_null_or_empty(queue_url, "queue_url")
        message_json = json.dumps(message_queue_dto.__dict__)

        response = self.client.send_message(
            QueueUrl=queue_url,
            DelaySeconds=delay_seconds,
            MessageBody=message_json)

        return response

    def receive_message(self,
                        number_of_messages=SqsSettings.MAX_NUMBER_OF_MESSAGES,
                        visibility_timeout=SqsSettings.VISIBILITY_TIMEOUT,
                        wait_time_seconds=SqsSettings.WAIT_TIME_SECONDS) -> list[SqsMessageDto]:
        """Receive message from the SQS queue"""
        queue_url = self.get_queue_url(self.queue_name)
        self.logger.info("receive_message queue_url: %s", queue_url)
        self.string_helper.validate_null_or_empty(queue_url, "queue_url")
        response = self.client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["All"],
            MaxNumberOfMessages=number_of_messages,
            MessageAttributeNames=["SentTimestamp", "ApproximateReceiveCount"],
            VisibilityTimeout=visibility_timeout,
            WaitTimeSeconds=wait_time_seconds
        )

        messages = response.get("Messages")
        if not messages:
            return []

        sqs_messages = []
        for message in messages:
            msg_obj = json.loads(message.get("Body"))
            attributes = message.get("Attributes")
            sqs_messages.append(SqsMessageDto(
                message_id=message.get("MessageId"),
                body=msg_obj,
                body_md5=message.get("MD5OfBody"),
                receipt_handle=message.get("ReceiptHandle"),
                sent_timestamp_milliseconds=attributes.get("SentTimestamp"),
                approximate_receive_count=attributes.get("ApproximateReceiveCount")))

        return sqs_messages

    def delete_message(self, queue_url: str, receipt_handle):
        """Delete message from the SQS queue"""
        self.logger.info(
            "delete_message, queue_url: %s, receipt_handle: %s", queue_url, receipt_handle)
        self.string_helper.validate_null_or_empty(queue_url, "queue_url")

        response = self.client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

        return response
