

class IllegalArgumentError(Exception):
    pass


class NotAFileError(Exception):
    pass


class IsAFileError(Exception):
    pass


__all__ = [
    'IsAFileError', 'NotAFileError', 'IllegalArgumentError'
]


