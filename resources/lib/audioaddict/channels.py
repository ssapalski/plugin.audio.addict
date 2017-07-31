import xbmcgui
import xbmcplugin
from audioaddict.api import AudioAddictApi


def create_list_item(channel):
    image_url = channel.image_default()
    list_item = xbmcgui.ListItem(label=channel.name,
                                 thumbnailImage=image_url,
                                 iconImage=image_url)

    list_item.setProperty('isPlayable', 'true')

    return list_item


def get_channels(network):
    api = AudioAddictApi(network.key)
    channels = api.channels()

    return channels


def add_channels_to_kodi_directory(addon, settings):
    network = settings.get_network(addon.args['network_key'])
    channels = get_channels(network)

    supported_channels = sorted(channels.supported(), key=lambda x: x.key)
    for channel in supported_channels:
        url_parameters = {
            'mode': 'play_stream',
            'network_key': network.key,
            'channel_key': channel.key,
            'channel_id': channel.id_
        }

        stream_url = addon.createUrl(url_parameters)
        list_item = create_list_item(channel)

        xbmcplugin.addDirectoryItem(handle=addon.handle,
                                    url=stream_url,
                                    listitem=list_item,
                                    isFolder=False,
                                    totalItems=len(supported_channels))

    xbmcplugin.endOfDirectory(handle=addon.handle, succeeded=True)

def show_channels(addon, settings):
    add_channels_to_kodi_directory(addon, settings)
