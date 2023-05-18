"""
    audioaddict.channels
    Functionality centered around channel presentation in Kodi.
"""

import xbmcgui
import xbmcplugin
from audioaddict.api import AudioAddictApi


def show_channels(addon, settings):
    add_channel_sort_methods(addon)
    add_channels_to_kodi_directory(addon, settings)


def add_channel_sort_methods(addon):
    sort_methods = [
        xbmcplugin.SORT_METHOD_LABEL,
        xbmcplugin.SORT_METHOD_DATEADDED,
    ]

    for sort_method in sort_methods:
        xbmcplugin.addSortMethod(addon.handle, sort_method)


def add_channels_to_kodi_directory(addon, settings):
    network = settings.get_network(addon.args['network_key'])
    channels = get_channels(network)

    for channel in channels:
        url_parameters = {
            'mode': 'play_stream',
            'network_key': network.key,
            'channel_key': channel.key
        }

        stream_url = addon.createUrl(url_parameters)
        list_item = create_list_item(channel)

        xbmcplugin.addDirectoryItem(handle=addon.handle,
                                    url=stream_url,
                                    listitem=list_item,
                                    isFolder=False,
                                    totalItems=len(channels))

    xbmcplugin.endOfDirectory(handle=addon.handle, succeeded=True)


def get_channels(network):
    api = AudioAddictApi(network.key)
    channels = api.channels()

    return channels


def create_list_item(channel):
    image_url = channel.image_default()
    list_item = xbmcgui.ListItem(label=channel.name)
    list_item.setArt ({"thumb":image_url})
    date, time = channel.creation_timestamp.split('T')
    timestamp = "%s %s" % (date, time.split('-')[0])

    list_item.setProperty('isPlayable', 'true')
    list_item.setInfo('video', {'dateadded': timestamp})

    return list_item
