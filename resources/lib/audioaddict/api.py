"""
    audioadditc.api
    Utility classes for accessing the AudioAddict API.
"""


import requests

from resources.lib.audioaddict.exceptions import ListenKeyError


class AudioAddictApi(object):

    def __init__(self, network_key):
        self._base_url = f'api.audioaddict.com/v1/{network_key}'

    def channels(self):
        r1 = requests.get(f'http://{self._base_url}/channels')
        r1.raise_for_status()

        r2 = requests.get(f'http://{self._base_url}/listen/channels')
        r2.raise_for_status()

        all_channels = r1.json()
        listen_channel_keys = [x['key'] for x in r2.json()]

        channels = []
        for channel in all_channels:
            if channel['key'] in listen_channel_keys:
                channels.append(Channel(channel))

        return channels

    def channel_by_key(self, key):
        r = requests.get(f'http://{self._base_url}/channels/key/{key}')
        r.raise_for_status()

        return Channel(r.json())

    def playlist(self, stream_key, channel_key, listen_key):
        r = requests.get(f'https://{self._base_url}/listen/{stream_key}/{channel_key}?listen_key={listen_key}')

        if r.status_code == 403:
            raise ListenKeyError()
        else:
            r.raise_for_status()

        return r.json()


class Channel(object):

    def __init__(self, parsed_json):
        self._channel = parsed_json

    def image_default(self):
        url = f'http:{self._channel["images"]["default"]}'
        url = url.split('{')[0]

        return url

    @property
    def key(self):
        return self._channel['key']

    @property
    def name(self):
        return self._channel['name']

    @property
    def creation_timestamp(self):
        return self._channel['created_at']
