# -*- coding: utf-8 -*-
"""Project commands module."""
import sys
import os
import click


@click.group(name='project')
@click.pass_context
def project_command(ctx):
    """Manage projects."""
    # pylint: disable=import-outside-toplevel
    from axon.commands.projects import get_project

    if ctx.invoked_subcommand != 'create':
        try:
            ctx.obj['project'] = get_project(os.getcwd(), ctx.obj['config'])
            sys.path.append(ctx.obj['project'].path)
        except FileNotFoundError:
            message = 'You are not within an axon project directory'
            click.secho(message, fg='red')
            ctx.exit()


@project_command.command(name='create')
@click.argument('name')
@click.option('--path', '-p', type=str)
@click.pass_context
def create_command(ctx, name, path):
    """Create a new project."""
    # pylint: disable=import-outside-toplevel
    from axon.commands.projects import create_project

    if path is None:
        path = os.path.join(os.getcwd(), name)

    create_project(name, path, ctx.obj['config'])


@project_command.command(name='install', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_context
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def install_packages(ctx, args):
    """Create a new project."""
    project = ctx.obj['project']
    project.install_packages(*args)


@project_command.command(name='pip', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_context
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.option('--save', '-s', is_flag=True)
def run_pip(ctx, args, save):
    """Create a new project."""
    project = ctx.obj['project']
    project.run_pip(*args, update=save)


@project_command.command(name='python', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_context
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run_python(ctx, args):
    """Run command with project's virtual env python."""
    project = ctx.obj['project']
    project.run_python(*args)


@project_command.command(name='run')
@click.argument('name')
@click.pass_context
def run_command(ctx, name):
    """Run a with dvc."""
    # pylint: disable=import-outside-toplevel
    from axon.commands.run import run
    run(ctx.obj['project'], name)


@project_command.command(name='train')
def train():
    """Train a model."""
    click.secho('training!', fg='green')


@project_command.command(name='evaluate')
def evaluate():
    """Evaluate a model."""
    click.secho('evaluating!', fg='green')
