import click

from . import errors, util
from .subcommands.initialize import initialize_application
from .subcommands.networks import (list_networks, add_network, remove_network,
                                   update_network)

from .subcommands.uninstall import uninstall_application

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def get_connection():
    try:
        return util.get_connection()
    except errors.MissingConfigError:
        click.secho('Please run the initialize command first.', fg='red')
        exit(1)

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Keep track of your credit card payments and reward redemptions."""
    pass

@main.command()
def initialize():
    """Initialize the application."""
    initialize_application()

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the networks.', default=True)
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add a network.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove a network.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update a network.')
def networks(command):
    """Manage card networks."""
    if command == 'list':
        list_networks(get_connection())
    elif command == 'add':
        add_network(get_connection())
    elif command == 'remove':
        remove_network(get_connection())
    elif command == 'update':
        update_network(get_connection())

@main.command()
def uninstall():
    """Remove the application files."""
    uninstall_application()
