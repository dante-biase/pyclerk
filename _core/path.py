import functools
from os import path as os_path
from pathlib import Path as __Path
import re
from typing import List, Tuple

from .constants import FORBIDDEN_PATH_CHARS, UNIVERSAL_FORBIDDEN_PATH_CHAR


def cleanup(path_s: str or list) -> str or list:
	if type(path_s) == list:
		return [cleanup(path) for path in path_s]
	else:
		path = re.sub('//+', '/', path_s.strip())
		if path != '/': path = path.rstrip('/')
		return path


def reorient(path: str) -> str:
	return path.replace('\\', '/')


def cat(path1: str, path2: str, *paths: str) -> str:
	inputs = list(filter(None, [path1, path2, *paths]))
	return cleanup('/'.join(inputs))


def join(subpaths: List[str]) -> str:
	if not subpaths:
		return ''
	elif len(subpaths) == 1:
		return cleanup(subpaths[0])
	else:
		return cat(*tuple(subpaths))


def split(path: str) -> List[str]:
	path = cleanup(path)
	split_path = list(filter(None, path.split('/')))
	if is_absolute(path): split_path.insert(0, '/')
	return split_path


def bisect(path: str, at: int or str = -1) -> Tuple[str, str]:
	if type(at) == str: at = index(at, path)
	if at != -1: at += 1
	split_path = split(path)
	return join(split_path[:at]), join(split_path[at:])


def strip_root(path: str) -> str:
	path = path.replace(root(path), '', 1).lstrip('/')
	return cleanup(path)

def strip_trail(path: str) -> str:
	path = base(path)
	return base(path)


def strip_base(path: str) -> str:
	return trail(path)


def strip_ext(path: str) -> str:
	path = cleanup(path_s=path)
	return re.sub(f'{ext(path)}$', '', path)


def replace(subpath: str, with_path: str, in_path: str) -> str:
	if not is_in_path(subpath, in_path):
		raise Exception()
	else:
		subpath, with_path, in_path = cleanup([subpath, with_path, in_path])
		split_path = in_path.split(subpath, 1)
		split_path.insert(1, with_path)
		new_path = join(split_path)
		if with_path == '': new_path = new_path.lstrip('/')
		return new_path


def insert(subpath: str, at: int or str, in_path: str) -> str:
	if type(at) == str:
		return replace(subpath=at, with_path=cat(subpath, at), in_path=in_path)
	else:
		split_path = split(in_path)
		split_path.insert(at, subpath)
		return join(split_path)


def append(subpath: str, to_path: str) -> str:
	return cat(path1=to_path, path2=subpath)


def remove(subpath: str, from_path: str) -> str:
	return replace(subpath, '', from_path)


def pop(path: str, at: int = -1) -> str:
	return split(path).pop(at)


def ltrim(path: str, by: int = 1) -> str:
	if by < 0:
		raise Exception()
	elif by == 0:
		return path
	else:
		return bisect(path, by - 1)[1]


def rtrim(path: str, by: int = 1) -> str:
	if by < 0:
		raise Exception()
	elif by == 0:
		return path
	else:
		return bisect(path, -(by + 1))[0]


def root(path: str) -> str:
	if path == '':
		return ''
	else:
		path = cleanup(path)
		return '/' if path == '/' else path.split('/', 1)[0]


def trail(path: str) -> str:
	path = cleanup(path)
	return '/' if path == '/' else os_path.dirname(path)


def shared_trail(path1: str, path2: str, *paths: str) -> str:
	inputs = [cleanup(path) for path in [path1, path2, *paths] if path != '']
	return os_path.commonprefix(inputs)


def base(path: str) -> str or None:
	path = cleanup(path)
	return '/' if path == '/' else __Path(path).name


def basename(path: str) -> str:
	path = cleanup(path)
	return '/' if path == '/' else __Path(path).stem


def ext(of_file: str) -> str:
	path = cleanup(of_file)
	return __Path(path).suffix


def subpath(path: str, start: int or str or None = None, end: int or str or None = None) -> str:
	if type(start) == str: start = index(start, in_path=path)
	if type(end) == str: end = index(end, in_path=path)
	return join(
			split(path)[start:end]
	)


