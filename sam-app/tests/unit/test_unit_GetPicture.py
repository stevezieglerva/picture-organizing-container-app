import unittest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from dateutil.parser import *
from domain.DatePicker import DateOptions, DatePicker, IDatePicker
from domain.DTOs import (
    GISDBRecord,
    PictureCatalogGroup,
    PictureDBRecord,
    PictureSelectionOption,
)
from domain.Picture import ImageIOLocal, ImageIOS3
from infrastructure.repository.CatalogRepo import FakeRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3FakeLocal
from infrastructure.system.Clock import FakeClock, ITellingTime
from use_cases.GetPicture import GetPictureUseCase


class FakeRandomPicker(IDatePicker):
    def get_date_type(self, today: datetime) -> DateOptions:
        return DateOptions(type="random", year=2023, month=1, day=1)


class Create(unittest.TestCase):
    def test_should_create_object(self):
        # Arrange
        subject = GetPictureUseCase(
            FakeRepo(None, FakeClock("2023-01-01")),
            "fake-bucket",
            S3FakeLocal(),
            DatePicker(),
            FakeClock("2023-02-03"),
            ImageIOLocal(),
        )


class SelectPicctureRandom(unittest.TestCase):
    def test_should_pick_landscape_random_pic(self):
        # Arrange
        repo = FakeRepo(None, FakeClock("2023-02-03"))
        repo.set_recently_updated(
            [
                (
                    "tests/unit/data/picture_files/2020-10-22 15.51.31.jpgx3000.jpg",
                    "landscape",
                    -2,
                    -1,
                ),
                ("tests/unit/data/picture_files/with_gps.jpg", "portrait", -2, -1),
            ]
        )
        repo.set_oldest_shown(
            [
                (
                    "tests/unit/data/picture_files/2020-10-22 15.51.31.jpgx3000.jpg",
                    "landscape",
                    -2,
                    -1,
                ),
                ("tests/unit/data/picture_files/with_gps.jpg", "portrait", -2, -1),
            ]
        )

        subject = GetPictureUseCase(
            repo,
            "fake-bucket",
            S3FakeLocal(),
            FakeRandomPicker(),
            FakeClock("2023-02-03"),
            ImageIOLocal(),
            resized_path_prefix="temp_",
        )

        # Act
        results = subject.get_picture(2000, 1000, "Mozilla")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results.key_small,
            "tests/unit/data/picture_files/2020-10-22 15.51.31.jpgx3000.jpg",
        )

    @unittest.skip("")
    def test_should_pick_portrait_random_pic(self):
        # Arrange
        repo = FakeRepo(None, FakeClock("2023-02-03"))
        repo.set_recently_updated(
            [
                ("updated_landscape.jpg", "landscape", -2, -1),
                ("updated_portrait.jpg", "portrait", -2, -1),
            ]
        )
        repo.set_oldest_shown(
            [
                ("oldest_landscape.jpg", "landscape", -100, -50),
                ("oldest_portrait.jpg", "portrait", -100, -50),
            ]
        )

        subject = GetPicture(
            repo,
            "fake-bucket",
            S3FakeLocal(),
            FakeRandomPicker(),
            FakeClock("2023-02-03"),
        )

        # Act
        results = subject.select_picture(300, 500, "Mozilla")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "oldest_portrait.jpg")


if __name__ == "__main__":
    unittest.main()
