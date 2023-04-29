from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass

from domain import Picture
from domain.Picture import Picture
from infrastructure.repository.DynamoDB import UsingDynamoDB


@dataclass(frozen=True)
class PictureRecord:
    s3_url: str


@dataclass(frozen=True)
class PictureCatalogGroup:
    picture: PictureRecord


def convert_picture_to_catalogrecords(picture: Picture) -> PictureCatalogGroup:
    picture_record = PictureRecord(picture.source)
    return PictureCatalogGroup(picture=picture_record)


class StoringCatalogData(ABC):
    @abstractmethod
    def __init__(self, db: UsingDynamoDB):
        raise NotImplemented

    @abstractmethod
    def write_picture_to_catalog(self, record: PictureCatalogGroup) -> None:
        raise NotImplemented


class PictureCatalogRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB):
        self._db = db

    def write_picture_to_catalog(self, record: PictureCatalogGroup):
        raise NotImplemented
