# -*- coding: utf-8 -*-
"""Test git commands."""
import tempfile
from uuid import uuid4
import os
from axon.commands import git_utils
from axon.commands.projects import create_basic_files


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


SAMPLE_PYTHON_FILE = '''# -*- coding: utf-8 -*-
"""Has module docstring."""
import os


def main():
    """Execute the main functionality of this module."""
    print(os.listdir('.'))


if __name__ == '__main__':
    main()
'''


def test_install_precommit_hooks():
    """Check if the hooks were properly installed."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = git_utils.create_repository(tmp_dir)

        assert not repo.untracked_files
        create_basic_files(tmp_dir)
        assert len(repo.untracked_files) == 9

        git_utils.add_all_files_to_repository(repo)
        assert not repo.untracked_files

        git_utils.install_precommit_hooks(repo)

        git_dir = os.path.join(tmp_dir, '.git')
        pre_commit_hooks = os.path.join(
            git_dir,
            'hooks',
            'pre-commit')

        with open(pre_commit_hooks, 'r') as precommitfile:
            hooks = precommitfile.read()
            assert 'pre-commit' in hooks

        with open(os.path.join(tmp_dir, 'sample.py'), 'w') as tmpfile:
            tmpfile.write(SAMPLE_PYTHON_FILE)

        assert repo.untracked_files == ['sample.py']
        git_utils.git_add_and_commit(repo, ['sample.py'], "testing hooks")
        assert not repo.untracked_files
