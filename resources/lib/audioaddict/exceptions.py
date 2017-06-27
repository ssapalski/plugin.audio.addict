class AudioAddictException(Exception):
    pass


class AuthenticationError(AudioAddictException):
    pass


class EmptyCredentialsError(AudioAddictException):
    pass
