from abc import ABC, abstractmethod

from domain.Picture import ImageIO, Picture


class GettingPictureFiles(ABC):
    @abstractmethod
    def get_picture_file(self, source: str) -> Picture:
        raise NotImplemented


class PictureFileRepo(GettingPictureFiles):
    def __init__(self, image_io: ImageIO):
        self._image_io = image_io

    def get_picture_file(self, source: str) -> Picture:
        picture = Picture(source, self._image_io)
        return picture
