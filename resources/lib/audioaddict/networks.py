"""
    audioaddict.networks
    Functionality centered around networks presentation in Kodi.
"""

import xbmcgui
import xbmcplugin

from audioaddict.exceptions import NoNetworksSelectedError


def show_networks(addon, settings):
    if num_activated_networks(addon, settings) == 0:
        message = "You have to select at least one network"
        raise NoNetworksSelectedError(message)

    for network in settings.networks:
        if not addon.getBooleanSetting('activate_%s' % network.key):
            continue

        url_parameters = {
            'mode': 'open_network',
            'network_key': network.key
        }

        list_item = xbmcgui.ListItem(label=network.display_name)
        url = addon.createUrl(url_parameters)
        xbmcplugin.addDirectoryItem(handle=addon.handle,
                                    url=url,
                                    listitem=list_item,
                                    isFolder=True,
                                    totalItems=len(settings.networks))

    xbmcplugin.endOfDirectory(handle=addon.handle,
                              succeeded=True)


def num_activated_networks(addon, settings):
    count = 0
    for network in settings.networks:
        if addon.getBooleanSetting('activate_%s' % network.key):
            count += 1

    return count
