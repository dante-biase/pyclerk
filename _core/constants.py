from math import inf as _inf
from platform import system as _system

OPERATING_SYSTEM = _system()

INF = _inf

VALID_MODES = {'o', 'a', 'x'}

VALID_UNITS = {'auto', 'by', 'kb', 'mb', 'gb', 'tb'}

UNIT_CONVERSION_MAP = {
		0: 'BY',
		1: 'KB',
		2: 'MB',
		3: 'GB',
		4: 'TB'
}

UNIT_CONVERSION_MAP_REVERSED = {v: k for k, v in UNIT_CONVERSION_MAP.items()}

CIPC = ':NUL:' # common illegal path code


class ClassBehaviorBlocker:

	def __setattr__(self, key, value):
		return
