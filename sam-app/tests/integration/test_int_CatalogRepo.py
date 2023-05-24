import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import PictureCatalogGroup, PictureDBRecord, PictureSelectionOption
from domain.Picture import ImageIOLocal, ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import add_new_picture_from_s3


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


class Updates(unittest.TestCase):
    def test_should_update_dates(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        add_new_picture_from_s3(
            "svz-master-pictures-new/original/2011/2011_10_02_IMG_7385_-_Copy.jpg",
            "master-pictures-catalog-test",
        )

        # Act
        results = subject.update_picture_record(
            "svz-master-pictures-new/original/2011/2011_10_02_IMG_7385_-_Copy.jpg",
            last_show="2000-01-01",
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


class Queries(unittest.TestCase):
    def test_should_get_picture(self):
        # Arrange
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )
        add_results = add_new_picture_from_s3(
            "svz-master-pictures-new/original/2017/2017-01-01_New_Years_Day_IMG_5405_-_Copy.JPG",
            "master-pictures-catalog-test",
        )
        print(add_results)

        # Act
        results = subject.get_picture(
            "svz-master-pictures-new/original/2017/2017-01-01_New_Years_Day_IMG_5405_-_Copy.JPG"
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results.s3_url,
            "svz-master-pictures-new/original/2017/2017-01-01_New_Years_Day_IMG_5405_-_Copy.JPG",
        )

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
        results = subject.get_recently_added(timedelta(minutes=1))
        print("\nFound:")
        for r in results:
            print(f"{r.date_added}: {r.s3_url}")

        # Assert
        self.assertEqual(type(results[0]), PictureSelectionOption)
        recent_s3_names = [obj.s3_url for obj in results]
        self.assertTrue(
            "svz-master-pictures-new/original/2012/2012_10_21_Frying_Pan_Park_Fall_NiceCanon_0796_-_Copy.jpg"
            in recent_s3_names
        )

    def test_should_get_oldest_shown(self):
        # Arrange
        add_results = add_new_picture_from_s3(
            "svz-master-pictures-new/original/2010/2010_04_03_IMG_1618_-_Copy.jpg",
            "master-pictures-catalog-test",
        )
        print("\n**** batch results:")
        print(add_results)
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

        # Act
        results = subject.get_oldest_shown()
        print("\nFound:")
        print(results[0])
        for count, r in enumerate(results):
            print(f"#{count+1:<2} {r.last_shown}: {r.s3_url}")

        # Assert
        self.assertEqual(type(results[0]), PictureSelectionOption)
        recent_s3_names = [obj.s3_url for obj in results]
        self.assertFalse(
            "svz-master-pictures-new/original/2012/2012_10_21_Frying_Pan_Park_Fall_NiceCanon_0796_-_Copy.jpg"
            in recent_s3_names
        )

        count_portait = [r for r in results if r.layout == "portrait"]
        self.assertEqual(len(count_portait), 5)
        count_landscape = [r for r in results if r.layout == "landscape"]
        self.assertEqual(len(count_landscape), 5)

    def test_should_get_for_month_day(self):
        # Arrange
        add_results = add_new_picture_from_s3(
            "svz-master-pictures-new/original/2010/2010_04_03_IMG_1618_-_Copy.jpg",
            "master-pictures-catalog-test",
        )
        add_results = add_new_picture_from_s3(
            "svz-master-pictures-new/original/2019/2019-04-03_Phone_Pictures_Owen_School_Concert_2019-04-03_13.27.28_-_Copy.jpg",
            "master-pictures-catalog-test",
        )

        print("\n**** batch results:")
        print(add_results)
        subject = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog-test"),
            RealClock(),
        )

        # Act
        results = subject.get_by_month_day(4, 3)
        print("\nFound:")
        print(results[0])
        for count, r in enumerate(results):
            print(f"#{count+1:<2} {r.last_shown}: {r.s3_url}")

        # Assert
        recent_s3_names = [obj.s3_url for obj in results]
        self.assertTrue(
            "svz-master-pictures-new/original/2010/2010_04_03_IMG_1618_-_Copy.jpg"
            in recent_s3_names
        )
        self.assertTrue(
            "svz-master-pictures-new/original/2019/2019-04-03_Phone_Pictures_Owen_School_Concert_2019-04-03_13.27.28_-_Copy.jpg"
            in recent_s3_names
        )


if __name__ == "__main__":
    unittest.main()
