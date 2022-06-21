import cv2
from datetime import date, datetime
from camera import Camera
from config import Config
import os

class Frame(object):

    def __init__(self, camera: Camera, image: cv2.Mat, timestamp: int):
        self._image: cv2.Mat = image
        self._camera = camera
        self._timestamp = timestamp

    @property
    def image(self) -> cv2.Mat:
        return self._image

    @property
    def camera(self) -> Camera:
        return self._camera

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def fullpath(self) -> str:
        return '{path}/{timestamp}.png'.format(
            path=self.path,
            timestamp=self.timestamp
        )

    @property
    def path(self) -> str:
        return '{path}/{datestamp}'.format(
            path=self.camera.images_folder,
            datestamp=self.camera.datestamp
        )

    def save(self):
        if not os.path.isdir(self.path):
            os.makedirs('{path}/{datestamp}'.format(
                path=self.camera.images_folder,
                datestamp=self.camera.datestamp
            ))
        cv2.imwrite(self.fullpath, self.image, [int(cv2.IMWRITE_PNG_COMPRESSION), int(Config.get_setting('png_compression'))])
