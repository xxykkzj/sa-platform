"""Council Scraping"""
from base_classes.dynamo_db_base import DynamoDbBase
from scraping.dtos.council_scraping_dto import CouncilScrapingDto


class CouncilScrapingDynamodb(DynamoDbBase):
    """Class for crud operations in dynamodb to store council scraping data"""

    def __init__(self) -> None:
        attributes_and_keys = [
            ("address", "S", "HASH"),
            ("org_id", "N", "RANGE"),
        ]
        super().__init__("council_scraping", attributes_and_keys)

    def get(self, org_id: int, address: str):
        """Get item by the org_id and address"""
        return self.get_item(self.get_key(org_id, address))

    def put(self, council_scraping: CouncilScrapingDto):
        """Upsert: Create an item, and update if exists"""
        return self.put_item(council_scraping.__dict__)

    def delete(self, org_id: int, address: str):
        """Delete an item"""
        return self.delete_item(self.get_key(org_id, address))

    def get_key(self, org_id: int, address: str):
        """Construct key for query"""
        return {
            "org_id": org_id,
            "address": address
        }
