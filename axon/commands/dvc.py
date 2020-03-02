# -*- coding: utf-8 -*-
"""DVC commands."""
#  pylint: disable=too-many-branches,too-many-arguments,too-many-locals
from subprocess import Popen


class DvcExecutionError(Exception):
    """Dvc execution error.

    Simple class that specifies an execution error from dvc.
    """


def run_command(args, exec_path=None):
    """Run process and return stdout or raise an execution error.

    A simple method that runs commands in shell.

    Parameters
    ----------
    args: list
        The complete list of arguments to execute as strings.

    exec_path: str
        Path from where to execute command.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    proc = Popen(args, cwd=exec_path)
    stdout, stderr = proc.communicate()

    if stderr:
        raise DvcExecutionError(stderr)

    return " ".join(args), stdout


def get_help(dvc_command):
    """Return help string according to dvc command.

    Simple method to return help output for any dvc command.

    Parameters
    ----------
    dvc_command: str
        Specify the command for help retrieval.

    Returns
    -------
    command: str
        The executed command.

    help_str: str
        The original help message of dvc as a string.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute.
    """
    args = ['dvc', dvc_command]
    args.append('-h')
    command, help_str = run_command(args)
    print(help_str)
    return command, help_str


def init(
        exec_path,
        no_scm=False,
        force=False,
        phelp=False,
        quiet=False,
        verbose=False):
    """Wrap dvc init command.

    This command initializes a DVC project on a directory.
    Note that by default the current working directory is expected to contain a
    Git repository, unless the 'no-scm' option is used.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    no_scm: bool
        Skip Git specific initialization, .dvc/.gitignore will not be written.

    force: bool
        Remove .dvc/ if it exists before initialization. Will remove any
        existing local cache. Useful when a previous dvc init has been
        corrupted.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
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

    return run_command(args, exec_path)


def remote(exec_path, command, phelp=False, quiet=False, verbose=False):
    """Wrap dvc remote command.

    A set of commands to set up and manage data remotes: add, default, list,
    modify, and remove.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    command: str
        Determines the behaviour of this method according to the following
        possibilities:
        'add' : Add remote.
        'default' : Set/unset default remote.
        'remove' : Remove remote.
        'modify' : Modify remote.
        'list' : List available remotes.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    if phelp:
        return get_help('remote')

    if command in ['add', 'default', 'remove', 'modify', 'list']:
        args = ['dvc', 'remote']

        if quiet:
            args += ['-q']

        if verbose:
            args += ['-v']

        args += [command]
        return run_command(args, exec_path)

    raise DvcExecutionError('Command ', command, ' is not a valid command for dvc \
        remote. Options are: "add | default | remove | modify | list"')


def pull(  # noqa: C901
        exec_path,
        targets,
        remote_storage,
        all_branches=False,
        all_tags=False,
        with_deps=False,
        recursive=False,
        force=False,
        jobs=None,
        phelp=False,
        quiet=False,
        verbose=False):
    """Wrap dvc pull command.

    Downloads missing files and directories from remote storage to the cache
    based on DVC-files in the workspace, then links the downloaded files into
    the workspace.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    targets: list
        Limit command scope to these DVC-files. Using 'recursive', directories
        to search DVC-files in can also be given.

    remote_storage: str
        Name of the remote storage to pull from (see dvc remote list). The
        argument REMOTE is a remote name defined using dvc remote.

    all_branches: bool
        Determines the files to download by examining DVC-files in all Git
        branches instead of just those present in the current workspace. It's
        useful if branches are used to track experiments or project
        checkpoints.

    all_tags: bool
        The same as 'all_branches' but Git tags are used to save different
        experiments or project checkpoints. Note that both options can be
        combined.

    with_deps: bool
        Determines files to download by tracking dependencies to the target
        DVC-files (stages). If no targets are provided, this option is ignored.
        By traversing all stage dependencies, DVC searches backward from the
        target stages in the corresponding pipelines. This means DVC will not
        pull files referenced in later stages than the targets.

    recursive: bool
        Determines the files to pull by searching each target directory and its
        subdirectories for DVC-files to inspect. If there are no directories
        among the targets, this option is ignored.

    force: bool
        Does not prompt when removing workspace files, which occurs when these
        file no longer match the current DVC-file references. This option
        surfaces behavior from the dvc fetch and dvc checkout commands because
        dvc pull in effect performs those 2 functions in a single command.

    jobs: int
        Number of threads to run simultaneously to handle the downloading of
        files from the remote storage. The default value is 4 * cpu_count().
        For SSH remotes, the default is just 4. Using more jobs may improve the
        total download speed if a combination of small and large files are
        being fetched.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    if phelp:
        return get_help('pull')

    args = ['dvc', 'pull']
    if quiet:
        args += ['-q']

    if verbose:
        args += ['-v']

    args += ['-r', remote_storage]
    if jobs is not None:
        args += ['-j', jobs]

    if all_branches and all_tags:
        args += ['-aT']
    elif all_branches:
        args += ['-a']
    elif all_tags:
        args += ['-T']

    if with_deps:
        args += ['-d']

    if recursive:
        args += ['-R']

    if force:
        args += ['-f']

    args += targets
    return run_command(args, exec_path)


