# -*- coding: utf-8 -*-
"""Projects module.

A projects is a self contained repository in which the whole of model
development takes place. The projects are structured in a specific manner
to facilitate navigation and help organize code.
"""
import os
from typing import Iterable
import git

from axon.commands.git_utils import create_repository as create_git_repository
from axon.commands.git_utils import add_all_files_to_repository
from axon.commands.git_utils import install_precommit_hooks
from axon.commands.git_utils import git_add_and_commit
from axon.commands.templates import get_template


BASIC_FILES = [
    'LICENCE',
    'README.md',
    'setup.py',
    'axon.config.yaml',
    '.gitignore',
    '.pre-commit-config.yaml',
    'MLProject',
    'conda.yaml',
    'requirements.txt',
]


class Project:
    """
    Project class.

    An axon project is the directory that contains all the code belonging to a
    machine learning project.
    """

    project_dir_postfix = '_project'

    def __init__(self, path: str, configuration: dict, validate: bool = True):
        self.path = path
        self.configuration = configuration
        self.name = (
            os.path.basename(self.path).replace(self.project_dir_postfix, '')
        )

        try:
            self.repo = git.Repo(self.path)
        except git.InvalidGitRepositoryError:
            self.repo = None

        if validate:
            self.validate()

    def validate(self):
        """
        Check if the repository has all the basic and necessary components.

        Will create or install them if missing.
        """
        if self.repo is None:
            self.repo = create_git_repository(self.path)

        if not self.has_basic_files():
            basic_files = create_basic_files(self.path)
            commit_message = 'Basic files added'
            git_add_and_commit(self.repo, basic_files, commit_message)

        if not self.has_directory_structure():
            structure_files = create_project_structure(
                self.name,
                self.path,
                self.configuration)
            commit_message = 'Base structure files added'
            git_add_and_commit(self.repo, structure_files, commit_message)

        if not self.has_precommit_hooks_installed():
            install_precommit_hooks(self.repo)

    @classmethod
    def create(cls, path: str, name: str, configuration: dict):
        """Create a new Project.

        Parameters
        ----------
        path: str
            The directory in which to create a project subdirectory.
        name: str
            A name for the project
        configuration: dict
            A dictionary with some configuration variables.

        Returns
        -------
        Project
            The resulting Project object that points to a directory with a
            fresh project start.

        Raises
        ------
        ValueError
            If a directory called name is previously present in the path.
        """
        project_directory = os.path.join(path, name + cls.project_dir_postfix)
        if os.path.exists(project_directory):
            message = (
                'A directory with this name already exists, please use'
                ' another name')
            raise ValueError(message)

        os.makedirs(project_directory)
        return cls(project_directory, configuration)

    def has_basic_files(self) -> bool:
        """Check if the project has all the basic files."""
        for filename in BASIC_FILES:
            path = os.path.join(self.path, filename)
            if not os.path.exists(path):
                return False

        return True

    def has_directory_structure(self) -> bool:
        """Check if the project has the basic directory structure."""
        directory_structure = self.configuration.get(
            'directory_structure',
            None)

        home_path = os.path.join(self.path, self.name)
        if not os.path.exists(home_path):
            return False

        init_file = os.path.join(home_path, '__init__.py')
        if not os.path.exists(init_file):
            return False

        if directory_structure is None:
            message = 'The directory structure is badly configured'
            raise ValueError(message)

        for subdirectory in directory_structure:
            directory_path = os.path.join(home_path, subdirectory)
            if not os.path.exists(directory_path):
                return False

            init_file = os.path.join(directory_path, '__init__.py')
            if not os.path.exists(init_file):
                return False

        return True

    def has_precommit_hooks_installed(self) -> bool:
        """Check if the project has the pre-commit hooks installed."""
        if self.repo is None:
            return False

        hooks_path = os.path.join(
            self.repo.git_dir,
            'hooks',
            'pre-commit')

        if not os.path.exists(hooks_path):
            return False

        with open(hooks_path, 'r') as precommitfile:
            hooks = precommitfile.read()

        return 'pre-commit' in hooks


def create_project(name: str, path: str, configuration: dict) -> Project:
    """Create a new project directory.

    Parameters
    ----------
    name : str
    path : str
    """
    project_directory = os.path.join(path, name + '_project')
    if os.path.exists(project_directory):
        message = (
            'A directory with this name already exists, please use'
            ' another name')
        raise ValueError(message)

    # Create a  new repository directory
    os.makedirs(project_directory)
    repository = create_git_repository(project_directory)

    # Add basic files and the directory structure
    create_basic_files(project_directory)
    create_project_structure(name, project_directory, configuration)

    # Commit the new files to git
    add_all_files_to_repository(repository, 'First commit')
    install_precommit_hooks(repository)

    return Project(os.path.abspath(project_directory), configuration)


def create_basic_files(path, context: dict = None) -> Iterable[str]:
    """Add basic files to new git repository."""
    if context is None:
        context = {}

    files = []
    for basic_file in BASIC_FILES:
        template = get_template(basic_file)
        filename = os.path.join(path, basic_file)
        with open(filename, 'w') as bfile:
            bfile.write(template.render(**context))

        files.append(filename)
    return files


def create_project_structure(
        name: str,
        path: str,
        configuration: dict) -> Iterable[str]:
    """Create the directory structure within a project directory."""
    directory_structure = configuration.get('directory_structure', None)
    created_files = []

    home_path = os.path.join(path, name)
    if not os.path.exists(home_path):
        os.makedirs(home_path)

    init_file = os.path.join(home_path, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w'):
            pass
    created_files.append(init_file)

    if directory_structure is None:
        message = 'The directory structure is badly configured'
        raise ValueError(message)

    for subdirectory in directory_structure:
        directory_path = os.path.join(home_path, subdirectory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        init_file = os.path.join(directory_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w'):
                pass

        created_files.append(init_file)

    return created_files


def get_project_path(path: str, configuration: dict) -> str:
    """Get root directory of the project that contains the provided path."""
    project_config_filename = configuration.get('config_filename')

    current_dir = os.path.abspath(path)
    while True:
        if project_config_filename in os.listdir(current_dir):
            return current_dir

        parent_dir = os.path.dirname(current_dir)
        if current_dir == parent_dir:
            message = 'No project was found at the given path ({})'
            message = message.format(path)
            raise FileNotFoundError(message)

        current_dir = parent_dir


def get_project(path: str, configuration: dict) -> Project:
    """
    Get the Project in the directory provided in path argument.

    If the path is not the root of the project, it will look for the root
    in the parent directories recursively.

    Parameters
    ----------
    path: str
        Path within the project.
    configuration: dict
        Configuration options.

    Returns
    -------
    Project

    Raises
    ------
    FileNotFoundError
        If the provided path is not contained within a project directory.
    """
    path = get_project_path(path, configuration)
    return Project(path, configuration)
