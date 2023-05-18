"""
    audioaddict.addon
    Extension of xbmcaddon.Addon with useful attributes and methods.
"""

import urllib.request, urllib.parse, urllib.error
import xbmcaddon


class ExtendedAddon(xbmcaddon.Addon):
    def __new__(cls, *args, **kwargs):
        return super(ExtendedAddon, cls).__new__(cls)

    def __init__(self, url, handle, args):
        super(ExtendedAddon, self).__init__()

        self.url = url
        self.handle = handle
        self.args = args

    def createUrl(self, params):
        return self.url + '?' + urllib.parse.urlencode(params)

    def getBooleanSetting(self, id_):
        setting = super(ExtendedAddon, self).getSetting(id_)

        if setting == 'true':
            return True
        elif setting == 'false':
            return False
        else:
            raise ValueError("id=%s isn't a boolean setting")
