import requests
from audioaddict.exceptions import AuthenticationError


class AudioAddictApi(object):
    def __init__(self, network_key):
        self._base_url = "api.audioaddict.com/v1/%s" % network_key

    def authenticate(self, username, password):
        """
        authenticate with the current network and return the listen_key along
        with other network specific authentication information.
        """
        r = requests.post("https://%s/members/authenticate" % self._base_url,
                          params={'username': username, 'password': password})

        if r.status_code == 403:
            raise AuthenticationError("username and password do not match")
        else:
            r.raise_for_status()

        return r.json()

    def _get_channel_keys(self):
        """
        return channel keys from 'listen API', those are the supported channels
        """
        r = requests.get("http://%s/listen/channels" % self._base_url)
        r.raise_for_status()

        return [x['key'] for x in r.json()]

    def _get_channel_info(self):
        """
        return all channels with extended information, this list also includes
        discontinued channels
        """
        r = requests.get("http://%s/channels" % self._base_url)
        r.raise_for_status()

        return r.json()

    def channels(self):
        """
        return list of supported channels of this network with extended channel
        information
        """
        channel_keys = self._get_channel_keys()
        channel_info = self._get_channel_info()

        channels = [x for x in channel_info if x['key'] in channel_keys]
        return sorted(channels, key=lambda channel: channel['key'])

    def playlist(self, stream_key, channel_key, listen_key):
        """
        return channnel playlist
        """
        r = requests.get("http://%s/listen/%s/%s?listen_key=%s" %
                         (self._base_url, stream_key, channel_key, listen_key))
        r.raise_for_status()

        return r.json()
