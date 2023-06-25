import logging
from dataclasses import asdict, dataclass

from DropboxRepo import DropboxRepo
from Picture import ImageIOS3, Picture, PictureSize
from S3 import S3Base

logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


class MoneyMaker:
    def __init__(self, s3: S3Base, dropbox: DropboxRepo):
        self.__s3 = s3
        self.__dropbox = dropbox

    def get_files(self, prefix: str, suffix: str = None) -> list:
        list = self.__s3.list_objects("svz-master-pictures-new", prefix)
        if suffix == None:
            return list
        return [o for o in list if o.key[-3:].lower() == suffix.lower()]

    def get_new_db_filename(self, old_filename: str) -> str:
        return "/" + old_filename

    def get_new_s3_filename(self, old_filename: str) -> str:
        if old_filename.startswith("raw-photos"):
            old_filename.replace("raw-photos/", "raw-photos/thumbnails/")
        return "raw-photos/thumbnails/" + old_filename

    def move_to_dropbox(self, s3_key: str):
        new_filename = self.get_new_db_filename(s3_key)
        file_bytes = self.__s3.get_object("svz-master-pictures-new", s3_key)
        self.__dropbox.upload_file_bytes(file_bytes, new_filename)
        return len(file_bytes)

    def resize_for_s3(self, key: str):
        new_filename = self.get_new_s3_filename(key)
        picture = Picture(f"svz-master-pictures-new/{key}", ImageIOS3())
        new_size = picture.resize(f"svz-master-pictures-new/{new_filename}", width=100)
        return new_filename, new_size
