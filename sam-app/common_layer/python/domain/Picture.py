import hashlib
import json
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Protocol, runtime_checkable

import boto3
import imagehash
from dateutil import parser
from exif import Image as ExifImage
from exif import Orientation
from GPSPhoto import gpsphoto
from PIL import Image, ImageOps


class ImageIO(Protocol):
    """Protocol to support variations and mocking"""

    def open(self, source: str) -> Image:
        "Return a PIL image file from the source"
        ...

    def save(self, new_path: str, image: Image):
        "Save the image file"
        ...

    def get_image_bytes(self, source):
        "Return the raw bytes of the image"
        ...


@runtime_checkable
class MatchesImageIO(ImageIO, Protocol):
    pass


class MissingNewPath(ValueError):
    pass


class MissingPercentage(ValueError):
    pass


class InvalidImageExtension(ValueError):
    pass


class PictureNotFound(ValueError):
    pass


class InvalidBucket(ValueError):
    pass


class ImageIOLocal:
    def open(self, source: str) -> Image:
        return Image.open(source)

    def save(self, new_path: str, image: Image):
        path = Path(new_path)
        extension = path.suffix.lower()
        print(f"\n\nExtension: {extension}")
        if extension in [".jpeg", ".jpg"]:
            format = "JPEG"
        elif extension in [".png"]:
            format = "PNG"
        else:
            raise InvalidImageExtension(
                f"{extension} is not valid so can't find valid image format."
            )

        current_exif = image.info.get("exif", None)
        if current_exif == None:
            print("saving without exif")
            return image.save(new_path, format)
        else:
            print("saving with exif")
            return image.save(new_path, format, exif=image.info["exif"])

    def get_image_bytes(self, source):
        with open(source, "rb") as file:
            return file.read()


class ImageIOS3:
    _image_bytes: BytesIO

    def open(self, source: str) -> Image:
        s3 = boto3.resource("s3")
        path = Path(source)
        bucket = path.parents[-2].name
        try:
            s3.meta.client.head_bucket(Bucket=bucket)
        except Exception as e:
            raise InvalidBucket(f"Error trying to access bucket: {bucket}")
        key = source.replace(bucket + "/", "")
        try:
            obj = s3.Object(bucket_name=bucket, key=key)
            obj_body = obj.get()["Body"].read()
        except:
            raise PictureNotFound(f"Can't find picture: {source}")
        self._image_bytes = obj_body
        return Image.open(BytesIO(self._image_bytes))

    def save(self, new_path: str, image: Image):
        s3 = boto3.resource("s3")
        path = Path(new_path)
        bucket = path.parents[-2].name
        try:
            s3.meta.client.head_bucket(Bucket=bucket)
        except Exception as e:
            raise InvalidBucket(f"Error trying to access bucket: {bucket}")

        key = new_path.replace(bucket + "/", "")
        extension = path.suffix.lower()
        print(f"\n\nExtension: {extension}")
        if extension in [".jpeg", ".jpg"]:
            format = "JPEG"
        elif extension in [".png"]:
            format = "PNG"
        else:
            raise InvalidImageExtension(
                f"{extension} is not valid so can't find valid image format."
            )
        buffer = BytesIO()
        current_exif = image.info.get("exif", None)
        if current_exif == None:
            image.save(buffer, format)
        else:
            image.save(buffer, format, exif=current_exif)
        buffer.seek(0)
        obj = s3.Object(bucket_name=bucket, key=key)
        resp = obj.put(Body=buffer)

    def get_image_bytes(self, source):
        return self._image_bytes


@dataclass(frozen=True)
class PictureSize:
    width: int
    height: int


