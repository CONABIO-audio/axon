# -*- coding: utf-8 -*-
"""DVC commands."""
from subprocess import Popen, PIPE, check_output
from git import create_repository, get_repository


class DvcExecutionError(Exception):
    """Dvc execution error.

    Simple class that specifies an execution error from dvc.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def init(no_scm=False, force=False, phelp=False, quiet=False, verbose=False):
    """Wrap dvc init command."""
    if phelp:
        return get_help('init')
    args = ['dvc', 'init']
    if no_scm:
        args += ['--no-scm']
    if force:
        args += ['-f']
    if quiet:
        args += ['-q']
    if verbose:
        args += ['-v']
    return run_shell_process(args)


def add(targets, file=None, phelp=False, quiet=True, verbose=False,
        recursive=False, no_commit=False):
    """Wrap dvc add command."""
    if phelp:
        return get_help('add')
    args = ['dvc', 'add']
    if quiet:
        args += ['-q']
    if verbose:
        args += ['-v']
    if recursive:
        args += ['-R']
    if no_commit:
        args += ['--no-commit']
    if file is not None:
        args += ['-f', file]
    args += targets
    return run_shell_process(args)


def run(command, wdir, deps=[], outs=[], outs_no_cache=[], metrics=[],
        metrics_no_cache=[], file=None, no_exec=False,
        overwrite_dvcfile=False, ignore_build_cache=False, no_commit=False,
        always_changed=False, phelp=False, quiet=False, verbose=False):
    """Wrap dvc run command."""
    if phelp:
        return get_help('add')
    args = ['dvc', 'run', '-w', wdir]
    if len(deps) > 0:
        args += ['-d'] + deps
    if len(outs) > 0:
        args += ['-o'] + outs
    if len(outs_no_cache) > 0:
        args += ['-O'] + outs_no_cache
    if len(metrics) > 0:
        args += ['-m'] + metrics
    if len(metrics_no_cache) > 0:
        args += ['-M'] + metrics_no_cache
    if file is not None:
        args += ['-f', 'file']
    if no_exec:
        args += ['--no-exec']
    if overwrite_dvcfile:
        args += ['--overwrite-dvcfile']
    if ignore_build_cache:
        args += ['--ignore-build-cache']
    if no_commit:
        args += ['--no-commit']
    if always_changed:
        args += ['--always-changed']
    if quiet:
        args += ['-q']
    if verbose:
        args += ['-v']
    return run_shell_process(args)


def pipeline(command='show', phelp=False, quiet=False, verbose=False):
    """Wrap dvc pipeline command."""
    if phelp:
        return get_help('pipeline')
    if command in ['show', 'list']:
        args = ['dvc', 'pipeline']
        if quiet:
            args += ['-q']
        if verbose:
            args += ['-v']
        args += [command]
        return run_shell_process(args)
    raise ValueError('Command ', command, ' is not a valid command for dvc \
        pipeline. Options are: "show | list"')


def run_shell_process(args):
    """Run process and return stdout or raises an execution error."""
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()
    if stderr:
        raise DvcExecutionError(stderr)
    return stdout


def get_help(dvc_command):
    """Return help string according to dvc command."""
    args = ['dvc', dvc_command]
    args.append('-h')
    help_str = check_output(args)
    print(help_str)
    return help_str
