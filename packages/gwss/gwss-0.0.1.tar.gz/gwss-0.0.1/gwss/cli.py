from importlib.metadata import version
import sys
import os
from pathlib import Path
from pprint import pprint

import click

from gwss import gwss, resolver_config
from gwss.config import config
from gwss.resolver import resolve_pkg
from gwss.utilities import prepare_config, path_validation, squish_info


class Site(object):
    def __init__(self, destination_directory):
        self.dest_dir = os.path.abspath(destination_directory or '.')

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("v{}".format(version('gwss')))
    ctx.exit()

@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=False)

@click.pass_context
def cli(ctx):
    pass

@cli.command(name='list', help="list the script and style names from the '{}' file".format(Path.joinpath(Path.home(), '.gwss')))
def ls():
    cfg = prepare_config(config)
    print(cfg)

@cli.command(help="get all urls and destination directories for styles and scripts")
@click.option('--dest-dir', '-d', default='.site')
def resolve(dest_dir):
    resolve_cfg = resolver_config.projects
    extension = ''
    for k, v in config.items():
        print("{}".format(v),)
        resolve_pkg(v)
    resolved_rendered = ''
    click.echo(resolved_rendered)

@cli.command()
@click.option('--dest-dir', '-d', default='.site')
def download(dest_dir):
    if path_validation(dest_dir):
        pass


