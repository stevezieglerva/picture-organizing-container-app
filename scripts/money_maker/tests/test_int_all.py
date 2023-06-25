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
        self.assertEqual(
            results, ["raw-photos/2023/2023-06-12 Pictures MOV/2023-06-12 22.44.42.mov"]
        )


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

    def test_should_get_new_s3_filename_for_raw_photos_pic(self):
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
            "raw-photos/Wx100/2023/2023-06-12 Pictures/2023-06-12 22.44.42.jpg",
        )

    def test_should_get_new_s3_filename_for_test_pic(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.get_new_s3_filename("test/2023-06-12 22.44.42.jpg")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results,
            "raw-photos/Wx100/test/2023-06-12 22.44.42.jpg",
        )

    def test_should_get_new_s3_filename_for_test_pic_midsize(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        results = subject.get_new_s3_filename("test/2023-06-12 22.44.42.jpg", 1500)
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results,
            "raw-photos/Wx1500/test/2023-06-12 22.44.42.jpg",
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
    def test_should_resize_thumbnail_version(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))
        orig_picture = Picture(
            "svz-master-pictures-new/tests/sample_1_with_gps.jpg",
            ImageIOS3(),
        )
        self.assertGreaterEqual(orig_picture.width, 2000)

        # Act
        filename, size = subject.resize_for_s3("tests/sample_1_with_gps.jpg", 200)
        print(f"test results: {filename}")

        # Assert
        self.assertEqual(filename, "raw-photos/Wx200/tests/sample_1_with_gps.jpg")
        self.assertEqual(size.width, 200)
        resized_picture = Picture("svz-master-pictures-new/" + filename, ImageIOS3())
        print(resized_picture)
        self.assertEqual(resized_picture.width, 200)
        self.assertEqual(resized_picture.gis_lat, 35.7374917)
        print(
            f"   orig_picture.hash_average_hash: {str(orig_picture.hash_average_hash)}\nresized_picture.hash_average_hash: {str(resized_picture.hash_average_hash)}"
        )
        print(orig_picture.hash_average_hash - resized_picture.hash_average_hash)
        self.assertLessEqual(
            orig_picture.hash_average_hash - resized_picture.hash_average_hash,
            0,
            "average_hash is different",
        )
        self.assertNotEqual(orig_picture.hash_unique, resized_picture.hash_unique)

    def test_should_resize_small_version(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))
        orig_picture = Picture(
            "svz-master-pictures-new/tests/sample_1_with_gps.jpg",
            ImageIOS3(),
        )
        self.assertGreaterEqual(orig_picture.width, 2000)

        # Act
        filename, size = subject.resize_for_s3("tests/sample_1_with_gps.jpg", 1500)
        print(f"test results: {filename}")

        # Assert
        self.assertEqual(filename, "raw-photos/Wx1500/tests/sample_1_with_gps.jpg")
        self.assertEqual(size.width, 1500)
        resized_picture = Picture("svz-master-pictures-new/" + filename, ImageIOS3())
        print(resized_picture)
        self.assertEqual(resized_picture.width, 1500)
        self.assertEqual(resized_picture.gis_lat, 35.7374917)
        print(
            f"orig_picture.hash_average_hash: {orig_picture.hash_average_hash}\nresized_picture.hash_average_hash: {resized_picture.hash_average_hash}"
        )
        self.assertEqual(
            orig_picture.hash_average_hash,
            resized_picture.hash_average_hash,
            "average hash is different",
        )
        self.assertNotEqual(orig_picture.hash_unique, resized_picture.hash_unique)


class RecordMeta(unittest.TestCase):
    def test_should_record_meta_data(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))
        input = Picture(
            "svz-master-pictures-new/original/2019/2019-04-14_Charlottesville_National_Championship_IMG_9003_-_Copy.JPG",
            ImageIOS3(),
        )

        # Act
        unique_filename, average_filename = subject.record_meta_data(input)
        print(f"test results: {unique_filename}")

        # Assert
        self.assertEqual(
            unique_filename,
            "output/meta/unique_hash/9d7ffda27b041a7a0ad03ba4935007f6.json",
        )


class MoveFiles(unittest.TestCase):
    def test_should_move_files_successfully(self):
        # Arrange
        subject = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))

        # Act
        success, error = subject.move_files(
            [
                "raw-photos/2022/2022-01-02 Phone Pictures/family/2022-01-02 20.42.14.jpg",
                "raw-photos/2022/2022-01-01 Pictures PNG/2022-01-01 12.25.41.png",
            ]
        )

        # Assert
        self.assertEqual(
            success,
            [
                "raw-photos/2022/2022-01-02 Phone Pictures/family/2022-01-02 20.42.14.jpg"
            ],
        )
        self.assertEqual(
            error, ["raw-photos/2022/2022-01-01 Pictures PNG/2022-01-01 12.25.41.png"]
        )


if __name__ == "__main__":
    unittest.main()
