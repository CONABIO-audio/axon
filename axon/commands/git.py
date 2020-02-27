# -*- coding: utf-8 -*-
"""Git commands."""
import os
from git import Repo


def create_repository(path):
    """Create and return a new repository at the given path.

    Parameters
    ----------
    path: str
        Path at which to create a new git repository.

    Returns
    -------
    repository: Repo
        A git.Repo object representing the newly created repository.

    Raises
    ------
    ValueError
        If the path does not exist or the path is a git repository.
    """
    if not os.path.exists(path):
        message = 'Git repository creation failed, path does not exist: {}.'
        message = message.format(path)
        raise ValueError(message)

    git_path = os.path.join(path, '.git')
    if os.path.exists(git_path):
        message = 'A git repository has already been initialized at this path'
        raise ValueError(message)

    repository = Repo.init(git_path, bare=True)
    print(repository.is_dirty())
    print(repository.untracked_files)
    return repository
