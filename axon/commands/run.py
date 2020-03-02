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

from axon.commands.projects import get_project
from axon.commands.dvc import run as dvc_run
from axon.config import get_config


def run(project, script_name):
    """
    Run a process within the project with dvc and git.

    The process will be loaded from the file indicated by script_name.
    This process file should describe all its dependencies and outputs
    so that dvc can be informed correctly.
    """
    process, script = project.get_process(script_name)

    command = "pythom -m axon.commands.train {} {}"
    command = command.format(project.path, script)

    filename, _ = os.path.splitext(script)
    file = os.path.join(project.path, filename) + '.dvc'

    dvc_run(
        exec_path=project.path,
        command=command,
        wdir=process.wdir,
        deps=process.deps,
        outs=process.outs,
        outs_no_cache=process.outs_no_cache,
        metrics=process.metrics,
        metrics_no_cache=process.metrics_no_cache,
        file=file)


def main(project_dir, script_name):
    """Run a process in project without git and dvc."""
    config = get_config()
    project = get_project(project_dir, config)
    process = project.get_process(script_name)(config)
    process()


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