def push(
        exec_path,
        targets,
        remote_storage,
        all_branches=False,
        all_tags=False,
        with_deps=False,
        recursive=False,
        jobs=None,
        phelp=False,
        quiet=False,
        verbose=False):
    """Wrap dvc push command.

    Uploads files or directories tracked by DVC to remote storage.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    targets: list
        Limit command scope to these DVC-files. Using 'recursive', directories
        to search DVC-files in can also be given.

    remote_storage: str
        Name of the remote storage to push to (see dvc remote list). The
        argument REMOTE is a remote name defined using dvc remote.

    all_branches: bool
        Determines the files to upload by examining DVC-files in all Git
        branches instead of just those present in the current workspace. It's
        useful if branches are used to track experiments or project
        checkpoints.

    all_tags: bool
        The same as 'all_branches', but Git tags are used to save different
        experiments or project checkpoints. Note that both options can be
        combined.

    with_deps: bool
        Determines files to upload by tracking dependencies to the target
        DVC-files (stages). If no targets are provided, this option is ignored.
        By traversing all stage dependencies, DVC searches backward from the
        target stages in the corresponding pipelines. This means DVC will not
        push files referenced in later stages than the targets.

    recursive: bool
        Determines the files to push by searching each target directory and its
        subdirectories for DVC-files to inspect. If there are no directories
        among the targets, this option is ignored.

    jobs: int
        Number of threads to run simultaneously to handle the uploading of
        files from the remote storage. The default value is 4 * cpu_count().
        For SSH remotes, the default is just 4. Using more jobs may improve the
        total upload speed if a combination of small and large files are being
        fetched.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    if phelp:
        return get_help('push')

    args = ['dvc', 'push']

    if quiet:
        args += ['-q']

    if verbose:
        args += ['-v']

    args += ['-r', remote_storage]
    if jobs is not None:
        args += ['-j', jobs]

    if all_branches and all_tags:
        args += ['-aT']
    elif all_branches:
        args += ['-a']
    elif all_tags:
        args += ['-T']

    if with_deps:
        args += ['-d']

    if recursive:
        args += ['-R']

    args += targets
    return run_command(args, exec_path)


def add(
        exec_path,
        targets,
        file=None,
        phelp=False,
        quiet=False,
        verbose=False,
        recursive=False,
        no_commit=False):
    """Wrap dvc add command.

    Track data files or directories with DVC, by creating a corresponding
    DVC-file.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    targets: list
        Input files/directories to add.

    file: str
        Specify name of the DVC-file it generates. If more than a single target
        are provided, this option is ignored. By default, the name of the
        generated DVC-file is <target>.dvc, where <target> is the file name of
        the given target. This option allows to set the name and the path of
        the generated DVC-file.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    recursive: bool
        Determines the files to add by searching each target directory and its
        subdirectories for data files. If there are no directories among the
        targets, this option is ignored. For each file found, a new DVC-file
        is created using the process described in this command's description.

    no_commit: bool
        Do not save outputs to cache. A DVC-file is created, and an entry is
        added to .dvc/state, while nothing is added to the cache. (The dvc
        status command will report that the file is not in cache.) This is
        analogous to using git add before git commit. Use dvc commit when ready
        to commit the results to cache.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
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
    return run_command(args, exec_path)


