import os
import shutil
import stat
from difflib import SequenceMatcher
from grp import getgrall, getgrgid, getgrnam
from math import log
from os import path as os_path
from pathlib import Path
from pwd import getpwall, getpwnam, getpwuid
from subprocess import call
from subprocess import run as __run
from types import GeneratorType
from typing import NoReturn
from zipfile import ZipFile

from psutil import disk_partitions

from core import path as pc_path
from core.assertions import (assert_exists, assert_is_dir, assert_is_file, assert_not_exists, assert_valid_arg)
from core.constants import *
from core.exceptions import IllegalArgumentError
from core.parties_and_permissions import *
from core.shortcuts import *

_pathcrumbs = [os.getcwd()]


def run(command: str) -> str:
	return __run(command.split(' '), capture_output=True, text=True).stdout.rstrip('\n')


def get_os() -> str:
	return OPERATING_SYSTEM


def get_cwd() -> str:
	return os.getcwd()


def get_cpd() -> int:
	return pc_path.depth(get_cwd())


def go_to(dir_path: str) -> str:
	new_cwd = get_full_path(dir_path)
	if _pathcrumbs[-1] != new_cwd:
		_pathcrumbs.append(new_cwd)
		os.chdir(new_cwd)

	return new_cwd


def step_back(step: int = 1, to_dir: str = None) -> str:
	cwd = get_cwd()
	if to_dir:
		step = pc_path.depth(cwd) - (pc_path.index(to_dir, cwd) + 1)

	requested_path = pc_path.rtrim(cwd, by=step)
	return go_to(requested_path)


def go_back() -> str:
	if len(_pathcrumbs) > 1:
		_pathcrumbs.pop()
		pwd = _pathcrumbs[-1]
		os.chdir(pwd)
		return pwd

	else:
		return get_cwd()


def show(dir_path: str = '.') -> NoReturn:
	call('open {directory}'.format(directory=dir_path), shell=True)


def already_exists(item: str) -> bool:
	return os_path.lexists(item)


def is_file(item: str) -> bool:
	return os_path.isfile(item)


def is_dir(item: str) -> bool:
	return os_path.isdir(item)


def is_hidden(item: str) -> bool:
	assert_exists(item)
	return pc_path.is_hidden(item)


def is_alias(item: str) -> bool:
	# TODO:
	return False


def is_empty(dir_path: str = '.') -> bool:
	return not bool(get_contents(dir_path))


def has_ext(item: str) -> bool:
	assert_exists(item)
	return pc_path.has_ext(item)


def is_in_path(item: str) -> bool:
	return pc_path.is_in_path(item, os.getcwd())


def item_in_dir(item_name: str, dir_path: str = '.', check_subfolders: bool = False) -> bool:
	if check_subfolders:
		return bool(find(item_name, in_dir=dir_path))
	else:
		return item_name.lower() in [file.lower() for file in get_contents(of_dir=dir_path)]


def hide(item: str) -> str:
	hidden_path = pc_path.hide(item)
	return rename(item, to=hidden_path)


def reveal(item: str) -> str:
	revealed_path = pc_path.reveal(item)
	return rename(item, to=revealed_path)


def rename(item: str, to: str) -> str:
	assert_exists(item)
	new_path = pc_path.rename(item, to)
	assert_not_exists(new_path)
	Path(item).rename(new_path)
	return get_full_path(new_path)


def change_basename(of_item: str, to: str) -> str:
	new_basename = pc_path.change_basename(of_item, to)
	return rename(item=of_item, to=new_basename)


def change_ext(of_file: str, new_ext: str) -> str:
	assert_is_file(of_file)
	new_path = pc_path.change_ext(of_file, new_ext)
	return rename(item=of_file, to=new_path)


def get_full_path(of_item: str) -> str:
	assert_exists(of_item)
	return str(Path(of_item).resolve())


def get_root(of_path: str) -> str:
	assert_exists(of_path)
	return pc_path.root(of_path)


def get_trail(of_path: str) -> str:
	full_path = get_full_path(of_path)
	return pc_path.trail(full_path)


def get_base(of_path: str) -> str:
	assert_exists(of_path)
	return pc_path.base(of_path)


def get_basename(of_path: str) -> str:
	assert_exists(of_path)
	return pc_path.basename(of_path)


def get_ext(of_file: str) -> str:
	assert_exists(of_file)
	return pc_path.ext(of_file)


