import unittest
from datetime import datetime
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import GISRecord, PictureCatalogGroup
from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.repository.DynamoDB import UsingDynamoDB
from infrastructure.system.Clock import FakeClock, ITellingTime
from use_cases.AddNewPicture import AddNewPicture


class FakeDynamoDB(UsingDynamoDB):
    def __init__(self, table_name):
        self.table_name = table_name

    def put_item(self, record) -> None:
        pass

    def put_batch(self, record) -> None:
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


class FakeRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        pass

    def add_new_picture_to_catalog(self, record: PictureCatalogGroup) -> None:
        pass

    def get_gis_data_by_state(self, state_id: str) -> List[GISRecord]:
        pass

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISRecord]:
        return [GISRecord(lat=36, long=-79, city="Springfield", state="VA")]


class Basic(unittest.TestCase):
    def test_should_add_new_picture_to_catalog_with_gps(self):
        # Arrange
        repo = FakeRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-02 03:04:05"),
        )
        subject = AddNewPicture(repo, FakeClock("2023-01-02 03:04:05"))
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(
            results.picture.sk, "tests/unit/data/picture_files/with_gps.jpg"
        )
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
        self.assertEqual(results.picture.city, "Springfield")
        self.assertEqual(results.picture.state, "VA")
        self.assertEqual(results.picture.gsi1_pk, "NEVER_SHOW")
        self.assertEqual(results.picture.gsi1_sk, "-")
        self.assertEqual(results.picture.gsi2_pk, "DATE_ADDED#portrait")
        self.assertTrue(results.picture.gsi2_sk.startswith("2023-01-02"))
        self.assertEqual(results.picture.gsi3_pk, "ON_THIS_DAY#01-13")
        self.assertTrue(results.picture.gsi3_sk.startswith("2023-01-13"))
        self.assertEqual(results.picture.gsi4_pk, "UNIQUE_HASH")
        self.assertEqual(results.picture.gsi4_sk, "048b5ba2c6a9f13b89e59c0751b6e8c3")
        self.assertEqual(results.picture.gsi5_pk, "DATE_TAKEN")
        self.assertEqual(results.picture.gsi5_sk, "2023-01-13T07:43:54")
        self.assertEqual(results.missing_gis_data, None)

    def test_should_add_new_picture_to_catalog_without_gps(self):
        # Arrange
        repo = FakeRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-02 03:04:05"),
        )
        subject = AddNewPicture(repo, FakeClock("2023-01-02 03:04:05"))
        picture = Picture(
            "tests/unit/data/picture_files/without_gps.jpg", ImageIOLocal()
        )
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(
            results.picture.sk, "tests/unit/data/picture_files/without_gps.jpg"
        )
        self.assertEqual(results.picture.gis_lat, -1)
        self.assertEqual(results.picture.gis_long, -1)
        self.assertEqual(results.picture.city, None)
        self.assertEqual(results.picture.state, None)
        self.assertEqual(results.missing_gis_data.pk, "MISSING_GIS")


class BasicHashRecord(unittest.TestCase):
    def test_should_add_new_hashes(self):
        # Arrange
        repo = FakeRepo(
            FakeDynamoDB("xyz"),
            FakeClock("2023-01-02 03:04:05"),
        )
        subject = AddNewPicture(repo, FakeClock("2023-01-02 03:04:05"))
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results.hashes), 2)
        self.assertEqual(results.hashes[0].pk, "HASH_AVERAGE_HASH")
        self.assertEqual(
            results.hashes[0].sk, "tests/unit/data/picture_files/with_gps.jpg"
        )
        self.assertEqual(results.hashes[0].gsi1_pk, "AVERAGE_HASH_1")
        self.assertEqual(results.hashes[0].gsi1_sk, "fdf9")
        self.assertEqual(results.hashes[0].gsi2_pk, "AVERAGE_HASH_2")
        self.assertEqual(results.hashes[0].gsi2_sk, "0303")
        self.assertEqual(results.hashes[0].gsi3_pk, "AVERAGE_HASH_3")
        self.assertEqual(results.hashes[0].gsi3_sk, "23f3")
        self.assertEqual(results.hashes[0].gsi4_pk, "AVERAGE_HASH_4")
        self.assertEqual(results.hashes[0].gsi4_sk, "1f0f")
        self.assertEqual(results.hashes[0].hash_value, "fdf9030323f31f0f")

        self.assertEqual(results.hashes[1].pk, "HASH_PHASH")
        self.assertEqual(
            results.hashes[1].sk, "tests/unit/data/picture_files/with_gps.jpg"
        )
        self.assertEqual(results.hashes[1].gsi1_pk, "PHASH_1")
        self.assertEqual(results.hashes[1].gsi1_sk, "aeea")


if __name__ == "__main__":
    unittest.main()
