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
    def test_should_create(self):
        # Arrange

        # Act
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

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
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(
            results.picture.sk, "tests/unit/data/picture_files/with_gps.jpg"
        )

    def test_should_add_s3_sample_1(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture(
            "svz-master-pictures-new/original/2023/2023-04-09_Pictures_On_Easter_at_Sierra_Glen_2023-04-09_19.29.23.jpeg",
            ImageIOS3(),
        )

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert

    #

    def test_should_add_s3_sample_2(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture(
            "svz-master-pictures-new/original/2023/2023-04-09_Pictures_On_Easter_at_Sierra_Glen_2023-04-09_19.29.31.jpeg",
            ImageIOS3(),
        )

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert


class HashSimilar(unittest.TestCase):
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
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(results.picture.sk, "/tmp/with_gps_.9.jpg")
        self.assertEqual(results.picture.date_taken, datetime(2023, 1, 13, 7, 43, 54))
        self.assertEqual(results.picture.height, 3628)
        self.assertEqual(results.picture.width, 2721)

    def test_should_add_cropped_still_portrait(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        picture.resize_fitting_aspect_ratio(
            "/tmp/with_gps_.4_.6.jpg",
            int(picture.width * 0.4),
            int(picture.height * 0.6),
        )
        resized = Picture("/tmp/with_gps_.4_.6.jpg", ImageIOLocal())

        # Act
        results = subject.add_new_picture_to_catalog(resized)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(results.picture.sk, "/tmp/with_gps_.4_.6.jpg")
        self.assertEqual(results.picture.height, 2419)
        self.assertEqual(results.picture.width, 1209)

    def test_should_add_cropped_but_changed_to_landscape(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        picture = Picture("tests/unit/data/picture_files/with_gps.jpg", ImageIOLocal())
        picture.resize_fitting_aspect_ratio(
            "/tmp/with_gps_flip_landscape.jpg",
            int(picture.width * 0.9),
            int(picture.height * 0.6),
        )
        resized = Picture("/tmp/with_gps_flip_landscape.jpg", ImageIOLocal())

        # Act
        results = subject.add_new_picture_to_catalog(resized)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(results.picture.sk, "/tmp/with_gps_flip_landscape.jpg")
        self.assertEqual(results.picture.height, 2419)
        self.assertEqual(results.picture.width, 2721)


class GPS(unittest.TestCase):
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
        self.assertEqual(results.picture.gis_lat, 35.7275917)
        self.assertEqual(results.picture.gis_long, -78.9425722)


class GIS(unittest.TestCase):
    def test_should_get_state_gis_data(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

        # Act
        results = subject.get_gis_data_by_state(
            "NC",
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 771)
        self.assertGreater(results[0].lat, 30)

    def test_should_get_lat_long_gis_data(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

        # Act
        results = subject.get_gis_data_by_lat_long(
            38.123,
            -79.123,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 56)
        self.assertGreater(results[0].lat, 30)


if __name__ == "__main__":
    unittest.main()
