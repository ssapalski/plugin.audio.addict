"""
    audioaddict.main
    The main entrance point of the addon.
"""

import xbmcgui

from audioaddict.exceptions import AuthenticationError, \
                                   EmptyCredentialsError, \
                                   NoNetworksSelectedError, \
                                   ListenKeyError

from audioaddict.resources import get_welcome_text
from audioaddict.settings import Settings
from audioaddict.networks import show_networks
from audioaddict.channels import show_channels
from audioaddict.addon import ExtendedAddon
from audioaddict.auth import credentials_empty
from audioaddict.play import play_stream
from audioaddict.gui import TextViewer


def run_addon(addon_url, addon_handle, addon_args):
    try:
        addon = ExtendedAddon(addon_url, addon_handle, addon_args)
        settings = Settings(addon)

        main(addon, settings)
    except EmptyCredentialsError as e:
        dialog = TextViewer(header='Welcome!', text=get_welcome_text(addon))
        dialog.doModal()
    except (AuthenticationError, NoNetworksSelectedError, ListenKeyError) as e:
        dialog = xbmcgui.Dialog()
        dialog.ok('Error', e.message)
        addon.openSettings()


def main(addon, settings):
    set_addon_defaults(addon)

    if credentials_empty(addon):
        raise EmptyCredentialsError()

    if not addon.args:
        show_networks(addon, settings)
    elif addon.args.get('mode') == 'open_network':
        show_channels(addon, settings)
    elif addon.args.get('mode') == 'play_stream':
        play_stream(addon, settings)


def set_addon_defaults(addon):
    if not addon.getSetting('quality_free'):
        addon.setSetting('quality_free', 'moderate')

    if not addon.getSetting('quality_premium'):
        addon.setSetting('quality_premium', 'high')
