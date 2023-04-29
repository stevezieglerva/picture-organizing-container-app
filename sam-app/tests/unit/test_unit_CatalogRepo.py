import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from infrastructure.repository.CatalogRepo import CatalogRepo
from infrastructure.repository.DynamoDB import UsingDynamoDB


class FakeDynamoDB(UsingDynamoDB):
    def __init__(self, table_name):
        self.table_name = table_name

    def put_item(self, record) -> None:
        raise NotImplemented

    def get_item(self, key) -> dict:
        raise NotImplemented

    def delete_item(self, key) -> None:
        raise NotImplemented

    def query_table_equal(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    def query_table_greater_than(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    def query_table_begins(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    def query_table_between(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    def query_index_begins(self, index_name, key) -> list:
        raise NotImplemented

    def scan_full(self) -> list:
        raise NotImplemented


class Basic(unittest.TestCase):
    def test_should_create(self):
        # Arrange

        # Act
        subject = CatalogRepo(FakeDynamoDB("xyz"))

    def test_should_write_picture(self):
        # Arrange
        subject = CatalogRepo(FakeDynamoDB("xyz"))

        # Act
        results = subject.write_picture_to_catalog(CatalogRecord())
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
