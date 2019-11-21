from os.path import isdir, isfile, exists
from pathlib import Path

from core.exceptions import NotAFileError, IsAFileError, IllegalArgumentError
from core.path import is_in_path


def assert_true(*conditions, else_raise, msg):
    if any(condition is False for condition in conditions):
        raise else_raise(msg)


def assert_false(*conditions, else_raise, msg):
    if any(condition is False for condition in conditions):
        raise else_raise(msg)


def assert_exists(path: str, error_msg=None) -> None:
    if not exists(path):
        raise FileNotFoundError(error_msg)


def assert_not_exists(path: str, error_msg=None) -> None:
    if exists(path):
        raise FileExistsError(error_msg)


def assert_is_dir(path: str, error_msg=None) -> None:
    if not isdir(path):
        raise NotADirectoryError(error_msg)


def assert_not_dir(path: str, error_msg=None) -> None:
    if isdir(path):
        raise IsADirectoryError(error_msg)


def assert_is_file(path: str, error_msg=None) -> None:
    if not isfile(path):
        raise NotAFileError(error_msg)


def assert_not_file(path: str, error_msg=None) -> None:
    if isfile(path):
        raise IsAFileError(error_msg)


def assert_has_ext(file_path: str, error_msg=None) -> None:
    if Path(file_path).stem == '':
        raise IllegalArgumentError(error_msg)


def assert_in_path(item_name: str, path=None, error_msg=None) -> None:
    if not is_in_path(item_name, path):
        raise FileNotFoundError(error_msg)


def assert_valid_arg(supplied, possible_values: set, error_msg=None) -> None:
    if supplied not in possible_values:
        raise IllegalArgumentError(error_msg)


__all__ = [
    'assert_exists', 'assert_false', 'assert_has_ext', 'assert_in_path', 'assert_is_dir', 'assert_is_file',
    'assert_not_dir', 'assert_not_exists', 'assert_not_file', 'assert_true', 'assert_valid_arg'

]