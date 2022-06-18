from os import path
import os
import json

class Config(object):

    settings = None

    def __init__(self):
        self.config_folder = './data'
        self.config_name = 'config.json'
        self.load_configuration()

    @staticmethod
    def get_setting(key):
        for k, v in Config.configuration.items():
            if key == k:
                return v
        return None

    def get_config_folder(self) -> str:
        return self.config_folder

    def get_config_name(self) -> str:
        return self.config_name

    def get_config_path(self) -> str:
        return path.join(self.get_config_folder(), self.get_config_name())

    # Load configuration 'config.json'
    def load_configuration(self):
        # Configuration name
        config_folder = self.get_config_folder()
        config_path = self.get_config_path()

        # Folder does not exist
        if not os.path.isdir(config_folder):
            os.mkdir(config_folder)

        # If config does not exist, make a blank one. Otherwise, open current
        if not path.exists(config_path):
            config_file = open(config_path, 'w')
            config_json_obj = json.loads(self.__get_default_config_blob())

            # prettify!
            formatted_json = json.dumps(config_json_obj, indent=2)
            config_file.write(formatted_json)
            config_file.close()

            print('config.json was generated in {path}'.format(path=config_path))
            os._exit(1)
        else:
            config_file = open(config_path, 'r')
            config_json_obj = json.load(config_file)

        self.config = self.__load(**config_json_obj)

    def __load(self, configuration):
        Config.configuration = configuration

    def __get_default_config_blob(self):
        return """
        {
            "configuration": {
                "delay": 10,
                "cameras": []
            }
        }
        """
