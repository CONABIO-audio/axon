# -*- coding: utf-8 -*-
"""Tests for project creation and management."""
import tempfile
import os
import pytest

from axon.commands import projects
from axon.config import get_config


BASE_CONFIGURATION = get_config()


def test_create_basic_files():
    """Check if can add basic project files to directory."""
    with tempfile.TemporaryDirectory() as path:
        # Add files
        projects.create_basic_files(path)

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
    name = 'tmp'
    with tempfile.TemporaryDirectory() as path:
        # Add files
        projects.create_project_structure(name, path, BASE_CONFIGURATION)

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


def test_create_project():
    """Check if a new project directory is created correctly."""
    name = 'tmp'
    with tempfile.TemporaryDirectory() as path:
        projects.create_project(name, path, BASE_CONFIGURATION)
        root_path = os.path.join(path, name + '_project')

        assert os.path.exists(root_path)

        with pytest.raises(ValueError):
            projects.create_project(name, path, BASE_CONFIGURATION)


def test_get_project():
    """Check that the root project directory is successfuly extracted."""
    name = 'tmp'
    with tempfile.TemporaryDirectory() as path:
        projects.create_project(name, path, BASE_CONFIGURATION)

        root_path = os.path.abspath(os.path.join(path, name + '_project'))
        paths = [
            os.path.join(root_path, name, subdir)
            for subdir in ['trainings', 'models', 'datasets', 'scripts']
        ]

        for path in paths:
            project = projects.get_project(path, BASE_CONFIGURATION)
            assert project.path == root_path


def test_project_has_git_repository():
    """Check if the Project builds the git repository correctly."""
    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=False)
        assert project.repo is None

    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=True)
        assert project.repo is not None


def test_has_precommit_hooks_installed():
    """Check if the Project method has_precommit_hooks_installed works fine."""
    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=False)
        assert not project.has_precommit_hooks_installed()

    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=True)
        assert project.has_precommit_hooks_installed()


def test_project_create():
    """Check if the create method of the Project class is working correctly."""
    with tempfile.TemporaryDirectory() as path:
        name = 'random'
        project = projects.Project.create(path, name, BASE_CONFIGURATION)
        assert project.path == os.path.join(path, name + '_project')
        assert project.repo is not None
        assert project.has_basic_files()
        assert project.has_directory_structure()
        assert project.has_precommit_hooks_installed()
