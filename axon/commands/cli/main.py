# -*- coding: utf-8 -*-
"""Main entry point to all axon commands."""
import sys
import os
import click
from axon.commands.projects import create_project
from axon.commands.projects import get_project
from axon.commands.run import run
# from axon.commands.train import train
# from axon.commands.evaluate import evaluate
from axon.config.main import get_config


def check_if_in_project(ctx):
    """
    Check if command was run from within a project directory.

    Exit the current process if not.
    """
    if 'project' not in ctx.obj:
        click.secho('You are not within an axon project directory', fg='red')
        sys.exit()


@click.group(name='axon')
@click.pass_context
def main(ctx):
    """Execute axon command."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = get_config()

    try:
        ctx.obj['project'] = get_project(os.getcwd(), ctx.obj['config'])
        sys.path.append(ctx.obj['project'].path)
    except FileNotFoundError:
        pass


@main.command(name='createproject')
@click.argument('name')
@click.argument('path')
@click.pass_context
def create_project_command(ctx, name, path):
    """Create a new project."""
    create_project(name, path, ctx.obj['config'])


@main.command(name='install', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_context
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def install_packages(ctx, args):
    """Create a new project."""
    check_if_in_project(ctx)
    project = ctx.obj['project']
    project.install_packages(*args)


@main.command(name='python', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_context
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run_python(ctx, args):
    """Run command with project's virtual env python."""
    check_if_in_project(ctx)
    project = ctx.obj['project']
    project.run_python(*args)


@main.command(name='run')
@click.argument('name')
@click.pass_context
def run_command(ctx, name):
    """Run a with dvc."""
    check_if_in_project(ctx)
    run(ctx.obj['project'], name)


@main.command(name='train')
@click.pass_context
def train(ctx):
    """Train a model."""
    check_if_in_project(ctx)
    click.secho('training!', fg='green')


@main.command(name='evaluate')
@click.pass_context
def evaluate(ctx):
    """Evaluate a model."""
    check_if_in_project(ctx)
    click.secho('evaluating!', fg='green')


if __name__ == '__main__':
    # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
    main(obj={})
