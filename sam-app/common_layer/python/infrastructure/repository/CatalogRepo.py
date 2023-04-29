from abc import ABC, abstractmethod

from domain import Picture


class StoringCatalogData(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplemented

    @abstractmethod
    def write_picture_to_catalog(self, record: CatalogRecord):
        raise NotImplemented
