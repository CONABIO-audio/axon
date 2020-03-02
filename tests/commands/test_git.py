# -*- coding: utf-8 -*-
"""Test git commands."""
import tempfile
from uuid import uuid4
import os
from axon.commands import git_utils


def test_create_repository():
    """Check if can create a working repository."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = git_utils.create_repository(tmp_dir)

        assert '.git' in os.listdir(tmp_dir)
        assert not repo.is_dirty()


def test_add_all_files():
    """Check if all files are beign added to the repository."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = git_utils.create_repository(tmp_dir)

        random_files = [
            os.path.join(tmp_dir, str(uuid4())[:10] + '.txt')
            for _ in range(30)
        ]

        for filename in random_files:
            with open(filename, 'w') as tmpfile:
                tmpfile.write('garbage')

        basenames = [
            os.path.basename(filename) for filename in random_files
        ]

        assert set(repo.untracked_files) == set(basenames)
        git_utils.add_all_files_to_repository(repo)
        assert not repo.untracked_files
