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

        return r.json()

    def channels(self):
        r = requests.get("http://%s/channels" % self._base_url)
        r.raise_for_status()

        channels = []
        for channel in r.json():
            if not channel['name'].startswith('X'):
                channels.append(channel)

        return sorted(channels, key=lambda channel: channel['key'])

    def playlist(self, stream_key, channel_key, listen_key):
        r = requests.get("https://%s/listen/%s/%s?listen_key=%s" %
                         (self._base_url, stream_key, channel_key, listen_key))

        if r.status_code == 403:
            raise ListenKeyError("listen key is invalid")
        else:
            r.raise_for_status()

        return r.json()
