import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain import Picture
from infrastructure.repository.S3 import S3


class Basic(unittest.TestCase):
    def test_should_create(self):
        # Arrange
        picture = Picture()

        # Act
        results = create_picture_record(picture)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.pk, "PICTURE")


if __name__ == "__main__":
    unittest.main()
