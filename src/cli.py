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
from .subcommands.programs import (list_programs, add_program, remove_program,
                                   update_program)
from .subcommands.payments import (list_payments, add_payment, remove_payment,
                                   update_payment)
from .subcommands.rewards import (list_rewards, add_reward, remove_reward,
                                  update_reward)
from .subcommands.stats import list_stats
from .subcommands.uninstall import uninstall_application

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def _get_connection():
    try:
        return util.get_connection()
    except errors.MissingConfigError:
        util.initialize_message()
        exit(1)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(None, '-v', '--version', message='%(version)s')
def main():
    """Keep track of your credit card payments and rewards."""

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
        list_networks(_get_connection())
    elif command == 'add':
        add_network(_get_connection())
    elif command == 'remove':
        remove_network(_get_connection())
    elif command == 'update':
        update_network(_get_connection())
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
        list_issuers(_get_connection())
    elif command == 'add':
        add_issuer(_get_connection())
    elif command == 'remove':
        remove_issuer(_get_connection())
    elif command == 'update':
        update_issuer(_get_connection())
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
        list_reward_types(_get_connection())
    elif command == 'add':
        add_reward_type(_get_connection())
    elif command == 'remove':
        remove_reward_type(_get_connection())
    elif command == 'update':
        update_reward_type(_get_connection())
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
        list_cards(_get_connection())
    elif command == 'add':
        add_card(_get_connection())
    elif command == 'remove':
        remove_card(_get_connection())
    elif command == 'update':
        update_card(_get_connection(), None)
    else:
        main(['cards', '--help'])

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the programs.')
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add a program.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove a program.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update a program.')
def programs(command):
    """Manage rewards programs."""
    if command == 'list':
        list_programs(_get_connection())
    elif command == 'add':
        add_program(_get_connection())
    elif command == 'remove':
        remove_program(_get_connection())
    elif command == 'update':
        update_program(_get_connection(), None)
    else:
        main(['programs', '--help'])

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the payments.')
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add a payment.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove a payment.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update a payment.')
def payments(command):
    """Manage payments."""
    if command == 'list':
        list_payments(_get_connection())
    elif command == 'add':
        add_payment(_get_connection())
    elif command == 'remove':
        remove_payment(_get_connection())
    elif command == 'update':
        update_payment(_get_connection(), None)
    else:
        main(['payments', '--help'])

@main.command()
@click.option('--list', '-l', 'command', flag_value='list',
              help='List the rewards.')
@click.option('--add', '-a', 'command', flag_value='add',
              help='Add a reward.')
@click.option('--rm', '-r', 'command', flag_value='remove',
              help='Remove a reward.')
@click.option('--update', '-u', 'command', flag_value='update',
              help='Update a reward.')
def rewards(command):
    """Manage rewards."""
    if command == 'list':
        list_rewards(_get_connection())
    elif command == 'add':
        add_reward(_get_connection())
    elif command == 'remove':
        remove_reward(_get_connection())
    elif command == 'update':
        update_reward(_get_connection(), None)
    else:
        main(['rewards', '--help'])

@main.command()
def stats():
    """Get rewards stats."""
    list_stats(_get_connection())

@main.command()
def uninstall():
    """Remove the application files."""
    uninstall_application()
