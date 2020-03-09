# -*- coding: utf-8 -*-
"""Axon configuration commands."""
from typing import List
from typing import Tuple
import os
from shutil import copyfile
import yaml
import click

from pygments import highlight
from pygments.lexers import YamlLexer
from pygments.formatters import Terminal256Formatter

from axon.config.main import BASE_CONFIG_PATH

BACKUP_CONFIG_PATH = BASE_CONFIG_PATH + '.bkp'


def validate_set_option(
        ctx: click.Context,
        param: str,
        options_tuple: tuple) -> List[Tuple[str, str]]:
    """Validate user supplied configuration option."""
    values = []

    for option in options_tuple:
        try:
            key, value = option.split(':', 1)
        except ValueError:
            message = 'Setting option must be in format key:value'
            raise click.BadParameter(message, param=param)

        configuration = ctx.obj['config']

        keys = key.split('.')
        current_section = configuration
        for n, subkey in enumerate(keys):
            if subkey not in current_section:
                current_parent = '.'.join(keys[:n])

                valid_options = list(sorted(current_section.keys()))
                options_str = '[ {} ]'.format(', '.join(valid_options))

                if current_parent:
                    message = (
                        f'Key "{subkey}" is not a valid configuration '
                        f'option for "{current_parent}". Valid options: '
                        f'{options_str}')
                else:
                    message = (
                        f'Key "{subkey}" is not a valid configuration '
                        f'option. Valid options: {options_str}')

                raise click.BadParameter(message, param=param)
            current_section = current_section[subkey]

        try:
            value = yaml.full_load(value)
        except yaml.YAMLError as error:
            message = f'Value {value} is invalid. Error: {str(error)}'
            raise click.BadParameter(message, param=param)

        values.append((key, value))
    return values


def deep_set(dictionary: dict, key: str, value: str):
    """Set dictionary value with dot notation."""
    keys = key.split('.')

    current_level = dictionary
    for subkey in keys[:-1]:
        if subkey not in current_level:
            current_level[subkey] = {}

        current_level = current_level[subkey]

    current_level[keys[-1]] = value


@click.group(name='config')
def config():
    """Entry point for all configuration commands."""


@config.command()
@click.pass_context
def show(ctx):
    """Show current configuration."""
    configuration = ctx.obj['config']
    show_configs(configuration)


@config.command(name='set')
@click.argument('set_options', nargs=-1, callback=validate_set_option)
@click.option('--global', 'target', flag_value='global', default=True)
@click.option('--local', 'target', flag_value='user')
def set_command(set_options, target):
    """Set configuration options."""
    if target == 'global':
        set_global_config(set_options)

    if target == 'local':
        set_local_config(set_options)

    click.secho('Configurations set.', fg='green')


@config.command()
def restore():
    """Restore configuration to default settings."""
    if os.path.exists(BACKUP_CONFIG_PATH):
        copyfile(BACKUP_CONFIG_PATH, BASE_CONFIG_PATH)
    click.secho('Configurations restored', fg='green')


def show_configs(configs):
    """Show current configuration."""
    yaml_string = yaml.dump(configs)

    formatted = highlight(
        yaml_string,
        YamlLexer(),
        Terminal256Formatter())

    click.echo(formatted)


def set_global_config(set_options):
    """Set global configuration."""
    if not os.path.exists(BACKUP_CONFIG_PATH):
        copyfile(BASE_CONFIG_PATH, BACKUP_CONFIG_PATH)

    with open(BASE_CONFIG_PATH, 'r') as yamlfile:
        global_configs = yaml.full_load(yamlfile)

    for key, value in set_options:
        deep_set(global_configs, key, value)

    with open(BASE_CONFIG_PATH, 'w') as yamlfile:
        yamlfile.write(yaml.dump(global_configs))


def set_local_config(set_options):
    """Set local configuration."""
    click.secho(str(set_options), fg='green')
