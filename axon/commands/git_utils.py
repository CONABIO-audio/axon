# -*- coding: utf-8 -*-
"""Git commands."""
import os
from typing import Iterable
from git import Repo


def create_repository(path: str) -> Repo:
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

    repository = Repo.init(path, mkdir=True)
    return repository


def get_repository(path: str) -> Repo:
    """Return GitPython repository object."""
    return Repo(path)


def add_all_files_to_repository(repo: Repo, commit_message: str = ''):
    """
    Add all changed files to the current repository.

    Warning: Should not be used often since this adds files without
    the user having full awareness of this.
    """
    repo.index.add(['*', '.*'])

    if commit_message == '':
        commit_message = 'Axon add all files'
    repo.index.commit(commit_message)


def git_add_and_commit(repo: Repo, files: Iterable[str], commit_message: str):
    """Add files to repository and commit."""
    repo.index.add(files)
    repo.index.commit(commit_message)
