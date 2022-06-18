from log import Log
from datetime import datetime, date

class Camera(object):

    def __init__(self, configuration):
        self._name = configuration['name']
        self._rtsp = configuration['rtsp']
        self.cleanup_cycles = 0

        if (self._name is None or self._rtsp is None):
            Log.logger().error('Missing camera data')

    @property
    def name(self):
        return self._name

    @property
    def rtsp_url(self):
        return self._rtsp

    @property
    def images_folder(self):
        return f'{self.camera_folder}/images'

    @property
    def camera_folder(self) -> str:
        return 'camera_data/{name}'.format(name=self.name)

    @property
    def timestamp(self) -> int:
        return int(datetime.now().timestamp())

    @property
    def datestamp(self) -> str:
        return date.today().strftime('%Y-%m-%d')

    def reset_cycles(self):
        self.cleanup_cycles = 0
