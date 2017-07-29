import xbmcgui
import xbmcplugin
from audioaddict.api import AudioAddictApi


def build_list_item(channel):
    list_item = xbmcgui.ListItem(label=channel.name,
                                 thumbnailImage=channel.image_default())

    list_item.setProperty('isPlayable', 'true')

    return list_item


def get_channels(network):
    api = AudioAddictApi(network.key)
    channels = api.channels()

    return channels


def show_channels(addon, settings):
    network = settings.get_network(addon.args['network_key'])
    channels = get_channels(network)

    supported_channels = channels.supported()
    for channel in supported_channels:
        url_parameters = {
            'mode': 'play_stream',
            'network_key': network.key,
            'channel_key': channel.key
        }

        stream_url = addon.buildUrl(url_parameters)
        list_item = build_list_item(channel)

        xbmcplugin.addDirectoryItem(handle=addon.handle,
                                    url=stream_url,
                                    listitem=list_item,
                                    isFolder=False,
                                    totalItems=len(supported_channels))

    xbmcplugin.endOfDirectory(handle=addon.handle, succeeded=True)
