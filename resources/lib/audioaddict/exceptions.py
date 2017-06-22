class AudioAddictException(Exception):
    pass


class AudioAddictApiError(AudioAddictException):
    pass


class AuthenticationError(AudioAddictApiError):
    pass
