import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import (
    GISDBRecord,
    HashDBRecord,
    MissingGISDataDBRecord,
    PictureCatalogGroup,
    PictureDBRecord,
)
from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import BatchResults, UsingDynamoDB
from infrastructure.system.Clock import FakeClock


class FakeDynamoDB(UsingDynamoDB):
    def __init__(self, table_name):
        self.table_name = table_name
        self.limit = 1

    def put_item(self, record) -> None:
        pass

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

    def put_batch(self, records: list) -> BatchResults:
        raise ValueError("Fake error for test")

    def delete_batch(self, records: list, batch_size: int = 25) -> BatchResults:
        raise NotImplementedError


class Basic(unittest.TestCase):
    def test_should_create(self):
        # Arrange

        # Act
        subject = PictureCatalogRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-01"),
        )


if __name__ == "__main__":
    unittest.main()
