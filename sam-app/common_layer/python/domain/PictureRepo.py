import json
import random
from abc import ABC, abstractclassmethod
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from typing import List

import boto3
from DatePicker import DatePicker
from dateutil.parser import *
from DynamoDB import DynamoDB
from Picture import ImageIOS3, Picture
from S3 import *


class ValidRandomPictureNotFound(ValueError):
    pass


@dataclass(frozen=True)
class PictureForAPI:
    key_small: str
    presigned_url: str
    height: int = None
    width: int = None
    db_record: dict = None
    picture_type: str = ""


class IStoringPictures(ABC):
    @abstractclassmethod
    def get_picture(self, **kwargs) -> PictureForAPI:
        raise NotImplementedError()


class PictureS3Repo(IStoringPictures):
    def __init__(self, bucket_name: str, s3: S3):
        self._bucket_name = bucket_name
        self._s3 = s3

    def get_picture(self, **kwargs) -> PictureForAPI:
        print(f"kwargs: {kwargs}")
        s3_client = boto3.client("s3")
        attempt = 0
        if kwargs == {} or (
            kwargs["picture_qualifier"] == None and kwargs["year"] == None
        ):
            print("Getting random picture")
            while True:
                attempt += 1
                years = [
                    "2022",
                    "2021",
                    "2020",
                    "2019",
                    "2018",
                    "2017",
                    "2016",
                    "2015",
                    "2014",
                    "2013",
                    "2012",
                    "2011",
                    "2010",
                    "2009",
                    "2008",
                    "2007",
                ]
                random_year = random.choice(years)
                random_month = str(random.randint(1, 12)).zfill(2)
                prefix = f"small/{random_year}/{random_year}-{random_month}"
                print(f"\nAttempt #{attempt} - prefix: {prefix}")
                list = self._s3.list_objects(self._bucket_name, prefix)
                if len(list) == 0:
                    prefix = f"small/{random_year}/{random_year}_{random_month}"
                    print(f"\tprefix: {prefix}")
                    list = self._s3.list_objects(self._bucket_name, prefix)
                    if len(list) == 0:
                        continue
                random_pic = random.choice(list)
                print(random_pic)

                presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": self._bucket_name,
                        "Key": random_pic.key,
                    },
                )

                return PictureForAPI(random_pic.key, presigned_url)
        else:
            if kwargs["picture_qualifier"] != None:
                if kwargs["picture_qualifier"] == "old":
                    years = [
                        "2015",
                        "2014",
                        "2013",
                        "2012",
                        "2011",
                        "2010",
                        "2009",
                        "2008",
                        "2007",
                    ]
                if kwargs["picture_qualifier"] == "new":
                    years = [str(datetime.now().year)]
                while True:
                    attempt += 1

                    random_year = random.choice(years)
                    random_month = str(random.randint(1, 12)).zfill(2)
                    prefix = f"small/{random_year}/{random_year}-{random_month}"
                    print(f"\nAttempt #{attempt} - prefix: {prefix}")
                    list = self._s3.list_objects(self._bucket_name, prefix)
                    if len(list) == 0:
                        prefix = f"small/{random_year}/{random_year}_{random_month}"
                        print(f"\tprefix: {prefix}")
                        list = self._s3.list_objects(self._bucket_name, prefix)
                        if len(list) == 0:
                            continue
                    random_pic = random.choice(list)
                    print(random_pic)

                    presigned_url = s3_client.generate_presigned_url(
                        "get_object",
                        Params={
                            "Bucket": self._bucket_name,
                            "Key": random_pic.key,
                        },
                    )

                    return PictureForAPI(random_pic.key, presigned_url)
            if kwargs["year"] != None:
                years = [kwargs["year"]]
                print(f"Getting for year: {years}")
                while True:
                    attempt += 1

                    random_year = random.choice(years)
                    random_month = str(random.randint(1, 12)).zfill(2)
                    prefix = f"small/{random_year}/{random_year}-{random_month}"
                    print(f"\nAttempt #{attempt} - prefix: {prefix}")
                    list = self._s3.list_objects(self._bucket_name, prefix)
                    if len(list) == 0:
                        prefix = f"small/{random_year}/{random_year}_{random_month}"
                        print(f"\tprefix: {prefix}")
                        list = self._s3.list_objects(self._bucket_name, prefix)
                        if len(list) == 0:
                            continue
                    random_pic = random.choice(list)
                    print(random_pic)

                    presigned_url = s3_client.generate_presigned_url(
                        "get_object",
                        Params={
                            "Bucket": self._bucket_name,
                            "Key": random_pic.key,
                        },
                    )

                    return PictureForAPI(
                        key_small=random_pic.key,
                        presigned_url=presigned_url,
                        height=random_pic.height,
                    )


