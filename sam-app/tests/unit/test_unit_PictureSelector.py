import unittest
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DatePicker import DateOptions
from domain.DTOs import PictureSelectionOption
from domain.PictureSelector import (
    get_device_name,
    get_target_dimensions,
    select_picture,
)


@dataclass(frozen=True)
class CatalogShortcut:
    s3_url: str
    layout: str
    date_added_delta: int
    last_shown_delta: int


def create_catalog_record_list(data: List[PictureSelectionOption]):
    return [
        PictureSelectionOption(
            s3_url=i.s3_url,
            layout=i.layout,
            date_added=datetime.now() + timedelta(days=i.date_added_delta),
            last_shown=datetime.now() + timedelta(days=i.last_shown_delta),
        )
        for i in data
    ]


class SelectPicture(unittest.TestCase):
    def test_should_get_oldest_landscape(self):
        # Arrange
        oldest_shown = create_catalog_record_list(
            [
                CatalogShortcut("A.jpg", "landscape", 200, 156),
                CatalogShortcut("B.jpg", "portrait", 300, 231),
            ]
        )
        recently_updated = []
        on_this_day = []

        # Act
        results = select_picture(
            DateOptions(type="random", year=1900, month=1, day=11),
            2000,
            1000,
            oldest_shown,
            recently_updated,
            on_this_day,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.s3_url, "A.jpg")

    def test_should_get_oldest_portrait(self):
        # Arrange
        oldest_shown = create_catalog_record_list(
            [
                CatalogShortcut("A.jpg", "landscape", 200, 156),
                CatalogShortcut("B.jpg", "portrait", 300, 231),
            ]
        )
        recently_updated = []
        on_this_day = []

        # Act
        results = select_picture(
            DateOptions(type="random", year=1900, month=1, day=11),
            1500,
            1900,
            oldest_shown,
            recently_updated,
            on_this_day,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.s3_url, "B.jpg")


class GetTargetDimensions(unittest.TestCase):
    def test_should_non_special_device(self):
        # Arrange

        # Act
        width, height = get_target_dimensions(1000, 900, "Safari")
        print(f"test results: {width}, {height}")

        # Assert
        self.assertEqual(width, 1000)
        self.assertEqual(height, 900)

    def test_should_add_height_for_steve_laptop(self):
        # Arrange

        # Act
        width, height = get_target_dimensions(1920, 1500, "Mac OS")
        print(f"test results: {width}, {height}")

        # Assert
        self.assertEqual(width, 1920)
        self.assertEqual(height, 1550)

    def test_should_add_height_for_charlotte_laptop(self):
        # Arrange

        # Act
        width, height = get_target_dimensions(1112, 1500, "Mac OS")
        print(f"test results: {width}, {height}")

        # Assert
        self.assertEqual(width, 1112)
        self.assertEqual(height, 1570)


class GetDeviceName(unittest.TestCase):
    def test_should_get_steve_phone(self):
        # Arrange

        # Act
        results = get_device_name(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1"
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "Steve Phone")


if __name__ == "__main__":
    unittest.main()
