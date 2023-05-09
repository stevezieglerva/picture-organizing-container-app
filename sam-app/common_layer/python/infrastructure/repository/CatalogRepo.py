import json
import random
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List

from domain import Picture
from domain.DTOs import GISDBRecord, PictureCatalogGroup, PictureDBRecord
from domain.Picture import Picture
from infrastructure.repository.DynamoDB import UsingDynamoDB
from infrastructure.system.Clock import ITellingTime
from ulid import ULID


class StoringCatalogData(ABC):
    @abstractmethod
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        raise NotImplemented

    @abstractmethod
    def add_new_picture_to_catalog(self, record: PictureCatalogGroup) -> None:
        raise NotImplemented

    @abstractmethod
    def get_gis_data_by_state(self, state_id: str) -> List[GISDBRecord]:
        raise NotImplemented

    @abstractmethod
    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISDBRecord]:
        raise NotImplemented

    @abstractmethod
    def get_recently_added(
        self, layout: str, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        pass


class PictureCatalogRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        self._db = db
        self._clock = clock

    def add_new_picture_to_catalog(self, picture_records: PictureCatalogGroup) -> dict:
        json_record_set = []
        json_record_set.append(asdict(picture_records.picture))
        for r in picture_records.hashes:
            json_record_set.append(asdict(r))
        if picture_records.missing_gis_data:
            print("adding missing gis")
            json_record_set.append(asdict(picture_records.missing_gis_data))
        print(json.dumps(json_record_set, indent=3, default=str))
        return self._db.put_batch(json_record_set)

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
        self, layout: str, delta: timedelta = timedelta(days=1)
    ) -> List[PictureDBRecord]:
        pass
        now = self._clock.get_time() - delta
        pk = f"DATE_ADDED#{layout}"
        sk = now.isoformat()
        raw_records = self._db.query_table_greater_than(
            {"gsi2_pk": pk, "gsi2_sk": sk}, "gsi2", False
        )
        object_records = []
        for r in raw_records:
            picture_db_record = PictureDBRecord(**r)
            object_records.append(picture_db_record)
        return object_records
