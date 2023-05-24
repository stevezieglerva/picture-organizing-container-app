import unittest
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.GeoLocator import GeoLocator
from infrastructure.repository.CatalogRepo import (
    GISDBRecord,
    PictureCatalogGroup,
    StoringCatalogData,
)


class FakeCatalog(StoringCatalogData):
    def __init__(self, table_name):
        self.table_name = table_name

    def add_new_picture_to_catalog(self, record: PictureCatalogGroup) -> None:
        raise NotImplemented

    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        return []

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        return [
            GISDBRecord(lat=36, long=-79, city="City C", state="NC"),
            GISDBRecord(lat=37, long=-88, city="City D", state="NC"),
        ]

    def get_recently_added(self):
        pass

    def get_by_month_day(self):
        pass

    def get_oldest_shown(self):
        pass


class Basics(unittest.TestCase):
    def test_should_find_city_in_the_cache(self):
        # Arrange
        cache = [
            GISDBRecord(lat=38, long=-80, city="City A", state="NC"),
            GISDBRecord(lat=39, long=-81, city="City B", state="NC"),
        ]
        subject = GeoLocator(FakeCatalog("test-table"), cache)

        # Act
        results = subject.locate(38.111, -80.2)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.city, "City A")
        self.assertEqual(results.state, "NC")
        self.assertEqual(results.min_combined_distance, 0.311)
        self.assertEqual(results.location, "cache")
        self.assertEqual(subject.cache_hit_ratio, 1.0)

    def test_should_find_city_in_from_repo(self):
        # Arrange
        cache = [
            GISDBRecord(lat=38, long=-80, city="City A", state="NC"),
            GISDBRecord(lat=39, long=-81, city="City B", state="NC"),
        ]
        subject = GeoLocator(FakeCatalog("test-table"), cache)

        # Act
        results = subject.locate(36, -78.7765)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.city, "City C")
        self.assertEqual(results.state, "NC")
        self.assertEqual(results.min_combined_distance, 0.2235)
        self.assertEqual(results.location, "cache")
        self.assertEqual(subject.cache_hit_ratio, 0.0)


class Cache(unittest.TestCase):
    def test_should_find_later_cities_based_on_previous_cache_additions(self):
        # Arrange
        subject = GeoLocator(FakeCatalog("test-table"))
        results = subject.locate(36.01, -78.7764)
        results = subject.locate(36.02, -78.7765)
        results = subject.locate(36.03, -78.7766)

        # Act
        results = subject.locate(36, -78.7765)
        print(f"test results: {results}")
        print(subject)

        # Assert
        self.assertGreaterEqual(subject.cache_hit_ratio, 0.75)


if __name__ == "__main__":
    unittest.main()
