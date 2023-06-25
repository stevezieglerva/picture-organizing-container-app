import json
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
    level=logging.INFO,
)


class MoneyMaker:
    def __init__(self, s3: S3Base, dropbox: DropboxRepo):
        self.__s3 = s3
        self.__dropbox = dropbox

    def get_files(self, prefix: str, suffix: str = None) -> list:
        list = self.__s3.list_objects("svz-master-pictures-new", prefix)
        if suffix == None:
            return list
        return [o.key for o in list if o.key[-3:].lower() == suffix.lower()]

    def get_new_db_filename(self, old_filename: str) -> str:
        return "/" + old_filename

    def get_new_s3_filename(self, old_filename: str, size: int = 100) -> str:
        new_folder = f"Wx{size}"
        if old_filename.startswith("raw-photos"):
            return old_filename.replace("raw-photos/", f"raw-photos/{new_folder}/")
        return f"raw-photos/{new_folder}/" + old_filename

    def move_to_dropbox(self, s3_key: str):
        new_filename = self.get_new_db_filename(s3_key)
        file_bytes = self.__s3.get_object("svz-master-pictures-new", s3_key)
        self.__dropbox.upload_file_bytes(file_bytes, new_filename)
        return len(file_bytes)

    def resize_for_s3(self, key: str, width: int):
        new_filename = self.get_new_s3_filename(key, width)
        picture = Picture(f"svz-master-pictures-new/{key}", ImageIOS3())
        new_size = picture.resize(
            f"svz-master-pictures-new/{new_filename}", width=width
        )
        return new_filename, new_size

    def record_meta_data(self, picture: Picture) -> str:
        unique_filename = f"output/meta/unique_hash/{picture.hash_unique}.json"
        with open(unique_filename, "w") as file:
            file.write(picture.__repr__())

        average_filename = f"output/meta/average_hash/{picture.hash_average_hash}.json"
        with open(average_filename, "w") as file:
            file.write(picture.__repr__())
        return unique_filename, average_filename

    def move_files(self, keys: list) -> list:
        success = []
        error = []
        for count, key in enumerate(keys):
            logging.info(f"Processing #{count+1}: {key}")
            if ".jpg" in key.lower() or ".jpeg" in key.lower():
                try:
                    for width in [200, 1500]:
                        new_key, size = self.resize_for_s3(key, width)
                        logging.info(f"\tresized: {new_key}")
                    self.move_to_dropbox(new_key)
                    success.append(key)
                except Exception as e:
                    logging.error(f"Exception processing '{key}': {e}")
                    error.append(key)
            else:
                logging.info(f"\tSkipping resizing")
                try:
                    self.move_to_dropbox(key)
                    success.append(key)
                except Exception as e:
                    logging.error(f"Exception processing '{key}': {e}")
                    error.append(key)

        return success, error