class PictureDynamoRepo(IStoringPictures):
    def __init__(
        self,
        db: DynamoDB,
        bucket_name: str,
        s3: S3,
        date_picker: DatePicker = DatePicker(),
        new_db: DynamoDB = DynamoDB("master-pictures-mega"),
    ):
        self._db = db
        self._new_db = new_db
        self._db.limit = 5
        self._bucket_name = bucket_name
        self._s3 = s3
        self._date_picker = date_picker

    def get_record(self, s3_url: str) -> dict:
        raw_record = self._db.get_item({"s3_url": s3_url})
        return raw_record

    def update_record(self, record: str):
        return self._db.put_item(record)

    def get_device_name(self, user_agent: str) -> str:
        if "Jio" in user_agent:
            return "Sony Bravia TV"
        if "iPhone OS 16_2" in user_agent:
            return "Steve Phone"
        if (
            "Mac OS X 10" in user_agent
            and "Chrome" not in user_agent
            and "Firefox" not in user_agent
        ):
            return "Charlotte iPad"
        if "Mac OS X 10" in user_agent:
            return "Steve Laptop"
        return ""

    def get_picture(
        self,
        viewport_height: int,
        viewport_width: int,
        user_agent: str = None,
        today: datetime = datetime.now(),
    ) -> PictureForAPI:
        print(f"viewport_height: {viewport_height}")
        print(f"viewport_width: {viewport_width}")
        print(f"user_agent: {user_agent}")
        print(f"today: {today}")

        MAX_ATTEMPTS = 5
        viewport_layout = "landscape"
        if viewport_height > viewport_width:
            viewport_layout = "portrait"
        print(f"viewport_layout: {viewport_layout}")

        date_picker = self._date_picker.get_date_type(today)
        print(f"Date picker: {date_picker}")
        records = []
        selected_type = date_picker.type
        if date_picker.type == "recently_added":
            import_date = parse(
                f"{date_picker.year}-{date_picker.month}-{date_picker.day}"
            )
            raw_records = self._db.query_table_greater_than(
                {
                    "layout": viewport_layout,
                    "date_added": import_date.strftime("%Y-%m-%d"),
                },
                "gsiLayoutDateAdded",
            )
            print(f"Found date_added: {len(raw_records)}")
            raw_records = sorted(raw_records, key=lambda x: x.get("last_shown", ""))
            records = self._remove_shown_recently(raw_records, today)
            print(f"Found date_added last_hour: {len(records)}")

        if date_picker.type == "on_this_day":
            raw_records = self._db.query_table_equal(
                {"month": date_picker.month, "day": date_picker.day},
                "gsiMonthDay",
            )
            print(f"Found on_this_day: {len(raw_records)}")
            raw_records = sorted(raw_records, key=lambda x: x.get("last_shown", ""))
            records = self._remove_shown_recently(raw_records, today)
            print(f"Found on_this_day last_hour: {len(records)}")

        if date_picker.type == "random" or records == []:
            selected_type = "random"
            records = self._db.query_table_equal(
                {"gsi_pk1": "LAST_SHOWN#landscape"}, "gsi_pk1-gsi_sk1-index"
            )
            print(f"Found random: {len(records)}")
        for count, selected_picture in enumerate(records[0:MAX_ATTEMPTS]):
            print(f"\nAttempt #{count + 1}")
            print(f"\nselected_picture: {selected_picture}")

            target_s3_file = selected_picture["s3_url"]
            listed_in_s3 = self._s3.list_objects(self._bucket_name, target_s3_file)
            print(f"listed_in_s3: {listed_in_s3}")
            if listed_in_s3 == []:
                print(
                    f"Couldn't actually find {target_s3_file} in the {self._bucket_name}"
                )
                self._clear_out_last_shown_since_s3_not_found(today, selected_picture)
                continue

            image_io_src = f"{self._bucket_name}/{target_s3_file}"
            try:
                print(f"image_io_src: {image_io_src}")
                pic = Picture(image_io_src, ImageIOS3())
            except:
                self._clear_out_last_shown_data_to_avoid_record(today, selected_picture)
                continue
            resized_new_key = (
                f"sweet-shuffle/current_resized_{random.randint(0, 100)}.jpg"
            )
            height_device_increase = 0
            if user_agent != None:
                if "Mac OS" in user_agent and (
                    viewport_width == 1920 or viewport_width == 1680
                ):
                    height_device_increase = 50
                    print(f"Adding height_device_increase: {height_device_increase}")
                if "Mac OS" in user_agent and viewport_width == 1112:
                    height_device_increase = 70
                    print(f"Adding height_device_increase: {height_device_increase}")
            new_size = pic.resize_fitting_aspect_ratio(
                f"{self._bucket_name}/{resized_new_key}",
                viewport_width,
                viewport_height + height_device_increase,
            )

            self._update_last_shown_data(
                today,
                selected_picture,
                selected_type,
                user_agent,
                viewport_width,
                viewport_height,
            )

            presigned_url = self._s3.get_presigned_url(
                self._bucket_name,
                resized_new_key,
            )
            return PictureForAPI(
                key_small=target_s3_file,
                presigned_url=presigned_url,
                height=new_size.height,
                width=new_size.width,
                db_record=selected_picture,
                picture_type=selected_type,
            )

        raise ValidRandomPictureNotFound(
            f"Couldn't not find a valid picture after {MAX_ATTEMPTS} attempts"
        )

    def _clear_out_last_shown_since_s3_not_found(self, today, selected_picture):
        selected_picture["date_updated"] = today.isoformat()
        selected_picture["gsi_pk1"] = "S3 not found error"
        selected_picture["gsi_sk1"] = "S3 not found error"
        self._db.put_item(selected_picture)

    def _clear_out_last_shown_data_to_avoid_record(self, today, selected_picture):
        selected_picture["date_updated"] = today.isoformat()
        selected_picture["gsi_pk1"] = "S3 IO error"
        selected_picture["gsi_sk1"] = "S3 IO error"
        self._db.put_item(selected_picture)

    def _update_last_shown_data(
        self,
        today: datetime,
        selected_picture: dict,
        date_picker_type: str,
        user_agent: str,
        viewport_width: int,
        viewport_height: int,
    ):
        selected_picture["date_updated"] = today.isoformat()
        selected_picture["last_shown"] = today.isoformat()
        gsi_pk1 = f"LAST_SHOWN#{selected_picture['layout']}"
        selected_picture["gsi_pk1"] = gsi_pk1
        selected_picture[
            "gsi_sk1"
        ] = f"{today.strftime('%Y-%m-%d')}_{str(random.randint(1, 100))}"
        view_count = selected_picture.get("view_count", 0) + 1
        selected_picture["view_count"] = view_count
        print(f"Updating: {selected_picture['s3_url']} ")
        self._db.put_item(selected_picture)

        print(f"Updating: shown_stats_history ")
        shown_stats_history = {}
        shown_stats_history["pk"] = f"SHOWN_STATS_HISTORY#{today.strftime('%Y-%m')}"
        shown_stats_history["sk"] = today.isoformat()
        shown_stats_history[
            "original_picture_pk"
        ] = f"ORIGINAL_PICTURE#{selected_picture['s3_url']}"
        shown_stats_history[
            "gsi1_pk"
        ] = f"ORIGINAL_PICTURE#{selected_picture['s3_url']}"
        shown_stats_history["gsi1_sk"] = today.isoformat()
        shown_stats_history["date_picker_type"] = date_picker_type
        shown_stats_history["user_agent"] = "" if user_agent is None else user_agent
        shown_stats_history["viewport_width"] = viewport_width
        shown_stats_history["viewport_height"] = viewport_height
        shown_stats_history["date_added"] = today.isoformat()
        shown_stats_history["date_updated"] = today.isoformat()
        shown_stats_history["date_taken"] = selected_picture["date_taken"]

        print(f"\tsaving: {shown_stats_history}")
        self._new_db.put_item(shown_stats_history)

    def _remove_shown_recently(self, records: list, today: datetime) -> list:
        older_shown = []
        for r in records:
            last_shown = parse(r.get("last_shown", "1900-01-01"))
            recently = today - timedelta(hours=1)
            print(f"checking: {last_shown} last shown with {recently} recently ")
            if last_shown < recently:
                older_shown.append(r)
        return older_shown


# Screen: 1920W x 1001H 1.92 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 980 W x 401 H 2.44 for Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1
# Screen: 1680W x 971 H 1.73 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1920W x 1001H 1.92 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 980 W x 401 H 2.44 for Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1
# Screen: 1680W x 971 H 1.73 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1920W x 1001H 1.92 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1680W x 971 H 1.73 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1920W x 1001H 1.92 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1680W x 971 H 1.73 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1920W x 1001H 1.92 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1680W x 971 H 1.73 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 1920W x 1001H 1.92 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
# Screen: 980 W x 1669H 0.59 for Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1
# Screen: 1680W x 971 H 1.73 for Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
