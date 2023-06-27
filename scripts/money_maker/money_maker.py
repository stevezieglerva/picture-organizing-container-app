import json
import logging
import os
import re
import sys
import uuid
from dataclasses import asdict, dataclass
from io import BytesIO

from DropboxRepo import DropboxRepo
from Picture import ImageIOLocal, ImageIOS3, Picture, PictureSize
from S3 import S3, S3Base

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
            return [o.key for o in list]
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
        return new_filename, new_size, picture

    def record_meta_data(self, picture: Picture) -> str:
        unique_filename = f"output/meta/unique_hash/{picture.hash_unique}.json"
        with open(unique_filename, "w") as file:
            file.write(picture.__repr__())

        average_filename = f"output/meta/average_hash/{picture.hash_average_hash}.json"
        with open(average_filename, "w") as file:
            file.write(picture.__repr__())
        return unique_filename, average_filename

    def move_files(self, keys: list, starting_prefix: str) -> list:
        success = []
        error = []
        for count, key in enumerate(keys):
            logging.info(f"Processing #{count+1}: {key}")
            if ".jpg" in key.lower() or ".jpeg" in key.lower():
                try:
                    temp_filenames = []
                    temp_filename = f"temp_{uuid.uuid1()}.jpg"
                    self.__s3.download_object(
                        "svz-master-pictures-new", key, temp_filename
                    )
                    picture = Picture(temp_filename, ImageIOLocal())
                    print(picture)
                    thumbnail_size = f"temp_Wx200_{temp_filename}"
                    picture.resize(thumbnail_size, width=200)
                    thumbnail_key = key.replace("raw-photos", "raw-photos/Wx200")
                    thumbnail_picture = Picture(thumbnail_size, ImageIOLocal())
                    buffer = BytesIO()
                    thumbnail_picture._pil_image.save(buffer, "JPEG")
                    buffer.seek(0)
                    self.__s3.put_object(
                        "svz-master-pictures-new",
                        thumbnail_key,
                        buffer,
                    )
                    logging.info(f"\tCopied thumbnail to S3: {thumbnail_key}")

                    small_size = f"temp_Wx1500_{temp_filename}"
                    picture.resize(small_size, width=1500)
                    dropbox_filename = key.replace("raw-photos", "/raw-photos/Wx1500")
                    self.__dropbox.upload_file(small_size, dropbox_filename)

                    logging.info(f"\tUploaded to Dropbox: {dropbox_filename}")
                    self.record_meta_data(picture)
                    success.append(key)
                except Exception as e:
                    logging.error(f"Exception processing '{key}': {e}")
                    error.append(key)
                    raise e
            else:
                logging.info(f"\tSkipping resizing")
                try:
                    self.move_to_dropbox(key)
                    success.append(key)
                except Exception as e:
                    logging.error(f"Exception processing '{key}': {e}")
                    error.append(key)
            if count % 5 == 0:
                self.log_success(success, error, key, starting_prefix)
                print(f"\n\n{starting_prefix}: {count}\n\n")
        self.log_success(success, error, key, starting_prefix)
        return success, error

    def log_success(self, success, error, key, starting_prefix):
        success_filename = f"output/progress/filenames/{starting_prefix}_success.txt"
        with open(success_filename, "w") as file:
            file.writelines([r + "\n" for r in success])
        error_filename = f"output/progress/filenames/{starting_prefix}_error.txt"
        with open(error_filename, "w") as file:
            file.writelines([r + "\n" for r in error])


def main(starting_prefix: str):
    db_oauth = os.environ["db"]
    app_key = os.environ["app_key"]
    mover = MoneyMaker(S3(), DropboxRepo(db_oauth, app_key))
    input = mover.get_files(f"raw-photos/2023/{starting_prefix}")

    # Act
    success, error = mover.move_files(input, starting_prefix)


if __name__ == "__main__":
    main(sys.argv[1])