def get_kind(of_item: str) -> str:
	if is_dir(of_item):
		return 'directory'
	elif is_alias(of_item):
		return 'alias'
	else:
		return pc_path.ext(of_item)[1:]


def get_size(of_item: str = '.', unit: str = 'by', precision: int = 1) -> tuple:
	assert_exists(of_item)
	assert_valid_arg(unit, VALID_UNITS)

	item_full_path = get_full_path(of_item)
	item_trail = pc_path.trail(item_full_path)
	size_in_bytes, unit = os_path.getsize(of_item), unit.upper()
	if is_dir(item_full_path):
		for directory, contents in traverse_contents(item_full_path):
			dir_path = pc_path.merge(item_trail, directory)
			size_in_bytes += os_path.getsize(of_item)
			for file in contents:
				try:
					size_in_bytes += os_path.getsize(pc_path.merge(dir_path, file))

				except FileNotFoundError:
					pass

	if unit == 'AUTO':
		unit_factor = int(log(size_in_bytes) / log(1024))
		UNIT_CONVERSION_MAP.get(unit_factor, 4)

	converted_size = round(float(size_in_bytes / (1024 ** UNIT_CONVERSION_MAP_REVERSED.get(unit, 'TB'))), precision)

	return converted_size, unit


def new_dir(name: str, in_dir: str = '.', mode: str = 'x', hidden: bool = False) -> str:
	final_path = _preprocess(item=name, destination=in_dir, mode=mode, make_hidden=hidden)
	os.mkdir(final_path)
	return final_path


def new_dirs(names: iter, in_dir: str = '.', mode: str = 'x', hidden: bool = False) -> list:
	return [new_dir(name, in_dir, mode, hidden) for name in names]


def new_file(name: str, in_dir: str = '.', mode: str = 'x', hidden: bool = False) -> str:
	final_path = _preprocess(item=name, destination=in_dir, mode=mode, make_hidden=hidden)
	open(final_path, 'x').close()
	return final_path


def new_files(names: iter, in_dir: str = '.', mode: str = 'x', hidden: bool = False) -> list:
	return [new_file(name, in_dir, mode, hidden) for name in names]


def delete(item: str, *items: str, from_dir='.') -> NoReturn:
	for file in (item, *items):
		try:
			file = pc_path.merge(from_dir, file)
			if is_dir(file):
				shutil.rmtree(file, ignore_errors=True)
			else:
				Path(file).unlink()

			assert_not_exists(file)

		except FileExistsError:
			raise PermissionError()


def delete_contents(of_dir: str = '.') -> NoReturn:
	if is_empty(of_dir):
		return

	delete(*get_contents(of_dir))


def empty_trash() -> NoReturn:
	delete_contents(Shortcuts.TRASH)


def move(item: str, to_dir: str, mode: str = 'x') -> str:
	assert_exists(item)
	final_path = _preprocess(item, destination=to_dir, mode=mode)
	shutil.move(item, final_path)
	return final_path


def move_items(items: iter, to_dir: str, mode: str = 'x') -> list:
	return [move(file_item, to_dir, mode) for file_item in items]


def move_contents(of_dir: str, to_dir: str, mode: str = 'x') -> list:
	dir_contents = tuple([pc_path.merge(of_dir, item) for item in get_contents(of_dir)])
	return move_items(*dir_contents, to_dir=to_dir, mode=mode)


def move_to_trash(item: str, *items: str) -> NoReturn:
	move_items([item, *items], to_dir=Shortcuts.TRASH, mode='a')


def copy(item, to_dir: str, mode: str = 'x') -> str:
	assert_exists(item)
	final_path = _preprocess(item, destination=to_dir, mode=mode)
	if is_dir(item):
		shutil.copytree(item, final_path)
	else:
		shutil.copy2(item, final_path)

	return final_path


def copy_items(items: iter, to_dir: str, mode: str = 'x') -> list:
	return [copy(file_item, to_dir, mode) for file_item in items]


def copy_contents(of_dir: str, to_dir: str, mode: str = 'x') -> list:
	dir_contents = tuple([pc_path.merge(of_dir, item) for item in get_contents(of_dir)])
	return copy_items(*dir_contents, to_dir=to_dir, mode=mode)


def duplicate(item: str) -> str:
	return copy(item=item, to_dir='.', mode='a')


