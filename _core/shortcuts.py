from pathlib import Path as _Path

from _core.constants import THIS_OPERATING_SYSTEM_NAME


class Shortcuts:
	HOME = str(_Path().home())
	if THIS_OPERATING_SYSTEM_NAME == 'Windows':
		# TODO:
		pass

	elif THIS_OPERATING_SYSTEM_NAME == 'Darwin':
		RECENTS = HOME + '/Recents'
		DESKTOP = HOME + '/Desktop'
		DOCUMENTS = HOME + '/Documents'
		DOWNLOADS = HOME + '/Downloads'
		APPLICATIONS = '/Applications'
		LIBRARY = '/Library'
		SYSTEM = '/System'
		USERS = '/Users'
		TRASH = HOME + '/.Trash'

	elif THIS_OPERATING_SYSTEM_NAME == 'Linux':
		# TODO:
		pass

	else:
		raise OSError()
