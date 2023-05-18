"""
    audioaddict.play
    Functionality triggered if the user starts/plays a channel.
"""

import urllib.parse
import requests
import xbmcplugin

from audioaddict.api import AudioAddictApi
from audioaddict.channels import create_list_item
from audioaddict.exceptions import NoStreamingServerOnlineError


def play_stream(addon, settings):
    network_key = addon.args['network_key']
    channel_key = addon.args['channel_key']

    network = settings.get_network(network_key)

    listen_key = addon.getSetting('listen_key')
    quality_key = addon.getSetting('quality')
    stream_key = network.get_stream_key(quality_key)

    api = AudioAddictApi(network_key)
    playlist = api.playlist(stream_key, channel_key, listen_key)
    channel = api.channel_by_key(channel_key)

    channel_url = get_valid_channel_url(playlist)
    stream_url = "%s|User-Agent=%s&Referer=%s" % (channel_url,
                                                  settings.user_agent,
                                                  network.referer)

    list_item = create_list_item(channel)
    list_item.setPath(stream_url)

    xbmcplugin.setResolvedUrl(addon.handle, True, list_item)


def get_valid_channel_url(playlist):
    for channel_url in playlist:
        parsed_url = urllib.parse.urlparse(channel_url)
        if server_online(parsed_url.netloc):
            return channel_url

    raise NoStreamingServerOnlineError()


def server_online(domain):
    try:
        requests.head("http://%s" % domain)
    except requests.exceptions.ConnectionError:
        return False

    return True
