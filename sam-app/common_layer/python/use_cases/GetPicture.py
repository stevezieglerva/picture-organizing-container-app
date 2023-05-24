import json

from domain.DatePicker import IDatePicker
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.repository.S3 import S3Base
from infrastructure.system.Clock import ITellingTime


class GetPicture:
    def __init__(
        self,
        repo: StoringCatalogData,
        s3: S3Base,
        date_picker: IDatePicker,
        clock: ITellingTime,
    ):
        self._repo = repo
        self._s3 = s3
        self._date_picker = date_picker
        self._clock = clock

    def get_picture(self, width: int, height: int, device: str):
        recently_updated = self._repo.get_recently_added()
        print(
            f"recently_updated: {json.dumps(recently_updated, indent=3, default=str)}"
        )

        oldest_shown = self._repo.get_oldest_shown()
        print(f"oldest_shown: {json.dumps(oldest_shown, indent=3, default=str)}")

        date_picker = self._date_picker.get_date_type(self._clock.get_time())
        print(f"Date picker: {date_picker}")
        records = []
        selected_type = date_picker.type
        print(f"selected_type: {selected_type}")

    def update_show_data(self):
        pass

    def resize_image_for_device(self):
        pass
