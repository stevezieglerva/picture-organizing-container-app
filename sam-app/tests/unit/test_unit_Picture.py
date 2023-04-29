import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.S3 import S3FakeLocal


class Basic(unittest.TestCase):
    def test_should_get_picture_with_gps(self):
        # Arrange

        # Act
        results = Picture(
            "tests/unit/data/picture_files/with_gps.jpg",
            ImageIOLocal(),
        )

        # Assert
        self.assertEqual(results.model, "iPhone 12")
        self.assertEqual(results.gis_lat, 35.7275917)
        self.assertEqual(results.gis_long, -78.9425722)

    def test_should_get_picture_without_gps(self):
        # Arrange

        # Act
        results = Picture(
            "tests/unit/data/picture_files/without_gps.jpg",
            ImageIOLocal(),
        )

        # Assert
        self.assertEqual(results.model, "iPhone XR")
        self.assertEqual(results.gis_lat, None)
        self.assertEqual(results.gis_long, None)


class GPSExifPreservedOnSave(unittest.TestCase):
    def test_should_get_picture_with_gps(self):
        # Arrange
        original_picture = Picture(
            "tests/unit/data/picture_files/with_gps.jpg",
            ImageIOLocal(),
        )
        print(original_picture)
        original_picture.save_as("/tmp/test_picture_organizing.jpg")

        # Act
        results = Picture(
            "/tmp/test_picture_organizing.jpg",
            ImageIOLocal(),
        )

        # Assert
        self.assertEqual(results.gis_lat, original_picture.gis_lat)
        self.assertEqual(results.gis_long, original_picture.gis_long)


if __name__ == "__main__":
    unittest.main()
