"""
    audioaddict.exceptions
    Simple exceptions specific to this addon.
"""


class AudioAddictException(Exception):
    pass


class EmptyCredentialsError(AudioAddictException):
    pass


class NoNetworksSelectedError(AudioAddictException):
    pass


class NoStreamingServerOnlineError(AudioAddictException):
    pass


class ListenKeyError(AudioAddictException):
    pass
