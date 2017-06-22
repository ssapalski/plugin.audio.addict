import os
import xbmc

# Just in case we are running on python 2.6, simplejson will be faster
try:
    import simplejson as json
except ImportError:
    import json


def load_settings(settings_path):
    with open(settings_path, 'r') as f:
        return json.loads(f.read())


def get_settings_path(addon):
    kodi_path = addon.getAddonInfo('path')
    real_path = xbmc.translatePath(kodi_path).decode('utf-8')

    return os.path.join(real_path, 'resources', 'data', 'settings.json')


class Settings(object):
    def __init__(self, addon):
        settings_path = get_settings_path(addon)
        self._settings = load_settings(settings_path)
        self._networks = None

    @property
    def user_agent(self):
        return self._settings['stream_url']['user_agent']

    def get_network(self, network_key):
        return NetworkSettings(network_key,
                               self._settings['networks'][network_key])

    @property
    def networks(self):
        if not self._networks:
            self._networks = []
            for network_key in self._settings['network_order']:
                self._networks.append(self.get_network(network_key))

        return self._networks


class NetworkSettings(object):
    def __init__(self, key, network):
        self._network = network
        self.key = key

    @property
    def domain(self):
        return self._network['domain']

    @property
    def display_name(self):
        return self._network['display_name']

    @property
    def referer(self):
        return "http://www.%s/" % self.domain

    def get_stream_key(self, quality_key, premium=False):
        streams = self._network['streams']

        if premium:
            stream_key = streams['premium'][quality_key]
        else:
            stream_key = streams['public'][quality_key]

        return stream_key
