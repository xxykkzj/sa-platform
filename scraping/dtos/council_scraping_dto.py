"""Council scraping dto"""
from dataclasses import dataclass

@dataclass
class CouncilScrapingDto():
    """Class for keeping track of an item in Council Scraping"""
    org_id: int
    address: str
    council: str
    status_code: int
    message: str
    request_id: str
    created_date: str
