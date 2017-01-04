"""Entry point for the CLI"""

import click

from .subcommands.initialize import init_handler
from .subcommands.networks import networks_handler

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Keep track of your credit card payments and reward redemptions."""
    pass

@main.command()
def init():
    """Initialize the application."""
    init_handler()

@main.command()
@click.option('--list', '-l', 'list_option', is_flag=True,
              help='List the networks.')
def networks(**kwargs):
    """Manage card networks."""
    networks_handler(**kwargs)
