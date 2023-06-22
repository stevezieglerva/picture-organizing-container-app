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
from domain.Picture import ImageIOS3
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3
from infrastructure.system.Clock import RealClock
from use_cases.GetPicture import GetPictureUseCase


class FakeRandomPicker(IDatePicker):
    def get_date_type(self, today: datetime) -> DateOptions:
        return DateOptions(type="random", year=2023, month=1, day=1)


class SelectPictureRandom(unittest.TestCase):
    def test_should_pick_landscape_random_pic(self):
        # Arrange
        repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog-test"), RealClock())

        subject = GetPictureUseCase(
            repo,
            "svz-master-pictures-new",
            S3(),
            FakeRandomPicker(),
            RealClock(),
            ImageIOS3(),
        )

        # Act
        results = subject.get_picture(2000, 1000, "Mozilla")
        print(f"test results: {results}")

        # Assert
        self.assertTrue(
            results.key_small.startswith("svz-master-pictures-new/original"),
            f"{results.key_small}",
        )
        self.assertTrue(
            results.presigned_url.startswith(
                "https://svz-master-pictures-new.s3.amazonaws.com/sweet_shuffle/current_resized_"
            ),
            f"{results.presigned_url}",
        )


if __name__ == "__main__":
    unittest.main()
