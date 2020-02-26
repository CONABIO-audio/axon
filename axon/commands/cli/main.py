# -*- coding: utf-8 -*-
"""Main entry point to all axon commands."""
import click
from axon.commands.projects import create_project


@click.group(name='axon')
def main():
    """Execute axon command."""


@main.command(name='createproject')
@click.argument('name')
@click.argument('path')
def create_project_command(name, path):
    """Create a new project."""
    create_project(name, path)


if __name__ == '__main__':
    main()
