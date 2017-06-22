import xbmcgui
import xbmcplugin

from audioaddict.api import AudioAddictApi


def get_listen_key(addon, settings):
    username = addon.getSetting('username')
    password = addon.getSetting('password')
    network = settings.networks[0]

    api = AudioAddictApi(network.key)
    response = api.authenticate(username, password)

    return response['listen_key']


def show_networks(addon, settings):
    listen_key = get_listen_key(addon, settings)

    for network in settings.networks:
        if not addon.getBooleanSetting('activate_%s' % network.key):
            continue

        url_parameters = {
            'mode': 'open_network',
            'network_key': network.key,
            'listen_key': listen_key
        }

        list_item = xbmcgui.ListItem(label=network.display_name)
        url = addon.buildUrl(url_parameters)
        xbmcplugin.addDirectoryItem(handle=addon.handle,
                                    url=url,
                                    listitem=list_item,
                                    isFolder=True,
                                    totalItems=len(settings.networks))

    xbmcplugin.endOfDirectory(handle=addon.handle,
                              succeeded=True)
