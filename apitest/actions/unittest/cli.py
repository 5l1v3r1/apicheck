#!/usr/bin/env python3

import click
import logging

from apitest import global_options

from .analyze.console import *
from .unittest.console import *


log = logging.getLogger('apitest')


@global_options()
@click.pass_context
def cli(ctx, **kwargs):  # pragma no cover
    ctx.obj = kwargs


@cli.command(help="Load an ApiTest file and display a summary")
@click.pass_context
@click.argument('file_path', required=True)
def analyze(ctx, **kwargs):
    launch_apitest_generate_load_in_console(ctx.obj, **kwargs)


@cli.command(help="Build unittest-like for testing the API")
@click.pass_context
@click.option('-o', '--output-dir', 'output_dir', required=True)
@click.argument('file_path', required=True)
def generate(ctx, **kwargs):
    launch_apitest_generate_unittest_in_console(ctx.obj, **kwargs)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli()
