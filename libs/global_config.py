import configparser
import os
import random

from libs.common import get_file_path
from libs.singleton import SingletonType

APIKEY_SECTION = 'ApiKey'
RPC_SECTION = 'RPCKey'


class GlobalConfig(metaclass=SingletonType):
    _proxy_list = []
    _proxy_index = -1
    _use_proxy = False

    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(get_file_path('conf/configs'))
        self.read_proxy_list()

    def read_proxy_list(self):
        self._proxy_list.clear()
        file_path = 'conf/proxies'
        if not os.path.exists(file_path):
            return
        pf = open(file_path)
        lines = pf.readlines(1000)
        for line in lines:
            if len(line) < 12:
                continue
            splits = line.strip().split(':')
            if len(splits) > 2:
                proxy = f"http://{splits[2]}:{splits[3]}@{splits[0]}:{splits[1]}"
            else:
                proxy = f"http://{splits[0]}:{splits[1]}"
            self._proxy_list.append(proxy)
        self.random_proxy()

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

    def random_proxy(self):
        self._proxy_index = random.randrange(-1, len(self._proxy_list))

    def get_a_proxy(self):
        if self._use_proxy is False or self._proxy_index < 0 or len(self._proxy_list) <= 0:
            return None
        return self._proxy_list[self._proxy_index]

    def use_proxy(self):
        self._use_proxy = True

    def is_use_proxy(self):
        return self._use_proxy
