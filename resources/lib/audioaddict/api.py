"""
    audioadditc.api
    Utility classes for accessing the AudioAddict API.
"""

import requests
from audioaddict.exceptions import AuthenticationError


class AudioAddictApi(object):
    """AudioAddict API.

    Args:
        network_key (str): The network to operate with

    """

    def __init__(self, network_key):
        self._base_url = "api.audioaddict.com/v1/%s" % network_key

    def authenticate(self, username, password):
        """Authenticate with the current network.

        Make an authentication request to retrieve user specific data which is
        needed for other API calls to work. Specifically this API will return
        the listen_key.

        Args:
            username (str): The username -> e-mail.
            password (str): The password.

        Returns:
            dict: Authentication data.

        Raises:
            audioaddict.exceptions.AuthenticationError:
                If authentication fails due to invalid credentials.

            requests.HTTPError: For any HTTP related error.

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
        """Return channels.

        Return a list of supported channels with extended channel information.

        Note:
            The result list is sorted ascending by channel_key.

        Raises:
            requests.HTTPError: For any HTTP related error.

        """
        channel_keys = self._get_channel_keys()
        channel_info = self._get_channel_info()

        channels = [x for x in channel_info if x['key'] in channel_keys]
        return sorted(channels, key=lambda channel: channel['key'])

    def playlist(self, stream_key, channel_key, listen_key):
        """Return channnel playlist.

        Return a playlist specific to a channel and stream quality.

        Args:
            stream_key (str): The stream_key specifying the quality.
            channel_key (str): The channel_key.
            listen_key (str): The listen_key.

        Returns:
            list: list of channels, each item is a dictionary.

        Raises:
            requests.HTTPError: For any HTTP related error.

        """
        r = requests.get("http://%s/listen/%s/%s?listen_key=%s" %
                         (self._base_url, stream_key, channel_key, listen_key))
        r.raise_for_status()

        return r.json()
