import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import PictureCatalogGroup, PictureRecord
from domain.Picture import ImageIOLocal, ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.system.Clock import RealClock


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
