import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from money_maker import *
from S3 import S3


class GetList(unittest.TestCase):
    def test_should_get_list_of_s3_files(self):
        # Arrange
        subject = MoneyMaker(S3())

        # Act
        results = subject.get_files("raw-photos/2023/2023-06-12")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 12)

    def test_should_get_list_of_just_mov_files(self):
        # Arrange
        subject = MoneyMaker(S3())

        # Act
        results = subject.get_files("raw-photos/2023/2023-06-12", "mov")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 1)


class GetNewFilenames(unittest.TestCase):
    def test_should_get_new_db_filename_for_movie(self):
        # Arrange
        subject = MoneyMaker(S3())

        # Act
        results = subject.get_new_db_filename(
            "raw-photos/2023/2023-06-12 Pictures MOV/2023-06-12 22.44.42.mov"
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(
            results, "raw-photos/2023/2023-06-12 Pictures MOV/2023-06-12 22.44.42.mov"
        )


if __name__ == "__main__":
    unittest.main()
