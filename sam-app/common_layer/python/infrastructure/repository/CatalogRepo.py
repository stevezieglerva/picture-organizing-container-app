import json
import random
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List

from dateutil.parser import *
from domain import Picture
from domain.DTOs import (
    GISDBRecord,
    PictureCatalogGroup,
    PictureDBRecord,
    PictureRecord,
    PictureSelectionOption,
)
from domain.Picture import Picture
from infrastructure.repository.DynamoDB import BatchResults, UsingDynamoDB
from infrastructure.system.Clock import ITellingTime
from ulid import ULID


class AddNewPictureFailed(ValueError):
    pass


class StoringCatalogData(ABC):
    @abstractmethod
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        raise NotImplemented

    @abstractmethod
    def add_new_picture_to_catalog(
        self, record: PictureCatalogGroup
    ) -> PictureCatalogGroup:
        raise NotImplemented

    @abstractmethod
    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        raise NotImplemented

    @abstractmethod
    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        raise NotImplemented

    @abstractmethod
    def get_recently_added(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureSelectionOption]:
        raise NotImplemented

    @abstractmethod
    def get_oldest_shown(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureSelectionOption]:
        raise NotImplemented

    @abstractmethod
    def get_by_month_day(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureSelectionOption]:
        raise NotImplemented


class PictureCatalogRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        self._db = db
        self._clock = clock
        self._limit = db.limit

    def get_picture(self, s3_url: str) -> PictureDBRecord:
        raw_record = self._db.query_table_equal({"pk": "PICTURE", "sk": s3_url})
        return PictureDBRecord(**raw_record[0])

    def add_new_picture_to_catalog(
        self, picture_records: PictureCatalogGroup
    ) -> PictureCatalogGroup:
        json_record_set = []
        json_record_set.append(asdict(picture_records.picture))
        for r in picture_records.hashes:
            json_record_set.append(asdict(r))
        if picture_records.missing_gis_data:
            print("adding missing gis")
            json_record_set.append(asdict(picture_records.missing_gis_data))
        print(json.dumps(json_record_set, indent=3, default=str))
        batch_results = self._db.put_batch(json_record_set)
        return batch_results

    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        results = self._db.query_table_equal(
            {"gsi2_pk": "STATE", "gsi2_sk": state_id}, "gsi2"
        )
        return [
            GISDBRecord(
                lat=r["lat"], long=r["lng"], city=r["city"], state=r["state_id"]
            )
            for r in results
        ]

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        rounded_lat = int(round(lat, 0))
        rounded_long = int(round(long, 0))
        sk = f"LAT_LONG#{rounded_lat},{rounded_long}__"
        results = self._db.query_table_begins(
            {"pk": "GIS_CITY", "sk": sk},
        )
        return [
            GISDBRecord(
                lat=r["lat"], long=r["lng"], city=r["city"], state=r["state_id"]
            )
            for r in results
        ]

    def get_recently_added(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureSelectionOption]:
        now = self._clock.get_time() - delta
        pk = f"DATE_ADDED#landscape"
        sk = now.isoformat()
        raw_records_all = self._db.query_table_greater_than(
            {"gsi2_pk": pk, "gsi2_sk": sk}, "gsi2", False
        )

        pk = f"DATE_ADDED#portrait"
        sk = now.isoformat()
        raw_records = self._db.query_table_greater_than(
            {"gsi2_pk": pk, "gsi2_sk": sk}, "gsi2", False
        )
        raw_records_all.extend(raw_records)

        object_records = []
        for r in raw_records_all:
            picture_db_record = PictureDBRecord(**r)
            object_records.append(
                PictureSelectionOption(
                    s3_url=picture_db_record.s3_url,
                    layout=picture_db_record.layout,
                    last_shown=parse(picture_db_record.last_shown),
                    date_added=parse(picture_db_record.date_added),
                )
            )
        return object_records

    def get_oldest_shown(self, limit: int = 5) -> List[PictureSelectionOption]:
        #  "gsi1_pk": "LAST_SHOWN#portrait",
        #  "gsi1_sk": "2023-05-08_59",
        self._db.limit = limit

        pk = f"LAST_SHOWN#landscape"
        raw_records_all = self._db.query_table_equal(
            {"gsi1_pk": pk},
            "gsi1",
        )

        pk = f"LAST_SHOWN#portrait"
        raw_records = self._db.query_table_equal(
            {"gsi1_pk": pk},
            "gsi1",
        )
        raw_records_all.extend(raw_records)
        object_records = []
        for r in raw_records_all:
            picture_db_record = PictureDBRecord(**r)
            object_records.append(
                PictureSelectionOption(
                    s3_url=picture_db_record.s3_url,
                    layout=picture_db_record.layout,
                    last_shown=parse(picture_db_record.last_shown),
                    date_added=parse(picture_db_record.date_added),
                )
            )
        self._db.limit = self._limit
        return object_records

    def get_by_month_day(self):
        raise NotImplementedError


class FakeRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        self._clock = clock

    def add_new_picture_to_catalog(
        self, record: PictureCatalogGroup
    ) -> PictureCatalogGroup:
        pass

    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        pass

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        pass

    def get_recently_added(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        return self._updated

    def get_oldest_shown(
        self, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        return self._oldest_shown

    def set_recently_updated(self, data: list):
        self._updated = [
            PictureSelectionOption(
                s3_url=i[0],
                layout=i[1],
                date_added=self._clock.get_time() + timedelta(i[2]),
                last_shown=self._clock.get_time() + timedelta(i[3]),
            )
            for i in data
        ]

    def set_oldest_shown(self, data: list):
        self._oldest_shown = [
            PictureSelectionOption(
                s3_url=i[0],
                layout=i[1],
                date_added=self._clock.get_time() + timedelta(i[2]),
                last_shown=self._clock.get_time() + timedelta(i[3]),
            )
            for i in data
        ]

    def get_by_month_day(self):
        pass


def create_picture_record_from_picture(
    picture: Picture, city: str, state: str
) -> PictureRecord:
    pass
