from enum import Enum
from math import inf as _inf
from pathlib import Path as _Path
from platform import system as _system
from stat import (
    S_IRWXU, S_IRUSR, S_IWUSR, S_IXUSR, S_IRWXG, S_IRGRP,
    S_IWGRP, S_IXGRP, S_IRWXO, S_IROTH, S_IWOTH, S_IXOTH
)

OPERATING_SYSTEM = _system()

INF = _inf

VALID_MODES = {'o', 'a', 'x'}

VALID_UNITS = {'auto', 'b', 'kb', 'mb', 'gb', 'tb'}

UNIT_CONVERSION_MAP = {
    0: 'B',
    1: 'KB',
    2: 'MB',
    3: 'GB',
    4: 'TB'
}

UNIT_CONVERSION_MAP_REVERSED = {v: k for k, v in UNIT_CONVERSION_MAP.items()}

CIPC = ':NUL:'


class _UniMeta:

    def __setattr__(self, key, value):
        return


class Parties(Enum):
    __metaclass__ = _UniMeta

    USER = 0
    GROUP = 1
    OTHERS = 2
    ALL = 3

    @staticmethod
    def members():
        return [Parties.USER, Parties.GROUP, Parties.OTHERS]


class Permissions:
    __metaclass__ = _UniMeta

    NO_ACCESS = 'No access'
    READ_ONLY = 'Read only'
    WRITE_ONLY = 'Write only'
    READ_AND_WRITE = 'Read & Write'
    EXECUTE = 'Execute'
    MIXED = 'Mixed'


class Shortcuts:
    __metaclass__ = _UniMeta

    HOME = str(_Path().home())
    if OPERATING_SYSTEM == 'Windows':
        # TODO:
        pass

    elif OPERATING_SYSTEM == 'Darwin':
        RECENTS = HOME + '/Recents'
        DESKTOP = HOME + '/Desktop'
        DOCUMENTS = HOME + '/Documents'
        DOWNLOADS = HOME + '/Downloads'
        APPLICATIONS = '/Applications'
        LIBRARY = '/Library'
        SYSTEM = '/System'
        USERS = '/Users'
        TRASH = HOME + '/.Trash'

    elif OPERATING_SYSTEM == 'Linux':
        # TODO:
        pass

    else:
        raise OSError()


PERMISSION_MODES = {

    Parties.USER: {
        Permissions.NO_ACCESS: 0,
        Permissions.READ_ONLY: S_IRUSR,
        Permissions.WRITE_ONLY: S_IWUSR,
        Permissions.READ_AND_WRITE: S_IRWXU,
        Permissions.EXECUTE: S_IXUSR

    },

    Parties.GROUP: {
        Permissions.NO_ACCESS: 0,
        Permissions.READ_ONLY: S_IRGRP,
        Permissions.WRITE_ONLY: S_IWGRP,
        Permissions.READ_AND_WRITE: S_IRWXG,
        Permissions.EXECUTE: S_IXGRP
    },

    Parties.OTHERS: {
        Permissions.NO_ACCESS: 0,
        Permissions.READ_ONLY: S_IROTH,
        Permissions.WRITE_ONLY: S_IWOTH,
        Permissions.READ_AND_WRITE: S_IRWXO,
        Permissions.EXECUTE: S_IXOTH
    },

    Parties.ALL: {
        Permissions.NO_ACCESS: 0,
        Permissions.READ_ONLY: 0o444,
        Permissions.WRITE_ONLY: 0o222,
        Permissions.READ_AND_WRITE: 0o666,
        Permissions.EXECUTE: 0o111
    }

}

PERMISSION_MASKS = {
    Parties.USER: S_IRWXU,
    Parties.GROUP: S_IRWXG,
    Parties.OTHERS: S_IRWXO,
    Parties.ALL: -1
}