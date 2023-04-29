import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOS3, Picture
from infrastructure.repository.S3 import S3


class Basic(unittest.TestCase):
    def test_should_get_picture_with_gps(self):
        # Arrange

        # Act
        results = Picture(
            "svz-master-pictures-new/tests/integration/picture_gps_exif/with_gps.jpg",
            ImageIOS3(),
        )
        print(results)

        # Assert
        self.assertEqual(results.model, "iPhone 12")
        self.assertEqual(results.gis_lat, 35.7275917)
        self.assertEqual(results.gis_long, -78.9425722)

    def test_should_get_picture_without_gps(self):
        # Arrange

        # Act
        results = Picture(
            "svz-master-pictures-new/tests/integration/picture_gps_exif/without_gps.jpg",
            ImageIOS3(),
        )
        print(results)

        # Assert
        self.assertEqual(results.model, "iPhone XR")
        self.assertEqual(results.gis_lat, None)
        self.assertEqual(results.gis_long, None)


class GPSExifPreservedOnSave(unittest.TestCase):
    def test_should_get_picture_with_gps(self):
        # Arrange
        original_picture = Picture(
            "svz-master-pictures-new/tests/integration/picture_gps_exif/without_gps.jpg",
            ImageIOS3(),
        )
        print(original_picture)
        original_picture.save_as(
            "svz-master-pictures-new/tests/integration/picture_gps_exif/tmp_saved.jpg"
        )

        # Act
        results = Picture(
            "svz-master-pictures-new/tests/integration/picture_gps_exif/tmp_saved.jpg",
            ImageIOS3(),
        )

        # Assert
        self.assertEqual(results.gis_lat, original_picture.gis_lat)
        self.assertEqual(results.gis_long, original_picture.gis_long)


if __name__ == "__main__":
    unittest.main()
