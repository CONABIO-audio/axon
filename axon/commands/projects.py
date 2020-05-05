# -*- coding: utf-8 -*-
"""Utilities for project management commands."""
from axon.project.project import Project
from axon.config.main import get_project_path


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


def create_project(path: str, name: str, configuration: dict) -> Project:
    """
    Create a new axon project.

    Parameters
    ----------
    path: str
        Path of parent directory.
    name: str
        Name for new axon project.
    configuration: dict
        Configuration dictionary.

    Returns
    -------
    Project
    """
    return Project.create(path, name, configuration)
