"""SQS Settings module"""

# pylint: disable=too-few-public-methods


class SqsSettings():
    """SQS Settings class"""
    QUEUE_DELAY_SECONDS = "60"
    MESSAGE_RETENTION_PERIOD = "86400"
    SEND_MESSAGE_DELAY_SECONDS = 0
    MAX_NUMBER_OF_MESSAGES = 10
    VISIBILITY_TIMEOUT = 60
    WAIT_TIME_SECONDS = 60

# pylint: enable=too-few-public-methods
