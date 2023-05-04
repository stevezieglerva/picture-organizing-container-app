import unittest
from datetime import datetime
from typing import List
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.DTOs import GISRecord, PictureCatalogGroup
from domain.Picture import ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import AddNewPicture


class Basic(unittest.TestCase):
    def test_should_add_new_picture_to_catalog_with_gps(self):
        # Arrange
        repo = PictureCatalogRepo(
            DynamoDB("master-pictures-catalog"),
            RealClock(),
        )
        subject = AddNewPicture(repo, RealClock())
        picture = Picture(
            "svz-master-pictures-new/original/2023/2023-04-16_Pictures_Boys_At_TAC_Swim_2023-04-16_11.36.25.jpeg",
            ImageIOS3(),
        )
        print(picture)

        # Act
        results = subject.add_new_picture_to_catalog(
            picture,
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.picture.pk, "PICTURE")
        self.assertEqual(
            results.picture.sk,
            "svz-master-pictures-new/original/2023/2023-04-16_Pictures_Boys_At_TAC_Swim_2023-04-16_11.36.25.jpeg",
        )
        self.assertEqual(results.picture.city, "Cary")
        self.assertEqual(results.picture.state, "NC")


if __name__ == "__main__":
    unittest.main()
