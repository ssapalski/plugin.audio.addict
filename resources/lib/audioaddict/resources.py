import os
import xbmc


def get_welcome_path(addon):
    kodi_path = addon.getAddonInfo('path')
    real_path = xbmc.translatePath(kodi_path).decode('utf-8')

    return os.path.join(real_path, 'resources', 'data', 'welcome.txt')


def get_welcome_text(addon):
    welcome_path = get_welcome_path(addon)

    with open(welcome_path, 'r') as f:
        return f.read()
