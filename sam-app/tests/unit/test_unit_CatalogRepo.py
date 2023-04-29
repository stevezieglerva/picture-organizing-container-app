import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.CatalogRepo import (
    PictureCatalogGroup,
    PictureCatalogRepo,
    PictureRecord,
)
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


class Basic(unittest.TestCase):
    def test_should_create(self):
        # Arrange

        # Act
        subject = PictureCatalogRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-01"),
        )

    def test_should_add_new_picture_to_catalog_with_gps(self):
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
        self.assertEqual(
            results.picture.pk, "PICTURE#tests/unit/data/picture_files/with_gps.jpg"
        )
        self.assertEqual(results.picture.sk, "-")
        self.assertTrue(results.picture.ulid != "")
        self.assertEqual(
            results.picture.s3_url, "tests/unit/data/picture_files/with_gps.jpg"
        )
        self.assertEqual(results.picture.date_taken, datetime(2023, 1, 13, 7, 43, 54))
        self.assertEqual(
            results.picture.date_added, FakeClock("2023-01-02 03:04:05").get_time()
        )
        self.assertEqual(
            results.picture.date_updated, FakeClock("2023-01-02 03:04:05").get_time()
        )
        self.assertEqual(results.picture.height, 4032)
        self.assertEqual(results.picture.width, 3024)
        self.assertEqual(results.picture.model, "iPhone 12")
        self.assertEqual(results.picture.layout, "portrait")
        self.assertEqual(results.picture.view_count, 0)
        self.assertTrue(results.picture.hash_average_hash != "")
        self.assertTrue(results.picture.hash_crop_resistant != "")
        self.assertTrue(results.picture.hash_phash != "")
        self.assertTrue(results.picture.hash_unique != "")
        self.assertEqual(results.picture.year, 2023)
        self.assertEqual(results.picture.month, 1)
        self.assertEqual(results.picture.day, 13)
        self.assertEqual(results.picture.update_desc, "01/02/23-created")
        self.assertEqual(results.picture.gis_lat, 35.7275917)
        self.assertEqual(results.picture.gis_long, -78.9425722)
        self.assertEqual(results.picture.gsi1_pk, "LAST_SHOWN#portrait")
        self.assertTrue(results.picture.gsi1_sk.startswith("2023-01-02"))
        self.assertEqual(results.picture.gsi2_pk, "DATE_ADDED#portrait")
        self.assertTrue(results.picture.gsi2_sk.startswith("2023-01-02"))


if __name__ == "__main__":
    unittest.main()
