"""Message queue settings"""
import os
# from dotenv import load_dotenv

# load_dotenv()

# pylint: disable=too-few-public-methods


class MessageQueueSettings():
    """Message Queue Settings"""
    WAIT_SECONDS = int(os.getenv("MESSAGE_QUEUE_WAIT_SECONDS", "3"))
    DELAY_ON_EXCEPTION = int(
        os.getenv("MESSAGE_QUEUE_DELAY_ON_EXCEPTION", "10"))
    MAX_RETRY_COUNT_ON_EXCEPTION = int(
        os.getenv("MESSAGE_QUEUE_MAX_RETRY_COUNT_ON_EXCEPTION", "15"))

# pylint: disable=too-few-public-methods
