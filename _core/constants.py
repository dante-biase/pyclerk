from math import inf as _inf
from platform import system as _system

THIS_OPERATING_SYSTEM = _system()

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

UMIPS = ':NUL:'  # universal-machine-illegal-path-string


class ClassBehaviorBlocker:

	def __setattr__(self, key, value):
		return
