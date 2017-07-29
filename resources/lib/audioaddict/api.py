"""
    audioadditc.api
    Utility classes for accessing the AudioAddict API.
"""

import requests
from audioaddict.exceptions import AuthenticationError, \
                                   ListenKeyError


class AudioAddictApi(object):
    def __init__(self, network_key):
        self._base_url = "api.audioaddict.com/v1/%s" % network_key

    def authenticate(self, username, password):
        r = requests.post("https://%s/members/authenticate" % self._base_url,
                          params={'username': username, 'password': password})

        if r.status_code == 403:
            raise AuthenticationError("username and password do not match")
        else:
            r.raise_for_status()

        return User(r.json())

    def channels(self):
        r = requests.get("http://%s/channels" % self._base_url)
        r.raise_for_status()

        channels = _create_channel_list(r.json())

        return Channels(channels)

    def channel_by_id(self, id_):
        r = requests.get("http://%s/channels/%s" % (self._base_url, id_))
        r.raise_for_status()

        return Channel(r.json())

    def playlist(self, stream_key, channel_key, listen_key):
        r = requests.get("https://%s/listen/%s/%s?listen_key=%s" %
                         (self._base_url, stream_key, channel_key, listen_key))

        if r.status_code == 403:
            raise ListenKeyError("listen key is invalid")
        else:
            r.raise_for_status()

        return r.json()


class User(object):
    def __init__(self, parsed_json):
        self._user = parsed_json

    @property
    def listen_key(self):
        return self._user['listen_key']


class Channels(object):
    def __init__(self, channels):
        self._channels = channels

    def supported(self):
        return [x for x in self._channels if x.supported()]


class Channel(object):
    def __init__(self, parsed_json):
        self._channel = parsed_json

    def image_default(self):
        url = "http:%s" % self._channel['images']['default']
        url = url.split('{')[0]

        return url

    def supported(self):
        if self.name.startswith('X'):
            return False

        return True

    @property
    def key(self):
        return self._channel['key']

    @property
    def name(self):
        return self._channel['name']

    @property
    def id_(self):
        return self._channel['id']


def _create_channel_list(parsed_json):
    channels = []
    for channel in parsed_json:
        channels.append(Channel(channel))

    return channels
