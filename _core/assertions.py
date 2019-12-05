from os.path import isdir, isfile, exists
from pathlib import Path
from typing import NoReturn

from _core.exceptions import NotAFileError, IsAFileError, IllegalArgumentError
from _core.path import is_in_path


def assert_true(*tests: bool, else_raise: Exception, error_message: str):
    if any(test is False for test in tests):
        raise else_raise(error_message)


def assert_false(*tests: bool, else_raise: Exception, error_message: str):
    if any(test is False for test in tests):
        raise else_raise(error_message)


def assert_exists(path: str, error_message: str or None = None) -> NoReturn:
    if not exists(path):
        raise FileNotFoundError(error_message)


def assert_not_exists(path: str, error_message: str or None = None) -> NoReturn:
    if exists(path):
        raise FileExistsError(error_message)


def assert_is_dir(path: str, error_message: str or None = None) -> NoReturn:
    if not isdir(path):
        raise NotADirectoryError(error_message)


def assert_not_dir(path: str, error_message: str or None = None) -> NoReturn:
    if isdir(path):
        raise IsADirectoryError(error_message)


def assert_is_file(path: str, error_message: str or None = None) -> NoReturn:
    if not isfile(path):
        raise NotAFileError(error_message)


def assert_not_file(path: str, error_message: str or None = None) -> NoReturn:
    if isfile(path):
        raise IsAFileError(error_message)


def assert_has_ext(file_path: str, error_message: str or None = None) -> NoReturn:
    if Path(file_path).stem == '':
        raise IllegalArgumentError(error_message)


def assert_in_path(item_name: str, path: str or None = None, error_message: str or None = None) -> NoReturn:
    if not is_in_path(item_name, path):
        raise FileNotFoundError(error_message)


def assert_valid_arg(supplied_argument: str, possible_arguments: set, error_message: str or None = None) -> NoReturn:
    if supplied_argument not in possible_arguments:
        raise IllegalArgumentError(error_message)


__all__ = [
    'assert_exists', 'assert_false', 'assert_has_ext', 'assert_in_path', 'assert_is_dir', 'assert_is_file',
    'assert_not_dir', 'assert_not_exists', 'assert_not_file', 'assert_true', 'assert_valid_arg'

]