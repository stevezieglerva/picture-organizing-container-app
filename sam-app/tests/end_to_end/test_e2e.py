import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import AddNewPicture


class AddPictures(unittest.TestCase):
    def test_should_add_several_new_pictures_from_original_2023(self):
        # Arrange
        subject = AddNewPicture(
            PictureCatalogRepo(DynamoDB("master-pictures-catalog"), RealClock()),
            RealClock(),
        )
        s3_files_2023 = S3().list_objects(
            "svz-master-pictures-new", "original/2023", total_max=5
        )

        # Act
        for s3_obj in s3_files_2023:
            picture = Picture(s3_obj.bucket + "/" + s3_obj.key, ImageIOS3())
            print(f"\n\n{picture.source}")
            print(f"\t{picture.width}x{picture.height}")
            print(f"\t{picture.model}")
            results = subject.add_new_picture_to_catalog(picture)
            print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
