from enum import Enum
from stat import (
	S_IRGRP, S_IROTH, S_IRUSR, S_IRWXG, S_IRWXO, S_IRWXU, S_IWGRP, S_IWOTH, S_IWUSR, S_IXGRP, S_IXOTH, S_IXUSR
)

from _core.constants import ClassBehaviorBlocker


class Party(Enum):
	USER = 0
	GROUP = 1
	OTHERS = 2
	ALL = 3

	@staticmethod
	def members():
		return [Party.USER, Party.GROUP, Party.OTHERS]


class Permission(Enum):
	MIXED = -1
	NO_ACCESS = 0
	READ_ONLY = 100
	READ_AND_WRITE = 110
	READ_AND_EXECUTE = 101
	WRITE_ONLY = 10
	WRITE_AND_EXECUTE = 101
	EXECUTE_ONLY = 1
	FULL_ACCESS = 111

	CODES = {

			NO_ACCESS   : {
					Party.USER : 0,
					Party.GROUP: 0,
					Party.OTHERS: 0,
					Party.ALL: 0
			},

			READ_ONLY: {
					Party.USER  : S_IRUSR,
					Party.GROUP : S_IRGRP,
					Party.OTHERS: S_IROTH,
					Party.ALL   : 0o444
			},

			WRITE_ONLY: {
					Party.USER  : S_IWUSR,
					Party.GROUP : S_IWGRP,
					Party.OTHERS: S_IWOTH,
					Party.ALL   : 0o222
			},

			READ_AND_WRITE: {
					Party.USER  : S_IRWXU,
					Party.GROUP : S_IRWXG,
					Party.OTHERS: S_IRWXO,
					Party.ALL   : 0o666
			},

			EXECUTE_ONLY: {
					Party.USER  : S_IXUSR,
					Party.GROUP : S_IXGRP,
					Party.OTHERS: S_IXOTH,
					Party.ALL   : 0o111
			}
	}


	MASKS = {
			Party.USER  : S_IRWXU,
			Party.GROUP : S_IRWXG,
			Party.OTHERS: S_IRWXO,
			Party.ALL   : -1
	}

	@staticmethod
	def match(read: bool = False, write: bool = False, execute: bool = False) -> 'Permission':
		permission = 0
		if read:
			permission += 100
		if write:
			permission += 10
		if execute:
			permission += 1

		return Permission(permission)


# def _generate_permission_label(can_read: bool, can_write: bool, can_execute: bool):
# 	perms = []
# 	if can_read:
# 		perms.append('Read')
# 	if can_write:
# 		perms.append('Write')
# 	if can_execute:
# 		perms.append('Execute')
#
# 	if len(perms) == 1:
# 		return f'{perms[0]} only'
# 	elif len(perms) == 2:
# 		return f'{perms[0]} & {perms[1]}'
# 	elif len(perms) == 3:
# 		return f'{perms[0]}, {perms[1]}, & {perms[2]}'
# 	else:
# 		return 'No access'


# Party.USER: {
# 		NO_ACCESS     : 0,
# 		READ_ONLY     : S_IRUSR,
# 		WRITE_ONLY    : S_IWUSR,
# 		READ_AND_WRITE: S_IRWXU,
# 		EXECUTE_ONLY  : S_IXUSR
#
# },
#
# Party.GROUP: {
# 		NO_ACCESS     : 0,
# 		READ_ONLY     : S_IRGRP,
# 		WRITE_ONLY    : S_IWGRP,
# 		READ_AND_WRITE: S_IRWXG,
# 		EXECUTE_ONLY  : S_IXGRP
# },
#
# Party.OTHERS: {
# 		NO_ACCESS     : 0,
# 		READ_ONLY     : S_IROTH,
# 		WRITE_ONLY    : S_IWOTH,
# 		READ_AND_WRITE: S_IRWXO,
# 		EXECUTE_ONLY  : S_IXOTH
# },
#
# Party.ALL: {
# 		NO_ACCESS     : 0,
# 		READ_ONLY     : 0o444,
# 		WRITE_ONLY    : 0o222,
# 		READ_AND_WRITE: 0o666,
# 		EXECUTE_ONLY  : 0o111
# }