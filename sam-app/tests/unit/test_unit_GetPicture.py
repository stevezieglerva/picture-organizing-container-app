import unittest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import GISDBRecord, PictureCatalogGroup, PictureDBRecord
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3FakeLocal
from infrastructure.system.Clock import FakeClock, ITellingTime
from use_cases.GetPicture import GetPicture


class FakeRepo(StoringCatalogData):
    def __init__(self, db: DynamoDB, clock: ITellingTime):
        pass

    def add_new_picture_to_catalog(
        self, record: PictureCatalogGroup
    ) -> PictureCatalogGroup:
        pass

    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        pass

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        pass

    def get_recently_added(
        self, layout: str, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        pass


class Create(unittest.TestCase):
    def test_should_create_object(self):
        # Arrange
        subject = GetPicture(FakeRepo(None, FakeClock("2023-01-01")))

        # Act
        results = subject.get_picture(1000, 1200, "Mozilla", datetime(2023, 1, 1))
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.key_small, "xyz")


if __name__ == "__main__":
    unittest.main()
