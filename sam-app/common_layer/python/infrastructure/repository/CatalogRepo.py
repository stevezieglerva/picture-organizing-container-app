from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass

from domain import Picture
from infrastructure.repository.CatalogRepo import CatalogRecord
from infrastructure.repository.DynamoDB import UsingDynamoDB


@dataclass(frozen=True)
class CatalogRecord:
    s3_url: str


class StoringCatalogData(ABC):
    @abstractmethod
    def __init__(self, db: UsingDynamoDB):
        raise NotImplemented

    @abstractmethod
    def write_picture_to_catalog(self, record: CatalogRecord) -> CatalogRecord:
        raise NotImplemented


class CatalogRepo(StoringCatalogData):
    def __init__(self, db: UsingDynamoDB):
        self._db = db

    def write_picture_to_catalog(self, record: CatalogRecord):
        raise NotImplemented
