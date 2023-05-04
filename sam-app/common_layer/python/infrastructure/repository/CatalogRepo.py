import json
import random
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List

from domain import Picture
from domain.DTOs import GISRecord, PictureCatalogGroup
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
    def get_gis_data_by_state(self, state_id: str) -> List[GISRecord]:
        raise NotImplemented

    @abstractmethod
    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISRecord]:
        raise NotImplemented


class PictureCatalogRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB, clock: ITellingTime):
        self._db = db
        self._clock = clock

    def add_new_picture_to_catalog(self, picture_records: PictureCatalogGroup) -> dict:
        json_record_set = []
        json_record_set.append(asdict(picture_records.picture))
        for r in picture_records.hashes:
            json_record_set.append(asdict(r))
        return self._db.put_batch(json_record_set)

    def get_gis_data_by_state(self, state_id: str) -> List[GISRecord]:
        results = self._db.query_table_equal(
            {"gsi2_pk": "STATE", "gsi2_sk": state_id}, "gsi2"
        )
        return [
            GISRecord(lat=r["lat"], long=r["lng"], city=r["city"], state=r["state_id"])
            for r in results
        ]

    def get_gis_data_by_lat_long(self, lat: float, long: float) -> List[GISRecord]:
        rounded_lat = int(round(lat, 0))
        rounded_long = int(round(long, 0))
        sk = f"LAT_LONG#{rounded_lat},{rounded_long}__"
        results = self._db.query_table_begins(
            {"pk": "GIS_CITY", "sk": sk},
        )
        return [
            GISRecord(lat=r["lat"], long=r["lng"], city=r["city"], state=r["state_id"])
            for r in results
        ]
