from log import Log

class Camera(object):

    def __init__(self, configuration):
        self.__name = configuration['name']
        self.__rtsp = configuration['rtsp']

        if (self.__name is None or self.__rtsp is None):
            Log.logger().error('Missing camera data')

    @property
    def name(self):
        return self.__name

    @property
    def rtsp_url(self):
        return self.__rtsp

    @property
    def images_folder(self):
        return f'{self.camera_folder}/images'

    @property
    def camera_folder(self) -> str:
        return 'camera_data/{name}'.format(name=self.name)
