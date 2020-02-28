# -*- coding: utf-8 -*-
"""Main entry point to all axon commands."""
import sys
import click
from axon.commands.projects import create_project
# from axon.commands.run import run
# from axon.commands.train import train
# from axon.commands.evaluate import evaluate
from axon.config.main import get_config


def check_if_in_project(ctx):
    return 'project_dir' in ctx


@click.group(name='axon')
@click.pass_context
def main(ctx):
    """Execute axon command."""
    # TODO: checkar que se está en una carpeta de proyecto
    # try: project = get_project()...
    # ctx['project_dir'] = project
    # ctx['config'] = get_config(project_dir)


@main.command(name='createproject')
@click.argument('name')
@click.argument('path')
def create_project_command(name, path):
    """Create a new project."""
    create_project(name, path)


@main.command(name='run')
@click.pass_context
def run(ctx, name, path):
    """Run a with dvc."""
    check_if_in_project(ctx)
    click.secho('running!', fg='green')


@main.command(name='run')
@click.pass_context
def train(ctx):
    """Train a model."""
    check_if_in_project(ctx)
    click.secho('training!', fg='green')


@main.command(name='run')
@click.pass_context
def evaluate(ctx):
    """Evaluate a model."""
    check_if_in_project(ctx)
    click.secho('evaluating!', fg='green')


if __name__ == '__main__':
    main()
