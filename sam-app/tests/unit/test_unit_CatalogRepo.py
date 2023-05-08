import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import UsingDynamoDB
from infrastructure.system.Clock import FakeClock


class FakeDynamoDB(UsingDynamoDB):
    def __init__(self, table_name):
        self.table_name = table_name

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


@unittest.skip("")
class BasicPictureRecord(unittest.TestCase):
    def test_should_create(self):
        # Arrange

        # Act
        subject = PictureCatalogRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-01"),
        )


@unittest.skip("")
class LastShownCorrect(unittest.TestCase):
    def test_should_not_use_last_shown_since_not_original(self):
        # Arrange
        subject = PictureCatalogRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-02 03:04:05"),
        )
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.last_shown, datetime(1900, 1, 1))
        self.assertEqual(results.picture.gsi1_pk, "NEVER_SHOW")
        self.assertTrue(results.picture.gsi1_sk.startswith("-"))

    def test_should_use_last_shown_since_original(self):
        # Arrange
        subject = PictureCatalogRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-02 03:04:05"),
        )
        picture = Picture(
            "tests/unit/data/picture_files/original/with_gps.jpg", ImageIOLocal()
        )
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.last_shown.year, 2023)
        self.assertEqual(results.picture.gsi1_pk, "LAST_SHOWN#portrait")
        self.assertTrue(results.picture.gsi1_sk.startswith("2023-01-01"))


if __name__ == "__main__":
    unittest.main()
