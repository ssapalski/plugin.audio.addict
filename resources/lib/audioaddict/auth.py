"""
    audioaddict.auth
    Functionality for retrieving authentication relevant data.
"""

import os
import json

from audioaddict.api import AudioAddictApi
from audioaddict.resources import get_profile_path


class AuthenticationCache(object):
    """Responsible for caching authentication related data."""
    def __init__(self, profile_path):
        self._cache_path = os.path.join(profile_path, 'auth.json')
        self._raw_cache = {}

    def load(self):
        """Load cache from disk."""
        if not os.path.exists(self._cache_path):
            return {}

        with open(self._cache_path, 'r') as file_:
            self._raw_cache = json.loads(file_.read())

    def dump(self):
        """Dump cache to disk."""
        with open(self._cache_path, 'w') as file_:
            file_.write(json.dumps(self._raw_cache))

    @property
    def listen_key(self):
        """The listen key."""
        return self._raw_cache.get('listen_key')

    @listen_key.setter
    def listen_key(self, listen_key):
        self._raw_cache['listen_key'] = listen_key


def get_listen_key(addon):
    """Return the listen_key."""
    if not addon.getBooleanSetting('use_primary_auth'):
        return addon.getSetting('listen_key')

    cache = AuthenticationCache(get_profile_path(addon))
    cache.load()

    if not cache.listen_key:
        auth = authenticate(addon)

        cache.listen_key = auth['listen_key']
        cache.dump()

    return cache.listen_key


def invalidate_listen_key(addon):
    """Invalidate the listen key."""
    cache = AuthenticationCache(get_profile_path(addon))
    cache.load()

    cache.listen_key = None
    cache.dump()


def authenticate(addon):
    """Authenticate and return authentication data."""
    username = addon.getSetting('username')
    password = addon.getSetting('password')

    api = AudioAddictApi(addon.args['network_key'])

    return api.authenticate(username, password)


def credentials_empty(addon):
    """Check if credentials are empty."""
    if addon.getBooleanSetting('use_primary_auth'):
        username = addon.getSetting('username')
        password = addon.getSetting('password')

        if not username and not password:
            return True
    else:
        if not addon.getSetting('listen_key'):
            return True

    return False
