import unittest
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.GeoLocator import GeoLocator
from infrastructure.repository.CatalogRepo import (
    GISRecord,
    PictureCatalogGroup,
    PictureCatalogRepo,
    StoringCatalogData,
)
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.system.Clock import RealClock


class Basics(unittest.TestCase):
    @unittest.skip("")
    def test_should_find_apex(self):
        # Arrange
        subject = GeoLocator(
            PictureCatalogRepo(DynamoDB("master-pictures-catalog"), RealClock())
        )

        # Act
        results = subject.locate(35.72757, -78.942597)

        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.city, "Apex")
        self.assertEqual(results.state, "NC")
        self.assertEqual(results.min_combined_distance, 0.0722)
        self.assertEqual(subject.cache_hit_ratio, 0.0)

    def test_should_find_city_random(self):
        # Arrange
        subject = GeoLocator(
            PictureCatalogRepo(DynamoDB("master-pictures-catalog"), RealClock())
        )

        # Act
        results = subject.locate(39.5, -98.35)

        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.city, "Glen Elder")

    def test_should_find_city_clifton(self):
        # Arrange
        subject = GeoLocator(
            PictureCatalogRepo(DynamoDB("master-pictures-catalog"), RealClock())
        )

        # Act
        results = subject.locate(38.7801, -77.3867)

        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.city, "Clifton")


@unittest.skip("")
class Cache(unittest.TestCase):
    def test_should_find_city_in_the_cache(self):
        # Arrange
        subject = GeoLocator(
            PictureCatalogRepo(DynamoDB("master-pictures-catalog"), RealClock())
        )
        results = subject.locate(36.01, -78.7764)
        results = subject.locate(36.02, -78.7765)
        results = subject.locate(36.03, -78.7766)

        # Act
        results = subject.locate(36, -78.7765)
        print(f"test results: {results}")
        print(subject)

        # Assert
        self.assertEqual(subject.cache_hit_ratio, 0.75)


# {
#     "Rileys Pond": {
#         "center": {
#             "lat": 35.725639,
#             "long": -78.916407
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Sierra Glen": {
#         "center": {
#             "lat": 35.72757,
#             "long": -78.942597
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "StMM": {
#         "center": {
#             "lat": 35.725203,
#             "long": -78.874998
#         },
#         "height": 0.5,
#         "width": 0.5
#     },
#     "AirBnB": {
#         "center": {
#             "lat": 35.7366,
#             "long": -78.845
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Dead Broke Farm": {
#         "center": {
#             "lat": 35.9636,
#             "long": -78.7299
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Lila E Jones Pool": {
#         "center": {
#             "lat": 35.7304,
#             "long": -78.8556
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "TAC": {
#         "center": {
#             "lat": 35.7759,
#             "long": -78.7545
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "New Valley Hope Railroad": {
#         "center": {
#             "lat": 35.66,
#             "long": -78.9756
#         },
#         "height": 1,
#         "width": 0.05
#     },
#     "Hayden Village Townhouse": {
#         "center": {
#             "lat": 38.8348,
#             "long": -77.3979
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Crowder Park": {
#         "center": {
#             "lat": 35.6947,
#             "long": -78.764
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Toll Brothers Design Studio": {
#         "center": {
#             "lat": 35.8541,
#             "long": -78.8251
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Publix": {
#         "center": {
#             "lat": 35.7375,
#             "long": -78.8937
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "McKimmon Conference Center": {
#         "center": {
#             "lat": 35.7827,
#             "long": -78.6853
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Red Truck Bakery": {
#         "center": {
#             "lat": 38.8649,
#             "long": -77.8575
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Scottish Hills Pool": {
#         "center": {
#             "lat": 35.7596,
#             "long": -78.8129
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Pullen Park": {
#         "center": {
#             "lat": 35.7805,
#             "long": -78.6625
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Grandma and Grandpa House": {
#         "center": {
#             "lat": 38.8072,
#             "long": -77.6065
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Coastal Flats": {
#         "center": {
#             "lat": 38.8577,
#             "long": -77.3565
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Avent Ferry Farm": {
#         "center": {
#             "lat": 35.6308,
#             "long": -78.8607
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Best Buy": {
#         "center": {
#             "lat": 35.762,
#             "long": -78.7395
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Costco": {
#         "center": {
#             "lat": 35.7467,
#             "long": -78.8272
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Phillips Farm": {
#         "center": {
#             "lat": 35.8279,
#             "long": -78.8717
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Dentist": {
#         "center": {
#             "lat": 38.8805,
#             "long": -77.3038
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Home Depot": {
#         "center": {
#             "lat": 35.749,
#             "long": -78.8807
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Toll Brothers Retreat": {
#         "center": {
#             "lat": 35.7349,
#             "long": -78.9466
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Carolina Inn": {
#         "center": {
#             "lat": 35.9097,
#             "long": -79.0544
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Cowfish": {
#         "center": {
#             "lat": 35.8373,
#             "long": -78.6404
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "The Market at Grelen": {
#         "center": {
#             "lat": 38.1993,
#             "long": -78.1937
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "New Hope Railroad": {
#         "center": {
#             "lat": 35.7015,
#             "long": -78.9412
#         },
#         "height": 1,
#         "width": 0.05
#     },
#     "Flooring Company": {
#         "center": {
#             "lat": 35.7731,
#             "long": -78.7813
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Southern Living House": {
#         "center": {
#             "lat": 35.7332,
#             "long": -79.117
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Junk Chapel Hill": {
#         "center": {
#             "lat": 35.8468,
#             "long": -79.1007
#         },
#         "height": 1,
#         "width": 0.35
#     },
#     "Seagroves Farms Pond Pictures": {
#         "center": {
#             "lat": 35.7283,
#             "long": -78.8295
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "Bass Lake Park": {
#         "center": {
#             "lat": 35.6419,
#             "long": -78.8069
#         },
#         "height": 0.05,
#         "width": 0.5
#     },
#     "Junk Starbucks": {
#         "center": {
#             "lat": 35.7988,
#             "long": -78.7951
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "St. Michael School": {
#         "center": {
#             "lat": 35.7875,
#             "long": -78.8213
#         },
#         "height": 0.25,
#         "width": 0.25
#     },
#     "Junk Zensar Location": {
#         "center": {
#             "lat": 35.9138,
#             "long": -78.9045
#         },
#         "height": 1,
#         "width": 0.25
#     },
#     "Cracker Barrel": {
#         "center": {
#             "lat": 35.9748,
#             "long": -77.8447
#         },
#         "height": 0.05,
#         "width": 0.25
#     },
#     "Downtown Clifton": {
#         "center": {
#             "lat": 38.7805,
#             "long": -77.3871
#         },
#         "height": 0.5,
#         "width": 0.50
#     },
#     "Wegmans": {
#         "center": {
#             "lat": 35.828731,
#             "long": -77.3871
#         },
#         "height": 0.05,
#         "width": 0.05
#     },
#     "DC": {
#         "center": {
#             "lat": 38.889891,
#             "long": -77.010109
#         },
#         "height": 2.5,
#         "width": 2.5
#     },
#     "Old Town Alexandria": {
#         "center": {
#             "lat": 38.816092,
#             "long": -77.051739
#         },
#         "height": 2.5,
#         "width": 1
#     }
# }


if __name__ == "__main__":
    unittest.main()
