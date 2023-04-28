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

    def test_should_get_picture(self):
        # Arrange
        subject = PictureFileRepo(
            ImageIOLocal(),
        )

        # Act
        results = subject.get_picture_file("sdkljlkjs")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
