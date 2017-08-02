"""
    audioaddict.resources
    Functionality related to internal resources like settings, paths, ...
"""

import os
import xbmc

# Just in case we are running on python 2.6, simplejson will be faster
try:
    import simplejson as json
except ImportError:
    import json


def get_welcome_text(addon):
    data_path = get_data_path(addon)
    welcome_text_path = os.path.join(data_path, 'welcome.txt')

    with open(welcome_text_path, 'r') as f:
        return f.read()


def get_raw_settings(addon):
    data_path = get_data_path(addon)
    settings_path = os.path.join(data_path, 'settings.json')

    with open(settings_path, 'r') as f:
        return json.loads(f.read())


def get_data_path(addon):
    addon_path = get_addon_path(addon)
    data_path = os.path.join(addon_path, 'resources', 'data')

    return data_path


def get_addon_path(addon):
    return get_translated_kodi_path(addon, 'path')


def get_profile_path(addon):
    return get_translated_kodi_path(addon, 'profile')


def get_translated_kodi_path(addon, id_):
    kodi_path = addon.getAddonInfo(id_)
    real_path = xbmc.translatePath(kodi_path).decode('utf-8')

    return real_path