def duplicate_items(item: str, *items: str) -> list:
	return copy_items([item, *items], to_dir='.', mode='a')


def compress(item: str, *items: str, output_name: str = 'Archive') -> str:
	output_name = f'{output_name}.zip'
	with ZipFile(output_name, 'w') as zfile:
		for file in (item, *items):
			zfile.write(file)

	return get_full_path(output_name)


def extract(zip_file: str, to_dir: str = '.') -> NoReturn:
	with ZipFile(zip_file, 'r') as zfile:
		zfile.extractall(to_dir)


def get_contents(of_dir: str = '.', include_hidden: bool = True) -> list:
	contents = os.listdir(of_dir)
	if not include_hidden:
		contents = [item for item in contents if not pc_path.is_hidden(item)]

	return contents


def get_subdirs(of_dir: str = '.', include_hidden: bool = True) -> list:
	return list(filter(is_dir, get_contents(of_dir, include_hidden)))


def get_subfiles(of_dir: str = '.', include_hidden: bool = True) -> list:
	return list(filter(is_file, get_contents(of_dir, include_hidden)))


def get_all_contents(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
                     ignore_errors: bool = False) -> list:
	return list(traverse_contents(of_dir, include_hidden, skip_empty, max_depth, ignore_errors))


def get_all_subdirs(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
                    ignore_errors: bool = False) -> list:
	return list(traverse_subdirs(of_dir, include_hidden, skip_empty, max_depth, ignore_errors))


def get_all_files(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
                  ignore_errors: bool = False) -> list:
	return list(traverse_files(of_dir, include_hidden, skip_empty, max_depth, ignore_errors))


def get_devices(all_devices: bool = False) -> dict:
	devices = {}
	for device in disk_partitions(all_devices):
		data = device._asdict()

		# ----------- reformat data -----------
		device_path = data['device']
		data.pop('device')
		data['opts'] = data['opts'].split(',')
		# -------------------------------------

		devices.update({device_path: data})

	return devices


def get_volumes() -> list:
	return get_contents('/Volumes')


def traverse(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
             ignore_errors: bool = False) -> GeneratorType:
	return _generate_contents(of_dir, include_hidden, skip_empty, max_depth, ignore_errors)


def traverse_contents(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
                      ignore_errors: bool = False) -> GeneratorType:
	for directory, subdirs, files in _generate_contents(of_dir, include_hidden, skip_empty, max_depth, ignore_errors):
		yield directory, subdirs + files


def traverse_subdirs(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
                     ignore_errors: bool = False) -> GeneratorType:
	for directory, subdirs, files in _generate_contents(of_dir, include_hidden, skip_empty, max_depth, ignore_errors):
		yield directory, subdirs


def traverse_files(of_dir: str = '.', include_hidden: bool = True, skip_empty: bool = False, max_depth: int = INF,
                   ignore_errors: bool = False) -> GeneratorType:
	for directory, subdirs, files in _generate_contents(of_dir, include_hidden, skip_empty, max_depth, ignore_errors):
		yield directory, files


def search(for_name: str, in_dir: str = '.', max_depth: int = INF, similarity: float = 0.5) -> list:
	matches = []
	for directory, contents in traverse_contents(of_dir=in_dir, max_depth=max_depth, skip_empty=True):
		for item in contents:
			if SequenceMatcher(None, for_name, item).ratio() >= similarity:
				matches.append(
						(directory, item)
				)

	return matches


def find(item_name: str, in_dir: str = '.', max_depth: int = INF) -> str:
	item_name = item_name.lower()
	for directory, contents in traverse_contents(of_dir=in_dir, max_depth=max_depth, skip_empty=True):
		for item in contents:
			if item.lower() == item_name:
				return pc_path.cat(directory, item)


def find_all(items_with_name: str, in_dir: str = '.', max_depth: int = INF) -> list:
	matches = []
	items_with_name = items_with_name.lower()
	for directory, contents in traverse_contents(of_dir=in_dir, max_depth=max_depth, skip_empty=True):
		for item in contents:
			if item.lower() == items_with_name:
				matches.append(
						pc_path.cat(directory, item)
				)

	return matches


def check_perms(of_item: str, of_party: Parties = Parties.USER) -> str:
	if of_party == Parties.ALL:
		perms = list(check_all_perms(of_item).values())
		if all(perm == perms[0] for perm in perms):
			return perms[0]
		else:
			return Permissions.MIXED
	else:
		return _check_perms(of_party, for_item=of_item)


