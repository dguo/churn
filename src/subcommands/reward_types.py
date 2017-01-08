import sqlite3

import click

from ..util import pick_with_cancel

def _get_reward_types(connection):
    command = 'SELECT description FROM reward_types ORDER BY description'
    return [row['description'] for row in connection.execute(command)]

def list_reward_types(connection):
    click.echo_via_pager('\n'.join(_get_reward_types(connection)))

def add_reward_type(connection):
    new_reward_type = click.prompt('Please enter a new reward type')
    command = 'INSERT INTO reward_types (description) VALUES (?)'
    with connection:
        try:
            connection.execute(command, (new_reward_type,))
        except sqlite3.IntegrityError:
            click.secho(
                'Failed to add duplicate reward type: ' + new_reward_type,
                fg='red')
            exit(1)

def remove_reward_type(connection):
    title = 'Please select a reward type.'
    reward_types = _get_reward_types(connection)
    if not reward_types:
        click.secho('There is no reward type to remove.', fg='red')
        return
    selection = pick_with_cancel(title, reward_types)
    if selection:
        command = 'DELETE FROM reward_types WHERE description = ?'
        with connection:
            connection.execute(command, (selection[0],))
        click.echo('Removed the reward type: ' + selection[0])

def update_reward_type(connection):
    title = 'Please select a reward type.'
    reward_types = _get_reward_types(connection)
    if not reward_types:
        click.secho('There is no reward type to update.', fg='red')
        return
    selection = pick_with_cancel(title, reward_types)
    if selection:
        new_reward_type = click.prompt('Please enter a new reward type')
        command = ('UPDATE reward_types SET description = ? '
                   'WHERE description = ?')
        with connection:
            connection.execute(command, (new_reward_type, selection[0]))
