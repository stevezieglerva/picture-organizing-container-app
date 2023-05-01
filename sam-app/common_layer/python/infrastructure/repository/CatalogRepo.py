import json
import random
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List

from domain import Picture
from domain.Picture import Picture
from infrastructure.repository.DynamoDB import UsingDynamoDB
from infrastructure.system.Clock import ITellingTime
from ulid import ULID


@dataclass(frozen=True)
class PictureRecord:
    pk: str
    sk: str
    ulid: str
    s3_url: str
    date_taken: datetime
    date_added: datetime
    date_updated: datetime
    height: int
    width: int
    layout: str
    view_count: int
    hash_average_hash: str  # ": "030078e0c0f4feff",
    hash_crop_resistant: str  # ": "0706061e3ab2c24b,b2e3090984346030,06baf24b28099430",
    hash_phash: str  # ": "f9298474f2c7c2c9",
    hash_unique: str  # ": "1f4550fc769debc4023299205427e6ef",
    year: int
    month: int
    day: int
    update_desc: str
    last_shown = datetime
    gsi1_pk: str = "-"
    gsi1_sk: str = "-"
    gsi2_pk: str = "-"
    gsi2_sk: str = "-"
    gsi3_pk: str = "-"
    gsi3_sk: str = "-"
    gsi4_pk: str = "-"
    gsi4_sk: str = "-"
    gsi5_pk: str = "-"
    gsi5_sk: str = "-"
    gis_lat: float = -1
    gis_long: float = -1
    last_shown: datetime = datetime(1900, 1, 1, 1, 1, 1)
    model: str = ""


@dataclass(frozen=True)
class HashRecord:
    pk: str
    sk: str
    hash_type: str
    hash_value: str
    s3_url: str


@dataclass(frozen=True)
class PictureCatalogGroup:
    picture: PictureRecord
    hashes: List[HashRecord]


class StoringCatalogData(ABC):
    @abstractmethod
    def __init__(self, db: UsingDynamoDB):
        raise NotImplemented

    @abstractmethod
    def add_new_picture_to_catalog(self, record: PictureCatalogGroup) -> None:
        raise NotImplemented


class PictureCatalogRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        self._db = db
        self._clock = clock

    def add_new_picture_to_catalog(self, picture: Picture) -> PictureCatalogGroup:
        records = self._convert_picture_to_catalogrecords(
            picture,
            self._clock.get_time(),
            self._clock.get_time(),
            "created",
        )
        picture_json = asdict(records.picture)
        print(f"Adding picture: {json.dumps(picture_json, indent=3, default=str)}")
        self._db.put_item(picture_json)
        return records

    def _convert_picture_to_catalogrecords(
        self,
        picture: Picture,
        date_added: datetime,
        date_updated: datetime,
        new_update_desc: str,
    ) -> PictureCatalogGroup:
        layout = "landscape"
        if picture.height > picture.width:
            layout = "portrait"
        update_tmsp = date_updated.strftime("%m/%d/%y")
        gis_lat = -1
        if picture.gis_lat != None:
            gis_lat = picture.gis_lat
        gis_long = -1
        if picture.gis_long != None:
            gis_long = picture.gis_long
        random_shown = random.randint(1, 100)

        last_shown_pk = "NEVER_SHOW"
        last_shown_date = datetime(1900, 1, 1)
        last_shown_sk = "-"
        if "original" in picture.source:
            last_shown_pk = f"LAST_SHOWN#{layout}"
            last_shown_date = date_added - timedelta(days=1)
            last_shown_sk = f"{last_shown_date.strftime('%Y-%m-%d')}_{random_shown}"

        on_this_day = picture.taken.strftime("%m-%d")

        picture_record = PictureRecord(
            pk=f"PICTURE",
            sk=picture.source,
            # only shown if original
            gsi1_pk=last_shown_pk,
            gsi1_sk=last_shown_sk,
            gsi2_pk=f"DATE_ADDED#{layout}",
            gsi2_sk=f"{date_added.isoformat()}",
            gsi3_pk=f"ON_THIS_DAY#{on_this_day}",
            gsi3_sk=f"{picture.taken.isoformat()}",
            gsi4_pk="UNIQUE_HASH",
            gsi4_sk=str(picture.hash_unique),
            gsi5_pk="DATE_TAKEN",
            gsi5_sk=picture.taken.isoformat(),
            ulid=str(ULID()),
            s3_url=picture.source,
            date_taken=picture.taken,
            date_added=date_added,
            date_updated=date_updated,
            height=picture.height,
            width=picture.width,
            layout=layout,
            view_count=0,
            hash_average_hash=str(picture.hash_average_hash),
            hash_crop_resistant=str(picture.hash_crop_resistant),
            hash_phash=str(picture.hash_phash),
            hash_unique=str(picture.hash_unique),
            year=picture.taken.year,
            month=picture.taken.month,
            day=picture.taken.day,
            model=picture.model,
            update_desc=f"{update_tmsp}-{new_update_desc}",
            gis_lat=gis_lat,
            gis_long=gis_long,
            last_shown=last_shown_date,
        )
        hashes = self._create_hash_dynamodb_recordset(
            "AVERAGE", str(picture.hash_average_hash), picture.source
        )
        hashes.extend(
            self._create_hash_dynamodb_recordset(
                "PHASH", str(picture.hash_phash), picture.source
            )
        )
        return PictureCatalogGroup(picture=picture_record, hashes=hashes)

    def _create_hash_dynamodb_recordset(
        self,
        hash_type: str,
        hash_value: str,
        s3_url: str,
    ) -> dict:
        records = []
        print(f"\t\t{hash_type}/{hash_value}")
        for i in range(0, int(len(hash_value) / 4)):
            start_index = i * 4
            end_index = start_index + 4
            hash_section = hash_value[start_index:end_index]
            # print(f"\t\t\thash_section: {hash_section}")
            pk = f"HASH_VALUE_{hash_type}_{i+1}#" + hash_section
            hash_record = HashRecord(
                pk=pk,
                sk=s3_url,
                hash_type=hash_type,
                hash_value=hash_value,
                s3_url=s3_url,
            )
            records.append(hash_record)
        return records


# {
#  "pk": "ORIGINAL_PICTURE#original/2016/2016_06_28_Omni_Homestead_2016_06_28_999_10_-_Copy.JPG",
#  "sk": "-",
#  "date_added": "2020-01-05T14:04:27.546226",
#  "date_taken": "2016-06-28",
#  "date_updated": "2023-04-24T10:31:35.978645",
#  "day": 28,
#  "gsi1_pk": "LAST_SHOWN#landscape",
#  "gsi1_sk": "2023-04-24_81",
#  "gsi2_pk": "DATE_ADDED#landscape",
#  "gsi2_sk": "2020-01-05T14:04:27.546226",
#  "hash_average_hash": "030078e0c0f4feff",
#  "hash_crop_resistant": "0706061e3ab2c24b,b2e3090984346030,06baf24b28099430",
#  "hash_phash": "f9298474f2c7c2c9",
#  "hash_unique": "1f4550fc769debc4023299205427e6ef",
#  "height": 3456,
#  "last_shown": "2023-04-24T00:32:23.502142",
#  "layout": "landscape",
#  "month": 6,
#  "random": 0,
#  "s3_url": "original/2016/2016_06_28_Omni_Homestead_2016_06_28_999_10_-_Copy.JPG",
#  "s3_url_lower": "original/2016/2016_06_28_omni_homestead_2016_06_28_999_10_-_copy.jpg",
#  "view_count": 3,
#  "width": 5184,
#  "year": 2016
# }
