"""Job Types"""

from enum import Enum


class JobType(Enum):
    """Job Type"""
    NONE = 0
    URL_STATUS_CHECKER = 1
    SCRAPE_COUNCIL = 2
    URL_STATUS_WEBSITE = 3
