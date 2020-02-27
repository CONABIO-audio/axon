# -*- coding: utf-8 -*-
"""Projects module.

A projects is a self contained repository in which the whole of model
development takes place. The projects are structured in a specific manner
to facilitate navigation and help organize code.
"""
import os

from axon.config import get_config
from .git import create_repository as create_git_repository
from .git import add_all_files_to_repository
from .git import install_precommit_hooks
from .templates import get_template


def create_project(name: str, path: str):
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
    add_basic_files(project_directory)
    create_project_structure(name, project_directory)

    # Commit the new files to git
    add_all_files_to_repository(repository, 'First commit')
    install_precommit_hooks(repository)


def add_basic_files(path: str, context: dict = None):
    """Add basic files to new git repository."""
    if context is None:
        context = {}

    # Create licence
    template = get_template('LICENCE')
    with open(os.path.join(path, 'LICENCE'), 'w') as licence:
        licence.write(template.render(**context))

    # Create readme
    template = get_template('README.md')
    with open(os.path.join(path, 'README.md'), 'w') as readme:
        readme.write(template.render(**context))

    # Create setup
    template = get_template('setup.py')
    with open(os.path.join(path, 'setup.py'), 'w') as setup:
        setup.write(template.render(**context))

    # Create config file
    template = get_template('axon.config.yaml')
    with open(os.path.join(path, 'axon.config.yaml'), 'w') as config:
        config.write(template.render(**context))

    # Create gitignore file
    template = get_template('gitignore')
    with open(os.path.join(path, '.gitignore'), 'w') as gitignore:
        gitignore.write(template.render(**context))

    # Create pre-commit-config file
    template = get_template('pre-commit-config.yaml')
    with open(os.path.join(path, '.pre-commit-config.yaml'), 'w') as config:
        config.write(template.render(**context))

    # Create MLproject file
    template = get_template('MLProject')
    with open(os.path.join(path, 'MLProject'), 'w') as mlproject:
        mlproject.write(template.render(**context))

    # Create conda.yaml file
    template = get_template('conda.yaml')
    with open(os.path.join(path, 'conda.yaml'), 'w') as conda:
        conda.write(template.render(**context))

    # Create requirements file
    template = get_template('requirements.txt')
    with open(os.path.join(path, 'requirements.txt'), 'w') as requirements:
        requirements.write(template.render(**context))


def create_project_structure(name: str, path: str):
    """Create the directory structure within a project directory."""
    config = get_config()
    directory_structure = config.get('directory_structure', None)

    home_path = os.path.join(path, name)
    if not os.path.exists(home_path):
        os.makedirs(home_path)

    init_file = os.path.join(home_path, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w'):
            pass

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
