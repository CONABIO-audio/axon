# -*- coding: utf-8 -*-
"""
Run command.

This command excutes python scripts but will track all produced information
to MLFlow and DVC.

Should point to a script file and read any sources of data or other code
dependencies and data outputs, and use them to run:

dvc run script -d dependencies -o outputs
"""
import os
import argparse
import click

from axon.commands.projects import get_project
from axon.commands.git_utils import git_add_and_commit
from axon.commands.dvc import run as dvc_run
from axon.config import get_config


def run(project, script_name):
    """
    Run a process within the project with dvc and git.

    The process will be loaded from the file indicated by script_name.
    This process file should describe all its dependencies and outputs
    so that dvc can be correctly informed.
    """
    process_class, script = project.get_process(script_name)
    process = process_class(
        config=project.configuration,
        wdir=project.pkg_path)

    script_rel_path = os.path.relpath(
        os.path.join(project.pkg_path, script),
        start=project.path)

    command = "{} -m axon.commands.run {} {}"
    command = command.format(
        project.get_venv_python_path(),
        project.path,
        script)

    filename, _ = os.path.splitext(script_rel_path)
    file = os.path.join(project.path, filename) + '.dvc'
    file = os.path.relpath(file, start=project.path)

    deps = process.get_dependencies()
    outs = process.get_outs()
    outs_no_cache = process.get_outs_no_cache()
    metrics = process.get_metrics()
    metrics_no_cache = process.get_metrics_no_cache()

    # Add script file and virtual env requirements to run deps
    deps += [script_rel_path, project.requirements_file]

    click.secho('[+] Starting DVC run', fg='cyan')
    dvc_run(
        exec_path=project.path,
        command=command,
        wdir=process.wdir,
        deps=deps,
        outs=outs,
        outs_no_cache=outs_no_cache,
        metrics=metrics,
        metrics_no_cache=metrics_no_cache,
        file=file)

    click.secho('[+] Adding files to git', fg='cyan')
    git_files = deps + [file]
    commit_message = 'Running %s' % command
    git_add_and_commit(
        project.repo,
        files=git_files,
        commit_message=commit_message)
    click.secho('[-] Run successful', fg='green')


def main(project_dir, script_name):
    """Run a process in project without git and dvc."""
    config = get_config()
    project = get_project(project_dir, config)
    process, _ = project.get_process(script_name)
    process(config, project.pkg_path)()


def parse_arguments():
    """Parse the arguments for the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'project_dir',
        type=str,
        help='Path to project')
    parser.add_argument(
        'script_name',
        type=str,
        help='Name of script containing process')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.project_dir, args.script_name)
