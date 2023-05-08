import csv
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from dateutil.parser import *
from domain.LocationGuesser import LocationGuesser

reader = csv.DictReader(open("tests/unit/data/s3_pic_list.csv"))
existing_pics = []
for row in reader:
    existing_pics.append(row)


class DontMatch(unittest.TestCase):
    def test_should_not_get_guess(self):
        results = LocationGuesser().guess(
            "original/2001/2001_fake.jpg",
            datetime(2001, 6, 19),
        )
        # Assert
        self.assertEqual(results, None)


class Matches(unittest.TestCase):
    def test_should_guess_2023_disney_fl(self):
        results = LocationGuesser().guess(
            "original/2022/2022-06-19_Pictures_Disney_2022-06-19_09.01.23.jpeg",
            datetime(2022, 6, 19),
        )
        # Assert
        self.assertEqual(
            results.city,
            "Lake Buena Vista",
        )
        self.assertEqual(
            results.state,
            "FL",
        )

    def test_should_guess_2014_disney_fl(self):
        results = LocationGuesser().guess(
            "original/2014/2014_08_21_Disney_2014_2014_08_21_999_19_-_Copy.jpg",
            datetime(2014, 8, 21),
        )
        # Assert
        self.assertEqual(
            results.city,
            "Lake Buena Vista",
        )
        self.assertEqual(
            results.state,
            "FL",
        )

    def test_should_guess_william_birthday(self):
        results = LocationGuesser().guess(
            "original/2012/2012_05_30_William_1st_Birthday_-_Steves_IMG_1519_-_Copy.jpg",
            datetime(2012, 5, 30),
        )
        # Assert
        self.assertEqual(
            results.city,
            "Clifton",
        )
        self.assertEqual(
            results.state,
            "VA",
        )

    def test_should_guess_steve_reunion(self):
        results = LocationGuesser().guess(
            "original/2012/2012_06_02_Steve_15_Year_UVA_Reunion_IMG_2117_-_Copy.jpg",
            datetime(2012, 6, 2),
        )
        # Assert
        self.assertEqual(
            results.city,
            "Charlottesville",
        )
        self.assertEqual(
            results.state,
            "VA",
        )

    def test_should_guess_christmas_va(self):
        results = LocationGuesser().guess(
            "original/2012/2012_Christmas_Eve.jpg",
            datetime(2012, 12, 24),
        )
        # Assert
        self.assertEqual(
            results.city,
            "Clifton",
        )
        self.assertEqual(
            results.state,
            "VA",
        )

    def test_should_guess_christmas_nc(self):
        results = LocationGuesser().guess(
            "original/2018/2018_Christmas_Day.jpg",
            datetime(2018, 12, 25),
        )
        # Assert
        self.assertEqual(
            results.city,
            "Apex",
        )
        self.assertEqual(
            results.state,
            "NC",
        )


class BatchProcessing(unittest.TestCase):
    def test_should_guess_right_cities(self):
        # Act
        count = 0
        for row in existing_pics:
            if row["Prev Sunday"] == "2/25/18":
                count += 1
                print(f"#{count} {row['key']}")

        results = []
        for row in existing_pics:
            guess = LocationGuesser().guess(row["key"], parse(row["date"]))
            results.append(guess)

        # Assert
        city = "Lake Buena Vista"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertEqual(len(guesses), 664, city)

        city = "Clifton"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 400, city)

        city = "Charlottesville"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertEqual(len(guesses), 169, city)

        city = "Ocean City"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 457, city)

        city = "Asheville"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertEqual(len(guesses), 113, city)

        city = "Centreville"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 388, city)

        city = "Fairfax Station"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 156, city)

        city = "Luray"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 83, city)

        city = "Wheaton"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 79, city)

        city = "Surf City"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 98, city)

        city = "Ashburn"
        guesses = [g for g in results if g is not None and g.city == city]
        print(guesses[0:1])
        self.assertGreaterEqual(len(guesses), 89, city)

        city_guessed = [g for g in results if g is not None]
        perc_guessed = round(len(city_guessed) / len(results), 2)
        print(f"\nGuessed: {perc_guessed:%}")
        self.assertGreaterEqual(perc_guessed, 0.5)


if __name__ == "__main__":
    unittest.main()
