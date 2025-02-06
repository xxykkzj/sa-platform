"""URL Status Dynamodb table"""

from base_classes.dynamo_db_base import DynamoDbBase
from dtos.url_status_dto import UrlStatusDto


class UrlStatusDynamoDb(DynamoDbBase):
    """Url Status data access in dynamodb"""
    def __init__(self) -> None:
        attributes_and_keys = [
            ("request_id", "S", "HASH")
        ]
        super().__init__("url_status", attributes_and_keys)

    def get(self, request_id: str):
        """Get item by the org_id and address"""
        return self.get_item(self.get_key(request_id))

    def put(self, url_status_dto: UrlStatusDto):
        """Upsert: Create an item, and update if exists"""
        return self.put_item(url_status_dto.__dict__)

    def delete(self, request_id: str):
        """Delete an item"""
        return self.delete_item(self.get_key(request_id))

    def get_key(self, request_id: str):
        """Construct key for query"""
        return {
            "request_id": request_id
        }
