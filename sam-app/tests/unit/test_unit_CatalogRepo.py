import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.CatalogRepo import (
    PictureCatalogRepo,
    convert_picture_to_catalogrecords_for_insert,
)
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


class RecordConversion(unittest.TestCase):
    def test_should_convert_picture_to_catalogs(self):
        # Arrange
        pic = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        print(pic)
        # Act
        results = convert_picture_to_catalogrecords_for_insert(
            pic, datetime(2023, 1, 2, 3, 4, 5)
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results.picture.pk, "PICTURE#tests/unit/data/picture_files/with_gps.jpg"
        )
        self.assertEqual(results.picture.sk, "-")
        self.assertTrue(results.picture.ulid != "")
        self.assertEqual(
            results.picture.s3_url, "tests/unit/data/picture_files/with_gps.jpg"
        )
        self.assertEqual(results.picture.date_taken, datetime(2023, 1, 13, 7, 43, 54))
        self.assertEqual(results.picture.date_added, datetime(2023, 1, 2, 3, 4, 5))
        self.assertEqual(results.picture.date_updated, datetime(2023, 1, 2, 3, 4, 5))
        self.assertEqual(results.picture.height, 4032)
        self.assertEqual(results.picture.width, 3024)
        self.assertEqual(results.picture.model, "iPhone 12")
        self.assertEqual(results.picture.layout, "portrait")


class Basic(unittest.TestCase):
    def test_should_create(self):
        # Arrange

        # Act
        subject = PictureCatalogRepo(FakeDynamoDB("xyz"))

    @unittest.skip("")
    def test_should_write_picture(self):
        # Arrange
        subject = PictureCatalogRepo(FakeDynamoDB("xyz"))

        # Act
        results = subject.write_picture_to_catalog(CatalogRecord())
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
