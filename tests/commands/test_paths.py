# -*- coding: utf-8 -*-
"""Test for axon path utilities."""
import os
import tempfile
import pytest

from axon.commands.paths import find_in_directory


FILES = [
    'scripts/subdir1/subdir2/file1.py',
    'scripts/subdir1/subdir2/file2.py',
    'scripts/subdir1/file1.py',
    'scripts/subdir1/file2.py',
    'scripts/file1.py',
    'scripts/file2.py',
    'datasets/subdir1/subdir2/file1.py',
    'datasets/subdir1/subdir2/file2.py',
    'datasets/subdir1/file1.py',
    'datasets/subdir1/file2.py',
    'datasets/file1.py',
    'datasets/file2.py',
    'datasets/file3.py',
    'trainings/subdir1/subdir2/file1.py',
    'trainings/subdir1/subdir2/file2.py',
    'trainings/subdir1/file1.py',
    'trainings/subdir1/file2.py',
    'trainings/file1.py',
    'trainings/file2.py',
    'file1.py',
    'file2.py',
    'file4.py'
]


def test_find_in_directory():
    """Check if can find files in directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        for filename in FILES:
            path = os.path.join(tmp_dir, filename)
            dirname = os.path.dirname(path)

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(path, 'w') as pyfile:
                pyfile.write("")

        # Raise ValueError searching with absolute path not in directory
        with pytest.raises(ValueError):
            find_in_directory(tmp_dir, '/file1.py')

        # Raise FileNotFoundError when no file exists
        unfindable_files = [
            os.path.join(tmp_dir, 'file3.py'),
            os.path.join(tmp_dir, 'file3'),
            os.path.join(tmp_dir, 'scripts', 'file3.py'),
            os.path.join(tmp_dir, 'scripts', 'file3'),
            'file5',
            'file5.py',
            'scripts/file4.py',
            'scripts.file4',
        ]

        for filename in unfindable_files:
            with pytest.raises(FileNotFoundError):
                find_in_directory(tmp_dir, filename)

        findable_files = [
            ('subdir1/subdir2/file1.py', 'scripts/subdir1/subdir2/file1.py'),
            ('subdir1.subdir2.file1', 'scripts/subdir1/subdir2/file1.py'),
            ('scripts/subdir1/subdir2/file1.py', 'scripts/subdir1/subdir2/file1.py'),  # noqa
            ('scripts.subdir1.subdir2.file1', 'scripts/subdir1/subdir2/file1.py'),  # noqa
            ('subdir1/file1.py', 'scripts/subdir1/file1.py'),
            ('subdir1.file1', 'scripts/subdir1/file1.py'),
            ('scripts/subdir1/file1.py', 'scripts/subdir1/file1.py'),
            ('scripts.subdir1.file1', 'scripts/subdir1/file1.py'),
            ('file1.py', 'scripts/file1.py'),
            ('file1', 'scripts/file1.py'),
            ('scripts/file1.py', 'scripts/file1.py'),
            ('scripts.file1', 'scripts/file1.py'),
            ('file4.py', 'file4.py'),
            ('file4', 'file4.py'),
            (os.path.join(tmp_dir, 'file4.py'), 'file4.py'),
        ]

        for name, truth in findable_files:
            found = find_in_directory(tmp_dir, name, subdirs=['scripts'])
            assert found == truth

        found = find_in_directory(
            tmp_dir,
            'file3',
            subdirs=['scripts', 'datasets'])
        assert found == 'datasets/file3.py'
