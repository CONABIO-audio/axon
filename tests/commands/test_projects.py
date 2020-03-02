# -*- coding: utf-8 -*-
"""Tests for project creation and management."""
import tempfile
import os
import sys
import pytest

from axon.commands import projects
from axon.core.processes import Process
from axon.config import get_config


BASE_CONFIGURATION = get_config()


@pytest.mark.skip()
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
            os.path.join(name, '__init__.py'),
            os.path.join(name, 'trainings'),
            os.path.join(name, 'models'),
            os.path.join(name, 'datasets'),
            os.path.join(name, 'preprocessors'),
            os.path.join(name, 'evaluators'),
            os.path.join(name, 'scripts'),
            os.path.join(name, 'trainings', '__init__.py'),
            os.path.join(name, 'models', '__init__.py'),
            os.path.join(name, 'datasets', '__init__.py'),
            os.path.join(name, 'preprocessors', '__init__.py'),
            os.path.join(name, 'evaluators', '__init__.py'),
            os.path.join(name, 'scripts', '__init__.py'),
        ]

        for filename in files_that_should_exists:
            assert os.path.exists(os.path.join(path, filename))


@pytest.mark.skip()
def test_create_project():
    """Check if a new project directory is created correctly."""
    name = 'tmp'
    with tempfile.TemporaryDirectory() as path:
        projects.create_project(name, path, BASE_CONFIGURATION)
        root_path = os.path.join(path, name + '_project')

        assert os.path.exists(root_path)

        with pytest.raises(ValueError):
            projects.create_project(name, path, BASE_CONFIGURATION)


@pytest.mark.skip()
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


@pytest.mark.skip()
def test_project_has_git_repository():
    """Check if the Project builds the git repository correctly."""
    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=False)
        assert project.repo is None

    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=True)
        assert project.repo is not None


@pytest.mark.skip()
def test_has_precommit_hooks_installed():
    """Check if the Project method has_precommit_hooks_installed works fine."""
    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=False)
        assert not project.has_precommit_hooks_installed()

    with tempfile.TemporaryDirectory() as path:
        project = projects.Project(path, BASE_CONFIGURATION, validate=True)
        assert project.has_precommit_hooks_installed()


@pytest.mark.skip()
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


SAMPLE_PROCESS_1 = '''
from axon.core.processes import Process


class SampleProcess(Process):
    def run(self):
        print("hello world!")
'''

SAMPLE_PROCESS_2 = '''
from axon.core.processes import Process


class SampleProcess(Process):
    def run(self):
        print("hello world!")


class AlternativeProcess(Process):
    def run(self):
        print("alternative process.")
'''


def test_project_get_process():
    """Test if project can retrieve a process defined within it."""
    with tempfile.TemporaryDirectory() as path:
        name = 'detector'
        project = projects.Project.create(path, name, BASE_CONFIGURATION)
        sys.path.append(project.path)

        files_to_create = [
            os.path.join('scripts', 'test1.py'),
            os.path.join('scripts', 'test2.py'),
            os.path.join('scripts', 'empty.py'),
            os.path.join('scripts', 'subdir1', 'test1.py'),
            os.path.join('scripts', 'subdir1', 'test2.py'),
            os.path.join('scripts', 'subdir1', 'empty.py'),
            os.path.join('scripts', 'subdir1', '__init__.py'),
            os.path.join('scripts', 'subdir1', 'subdir2', '__init__.py'),
            os.path.join('scripts', 'subdir1', 'subdir2', 'test1.py'),
            os.path.join('scripts', 'subdir1', 'subdir2', 'test2.py'),
            os.path.join('scripts', 'subdir1', 'subdir2', 'empty.py'),
        ]

        for filename in files_to_create:
            module_path = os.path.join(project.pkg_path, filename)
            dirname = os.path.dirname(module_path)

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(module_path, 'w') as pyfile:
                if 'test1' in filename:
                    pyfile.write(SAMPLE_PROCESS_1)
                elif 'test2' in filename:
                    pyfile.write(SAMPLE_PROCESS_2)
                else:
                    pyfile.write("")

        should_find_w_no_name = [
            'test1',
            'test1.py',
            'subdir1/test1.py',
            'subdir1.test1',
            'subdir1/subdir2/test1.py',
            'subdir1.subdir2.test1',
        ]

        for name in should_find_w_no_name:
            process, _ = project.get_process(name)
            assert issubclass(process, Process)

            name_erroneus_class = name + ':AlternativeProcess'
            with pytest.raises(ValueError):
                project.get_process(name_erroneus_class)

        should_find_w_name = [
            'test2:AlternativeProcess',
            'test2.py:AlternativeProcess',
            'subdir1/test2.py:AlternativeProcess',
            'subdir1.test2:AlternativeProcess',
            'subdir1/subdir2/test2.py:AlternativeProcess',
            'subdir1.subdir2.test2:AlternativeProcess',
        ]

        for name in should_find_w_name:
            process, _ = project.get_process(name)
            assert issubclass(process, Process)
            assert process.__name__ == 'AlternativeProcess'

            name_no_class = name.split(':')[0]
            with pytest.raises(ValueError):
                project.get_process(name_no_class)

        should_not_find = [
            'empty',
            'empty.py',
            'subdir1.empty',
            'subdir1/empty.py',
            'subdir1.subdir2.empty',
            'subdir1/subdir2/empty.py',
        ]

        for name in should_not_find:
            with pytest.raises(ValueError):
                project.get_process(name_no_class)

        sys.path.pop(-1)
