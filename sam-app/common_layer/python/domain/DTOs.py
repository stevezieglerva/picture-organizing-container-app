from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

from infrastructure.repository.DynamoDB import BatchResults


@dataclass(frozen=True)
class GISDBRecord:
    lat: float
    long: float
    city: str
    state: str


@dataclass(frozen=True)
class PictureRecord:
    s3_url: str
    ulid: str
    date_taken: datetime
    height: int
    width: int
    layout: str
    hash_average_hash: str  # ": "030078e0c0f4feff",
    hash_crop_resistant: str  # ": "0706061e3ab2c24b,b2e3090984346030,06baf24b28099430",
    hash_phash: str  # ": "f9298474f2c7c2c9",
    hash_unique: str  # ": "1f4550fc769debc4023299205427e6ef",
    gis_lat: float = -1
    gis_long: float = -1
    city: str = None
    state: str = None
    model: str = ""


@dataclass(frozen=True)
class PictureDBRecord:
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
    city: str = None
    state: str = None
    last_shown: datetime = datetime(1900, 1, 1, 1, 1, 1)
    model: str = ""


@dataclass(frozen=True)
class HashDBRecord:
    pk: str
    sk: str
    hash_type: str
    hash_value: str
    gsi1_pk: str
    gsi1_sk: str
    gsi2_pk: str
    gsi2_sk: str
    gsi3_pk: str
    gsi3_sk: str
    gsi4_pk: str
    gsi4_sk: str
    s3_url: str


@dataclass(frozen=True)
class MissingGISDataDBRecord:
    pk: str
    sk: str
    s3_url: str
    date_added: str
    date_updated: str


@dataclass(frozen=True)
class PictureCatalogGroup:
    picture: PictureDBRecord
    hashes: List[HashDBRecord]
    missing_gis_data: MissingGISDataDBRecord


@dataclass(frozen=True)
class PictureForAPI:
    key_small: str
    presigned_url: str
    height: int = None
    width: int = None
    db_record: dict = None
    picture_type: str = ""


@dataclass(frozen=True)
class PictureSelectionOption:
    s3_url: str
    layout: str
    last_shown: datetime
    date_added: datetime


@dataclass(frozen=True)
class PictureForAPI:
    key_small: str
    presigned_url: str
    height: int
    width: int
    db_record: dict
    picture_type: str