def shared_subpath(path1: str, path2: str, *paths: str) -> str or None:
	inputs = list(filter(None, cleanup([path1, path2, *paths])))
	whats_shared = os_path.commonpath(inputs)
	if whats_shared == '':
		return None
	else:
		return whats_shared


def depth(path: str) -> int:
	return len(split(path=path))


def index(of_item: str, in_path: str) -> int:
	try:
		return split(path=in_path).index(of_item)
	except ValueError:
		if is_subpath(path=of_item, path=in_path):
			raise ValueError("a path is not indexable by its subpath")
		else:
			raise ValueError(f"{of_item} not in {in_path}")


def hide(path: str) -> str:
	if path == '/':
		raise Exception()
	elif is_hidden(path):
		return path
	else:
		base_path = base(path=path)
		return cleanup(
				path.replace(base_path, '.' + base_path)
		)


def reveal(path: str) -> str:
	if not is_hidden(path):
		return path
	else:
		base_path = base(path=path)
		return cleanup(
				path.replace(base_path, base_path.lstrip('.'))
		)


def rename(path: str, to: str) -> str:
	return cat(trail(path=path), base(path=to))


def change_base(path: str, to: str) -> str:
	return cleanup(
			path.replace(base(path), to)
	)


def change_basename(path: str, to: str) -> str:
	return cleanup(
			path.replace(basename(path), to)
	)


def change_ext(of_file: str, new_ext: str) -> str:
	if not new_ext.startswith('.'): new_ext = '.' + new_ext
	return strip_ext(of_file) + new_ext


def increment_base(path: str) -> str:
	path_trail, path_base, base_ext = ('' if attribute is None else attribute for attribute in deconstruct(path))

	copy_pattern = r' \d+$'
	existing_copy_number = re.search(copy_pattern, path_base)
	if existing_copy_number:
		new_copy_number = ' ' + str(int(existing_copy_number.group(0)) + 1)
		new_base = re.sub(copy_pattern, new_copy_number, path_base)
	else:
		new_base = path_base + ' 1'

	return cat(path_trail, new_base + base_ext)


def deconstruct(path: str) -> Tuple[str, str, str]:
	return trail(path=path), basename(path=path), ext(of_file=path)


def is_legal(path: str) -> bool:
	path_is_legally_formatted = not any(has_ext(item) for item in split(trail(path=path)))
	path_contains_no_forbidden_characters = not any(char in path for char in FORBIDDEN_PATH_CHARS)
	return path_is_legally_formatted and path_contains_no_forbidden_characters


def is_absolute(path: str) -> bool:
	return path.strip().startswith('/')


def is_relative(path: str) -> bool:
	return not is_absolute(path)


def is_hidden(path: str) -> bool:
	return base(path=path).startswith('.')


def is_in_path(subpath: str, path: str) -> bool:
	test_path = cleanup(path).replace(subpath.rstrip('/'), UNIVERSAL_FORBIDDEN_PATH_CHAR, 1)
	return UNIVERSAL_FORBIDDEN_PATH_CHAR in split(test_path)


def is_subpath(path: str, path: str) -> bool:
	if _is_empty(path):
		return False
	else:
		path, path = cleanup([path, path])
		return re.match(f'^{path}', path) is not None


def has_ext(path: str) -> bool:
	return ext(path) is not None


def have_shared_trail(path1: str, path2: str, *paths: str) -> bool:
	return shared_trail(path1, path2, *paths) is not None


def have_shared_subpath(path1: str, path2: str, *paths: str) -> bool:
	return shared_subpath(path1, path2, *paths) is not None


def _is_empty(input_: str) -> bool:
	return input_.strip() == ''


__all__ = ['cleanup', 'reorient', 'cat', 'join', 'split', 'bisect', 'strip_root', 'strip_trail',
           'strip_base', 'strip_ext', 'replace', 'insert', 'append', 'remove', 'ltrim', 'rtrim', 'root', 'trail',
           'shared_trail', 'base',
           'basename', 'ext', 'subpath', 'shared_subpath', 'depth', 'index', 'hide', 'reveal', 'rename',
           'change_base', 'change_basename', 'change_ext', 'increment_base', 'deconstruct', 'is_legal', 'is_absolute',
           'is_relative', 'is_hidden', 'is_in_path', 'is_subpath', 'has_ext', 'have_shared_trail',
           'have_shared_subpath']