class Picture:
    source: str
    width: int
    height: int
    hash_unique: str
    hash_phash: imagehash.ImageHash
    hash_average_hash: imagehash.ImageHash
    hash_crop_resistant: imagehash.ImageHash
    orientation: int = None
    model: str = None
    taken: datetime = None
    gis_lat: float = None
    gis_long: float = None

    def __init__(self, source: str, image_io: ImageIO, rotate_on_open: bool = True):
        assert isinstance(
            image_io, MatchesImageIO
        ), "image_io doesn't follow the ImageIO Protocol"
        self.source = source
        self.image_io = image_io

        self._pil_image = self.image_io.open(source)
        if rotate_on_open:
            self._pil_image = ImageOps.exif_transpose(self._pil_image)

        self.width, self.height = self._pil_image.size
        self.hash_unique = hashlib.md5(self._pil_image.tobytes()).hexdigest()
        self.hash_phash = imagehash.phash(self._pil_image)
        self.hash_average_hash = imagehash.average_hash(self._pil_image)
        self.hash_crop_resistant = imagehash.crop_resistant_hash(self._pil_image)

        bytes_data = self.image_io.get_image_bytes(self.source)
        self._exif_image = ExifImage(bytes_data)
        tags = self._exif_image.list_all()
        # print(json.dumps(sorted(tags), indent=3, default=str))
        if "orientation" in tags:
            self.orientation = self._exif_image.orientation
        if "model" in tags:
            self.model = self._exif_image.model
        if "datetime" in tags:
            img_taken_str = self._exif_image.datetime
            print(f"Raw img_taken_str: {img_taken_str}")
            # Raw img_taken_str: 2016:09:25 16:25:02
            # Raw img_taken_str: 2023:02:04 17:37:40
            img_taken_colons_replace = re.sub(
                r"(20..):(..):(..) ", r"\1-\2-\3 ", img_taken_str
            )
            print(f"img_taken_colons_replace: {img_taken_colons_replace}")
            img_taken = parser.parse(img_taken_colons_replace)
            self.taken = img_taken
            print(f"self.taken: {self.taken}")
        else:
            # Try to get date from filename
            # 2022-03-19_19.07.41
            date_regex = "2[0-9][0-9][0-9][\-_][0-9][0-9][\-_][0-9][0-9]"
            dates = re.findall(date_regex, source)
            time_regex = "[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]"
            times = re.findall(time_regex, source)
            if dates:
                date_str = dates[0].replace("_", "-")
                time_str = ""
                if times:
                    time_str = times[0].replace(".", ":")
                self.taken = parser.parse(f"{date_str} {time_str}")
        if "gps_latitude" in self._exif_image.list_all():
            lat_degrees = self._convert_gis_dms_to_dd(
                self._exif_image.gps_latitude, self._exif_image.gps_latitude_ref
            )
            long_degrees = self._convert_gis_dms_to_dd(
                self._exif_image.gps_longitude, self._exif_image.gps_longitude_ref
            )
            self.gis_lat = round(lat_degrees, 7)
            self.gis_long = round(long_degrees, 7)

    def __str__(self):
        text = f"""source:      {self.source}
taken        {self.taken}
width:       {self.width}
height:      {self.height}
aspect:      {round(self.width / self.height, 2)}
orientation: {self.orientation}
model:       {self.model}
lat:         {self.gis_lat}
long:        {self.gis_long}
"""
        return text

    def _convert_gis_dms_to_dd(self, gps_coords, gps_coords_ref):
        d, m, s = gps_coords
        dd = d + m / 60 + s / 3600
        if gps_coords_ref.upper() in ("S", "W"):
            return -dd
        elif gps_coords_ref.upper() in ("N", "E"):
            return dd
        else:
            raise RuntimeError("Incorrect gps_coords_ref {}".format(gps_coords_ref))

    def resize(self, new_path: str, **kwargs):
        width = kwargs.get("width", None)
        height = kwargs.get("height", None)
        percentage = kwargs.get("percentage", None)
        if width and not height:
            perc_change = width / self.width
            height = int(self.height * perc_change)
        if height and not width:
            perc_change = height / self.height
            width = int(self.width * perc_change)
        if not height and not width:
            if percentage == None:
                raise (
                    MissingPercentage(
                        "Need percentage if width and height not provided."
                    )
                )
            width = int(self.width * percentage)
            height = int(self.height * percentage)

        resized = self._pil_image.resize((width, height), Image.ANTIALIAS)
        new_width, new_height = resized.size
        self.image_io.save(new_path, resized)
        return PictureSize(width=new_width, height=new_height)

    def resize_fitting_aspect_ratio(self, new_path, ideal_width, ideal_height):

        aspect = self.width / float(self.height)
        print(f"aspect: {aspect}")
        ideal_aspect = ideal_width / float(ideal_height)
        print(f"ideal_aspect: {ideal_aspect}")

        if aspect > ideal_aspect:
            # Then crop the left and right edges:
            new_width = int(ideal_aspect * self.height)
            offset = (self.width - new_width) / 2
            resize = (offset, 0, self.width - offset, self.height)
        else:
            # ... crop the top and bottom:
            new_height = int(self.width / ideal_aspect)
            offset = (self.height - new_height) / 2
            resize = (0, offset, self.width, self.height - offset)

        cropped_resized_image = self._pil_image.crop(resize).resize(
            (ideal_width, ideal_height), Image.ANTIALIAS
        )
        self.image_io.save(new_path, cropped_resized_image)
        print(
            f"Resized aspect: {self.width}W x {self.height}H -> {ideal_width}W x {ideal_height}H"
        )
        return PictureSize(width=ideal_width, height=ideal_height)

    def crop(self, new_path, one, two, three, four):
        aspect = self.width / float(self.height)
        print(f"aspect: {aspect}")
        ideal_aspect = ideal_width / float(ideal_height)
        print(f"ideal_aspect: {ideal_aspect}")

        if aspect > ideal_aspect:
            # Then crop the left and right edges:
            new_width = int(ideal_aspect * self.height)
            offset = (self.width - new_width) / 2
            resize = (offset, 0, self.width - offset, self.height)
        else:
            # ... crop the top and bottom:
            new_height = int(self.width / ideal_aspect)
            offset = (self.height - new_height) / 2
            resize = (0, offset, self.width, self.height - offset)

        cropped_resized_image = self._pil_image.crop(resize).resize(
            (ideal_width, ideal_height), Image.ANTIALIAS
        )
        self.image_io.save(new_path, cropped_resized_image)
        print(
            f"Resized aspect: {self.width}W x {self.height}H -> {ideal_width}W x {ideal_height}H"
        )
        return PictureSize(width=ideal_width, height=ideal_height)

    def save_as(self, new_path: str):
        self.image_io.save(new_path, self._pil_image)

    def show(self):
        self._pil_image.show()


def open_picture(type: str, source: str, rotate_on_open: bool = True) -> Picture:
    if type not in ["local", "s3"]:
        raise ValueError(f"{type} is not local or s3.")
    if type == "local":
        return Picture(source, ImageIOLocal(), rotate_on_open)
    return Picture(source, ImageIOS3(), rotate_on_open)
