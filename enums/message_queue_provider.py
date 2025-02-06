"""QUEUE Provider"""
from enum import Enum

class MessageQueueProvider(Enum):
    """Message Queue providers"""
    NONE = 0
    SQS = 1
    RABBIT_MQ = 2
