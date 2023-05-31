import json

from domain.DatePicker import IDatePicker
from domain.DTOs import PictureForAPI
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.repository.S3 import S3Base
from infrastructure.system.Clock import ITellingTime


class GetPictureUseCase:
    def __init__(
        self,
        repo: StoringCatalogData,
        bucket: str,
        s3: S3Base,
        date_picker: IDatePicker,
        clock: ITellingTime,
    ):
        self._repo = repo
        self._bucket = bucket
        self._s3 = s3
        self._date_picker = date_picker
        self._clock = clock

    def get_picture(self, width: int, height: int, user_agent: str)

    def update_show_data(self):
        pass

    def resize_image_for_device(self):
        pass
