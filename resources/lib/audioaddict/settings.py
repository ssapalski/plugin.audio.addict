"""
    audioaddict.settings
    Functionality for internal settings.
"""

import json
import os

from resources.lib.audioaddict.resources import get_raw_settings

import xbmc


class Settings(object):

    def __init__(self, addon):
        self._settings = get_raw_settings(addon)

    @property
    def user_agent(self):
        return self._settings['http']['user_agent']

    def get_network(self, network_key):
        return NetworkSettings(network_key,
                               self._settings['networks'][network_key],
                               self._settings['quality'])

    @property
    def networks(self):
        networks = []
        for network_key in self._settings['networks']:
            networks.append(self.get_network(network_key))

        return sorted(networks, key=lambda x: x.sort_key)


class NetworkSettings(object):

    def __init__(self, key, network, quality):
        self._network = network
        self._quality = quality

        self.key = key

    @property
    def referer(self):
        return f'http://www.{self.domain}/'

    @property
    def domain(self):
        return self._network['domain']

    @property
    def display_name(self):
        return self._network['display_name']

    @property
    def sort_key(self):
        return self._network['sort_key']

    def get_stream_key(self, quality_key):
        return self._quality[quality_key]


def load_settings(settings_path):
    with open(settings_path, 'r') as f:
        return json.loads(f.read())


def get_settings_path(addon):
    kodi_path = addon.getAddonInfo('path')
    real_path = xbmc.translatePath(kodi_path)

    return os.path.join(real_path, 'resources', 'data', 'settings.json')
