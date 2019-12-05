from pathlib import Path as _Path
from _core.constants import ClassBehaviorBlocker, OPERATING_SYSTEM


class Shortcuts:
	__metaclass__ = ClassBehaviorBlocker

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