def check_all_perms(of_item: str) -> dict:
	perms = {}
	for party in Parties.members():
		perms[party.name] = _check_perms(of_party=party, for_item=of_item)
	return perms


def change_perms(of_item: str, to_perm: Permissions, for_party: Parties = Parties.USER,
                 recursively: bool = False) -> NoReturn:
	if to_perm == Permissions.MIXED:
		raise IllegalArgumentError()

	_change_perms(of_item, to_perm, for_party, recursively)


def check_owner(of_item: str):
	item_stat = os.stat(of_item).st_uid
	return getpwuid(item_stat).pw_name, getpwuid(item_stat).pw_uid


def change_owner(of_item: str, to_user: int or str = -1, to_group: int or str = -1) -> NoReturn:
	if not (to_user or to_group):
		raise IllegalArgumentError()
	elif type(to_user) == str:
		user_id = getpwnam(to_user).pw_uid
	elif type(to_group) == str:
		group_id = getpwuid(to_group).pw_name

	os.chown(of_item, user_id, group_id)


def get_user_name(from_user_id: int) -> str:
	return getpwuid(from_user_id).pw_name


def get_user_id(from_user_name: str) -> int:
	return getpwnam(from_user_name).pw_uid


def get_all_user_names() -> list:
	return _sort_accounts([user.pw_name for user in getpwall()])


def get_all_user_ids() -> list:
	return list(set([get_user_id(from_user_name=user_name) for user_name in get_all_user_names()]))


def get_all_users() -> list:
	return [(user_name, get_user_id(from_user_name=user_name)) for user_name in get_all_user_names()]


def get_memberships(of_user: str or int) -> list:
	if type(of_user) == int:
		of_user = get_user_name(of_user)

	return [group_name for group_name, members in get_groups_and_members().items() if of_user in members]


def get_group_name(from_group_id: int) -> str:
	return getgrgid(from_group_id).gr_name


def get_group_id(from_group_name: str) -> int:
	return getgrnam(from_group_name).gr_gid


def get_all_group_names() -> list:
	return _sort_accounts([group.gr_name for group in getgrall()])


def get_all_group_ids() -> list:
	return list(set([get_group_id(from_group_name=group_name) for group_name in get_all_group_names()]))


def get_all_groups() -> list:
	return [(group_name, get_group_id(from_group_name=group_name)) for group_name in get_all_group_names()]


def get_members(of_group: str or int) -> list:
	if type(of_group) == int:
		of_group = get_group_name(from_group_id=of_group)

	return getgrnam(of_group).gr_mem


def get_all_account_names() -> list:
	return _sort_accounts(get_all_user_names() + get_all_group_names())


def get_all_account_ids() -> list:
	return list(set(get_all_user_ids()) | set(get_all_group_ids()))


def get_all_accounts() -> list:
	return _sort_accounts(get_all_users() + get_all_groups())


def get_groups_and_members() -> dict:
	groups_and_members = {}
	for group_name in get_all_group_names():
		groups_and_members[group_name] = ', '.join(get_members(of_group=group_name))

	return groups_and_members


'''
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
'''


def _preprocess(item: str, destination: str, mode: str, make_hidden: bool = False) -> str:
	assert_valid_arg(mode, VALID_MODES)
	destination = str(Path(destination).resolve())
	item_base = pc_path.base(item)
	target_path = pc_path.merge(destination, item_base)

	if make_hidden:
		target_path = pc_path.hide(target_path)

	if already_exists(target_path):
		if mode == 'o':
			delete(item, from_dir=destination)
		elif mode == 'a':
			target_path = pc_path.increment_base(target_path)
			while already_exists(target_path):
				target_path = pc_path.increment_base(target_path)
		else:
			raise FileExistsError()

	return target_path


