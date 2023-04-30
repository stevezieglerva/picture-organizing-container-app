import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOLocal, ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import (
    PictureCatalogGroup,
    PictureCatalogRepo,
    PictureRecord,
)
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.system.Clock import RealClock


class Basic(unittest.TestCase):
    @unittest.skip("")
    def test_should_create(self):
        # Arrange

        # Act
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

    @unittest.skip("")
    def test_should_add_new_local_picture_to_catalog_with_gps(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())

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
        self.assertTrue("-created" in results.picture.update_desc)

    def test_should_add_new_resized_with_correct_gps_and_hashes(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        picture.resize_fitting_aspect_ratio(
            "/tmp/with_gps_.9.jpg",
            int(picture.width * 0.9),
            int(picture.height * 0.9),
        )
        resized = Picture("/tmp/with_gps_.9.jpg", ImageIOLocal())

        # Act
        results = subject.add_new_picture_to_catalog(resized)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE#/tmp/with_gps_.9.jpg")
        self.assertEqual(results.picture.sk, "-")
        self.assertTrue(results.picture.ulid != "")
        self.assertEqual(results.picture.s3_url, "/tmp/with_gps_.9.jpg")
        self.assertEqual(results.picture.date_taken, datetime(2023, 1, 13, 7, 43, 54))
        self.assertEqual(results.picture.height, 3628)
        self.assertEqual(results.picture.width, 2721)

    def test_should_add_new_cropped_with_correct_gps_and_hashes(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        picture.resize_fitting_aspect_ratio(
            "/tmp/with_gps_.9.jpg",
            int(picture.width * 0.9),
            int(picture.height * 0.9),
        )
        resized = Picture("/tmp/with_gps_.9.jpg", ImageIOLocal())

        # Act
        results = subject.add_new_picture_to_catalog(resized)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE#/tmp/with_gps_.9.jpg")
        self.assertEqual(results.picture.sk, "-")
        self.assertTrue(results.picture.ulid != "")
        self.assertEqual(results.picture.s3_url, "/tmp/with_gps_.9.jpg")
        self.assertEqual(results.picture.date_taken, datetime(2023, 1, 13, 7, 43, 54))
        self.assertEqual(results.picture.height, 3628)
        self.assertEqual(results.picture.width, 2721)

    @unittest.skip("")
    def test_should_add_new_local_picture_to_catalog_without_gps(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
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
        self.assertEqual(results.picture.gis_lat, -1)
        self.assertEqual(results.picture.gis_long, -1)

    @unittest.skip("")
    def test_should_add_new_s3_picture_to_catalog_with_gps(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture(
            "svz-master-pictures-new/tests/integration/picture_gps_exif/with_gps.jpg",
            ImageIOS3(),
        )
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results.picture.pk,
            "PICTURE#svz-master-pictures-new/tests/integration/picture_gps_exif/with_gps.jpg",
        )
        self.assertEqual(results.picture.gis_lat, 35.7275917)
        self.assertEqual(results.picture.gis_long, -78.9425722)


if __name__ == "__main__":
    unittest.main()