def run(  # noqa: C901
        exec_path,
        command,
        wdir,
        deps=None,
        outs=None,
        outs_no_cache=None,
        metrics=None,
        metrics_no_cache=None,
        file=None,
        no_exec=False,
        overwrite_dvcfile=False,
        ignore_build_cache=False,
        no_commit=False,
        always_changed=False,
        phelp=False,
        quiet=False,
        verbose=False):
    """Wrap dvc run command.

    Generate a stage file (DVC-file) from a given command and execute the
    command.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    deps: list
        Specify a files or a directories the stage depends on. Multiple
        dependencies can be specified within this list. Usually, each
        dependency is a file or a directory with data, or a code file, or a
        configuration file. DVC also supports certain external dependencies.

    outs: list
        Specify a file or directory that is the result of running the command.
        Multiple outputs can be specified within this list. DVC builds a
        dependency graph (pipeline) to connect different stages with each other
        based on this list of outputs and dependencies (see 'deps'). DVC
        tracks all output files and directories and puts them into the cache
        (this is similar to what's happening when you use dvc add).

    outs_no_cache: list
        The same as 'outs' except that outputs are not tracked by DVC. It means
        that they are not cached, and it's up to a user to save and version
        control them. This is useful if the outputs are small enough to be
        tracked by Git directly, or if these files are not of future interest.

    metrics: list
        Specify a metric type of output. This option behaves like -o but also
        adds metric: true in the output record of the resulting stage file.
        Metrics are usually small, human readable files (e.g. JSON or CSV) with
        numeric values or other information that describes a model (or any
        other regular output). See dvc metrics to learn more about using
        metrics.

    metrics_no_cache: list
        The same as 'metrics' except that files are not tracked by DVC. It
        means that they are not cached, and it's up to a user to save and
        version control them. This is typically desirable with metric files,
        because they are small enough to be tracked by Git directly. See also
        the difference between 'outs' and 'outs_no_cache'.

    file: str
        Specify a path and/or file name for the stage file generated by this
        command (e.g. file = 'stages/stage.dvc'). This overrides the default
        file name: <file>.dvc, where <file> is the file name of the first
        output or metric.

    wdir: str
        Specifies a working directory for the command to run in. dvc run
        expects that dependencies, outputs, metric files are specified relative
        to this directory. This value is saved in the wdir field of the stage
        file generated (as a relative path to the location of the DVC-file) and
        is used by dvc repro to change the working directory before executing
        the command.

    no_exec: bool
        Create a stage file, but do not execute the command defined in it, nor
        track dependencies or outputs with DVC. In the DVC-file contents, the
        file hash values will be empty; They will be populated the next time
        this stage is actually executed. This is useful if, for example, you
        need to build a pipeline (dependency graph) first, and then run it all
        at once.

    overwrite_dvcfile: bool
        Overwrite an existing DVC-file (with file name determined by the logic
        described in the 'file' option) without asking for confirmation.

    no_commit:
        Do not save outputs to cache. A DVC-file is created, and an entry is
        added to .dvc/state, while nothing is added to the cache. (The dvc
        status command will report that the file is not in cache.) This is
        analogous to using git add before git commit. Use dvc commit when ready
        to commit the results to cache.  Useful when running different
        experiments and you don't want to fill up your cache with temporary
        files. Use 'commit' command when ready to commit the results to cache.

    always_changed: bool
        Always consider this DVC-file as changed. As a result dvc status will
        report it as always changed and dvc repro will always execute it.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    if phelp:
        return get_help('add')

    args = ['dvc', 'run', '-w', wdir]

    if deps:
        for dependency in deps:
            args += ['-d', dependency]

    if outs:
        for out in outs:
            args += ['-o', out]

    if outs_no_cache:
        for out in outs_no_cache:
            args += ['-O', out]

    if metrics:
        for metric in metrics:
            args += ['-m', metric]

    if metrics_no_cache:
        for mnc in metrics_no_cache:
            args += ['-M', mnc]

    if file is not None:
        args += ['-f', file]

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

    args += [command]
    return run_command(args, exec_path)


def repro(  # noqa: C901
        exec_path,
        targets,
        force=False,
        cwd=None,
        single_item=False,
        recursive=True,
        no_commit=False,
        metrics=True,
        dry=False,
        interactive=False,
        run_pipeline=True,
        run_all_pipelines=False,
        ignore_build_cache=False,
        downstream=False,
        phelp=False,
        verbose=False,
        quiet=False):
    """Wrap dvc repro command.

    Generate a stage file (DVC-file) from a given command and execute the
    command.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    targets:list
        DVC-file to reproduce. 'Dvcfile' by default.

    force: bool
        Reproduce a pipeline, regenerating its results, even if no changes were
        found. This executes all of the stages by default, but it can be
        limited with the targets argument, or the 'single_item', 'pipeline' and
        'cwd' arguments.

    single_item: bool
        Reproduce only a single stage by turning off the recursive search for
        changed dependencies. Multiple stages are executed (non-recursively)
        if multiple stage files are given as targets.

    cwd: str
        Directory within the project to reproduce from. If no targets are
        given, it attempts to use Dvcfile in the specified directory. Instead
        of using 'cwd', one can alternately specify a target in a subdirectory
        as path/to/target.dvc. This option can be useful for example with
        subdirectories containing a separate pipeline that can either be
        reproduced as part of the pipeline in the parent directory, or as an
        independent unit.

    recursive: bool
        Determines the stages to reproduce by searching each target directory
        and its subdirectories for DVC-files to inspect. If there are no
        directories among the targets, this option is ignored.

    no_commit: bool
        Do not save outputs to cache. (See dvc run.) Useful when running
        different experiments and you don't want to fill up the cache with
        temporary files. Use dvc commit when ready to commit the results to
        cache.

    metrics: bool
        Show metrics after reproduction. The target pipelines must have at
        least one metric file defined either with the dvc metrics command, or
        by the 'metrics' or 'metrics_no_cache' arguments on the run
        command.

    dry: bool
        Only print the commands that would be executed without actually
        executing the commands.

    interactive: bool
        Ask for confirmation before reproducing each stage. The stage is only
        executed if the user types "y"

    run_pipeline: bool
        Reproduce the entire pipelines that the stage file targets belong to.
        Use pipeline command='show' and for file <target>.dvc to show the
        parent pipeline of a target stage.

    run_all_pipelines: bool
        Reproduce all pipelines, for all the stage files present in DVC
        repository.

    ignore_build_cache: bool
        In cases like ... -> A (changed) -> B -> C it will reproduce A first
        and then B, even if B was previously executed with the same inputs from
        A (cached). To be precise, it reproduces all descendants of a changed
        stage or the stages following the changed stage, even if their direct
        dependencies did not change.
        It can be useful when we have a common dependency among all stages, and
        want to specify it only once (for stage A here). For example, if we
        know that all stages (A and below) depend on requirements.txt, we can
        specify it in A, and omit it in B and C.
        Like with the same option on dvc run, this is a way to force-execute
        stages without changes. This can also be useful for pipelines
        containing stages that produce non-deterministic (semi-random) outputs,
        where outputs can vary on each execution, meaning the cache cannot be
        trusted for such stages.

    downstream: bool
        Only execute the stages after the given targets in their corresponding
        pipelines, including the target stages themselves.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    if phelp:
        return get_help('repro')

    args = ['dvc', 'repro']
    if force:
        args += ['-f']
    if cwd is not None:
        args += ['-c', cwd]
    if single_item:
        args += ['-s']
    if recursive:
        args += ['-R']
    if no_commit:
        args += ['--no-commit']
    if metrics:
        args += ['-m']
    if dry:
        args += ['-d']
    if interactive:
        args += ['-i']
    if run_pipeline:
        args += ['-p']
    if run_all_pipelines:
        args += ['-P']
    if ignore_build_cache:
        args += ['--ignore-build-cache']
    if downstream:
        args += ['--downstream']
    if quiet:
        args += ['-q']
    if verbose:
        args += ['-v']
    args += targets

    return run_command(args, exec_path)


def pipeline(
        exec_path,
        command='show',
        phelp=False,
        quiet=False,
        verbose=False):
    """Wrap dvc pipeline command.

    A set of commands to manage pipelines: show and list.

    Parameters
    ----------
    exec_path: str
        Path from where to execute command.

    command: str
        Determines the behaviour of this method according to the following
        possibilities:
        'show' : Show pipeline.
        'list' : List pipelines.

    phelp: bool
        Returns original dvc usage/help message.

    quiet: bool
        Do not write anything to standard output. Exit with 0 if no problems
        arise, otherwise 1.

    verbose: bool
        Displays detailed tracing information.

    Returns
    -------
    command: str
        The executed command.

    command_output: str
        The stdout resulting from running the process in shell.

    Raises
    ------
    DvcExecutionError
        If the command fails to execute and prints original stderr output.
    """
    if phelp:
        return get_help('pipeline')

    if command in ['show', 'list']:
        args = ['dvc', 'pipeline']

        if quiet:
            args += ['-q']

        if verbose:
            args += ['-v']

        args += [command]
        return run_command(args, exec_path)

    raise DvcExecutionError('Command ', command, ' is not a valid command for dvc \
        pipeline. Options are: "show | list"')
