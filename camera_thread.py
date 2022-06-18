from datetime import datetime, date
from threading import Thread
from camera import Camera
from log import Log
import glob
import cv2
import os

class CameraThread(Thread):

    def __init__(self, camera: Camera, save: bool):
        Thread.__init__(self)
        self.camera = camera
        self.save = save

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

        timestamp = int(datetime.now().timestamp())
        if _ and frame is not None:
            datestamp = date.today().strftime('%Y-%m-%d')
            Log.logger().info('[{name}] Photo taken ({timestamp}.jpg)'.format(name=self.camera.name, timestamp=time))
            cv2.imwrite('{path}/{date}/{timestamp}.jpg'.format(path=self.camera.images_folder, date=datestamp, timestamp=timestamp), frame)

        if self.save:
            self.build_video()

    def build_video(self):
        img_array = []
        datestamp = date.today().strftime('%Y-%m-%d')
        files = glob.glob('{path}/{date}/*.jpg'.format(path=self.camera.images_folder, date=datestamp))
        files.sort()
        for filename in files:
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)

        datestamp = datetime.date.today().strftime('%Y-%m-%d')
        out = cv2.VideoWriter('{path}/{name}.mp4'.format(path=self.camera.camera_folder, name=datestamp),cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
