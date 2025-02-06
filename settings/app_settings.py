"""App settings module"""
import os
# from dotenv import load_dotenv

from enums.message_queue_provider import MessageQueueProvider
# load_dotenv()

# pylint: disable=too-few-public-methods
# pylint: disable=no-method-argument


class AppSettings():
    """App Settings"""
    USE_AWS = os.getenv("USE_AWS", "False") == "True"
    USE_RABBITMQ = os.getenv("USE_RABBITMQ", "False") == "True"

    def message_queue_provider():
        """message queue provider"""
        if AppSettings.USE_AWS:
            return MessageQueueProvider.SQS

        if AppSettings.USE_RABBITMQ:
            return MessageQueueProvider.RABBIT_MQ

        return MessageQueueProvider.NONE

# pylint: enable=too-few-public-methods
# pylint: enable=no-method-argument
