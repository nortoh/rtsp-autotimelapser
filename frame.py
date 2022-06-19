import cv2
from datetime import date, datetime
from camera import Camera

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
    def path(self) -> str:
        return '{path}/{datestamp}/{timestamp}.png'.format(
            path=self.camera.images_folder,
            datestamp=self.camera.datestamp,
            timestamp=self.timestamp
        )

    def save(self):
        cv2.imwrite(self.path, self.image)
