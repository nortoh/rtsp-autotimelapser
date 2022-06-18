from timelapse_thread import TimelapseThread
from timelapse import Timelapse
from threading import Thread, Lock
from camera import Camera
from frame import Frame
from log import Log
import cv2
import os

class CameraThread(Thread):

    def __init__(self, camera: Camera, save: bool):
        Thread.__init__(self)
        self.camera = camera
        self.save = save
        self._new_frames = []
        self._lock = Lock()

    def run(self) -> None:
        self._lock.acquire()
        self.open_connection()
        self._lock.release()

    # Open connection to camera
    def open_connection(self):
        os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
        camera_connection = cv2.VideoCapture(self.camera.rtsp_url, cv2.CAP_FFMPEG)

        if not camera_connection.isOpened():
            Log.logger().error('Could not open connection to {name}'.format(name=self.camera.name))
            return

        self.capture_photo(connection=camera_connection)

    # Capture a photo
    def capture_photo(self, connection):
        _, frame = connection.read()
        connection.release()

        if _ and frame is not None:
            captured_frame: Frame = Frame(camera=self.camera, image=frame, timestamp=self.camera.timestamp)
            captured_frame.save()

            Log.logger().info('[{name}] Photo taken ({timestamp}.png)'.format(
                name=captured_frame.camera.name,
                timestamp=captured_frame.timestamp)
            )

        if self.save:
            self.build_video()

    def build_video(self):
        timelapse = Timelapse(camera=self.camera)
        timelapse_thread = TimelapseThread(timelapse=timelapse)
        timelapse_thread.start()
        timelapse_thread.join()
