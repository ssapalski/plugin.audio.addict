import os
import xbmc


def get_addon_path(addon):
    kodi_path = addon.getAddonInfo('path')
    real_path = xbmc.translatePath(kodi_path).decode('utf-8')

    return real_path


def get_data_path(addon):
    addon_path = get_addon_path(addon)
    data_path = os.path.join(addon_path, 'resources', 'data')

    return data_path


def get_welcome_text(addon):
    data_path = get_data_path(addon)
    welcome_text_path = os.path.join(data_path, 'welcome.txt')

    with open(welcome_text_path, 'r') as f:
        return f.read()
