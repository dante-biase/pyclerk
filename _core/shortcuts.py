from pathlib import Path as _Path
from _core.constants import ClassBehaviorBlocker, THIS_OPERATING_SYSTEM


class Shortcuts:
	__metaclass__ = ClassBehaviorBlocker

	HOME = str(_Path().home())
	if THIS_OPERATING_SYSTEM == 'Windows':
		# TODO:
		pass

	elif THIS_OPERATING_SYSTEM == 'Darwin':
		RECENTS = HOME + '/Recents'
		DESKTOP = HOME + '/Desktop'
		DOCUMENTS = HOME + '/Documents'
		DOWNLOADS = HOME + '/Downloads'
		APPLICATIONS = '/Applications'
		LIBRARY = '/Library'
		SYSTEM = '/System'
		USERS = '/Users'
		TRASH = HOME + '/.Trash'

	elif THIS_OPERATING_SYSTEM == 'Linux':
		# TODO:
		pass

	else:
		raise OSError()
