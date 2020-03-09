# -*- coding: utf-8 -*-
"""Main entry point to all axon commands."""
import click

from axon.config.main import get_config
from axon.commands.cli.config import config
from axon.commands.cli.projects import project_command


@click.group(name='axon')
@click.pass_context
def main(ctx):
    """Execute axon command."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = get_config()


main.add_command(config)
main.add_command(project_command)


if __name__ == '__main__':
    # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
    main(obj={})
