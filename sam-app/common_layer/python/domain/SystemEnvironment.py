from dataclasses import asdict, dataclass

from domain.DatePicker import IDatePicker
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.repository.S3 import S3Base
from infrastructure.system.Clock import ITellingTime


@dataclass(frozen=True)
class SystemEnvironment:
    catalog_repo: StoringCatalogData
    bucket: str
    s3: S3Base
    date_picker: IDatePicker
    clock: ITellingTime
