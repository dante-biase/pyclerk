from os import path as os_path
from pathlib import Path as __Path
from re import search, sub
from typing import Tuple, List

from _core.exceptions import IllegalArgumentError
from .constants import UMIPS, THIS_OPERATING_SYSTEM


def cleanup(path: str) -> str:
	path = sub('//+', '/', path).replace(' ', '').strip()
	return path.rstrip("/") if has_ext(path) else path


def reorient(path: str) -> str:
	return path.replace('\\', '/')


def merge(path1: str, path2: str, *paths: str) -> str:
	return cleanup(_merge(path1, path2, *paths))


def _merge(path1: str, path2: str, *paths: str) -> str:
	merged = os_path.join(path1, path2)
	return merge(merged, *paths) if paths else merged


def cat(path1: str, path2: str, *paths: str) -> str:
	return cleanup('/'.join([path1, path2, *paths]))


def join(subpaths: List[str]) -> str:
	return cleanup(subpaths[0]) if len(subpaths) == 1 else cat(*tuple(subpaths))


def split(path: str) -> list:
	split_path = [item for item in cleanup(path).split('/') if item != '']
	return ['/'] + split_path if path.startswith('/') else split_path


def bisect(path: str, at_index: int or str = -1) -> tuple:
	if type(at_index) == str:
		at_index = index(at_index, path)

	dirs = split(path)
	return join(*dirs[:at_index]), join(*dirs[at_index:])


def strip_root(of_path: str) -> str:
	return of_path.replace(root(of_path), '', 1)


def strip_trail(of_path: str) -> str:
	return base(of_path)


def strip_base(of_path: str) -> str:
	return trail(of_path)


def strip_ext(of_path: str) -> str:
	return of_path.replace(ext(of_path), '')


def replace(subpath: str, with_path: str, in_path: str) -> str:
	split_path = in_path.split(subpath)
	split_path.insert(1, with_path)
	return join(split_path)


def insert(subpath: str, at_index: int or str, in_path: str) -> str:
	if type(at_index) == str:
		at_index == index(of_item=at_index, in_path=subpath)

	split_path = split(in_path)
	split_path.insert(at_index, subpath)
	return join(*split_path)


def append(subpath: str, to_path: str) -> str:
	return cat(path1=to_path, path2=subpath)


def remove(subpath: str, from_path: str) -> str:
	return replace(subpath, '', from_path)


def pop(path: str, at_index: int = -1) -> str:
	return split(path).pop(at_index)


def ltrim(path: str, by: int = 1) -> str:
	return bisect(path, by)[1]


def rtrim(path: str, by: int = 1) -> str:
	return bisect(path, -by)[0]


def root(of_path: str) -> str:
	if of_path.startswith('/'):
		return '/'
	else:
		return of_path.split('/', 1)[0]


def trail(of_path: str) -> str:
	return os_path.dirname(of_path)


def base(of_path: str) -> str:
	return __Path(of_path).name


def basename(of_path: str) -> str:
	return __Path(of_path).stem


def ext(of_file_path: str) -> str:
	file_ext = __Path(of_file_path).suffix
	return file_ext if file_ext != '' else None


def subpath(of_path: str, start: int or str or None = None, end: int or str or None = None) -> str:
	if start == end:
		return ''
	else:
		if type(start) == str:
			start = index(start, in_path=of_path)
		if type(end) == str:
			end = index(end, in_path=of_path)

		return join(split(of_path)[start:end])


def depth(of_path: str) -> int:
	return len(split(of_path))


def index(of_item: str, in_path: str) -> int:
	return split(in_path).index(of_item)


def hide(path: str) -> str:
	if is_hidden(path):
		return path

	path_base = base(path)
	hidden_path = path.replace(path_base, '.' + path_base)
	return hidden_path


def reveal(path: str) -> str:
	if not is_hidden(path):
		return path

	path_base = base(path)
	return path.replace(path_base, path_base.lstrip('.'))


def rename(path: str, to: str) -> str:
	path_trail = trail(path)
	return cat(path_trail, base(of_path=to))


def change_base(of_path: str, to: str) -> str:
	return of_path.replace(base(of_path), to)


def change_basename(of_path: str, to: str) -> str:
	if has_ext(to):
		raise IllegalArgumentError()

	return of_path.replace(basename(of_path), to)


def change_ext(of_file: str, new_ext: str) -> str:
	if not new_ext.startswith('.'):
		new_ext = '.' + new_ext

	if has_ext(of_file):
		return of_file.replace(ext(of_file), new_ext)
	else:
		return of_file + new_ext


def increment_base(path: str) -> str:
	path_trail, path_base, path_ext = deconstruct(path)
	copy_pattern = r' \d+$'
	previous_copy_number = search(copy_pattern, path_base)
	if previous_copy_number is not None:
		new_copy_number = ' ' + str(int(previous_copy_number.group(0)) + 1)
		new_base = sub(copy_pattern, new_copy_number, path_base)
	else:
		new_base = path_base + ' 1'

	return cat(path_trail, new_base + path_ext)


def deconstruct(path: str) -> Tuple[str, str, str]:
	return trail(path), basename(path), ext(path)


def is_legal(path):
	return not (
			any(has_ext(item) for item in path.split("/")[:-1]) and
			UMIPS not in path
	)


def is_hidden(path: str) -> bool:
	return base(path).startswith('.')


def is_in_path(item_name: str, path: str) -> bool:
	return any(item == item_name for item in split(path))


def is_subpath(path: str, of_path: str) -> bool:
	test_path = of_path.replace(path.strip('/'), UMIPS)
	return UMIPS in split(test_path)


def has_ext(path: str) -> bool:
	return ext(path) is not None


__all__ = ['cleanup', 'reorient', 'merge', 'cat', 'join', 'split', 'bisect', 'strip_root', 'strip_trail',
           'strip_base', 'strip_ext', 'replace', 'insert', 'append', 'remove', 'ltrim', 'rtrim', 'root', 'trail', 'base',
           'basename', 'ext', 'subpath', 'depth', 'index', 'hide', 'reveal', 'sub', 'rename',
           'change_base', 'change_basename', 'change_ext', 'increment_base', 'deconstruct', 'is_legal',
           'is_hidden', 'is_in_path', 'is_subpath', 'has_ext']
