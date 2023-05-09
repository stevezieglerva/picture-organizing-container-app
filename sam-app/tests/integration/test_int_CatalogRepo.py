import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import PictureCatalogGroup, PictureDBRecord
from domain.Picture import ImageIOLocal, ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import add_new_picture_from_s3


@unittest.skip("wip")
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


class Queries(unittest.TestCase):
    def test_should_get_recently_added(self):
        # Arrange
        add_results = add_new_picture_from_s3(
            "svz-master-pictures-new/original/2012/2012_10_21_Frying_Pan_Park_Fall_NiceCanon_0796_-_Copy.jpg",
            "master-pictures-catalog-test",
        )
        print("\n**** batch results:")
        print(add_results)
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

        # Act
        results = subject.get_recently_added("portrait", timedelta(minutes=1))
        print("\nFound:")
        for r in results:
            print(f"{r.date_added}: {r.s3_url}")

        # Assert
        self.assertEqual(
            results[0].s3_url,
            "svz-master-pictures-new/original/2012/2012_10_21_Frying_Pan_Park_Fall_NiceCanon_0796_-_Copy.jpg",
        )


if __name__ == "__main__":
    unittest.main()
