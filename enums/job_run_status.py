"""Job run Status"""
from enum import Enum


class JobRunStatus(Enum):
    """Job run Status"""
    NONE = 0
    # request received but processing yet to start
    PENDING = 1
    IN_PROGRESS = 2
    SUCCESS = 3
    FAILED = 4
