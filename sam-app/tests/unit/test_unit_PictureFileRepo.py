import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOLocal, Picture
from infrastructure.repository.PictureFileRepo import PictureFileRepo
from infrastructure.repository.S3 import S3FakeLocal


class Basic(unittest.TestCase):
    def test_should_init(self):

        # Act
        subject = PictureFileRepo(
            ImageIOLocal(),
        )

    def test_should_get_picture_with_gps(self):
        # Arrange
        subject = PictureFileRepo(
            ImageIOLocal(),
        )

        # Act
        results = subject.get_picture_file("tests/unit/data/picture_files/with_gps.jpg")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.model, "iPhone 12")
        self.assertEqual(results.gis_lat, 35.7275917)
        self.assertEqual(results.gis_long, -78.9425722)


if __name__ == "__main__":
    unittest.main()
