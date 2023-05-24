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
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3FakeLocal
from infrastructure.system.Clock import FakeClock, ITellingTime
from use_cases.GetPicture import GetPicture


class FakeRepo(StoringCatalogData):
    def __init__(self, db: DynamoDB, clock: ITellingTime):
        self._clock = clock

    def add_new_picture_to_catalog(
        self, record: PictureCatalogGroup
    ) -> PictureCatalogGroup:
        pass

    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        pass

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        pass

    def get_recently_added(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        return self._updated

    def get_oldest_shown(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        return self._oldest_shown

    def set_recently_updated(self, data: list):
        self._updated = [
            PictureSelectionOption(
                s3_url=i[0],
                layout=i[1],
                date_added=self._clock.get_time() + timedelta(i[2]),
                last_shown=self._clock.get_time() + timedelta(i[3]),
            )
            for i in data
        ]

    def set_oldest_shown(self, data: list):
        self._oldest_shown = [
            PictureSelectionOption(
                s3_url=i[0],
                layout=i[1],
                date_added=self._clock.get_time() + timedelta(i[2]),
                last_shown=self._clock.get_time() + timedelta(i[3]),
            )
            for i in data
        ]

    def get_by_month_day(self):
        pass

    def get_oldest_shown(self):
        pass


class FakeRandomPicker(IDatePicker):
    def get_date_type(self, today: datetime) -> DateOptions:
        return DateOptions(type="random", year=2023, month=1, day=1)


class Create(unittest.TestCase):
    def test_should_create_object(self):
        # Arrange
        subject = GetPicture(
            FakeRepo(None, FakeClock("2023-01-01")),
            S3FakeLocal(),
            DatePicker(),
            FakeClock("2023-02-03"),
        )


class RandomPictures(unittest.TestCase):
    def test_should_pick_random_pic(self):
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
            repo, S3FakeLocal(), FakeRandomPicker(), FakeClock("2023-02-03")
        )

        # Act
        results = subject.get_picture(2000, 1000, "Mozilla")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.key_small, "oldest_landscape.jpg")


if __name__ == "__main__":
    unittest.main()
