import json
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.Picture import ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import AddNewPicture, add_new_picture_from_s3


class AddPictures(unittest.TestCase):
    # def test_should_find_several_newly_added_pictures_from_original_2023(self):
    #     # Arrange
    #     s3_files_2023 = S3().list_objects(
    #         "svz-master-pictures-new", "original/2023", total_max=5
    #     )
    #     for s3_obj in s3_files_2023:
    #         results = add_new_picture_from_s3(
    #             s3_obj.bucket + "/" + s3_obj.key, "master-pictures-catalog-test"
    #         )
    #     s3_sources = [f"{s3_obj.bucket}/{s3_obj.key}" for s3_obj in s3_files_2023]

    #     repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog-test"), RealClock())

    #     # Act
    #     results = repo.get_recently_added("landscape")
    #     print("\nFound recently added:")
    #     for r in results:
    #         print(f"{r.date_added}: {r.layout:<15} {r.s3_url}")
    #     repo_sources = [r.s3_url for r in results]

    #     # Assert
    #     for s3_source in s3_sources:
    #         self.assertTrue(
    #             s3_source in repo_sources,
    #             f"Can't find {s3_source} in {sorted(repo_sources)}",
    #         )

    # def test_should_find_several_newly_added_pictures_from_original_2012(self):
    #     # Arrange
    #     s3_files_2023 = S3().list_objects(
    #         "svz-master-pictures-new", "original/2012", total_max=20
    #     )
    #     for s3_obj in s3_files_2023:
    #         results = add_new_picture_from_s3(
    #             s3_obj.bucket + "/" + s3_obj.key, "master-pictures-catalog-test"
    #         )
    #     s3_sources = [f"{s3_obj.bucket}/{s3_obj.key}" for s3_obj in s3_files_2023]

    #     repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog-test"), RealClock())

    #     # Act
    #     results = repo.get_recently_added("landscape")
    #     print("\nFound recently added:")
    #     for r in results:
    #         print(f"{r.date_added}: {r.layout:<15} {r.s3_url}")
    #     repo_sources = [r.s3_url for r in results]

    #     # Assert
    #     for s3_source in s3_sources:
    #         self.assertTrue(
    #             s3_source in repo_sources,
    #             f"Can't find {s3_source} in {sorted(repo_sources)}",
    #         )

    def test_should_find_several_newly_added_pictures_from_original_2016(self):
        # Arrange
        s3_files_2023 = S3().list_objects(
            "svz-master-pictures-new",
            "original/2016/2016-09-05_",
            total_max=20,
        )
        for s3_obj in s3_files_2023:
            results = add_new_picture_from_s3(
                s3_obj.bucket + "/" + s3_obj.key, "master-pictures-catalog-test"
            )
        s3_sources = [f"{s3_obj.bucket}/{s3_obj.key}" for s3_obj in s3_files_2023]

        repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog-test"), RealClock())

        # Act
        results = repo.get_recently_added()
        print("\nFound recently added:")
        for r in results:
            print(f"{r.date_added}: {r.layout:<15} {r.s3_url}")
        repo_sources = [r.s3_url for r in results]

        # Assert
        for s3_source in s3_sources:
            self.assertTrue(
                s3_source in repo_sources,
                f"Can't find {s3_source} in {sorted(repo_sources)}",
            )

    # def test_should_find_several_newly_added_pictures_from_fl_spring_break_2019(self):
    #     # Arrange
    #     s3_files = S3().list_objects(
    #         "svz-master-pictures-new",
    #         "original/2019/2019-04-23_Florida_Spring_Break_",
    #         total_max=20,
    #     )
    #     for s3_obj in s3_files:
    #         results = add_new_picture_from_s3(
    #             s3_obj.bucket + "/" + s3_obj.key, "master-pictures-catalog-test"
    #         )
    #     s3_sources = [f"{s3_obj.bucket}/{s3_obj.key}" for s3_obj in s3_files]

    #     repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog-test"), RealClock())

    #     # Act
    #     results = repo.get_recently_added("landscape")
    #     print("\nFound recently added:")
    #     for r in results:
    #         print(f"{r.date_added}: {r.layout:<15} {r.s3_url}")
    #     repo_sources = [r.s3_url for r in results]

    #     # Assert
    #     for s3_source in s3_sources:
    #         self.assertTrue(
    #             s3_source in repo_sources,
    #             f"Can't find {s3_source} in {sorted(repo_sources)}",
    #         )

    # def test_should_find_several_newly_added_pictures_from_raw_2022(self):
    #     # Arrange
    #     s3_files = S3().list_objects(
    #         "svz-master-pictures-new", "raw-photos/2022", total_max=50
    #     )
    #     s3_files_to_add = []
    #     for s3_obj in s3_files:
    #         if "jpg" in s3_obj.key.lower() or "jpeg" in s3_obj.key.lower():
    #             try:
    #                 results = add_new_picture_from_s3(
    #                     s3_obj.bucket + "/" + s3_obj.key, "master-pictures-catalog-test"
    #                 )
    #                 s3_files_to_add.append(s3_obj)
    #             except Exception as e:
    #                 print(f"*** Exception: {e}")
    #         else:
    #             print(f"Skipping: {s3_obj.key} because not a jpg")
    #     s3_sources = [f"{s3_obj.bucket}/{s3_obj.key}" for s3_obj in s3_files_to_add]

    #     repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog-test"), RealClock())

    #     # Act
    #     results = repo.get_recently_added()
    #     print("\nFound recently added:")
    #     for r in results:
    #         print(f"{r.date_added}: {r.layout:<15} {r.s3_url}")
    #     repo_sources = [r.s3_url for r in results]

    #     # Assert
    #     for count, s3_source in enumerate(s3_sources):
    #         self.assertTrue(
    #             s3_source in repo_sources,
    #             f"Can't find #{count}. {s3_source} in {sorted(repo_sources)}",
    #         )


if __name__ == "__main__":
    unittest.main()
