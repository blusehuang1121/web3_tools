import configparser

from libs.common import get_file_path
from libs.singleton import SingletonType

APIKEY_SECTION = 'ApiKey'
RPC_SECTION = 'RPCKey'


class GlobalConfig(metaclass=SingletonType):
    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(get_file_path('conf/configs'))

    def moralis_key(self):
        return self._config_parser.get(APIKEY_SECTION, 'moralis_key')

    def has_rpc_key(self, rpc_key):
        return self._config_parser.has_option(RPC_SECTION, rpc_key)

    def get_rpc(self, rpc_key):
        if not self._config_parser.has_option(RPC_SECTION, rpc_key):
            return ''
        return self._config_parser.get(RPC_SECTION, rpc_key)

    def get(self, section, key):
        return self._config_parser.get(section, key)
