# -*- coding: utf-8 -*-
"""Tests for project creation and management."""
import tempfile
import os
import logging
from axon.commands import projects

logging.basicConfig(level=logging.INFO)


def test_add_basic_files():
    """Check if can add basic project files to directory."""
    tmp_dir = tempfile.TemporaryDirectory()
    path = tmp_dir.name

    # Add files
    projects.add_basic_files(path)

    # Licence should exists
    file_path = os.path.join(path, 'LICENCE')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # Readme should exists
    file_path = os.path.join(path, 'README.md')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # setup.py file should exists
    file_path = os.path.join(path, 'setup.py')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # axon config file should exists
    file_path = os.path.join(path, 'axon.config.yaml')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # gitignore file should exists
    file_path = os.path.join(path, '.gitignore')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # precommit file should exists
    file_path = os.path.join(path, '.pre-commit-config.yaml')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # mlproyect file should exists
    file_path = os.path.join(path, 'MLproject')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # conda file should exists
    file_path = os.path.join(path, 'conda.yaml')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0

    # requirements file should exists
    file_path = os.path.join(path, 'requirements.txt')
    assert os.path.exists(file_path)
    with open(file_path, 'r') as file_obj:
        assert len(file_obj.read()) > 0


def test_create_basic_directory_structure():
    """Check if can add create project directory structure."""
    tmp_dir = tempfile.TemporaryDirectory()
    path = tmp_dir.name
    name = 'tmp'

    # Add files
    projects.create_project_structure(name, path)

    files_that_should_exists = [
        name + '/trainings',
        name + '/models',
        name + '/datasets',
        name + '/preprocessors',
        name + '/evaluators',
        name + '/scripts',
        name + '/trainings/__init__.py',
        name + '/models/__init__.py',
        name + '/datasets/__init__.py',
        name + '/preprocessors/__init__.py',
        name + '/evaluators/__init__.py',
        name + '/scripts/__init__.py'
    ]

    for filename in files_that_should_exists:
        assert os.path.exists(os.path.join(path, filename))
