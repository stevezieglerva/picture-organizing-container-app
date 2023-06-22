import json
import random

from domain.DatePicker import IDatePicker
from domain.DTOs import PictureForAPI
from domain.Picture import ImageIO, Picture
from domain.PictureSelector import get_target_dimensions, select_picture
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
        image_io: ImageIO,
        resized_path_prefix: str = "",
    ):
        self._repo = repo
        self._bucket = bucket
        self._s3 = s3
        self._date_picker = date_picker
        self._clock = clock
        self._imageio = image_io
        self._resized_path_prefix = "/sweet_shuffle/"
        if resized_path_prefix != "":
            self._resized_path_prefix = resized_path_prefix

    def get_picture(self, width: int, height: int, user_agent: str) -> PictureForAPI:
        oldest_shown = self._repo.get_oldest_shown()
        recently_added = self._repo.get_recently_added()
        on_this_day = []

        selected_picture = select_picture(
            self._date_picker.get_date_type(self._clock.get_time()),
            width,
            height,
            oldest_shown,
            recently_added,
            on_this_day,
        )
        print(f"selected_picture: {selected_picture}")

        picture = Picture(selected_picture.s3_url, self._imageio)

        resize_width, resize_height = get_target_dimensions(width, height, user_agent)
        resized_new_key = (
            f"{self._resized_path_prefix}current_resized_{random.randint(0, 100)}.jpg"
        )
        resized_picture = picture.resize_fitting_aspect_ratio(
            f"{self._bucket}{resized_new_key}", resize_width, resize_height
        )
        presigned_url = self._s3.get_presigned_url(self._bucket, resized_new_key)

        return PictureForAPI(
            key_small=selected_picture.s3_url,
            presigned_url=presigned_url,
            height=resize_height,
            width=resize_width,
            db_record={},
            picture_type="",
        )

    def update_show_data(self):
        pass
