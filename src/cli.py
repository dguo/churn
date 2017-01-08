import click

from . import errors, util
from .subcommands.initialize import initialize_application
from .subcommands.networks import (list_networks, add_network, remove_network,
                                   update_network)
from .subcommands.issuers import (list_issuers, add_issuer, remove_issuer,
                                  update_issuer)
from .subcommands.config import (list_config, update_config)
from .subcommands.reward_types import (list_reward_types, add_reward_type,
                                       remove_reward_type, update_reward_type)
from .subcommands.cards import (list_cards, add_card, remove_card, update_card)

from .subcommands.uninstall import uninstall_application

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def get_connection():
    try:
        return util.get_connection()
    except errors.MissingConfigError:
        util.initialization_message()
        exit(1)

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Keep track of your credit card payments and reward redemptions."""

@main.command()
def initialize():
    """Initialize the application."""
    initialize_application()

# pylint: disable=too-many-function-args

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the networks.')
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
    else:
        main(['networks', '--help'])

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the issuers.')
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add an issuer.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove an issuer.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update an issuer.')
def issuers(command):
    """Manage card issuers."""
    if command == 'list':
        list_issuers(get_connection())
    elif command == 'add':
        add_issuer(get_connection())
    elif command == 'remove':
        remove_issuer(get_connection())
    elif command == 'update':
        update_issuer(get_connection())
    else:
        main(['issuers', '--help'])

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the details.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update the data location.')
def config(command):
    """Manage the configuration."""
    if command == 'list':
        list_config()
    elif command == 'update':
        update_config()
    else:
        main(['config', '--help'])

@main.command(name='reward-types')
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the reward types.')
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add a reward type.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove a reward type.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update a reward type.')
def reward_types(command):
    """Manage reward types."""
    if command == 'list':
        list_reward_types(get_connection())
    elif command == 'add':
        add_reward_type(get_connection())
    elif command == 'remove':
        remove_reward_type(get_connection())
    elif command == 'update':
        update_reward_type(get_connection())
    else:
        main(['reward-types', '--help'])

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the cards.')
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add a card.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove a card.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update a card.')
def cards(command):
    """Manage cards."""
    if command == 'list':
        list_cards(get_connection())
    elif command == 'add':
        add_card(get_connection())
    elif command == 'remove':
        remove_card(get_connection())
    elif command == 'update':
        update_card(get_connection(), None)
    else:
        main(['cards', '--help'])

@main.command()
def uninstall():
    """Remove the application files."""
    uninstall_application()
