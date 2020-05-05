# -*- coding: utf-8 -*-
"""Path module.

This module contains utilities for path handling within a project.
"""
import os
from typing import Iterable


def find_in_directory(
        path: str,
        name: str,
        subdirs: Iterable[str] = None) -> str:
    """
    Find module in directory.

    This function will try to match the name provided to a file contained in
    the directory at path. The name of the file can be specified in any of
    the following manners:

    1) Absolute path. This will return the relative path if the file exists and
    is contained within the directory.

    2) Path relative to the directory, such as ::

        subdir1/subdir2/module.py -> path/subdir1/subdir2/module.py

    3) Path relative to the directory in the module (dot) syntax, such as ::

        subdir1.subdir2.module -> path/subdir1/subdir2/module.py

    4) Path relative to a subdirectory that was provided in the subdirs
    argument, such as the following example where subdirs contains subdir1 ::

        subdir2/module.py -> path/subdir1/subdir2/module.py

    5) Path relative to a subdirectory that was provided in the subdirs
    argument, in the module (dot) syntax, such as  ::

        subdir2.module -> path/subdir1/subdir2/module.py

    When matching non absolute paths, the options 4) and 5)
    will have precedence to 2) and 3).

    Parameters
    ----------
    path: str
        Path of directory in which to conduct the search.
    name: str
        Name of module to search
    subdirs: Iterable[str], optional
        Subdirectories to use as base directories.

    Returns
    -------
    str
        The relative path of the first file the matched the name provided

    Raises
    ------
    ValueError
        When the name provided is an absolute path but is not contained
        in the directory at path.

    FileNotFoundError
        When no matching file was found in the directory or the subdirectories.
    """
    if subdirs is None:
        subdirs = []

    if os.path.isabs(name):
        return _handle_absolute_path(path, name)

    original_name = name

    # Remove python extension
    if name[-3:] == '.py':
        name = name[:-3]

    # Change dot syntax to path syntax
    name = name.replace('.', os.sep)

    # Add python extension
    name += '.py'

    for subdir in subdirs:
        potential_file = os.path.join(path, subdir, name)
        if os.path.exists(potential_file):
            return os.path.relpath(potential_file, start=path)

    potential_file = os.path.join(path, name)
    if os.path.exists(potential_file):
        return os.path.relpath(potential_file, start=path)

    message = (
        "The file with name {} couldn't be found within "
        "the directory {}".format(
            original_name,
            path
        ))
    raise FileNotFoundError(message)


def _handle_absolute_path(path: str, name: str) -> str:
    if path not in name:
        message = 'The given file is not inside the directory {}'
        message = message.format(path)
        raise ValueError(message)

    if not os.path.exists(name):
        message = 'The given file with absolute path {} does not exists'
        message = message.format(name)
        raise FileNotFoundError(message)

    return os.path.relpath(name, start=path)
