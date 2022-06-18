from curses import KEY_BTAB
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
        Log('timelapser')

    def boot(self):
        Log.logger().info('Booting timelapser by nortoh')

        self.delay = self.config.get_setting('delay')

        if (self.delay is None or self.delay < 0):
            Log.logger().error('Invalid delay')
            os._exit(1)

        Log.logger().info('Delay is set to {delay} seconds'.format(delay=self.delay))

        grammar = ('camera', 'cameras')[len(self.camera_configs) > 1]
        Log.logger().info(f'Collected {len(self.camera_configs)} {grammar}')

        for camera_config in self.camera_configs:
            camera = Camera(configuration=camera_config)

            if not os.path.isdir('camera_data/{name}/images'.format(name=camera.name)):
                os.makedirs('camera_data/{name}/images/'.format(name=camera.name))

        self.start()

    def start(self):
        try:
            while True:
                current_day = int(date.today().strftime('%d'))
                if current_day != self.boot_day:
                    self.boot_day = current_day
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