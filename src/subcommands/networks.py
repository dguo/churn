import sqlite3

import click
from pick import pick

from ..util import pick_with_cancel

def _get_networks(connection):
    command = 'SELECT id, name FROM card_networks ORDER BY name'
    return connection.execute(command).fetchall()

def select_network_id(connection):
    networks = _get_networks(connection)
    selection = pick([network['name'] for network in networks],
                     'Select the card network:')
    return networks[selection[1]]['id']

def list_networks(connection):
    click.echo_via_pager('\n'.join(
        [network['name'] for network in _get_networks(connection)]
    ))

def add_network(connection):
    new_network = click.prompt('Please enter a new card network')
    command = 'INSERT INTO card_networks (name) VALUES (?)'
    with connection:
        try:
            connection.execute(command, (new_network,))
        except sqlite3.IntegrityError:
            click.secho('Failed to add duplicate card network: ' + new_network,
                        fg='red')
            exit(1)

def remove_network(connection):
    title = 'Please select a card network.'
    networks = _get_networks(connection)
    if not networks:
        click.secho('There is no network to remove.', fg='red')
        return
    selection = pick_with_cancel(title,
                                 [network['name'] for network in networks])
    if selection:
        command = 'DELETE FROM card_networks WHERE name = ?'
        with connection:
            connection.execute(command, (selection[0],))
        click.echo('Removed the card network: ' + selection[0])

def update_network(connection):
    title = 'Please select a card network.'
    networks = _get_networks(connection)
    if not networks:
        click.secho('There is no network to update.', fg='red')
        return
    selection = pick_with_cancel(title,
                                 [network['name'] for network in networks])
    if selection:
        new_name = click.prompt('Please enter a new name')
        command = 'UPDATE card_networks SET name = ? WHERE name = ?'
        with connection:
            connection.execute(command, (new_name, selection[0]))
