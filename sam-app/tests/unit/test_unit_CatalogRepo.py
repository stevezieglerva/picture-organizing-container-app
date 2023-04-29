import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from infrastructure.repository.CatalogRepo import CatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB


class Basic(unittest.TestCase):
    def test_should_create(self):
        # Arrange

        # Act
        subject = CatalogRepo(DynamoDB("xyz"))

    def test_should_write_picture(self):
        # Arrange
        subject = CatalogRepo(DynamoDB("xyz"))

        # Act
        results = subject.write_picture_to_catalog(CatalogRecord())
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
