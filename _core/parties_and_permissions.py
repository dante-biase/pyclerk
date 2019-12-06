from stat import (
	S_IRGRP, S_IROTH, S_IRUSR, S_IRWXG, S_IRWXO, S_IRWXU, S_IWGRP, S_IWOTH, S_IWUSR, S_IXGRP, S_IXOTH, S_IXUSR
)

from _core.constants import ClassBehaviorBlocker


class Parties:
	__metaclass__ = ClassBehaviorBlocker

	USER = 0
	GROUP = 1
	OTHERS = 2
	ALL = 3

	@staticmethod
	def members():
		return [Parties.USER, Parties.GROUP, Parties.OTHERS]


class Permissions:
	__metaclass__ = ClassBehaviorBlocker

	NO_ACCESS = 'No access'
	READ_ONLY = 'Read only'
	WRITE_ONLY = 'Write only'
	READ_AND_WRITE = 'Read & Write'
	EXECUTE = 'Execute'
	MIXED = 'Mixed'


PERMISSION_MODES = {

		Parties.USER  : {
				Permissions.NO_ACCESS     : 0,
				Permissions.READ_ONLY     : S_IRUSR,
				Permissions.WRITE_ONLY    : S_IWUSR,
				Permissions.READ_AND_WRITE: S_IRWXU,
				Permissions.EXECUTE       : S_IXUSR

		},

		Parties.GROUP : {
				Permissions.NO_ACCESS     : 0,
				Permissions.READ_ONLY     : S_IRGRP,
				Permissions.WRITE_ONLY    : S_IWGRP,
				Permissions.READ_AND_WRITE: S_IRWXG,
				Permissions.EXECUTE       : S_IXGRP
		},

		Parties.OTHERS: {
				Permissions.NO_ACCESS     : 0,
				Permissions.READ_ONLY     : S_IROTH,
				Permissions.WRITE_ONLY    : S_IWOTH,
				Permissions.READ_AND_WRITE: S_IRWXO,
				Permissions.EXECUTE       : S_IXOTH
		},

		Parties.ALL   : {
				Permissions.NO_ACCESS     : 0,
				Permissions.READ_ONLY     : 0o444,
				Permissions.WRITE_ONLY    : 0o222,
				Permissions.READ_AND_WRITE: 0o666,
				Permissions.EXECUTE       : 0o111
		}

}

PERMISSION_BIT_MASKS = {
		Parties.USER  : S_IRWXU,
		Parties.GROUP : S_IRWXG,
		Parties.OTHERS: S_IRWXO,
		Parties.ALL   : -1
}