def _generate_contents(of_dir: str, include_hidden: bool, skip_empty: bool, max_depth: int or float,
                       ignore_errors: bool) -> GeneratorType:

	def _content_generator(_of_dir: str, _include_hidden: bool, _skip_empty: bool, _max_depth: int,
	                       _ignore_errors: bool) -> GeneratorType:
		dir_trail = pc_path.trail(_of_dir) + '/'

		for directory, subdirectories, files in os.walk(_of_dir):

			try:
				directory = pc_path.strip(dir_trail, directory)
				dir_depth = pc_path.depth(directory)
				if not dir_depth > _max_depth:
					# if not (include_hidden and pc_path.is_hidden(directory)):
					# 	subdirectories = [item for item in subdirectories if not pc_path.is_hidden(item)]
					# 	files = [item for item in files if not pc_path.is_hidden(item)]

					if not (_skip_empty and not (subdirectories or files)):
						yield directory, subdirectories, files

			except PermissionError:
				if not _ignore_errors:
					raise PermissionError()

	if of_dir == '.':
		of_dir = get_full_path(of_dir)
	else:
		assert_is_dir(of_dir)

	return _content_generator(
			_of_dir=of_dir,
			_include_hidden=include_hidden,
			_skip_empty=skip_empty,
			_max_depth=max_depth,
			_ignore_errors=ignore_errors
	)


def _check_perms(of_party: Parties, for_item: str) -> str:
	current_perms = stat.S_IMODE(os.stat(for_item).st_mode)
	party_perms = PERMISSION_MODES[of_party]
	can_read = bool(current_perms & party_perms[Permissions.READ_ONLY])
	can_write = bool(current_perms & party_perms[Permissions.WRITE_ONLY])
	# can_execute = bool(current_perms & party_perms[Permissions.EXECUTE])
	# TODO: add execute permissions to Permissions, implement logic below

	if can_read and can_write:
		return Permissions.READ_AND_WRITE
	elif can_read:
		return Permissions.READ_ONLY
	elif can_write:
		return Permissions.WRITE_ONLY
	else:
		return Permissions.NO_ACCESS


def _change_perms(of_item: str, to_perm: Permissions, for_party: Parties, recursively: bool) -> NoReturn:
	_change_item_perms(of_item, to_perm, for_party)

	if recursively and os_path.isdir(of_item):
		for directory, contents in os.walk(of_item):
			_change_item_perms(of_item=directory, to_perm=to_perm, for_party=for_party)
			for item in contents:
				_change_item_perms(of_item=pc_path.merge(directory, item), to_perm=to_perm, for_party=for_party)


def _change_item_perms(of_item: str, to_perm: Permissions, for_party: Parties) -> NoReturn:
	current_perms = stat.S_IMODE(os.stat(of_item).st_mode)
	party_mask = PERMISSION_BIT_MASKS[for_party]
	new_perm = PERMISSION_MODES[for_party][to_perm]
	os.chmod(of_item, (current_perms & ~party_mask) | new_perm)


def _sort_accounts(accounts: list) -> list:
	return sorted(set(accounts), key=lambda account: (account[0].startswith('_'), account))


__all__ = ['run', 'get_os', 'get_cwd', 'get_cpd', 'go_to', 'step_back', 'go_back', 'show',
           'already_exists',
           'is_file', 'is_dir', 'is_hidden', 'is_alias', 'is_empty', 'has_ext', 'is_in_path', 'item_in_dir', 'hide',
           'reveal', 'rename', 'change_basename', 'change_ext', 'get_full_path', 'get_root', 'get_trail', 'get_base',
           'get_basename', 'get_ext', 'get_kind', 'get_size', 'new_dir', 'new_dirs', 'new_file', 'new_files', 'delete',
           'delete_contents', 'empty_trash', 'move', 'move_items', 'move_contents', 'move_to_trash', 'copy',
           'copy_items', 'copy_contents', 'duplicate', 'duplicate_items', 'compress', 'extract', 'get_contents',
           'get_subdirs', 'get_subfiles', 'get_all_contents', 'get_all_subdirs', 'get_all_files', 'get_devices',
           'get_volumes', 'traverse', 'traverse_contents', 'traverse_subdirs', 'traverse_files', 'search', 'find',
           'find_all', 'check_perms', 'check_all_perms', 'change_perms', 'check_owner', 'change_owner', 'get_user_name',
           'get_user_id', 'get_all_user_names', 'get_all_user_ids', 'get_all_users', 'get_memberships',
           'get_group_name',
           'get_group_id', 'get_all_group_names', 'get_all_group_ids', 'get_all_groups', 'get_members',
           'get_all_account_names', 'get_all_account_ids', 'get_all_accounts', 'get_groups_and_members',

           'Parties', 'Permissions', 'Shortcuts'
           ]
