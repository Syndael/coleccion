import configparser
import os


class ConfigParser:
    _lector_config = None

    def get_value(self, key):
        return self._get_config_parser().get('config', key)

    def get_boolean_value(self, key):
        return self._get_config_parser().get('config', key) == '1'

    def _get_config_parser(self):
        if self._lector_config is None:
            self._lector_config = configparser.RawConfigParser()
            fichero_config = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.txt')
            self._lector_config.read(fichero_config)

        return self._lector_config

    def reloadConfigParser(self):
        self._lector_config = None
        return self._get_config_parser()
