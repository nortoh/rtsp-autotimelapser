from config import Config
from log import Log
from camera_thread import CameraThread
from timelapse_thread import TimelapseThread
from camera import Camera
from timelapse import Timelapse
from datetime import date, datetime
from time import sleep
import os

class Application(object):

    def __init__(self):
        self.config = Config()
        self.camera_configs = list(self.config.get_setting('cameras'))
        self.camera_threads = []
        self.cameras = []
        self.hour = datetime.now().strftime('%H')
        self.__version = 1.1
        Log('timelapser')

    def boot(self):
        Log.logger().info('timelapser by nortoh v{version}'.format(version=self.__version))

        self.delay = int(self.config.get_setting('delay'))
        self.cycles_limit = int(self.config.get_setting('cycles_limit'))

        if (self.delay is None or self.delay < 0 or self.cycles_limit is None):
            Log.logger().error('Invalid configuration file')
            os._exit(1)

        Log.logger().info('delay: {delay} seconds, cycles_limit: {cycles_limit}'.format(delay=self.delay, cycles_limit=self.cycles_limit))

        grammar = ('camera', 'cameras')[len(self.camera_configs) > 1]
        Log.logger().info('Collected {configs} {grammar}'.format(configs=len(self.camera_configs), grammar=grammar))

        for camera_config in self.camera_configs:
            camera = Camera(configuration=camera_config)
            self.cameras.append(camera)

            datestamp = date.today().strftime('%Y-%m-%d')
            if not os.path.isdir('camera_data/{name}/images/{date}'.format(name=camera.name, date=datestamp)):
                os.makedirs('camera_data/{name}/images/{date}'.format(name=camera.name, date=datestamp))

        self.start()

    def start(self):
        try:
            while True:
                current_hour = datetime.now().strftime('%H')

                if current_hour != self.hour:
                    Log.logger().info('Time of the hour to save another beatiful timelapse')
                    self.hour = current_hour
                    for camera in self.cameras:
                        timelapse_thread = TimelapseThread(timelapse=Timelapse(camera=camera))
                        timelapse_thread.start()
                        timelapse_thread.join()

                for camera in self.cameras:
                    self.start_camera_thread(camera=camera, save=True)

                sleep(self.delay)
        except KeyboardInterrupt as e:
            Log.logger().warning('STOPPING THREAD')

    def start_camera_thread(self, camera: Camera, save: bool):
        thread = CameraThread(camera=camera, save=save)
        thread.start()
        thread.join()

if __name__ == '__main__':
    app = Application()
    app.boot()
