from math import inf as _inf
from platform import system as _system

THIS_OPERATING_SYSTEM_NAME = _system()

INF = _inf

VALID_MODES = {'o', 'a', 'x'}

VALID_UNITS = {'auto', 'by', 'kb', 'mb', 'gb', 'tb'}

UNIT_CONVERSION_MAP = {
		0: 'by',
		1: 'kb',
		2: 'mb',
		3: 'gb',
		4: 'tb'
}

UNIT_CONVERSION_MAP_REVERSED = {v: k for k, v in UNIT_CONVERSION_MAP.items()}

if THIS_OPERATING_SYSTEM_NAME == 'Windows':
	FORBIDDEN_PATH_CHARS = {'/', ':', '*', '?', "\"", '<', '>', '|'}
elif THIS_OPERATING_SYSTEM_NAME == 'Darwin':
	FORBIDDEN_PATH_CHARS = {':'}
elif THIS_OPERATING_SYSTEM_NAME == 'Unix':
	# TODO:
	pass
else:
	# TODO:
	pass


UNIVERSAL_FORBIDDEN_PATH_CHAR = ':'


class ClassBehaviorBlocker:

	def __setattr__(self, key, value):
		raise AttributeError()
