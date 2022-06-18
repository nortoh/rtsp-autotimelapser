from config import Config
from log import Log
from camera_thread import CameraThread
from camera import Camera
from datetime import date
from time import sleep
import os

class Application(object):

    def __init__(self):
        self.config = Config()
        self.camera_configs = list(self.config.get_setting('cameras'))
        self.camera_threads = []
        self.boot_day = int(date.today().strftime('%d'))
        self.__version = 1.0
        Log('timelapser')

    def boot(self):
        Log.logger().info('timelapser by nortoh v{version}'.format(version=self.__version))

        self.delay = self.config.get_setting('delay')

        if (self.delay is None or self.delay < 0):
            Log.logger().error('Invalid delay')
            os._exit(1)

        Log.logger().info('Delay is set to {delay} seconds'.format(delay=self.delay))

        grammar = ('camera', 'cameras')[len(self.camera_configs) > 1]
        Log.logger().info('Collected {configs} {grammar}'.format(configs=len(self.camera_configs), grammar=grammar))

        for camera_config in self.camera_configs:
            camera = Camera(configuration=camera_config)

            datestamp = date.today().strftime('%Y-%m-%d')
            if not os.path.isdir('camera_data/{name}/images/{date}'.format(name=camera.name, date=datestamp)):
                os.makedirs('camera_data/{name}/images/{date}'.format(name=camera.name, date=datestamp))

        self.start()

    def start(self):
        try:
            while True:
                current_day = int(date.today().strftime('%d'))
                if current_day != self.boot_day:
                    self.boot_day = current_day
                    datestamp = date.today().strftime('%Y-%m-%d')

                    path = 'camera_data/{name}/images/{date}'.format(name=camera.name, date=datestamp)
                    if not os.path.isdir(path):
                        os.makedirs(path)

                    for camera_config in self.camera_configs:
                        camera = Camera(configuration=camera_config)
                        self.start_camera_thread(camera=camera, save=True)
                else:
                    for camera_config in self.camera_configs:
                        camera = Camera(configuration=camera_config)
                        self.start_camera_thread(camera=camera, save=True)

                sleep(int(self.config.get_setting('delay')))
        except KeyboardInterrupt as e:
            Log.logger().warning('STOPPING THREAD')

    def start_camera_thread(self, camera: Camera, save: bool):
        thread = CameraThread(camera=camera, save=save)
        thread.start()
        thread.open_connection()
        thread.join()

if __name__ == '__main__':
    app = Application()
    app.boot()
