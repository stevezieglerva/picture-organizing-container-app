import os
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from DropboxRepo import DropboxRepo
from money_maker import *
from Picture import ImageIOS3, Picture
from S3 import S3

db_oauth = os.environ["db"]
app_key = os.environ["app_key"]


class S3Download(unittest.TestCase):
    def test_should_should_download_file(self):
        # Arrange
        subject = S3()
        file_path = "tests/downloads/file_1.mov"

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"The file '{file_path}' has been deleted successfully.")
            except Exception as e:
                print(
                    f"An error occurred while deleting the file '{file_path}': {str(e)}"
                )

        # Act
        results = subject.download_object(
            "svz-master-pictures-new",
            "tests/sample_1.jpg",
            file_path,
        )
        print(f"test results: {results}")

        # Assert
        self.assertTrue(os.path.exists(file_path))


class GetList(unittest.TestCase):
    def test_should_get_list_of_s3_files(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.get_files("raw-photos/2023/2023-06-12")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 12)

    def test_should_get_list_of_just_mov_files(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.get_files("raw-photos/2023/2023-06-12", "mov")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 1)


class GetNewFilenames(unittest.TestCase):
    def test_should_get_new_db_filename_for_movie(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.get_new_db_filename(
            "raw-photos/2023/2023-06-12 Pictures MOV/2023-06-12 22.44.42.mov"
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results, "/raw-photos/2023/2023-06-12 Pictures MOV/2023-06-12 22.44.42.mov"
        )

    def test_should_get_new_s3_filename_for_movie(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.get_new_s3_filename(
            "raw-photos/2023/2023-06-12 Pictures/2023-06-12 22.44.42.jpg"
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results,
            "raw-photos/thumbnails/2023/2023-06-12 Pictures/2023-06-12 22.44.42.jpg",
        )


class MoveToDB(unittest.TestCase):
    def test_should_move_to_dropbox_jpg(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.move_to_dropbox("tests/sample_1.jpg")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, 9235281)


class ResizeForS3(unittest.TestCase):
    def test_should_resize_small_version(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        filename, size = subject.resize_for_s3("tests/sample_1_with_gps.jpg")
        print(f"test results: {filename}")

        # Assert
        self.assertEqual(filename, "raw-photos/thumbnails/tests/sample_1_with_gps.jpg")
        self.assertEqual(size.width, 100)
        picture = Picture("svz-master-pictures-new/" + filename, ImageIOS3())
        print(picture)
        self.assertEqual(picture.width, 100)
        self.assertEqual(picture.gis_lat, 35.7374917)


if __name__ == "__main__":
    unittest.main()
