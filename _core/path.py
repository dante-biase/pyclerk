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
	return cleanup(
			path_s='/'.join(inputs)
	)


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


def strip_root(of_path: str) -> str:
	return cleanup(
			path_s=of_path.replace(root(of_path), '', 1).lstrip('/')
	)


def strip_trail(of_path: str) -> str:
	return cleanup(
			path_s=of_path.replace(trail(of_path), '', 1)
	).lstrip('/')


def strip_base(of_path: str) -> str:
	return cleanup(
			path_s=of_path.replace(base(of_path), '', 1)
	)


def strip_ext(of_path: str) -> str:
	of_path = cleanup(path_s=of_path)
	ext_of_path = ext(of_path)
	if ext_of_path is None:
		return of_path
	else:
		return of_path.replace(ext_of_path, '')


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


def root(of_path: str) -> str or None:
	if of_path == '':
		return None
	else:
		of_path = cleanup(of_path)
		if is_absolute(of_path):
			return '/'
		else:
			return of_path.split('/', 1)[0]


def trail(of_path: str) -> str or None:
	if of_path == '':
		return None
	else:
		of_path = cleanup(of_path)
		return '/' if of_path == '/' else os_path.dirname(of_path)


def shared_trail(path1: str, path2: str, *paths: str) -> str or None:
	inputs = [cleanup(path) for path in [path1, path2, *paths] if path != '']
	whats_shared = os_path.commonprefix(inputs)
	if whats_shared == '':
		return None
	else:
		return whats_shared


def base(of_path: str) -> str or None:
	if _is_empty(of_path):
		return None
	else:
		of_path = cleanup(of_path)
		return '/' if of_path == '/' else __Path(of_path).name


def basename(of_path: str) -> str or None:
	if _is_empty(of_path):
		return None
	else:
		of_path = cleanup(of_path)
		return '/' if of_path == '/' else __Path(of_path).stem


def ext(of_file: str) -> str or None:
	if _is_empty(of_file):
		return None
	else:
		file_ext = __Path(cleanup(of_file)).suffix
		if not file_ext: file_ext = None
		return file_ext


def subpath(of_path: str, start: int or str or None = None, end: int or str or None = None) -> str:
	if type(start) == str: start = index(start, in_path=of_path)
	if type(end) == str: end = index(end, in_path=of_path)
	return join(
			split(of_path)[start:end]
	)


def shared_subpath(path1: str, path2: str, *paths: str) -> str or None:
	inputs = list(filter(None, cleanup([path1, path2, *paths])))
	whats_shared = os_path.commonpath(inputs)
	if whats_shared == '':
		return None
	else:
		return whats_shared


def depth(of_path: str) -> int:
	return len(split(path=of_path))


def index(of_item: str, in_path: str) -> int:
	try:
		return split(path=in_path).index(of_item)
	except ValueError:
		if is_subpath(path=of_item, of_path=in_path):
			raise ValueError("a path is not indexable by its subpath")
		else:
			raise ValueError(f"{of_item} not in {in_path}")


def hide(path: str) -> str:
	if path == '/':
		raise Exception()
	elif is_hidden(path):
		return path
	else:
		base_of_path = base(of_path=path)
		return cleanup(
				path.replace(base_of_path, '.' + base_of_path)
		)


def reveal(path: str) -> str:
	if not is_hidden(path):
		return path
	else:
		base_of_path = base(of_path=path)
		return cleanup(
				path.replace(base_of_path, base_of_path.lstrip('.'))
		)


def rename(path: str, to: str) -> str:
	return cat(trail(of_path=path), base(of_path=to))


def change_base(of_path: str, to: str) -> str:
	return cleanup(
			of_path.replace(base(of_path), to)
	)


def change_basename(of_path: str, to: str) -> str:
	return cleanup(
			of_path.replace(basename(of_path), to)
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
	return trail(of_path=path), basename(of_path=path), ext(of_file=path)


def is_legal(path: str) -> bool:
	path_is_legally_formatted = not any(has_ext(item) for item in split(trail(of_path=path)))
	path_contains_no_forbidden_characters = not any(char in path for char in FORBIDDEN_PATH_CHARS)
	return True if path_is_legally_formatted and path_contains_no_forbidden_characters else False


def is_absolute(path: str) -> bool:
	return path.strip().startswith('/')


def is_relative(path: str) -> bool:
	return not is_absolute(path)


def is_hidden(path: str) -> bool:
	return base(of_path=path).startswith('.')


def is_in_path(subpath: str, path: str) -> bool:
	test_path = cleanup(path).replace(subpath.rstrip('/'), UNIVERSAL_FORBIDDEN_PATH_CHAR, 1)
	return UNIVERSAL_FORBIDDEN_PATH_CHAR in split(test_path)


def is_subpath(path: str, of_path: str) -> bool:
	if _is_empty(path):
		return False
	else:
		path, of_path = cleanup([path, of_path])
		return re.match(f'^{path}', of_path) is not None


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
