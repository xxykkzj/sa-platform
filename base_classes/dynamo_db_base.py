"""Dynamo DB base class"""

from base_classes.aws_client_base import AwsClientBase


class DynamoDbBase(AwsClientBase):
    """Dynamo Db base class"""
    def __init__(self, table_name, attributes_and_keys) -> None:
        super().__init__("dynamodb")
        self.string_helper.validate_null_or_empty(table_name, "table_name")
        self.table_name = table_name
        self.table = self.create_table_if_not_exists(attributes_and_keys)

    def create_table_if_not_exists(self, attributes_and_keys):
        """Create table if not exists"""
        tables = self.client.list_tables()['TableNames']
        if self.table_name in tables:
            return self.resource.Table(self.table_name)

        return self.create_table(attributes_and_keys)

    def get_attribute_and_key_schema(self, name, attr_type, key_type):
        """construct attribute and key schema"""
        attribute = {
            "AttributeName": name,
            "AttributeType": attr_type
        }

        key_schema = {
            "AttributeName": name,
            "KeyType": key_type
        }

        return attribute, key_schema

    def get_attribute_definitions_and_key_schemas(self, attributes_and_keys: list):
        """Create attribute definitions and key schemas"""
        attribute_definitions = []
        key_schemas = []

        for name, attr_type, key in attributes_and_keys:
            attribute, key_schema = self.get_attribute_and_key_schema(
                name, attr_type, key)
            attribute_definitions.append(attribute)
            key_schemas.append(key_schema)

        return attribute_definitions, key_schemas

    def create_table(self, attributes_and_keys):
        """Create dynamo db table"""
        attribute_definitions, key_schemas = self.get_attribute_definitions_and_key_schemas(
            attributes_and_keys)
        table = self.resource.create_table(
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schemas,
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            TableName=self.table_name
        )

        table.wait_until_exists()

        print(f"Table {self.table_name} created successfully,")

        return table

    def delete_table(self):
        """Delete table from dynamodb"""
        if self.table is not None:
            return self.table.delete()

        return {"message": "Table object is None"}

    def get_item(self, key: dict):
        """get item"""
        return self.table.get_item(Key=key)

    def put_item(self, item):
        """Upsert: Create an item, and update if exists"""
        return self.table.put_item(Item=item)

    def delete_item(self, key: dict):
        """Delete an item"""
        return self.table.delete_item(Key=key)
