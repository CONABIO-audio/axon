# -*- coding: utf-8 -*-
"""Basic configuration utilities."""
import os
import logging
import collections.abc
import yaml


BASE_CONFIG_NAME = 'base_config.yaml'
BASE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), BASE_CONFIG_NAME)


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
            load_and_update_configurations(config_file, config)
        else:
            logging.warning(
                'User axon config file does not exist: %s',
                config_file)

    # Look for a configuration file within the current directory or parent
    # directories and read configuration.
    try:
        project_config_file_name = config.get('config_filename', None)
        project_directory = get_project_path(os.getcwd(), config)

        project_config_file = os.path.join(
            project_directory,
            project_config_file_name)
        load_and_update_configurations(project_config_file, config)

    except FileNotFoundError:
        pass

    return config


def load_and_update_configurations(config_file, configurations):
    """Read configuration file and update any new settings."""
    try:
        with open(config_file, 'r') as yamlfile:
            new_configs = yaml.full_load(yamlfile)

        configurations = update(configurations, new_configs)
    except yaml.YAMLError:
        logging.warning(
            'Could not read user axon project config file: %s',
            config_file)


def update(settings, new_settings):
    """Recursive replacement of settings."""
    for key, value in new_settings.items():
        if isinstance(value, collections.abc.Mapping):
            settings[key] = update(settings.get(key, {}), value)
        else:
            settings[key] = value
    return settings
