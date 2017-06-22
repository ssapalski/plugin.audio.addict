import xbmcgui
import xbmcplugin
from audioaddict.api import AudioAddictApi


def build_icon_url(channel):
    icon_url = "http:%s" % channel['images']['default']
    icon_url = icon_url.split('{')[0]

    return icon_url


def build_list_item(channel):
    icon_url = build_icon_url(channel)
    list_item = xbmcgui.ListItem(label=channel['name'],
                                 thumbnailImage=icon_url)

    list_item.setProperty('isPlayable', 'true')

    return list_item


def get_channels(network):
    api = AudioAddictApi(network.key)
    channels = api.channels()

    return channels


def show_channels(addon, settings):
    network = settings.get_network(addon.args['network_key'])
    channels = get_channels(network)

    for channel in channels:
        url_parameters = {
            'mode': 'play_stream',
            'network_key': network.key,
            'channel_key': channel['key'],
            'listen_key': addon.args['listen_key']
        }

        stream_url = addon.buildUrl(url_parameters)
        list_item = build_list_item(channel)

        xbmcplugin.addDirectoryItem(handle=addon.handle,
                                    url=stream_url,
                                    listitem=list_item,
                                    isFolder=False,
                                    totalItems=len(channels))

    xbmcplugin.endOfDirectory(handle=addon.handle, succeeded=True)
