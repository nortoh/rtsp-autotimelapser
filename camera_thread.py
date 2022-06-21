from timelapse_thread import TimelapseThread
from timelapse import Timelapse
from threading import Thread, Lock
from camera import Camera
from frame import Frame
from config import Config
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

        # Release camera connection when we are finished
        camera_connection.release()
        del camera_connection

    # Capture a photo
    def capture_photo(self, connection):
        _, frame = connection.read()

        # Did we get a image?
        if _ and frame is not None:
            captured_frame: Frame = Frame(camera=self.camera, image=frame, timestamp=self.camera.timestamp)
            captured_frame.save()

            Log.logger().info('[{name}] Photo taken ({path})'.format(
                name=captured_frame.camera.name,
                path=captured_frame.fullpath
            ))
            del captured_frame, frame, _

        # Do we save our video?
        if self.save:
            if self.camera.cycles > int(Config.get_setting('cycles_limit')):
                self.camera.cycles = 0

                timelapse_thread = TimelapseThread(timelapse=Timelapse(camera=self.camera))
                timelapse_thread.start()
                timelapse_thread.join()
            else:
                self.camera.cycles += 1
                Log.logger().info('({camera}) Cycle: {cycles}'.format(
                    camera=self.camera.name, cycles=self.camera.cycles
                ))
