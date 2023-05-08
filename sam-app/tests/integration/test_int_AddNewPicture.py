import unittest
from datetime import datetime
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import GISRecord, PictureCatalogGroup
from domain.Picture import ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import AddNewPicture


@unittest.skip("")
class Basic(unittest.TestCase):
    def test_should_add_new_picture_to_catalog_with_gps(self):
        # Arrange
        repo = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        subject = AddNewPicture(repo, RealClock())
        picture = Picture(
            "svz-master-pictures-new/original/2023/2023-04-16_Pictures_Boys_At_TAC_Swim_2023-04-16_11.36.25.jpeg",
            ImageIOS3(),
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
            results.picture.sk,
            "svz-master-pictures-new/original/2023/2023-04-16_Pictures_Boys_At_TAC_Swim_2023-04-16_11.36.25.jpeg",
        )
        self.assertEqual(results.picture.city, "Cary")
        self.assertEqual(results.picture.state, "NC")

    def test_should_add_new_picture_to_catalog_without_gps(self):
        # Arrange
        db = DynamoDB("master-pictures-catalog-test")
        repo = PictureCatalogRepo(
            db,
            RealClock(),
        )
        subject = AddNewPicture(repo, RealClock())
        picture = Picture(
            "svz-master-pictures-new/original/2014/2014_08_20_Disney_2014_2014_08_20_999_52_-_Copy.jpg",
            ImageIOS3(),
        )
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        print("\n\n\n checking for missing_gis")
        records = db.query_table_equal(
            {
                "pk": "MISSING_GIS",
                "sk": "svz-master-pictures-new/original/2014/2014_08_20_Disney_2014_2014_08_20_999_52_-_Copy.jpg",
            }
        )
        print(records)
        self.assertGreater(len(records), 0)

    def test_should_get_picture_data(self):
        # Arrange
        subject = Class()

        # Act
        results = subject.method()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


class BulkAdd(unittest.TestCase):
    def test_should_add_new_picture_to_catalog_with_gps(self):

        db = DynamoDB("master-pictures-catalog-test")
        repo = PictureCatalogRepo(
            db,
            RealClock(),
        )
        subject = AddNewPicture(repo, RealClock())

        # Act
        picture_s3_urls = S3().list_objects(
            "svz-master-pictures-new",
            "raw-photos/2022/2022-01-20",
            total_max=20,
        )
        for picture in picture_s3_urls:
            if "jpg" in picture.key.lower() or "jpeq" in picture.key.lower():
                print(f"\n\nProcessing: {picture.key}")
                picture = Picture(
                    f"{picture.bucket}/{picture.key}",
                    ImageIOS3(),
                )
                subject.add_new_picture_to_catalog(picture)

        # results = subject.add_new_picture_to_catalog(
        #     picture,
        # )
        # print(f"test results: {results}")


if __name__ == "__main__":
    unittest.main()
