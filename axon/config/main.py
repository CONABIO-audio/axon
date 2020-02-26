# -*- coding: utf-8 -*-
"""Basic configuration utilities."""
import os
import logging
import collections.abc
import yaml


BASE_CONFIG_NAME = 'base_config.yaml'
BASE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), BASE_CONFIG_NAME)


def get_config():
    """Load and return configuration settings from files."""
    # Load basic configuration
    with open(BASE_CONFIG_PATH, 'r') as yamlfile:
        config = yaml.full_load(yamlfile)

    # Load and replace configs in user provided setting files
    user_config_files = config.get('config_files', [])

    if not isinstance(user_config_files, (list, tuple)):
        if user_config_files is None:
            user_config_files = []
        else:
            user_config_files = [user_config_files]

    for config_file in user_config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as yamlfile:
                    user_config = yaml.full_load(yamlfile)

                config = update(config, user_config)
            except yaml.YAMLError:
                logging.warning(
                    'Could not read user axon config file: %s',
                    config_file)
        else:
            logging.warning(
                'User axon config file does not exist: %s',
                config_file)

    # Look for a configuration file within the current directory or parent
    # directories and read configuration.
    project_config_file_name = config.get('config_file_name', None)
    project_directory = find_project(project_config_file_name)

    if project_directory is not None:
        project_config_file = os.path.join(
            project_directory,
            project_config_file_name)
        try:
            with open(project_config_file, 'r') as yamlfile:
                project_config = yaml.full_load(yamlfile)

            config = update(config, project_config)
        except yaml.YAMLError:
            logging.warning(
                'Could not read user axon project config file: %s',
                project_config_file)

    return config


def update(settings, new_settings):
    """Recursive replacement of settings."""
    for key, value in new_settings.items():
        if isinstance(value, collections.abc.Mapping):
            settings[key] = update(settings.get(key, {}), value)
        else:
            settings[key] = value
    return settings


def find_project(config_filename):
    """Get project directory.

    This function will look recursively for a configuration file
    with the given name, repeating the search on the parent directory
    if not found.

    Parameters
    ----------
    config_filename: str
        The name of the configuration file to look for. A directory will be
        declared a project directory if a configuration file with this name
        is found in it.

    Returns
    -------
    str
        The path of the project directory. If none is found it will return
        None.
    """
    current_directory = os.path.abspath(os.getcwd())

    while True:
        potential_config_file = os.path.join(
            current_directory,
            config_filename)
        if os.path.exists(potential_config_file):
            return current_directory

        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            return None

        current_directory = parent_directory
