"""
    audioaddict.play
    Functionality triggered if the user starts/plays a channel.
"""

import xbmcplugin

from audioaddict.api import AudioAddictApi
from audioaddict.auth import get_listen_key, invalidate_listen_key
from audioaddict.channels import create_list_item
from audioaddict.exceptions import ListenKeyError

def get_stream_key(addon, network):
    premium = addon.getBooleanSetting('premium')

    if premium:
        quality_key = addon.getSetting('quality_premium')
    else:
        quality_key = addon.getSetting('quality_free')

    return network.get_stream_key(quality_key, premium)


def get_playlist(addon, network_key, stream_key, channel_key):
    api = AudioAddictApi(network_key)
    listen_key = get_listen_key(addon)

    try:
        playlist = api.playlist(stream_key, channel_key, listen_key)
    except ListenKeyError as e:
        if addon.getSetting('use_primary_auth'):
            invalidate_listen_key(addon)
            listen_key = get_listen_key(addon)
            playlist = api.playlist(stream_key, channel_key, listen_key)
        else:
            raise e

    return playlist


def play_stream(addon, settings):
    network_key = addon.args['network_key']
    channel_key = addon.args['channel_key']
    channel_id = addon.args['channel_id']

    network = settings.get_network(network_key)
    stream_key = get_stream_key(addon, network)
    playlist = get_playlist(addon, network_key, stream_key, channel_key)

    stream_url = "%s|User-Agent=%s&Referer=%s" % (playlist[0],
                                                  settings.user_agent,
                                                  network.referer)

    api = AudioAddictApi(network_key)
    channel = api.channel_by_id(channel_id)

    list_item = create_list_item(channel)
    list_item.setPath(stream_url)

    xbmcplugin.setResolvedUrl(addon.handle, True, list_item)
