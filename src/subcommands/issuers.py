import sqlite3

import click
from pick import pick
from tabulate import tabulate

from ..util import pick_with_cancel, successful_update_message

def _get_issuers(connection):
    command = 'SELECT id, name FROM card_issuers ORDER BY name'
    return connection.execute(command).fetchall()

def select_issuer_id(connection):
    issuers = _get_issuers(connection)
    selection = pick([issuer['name'] for issuer in issuers],
                     'Select the card issuer:')
    return issuers[selection[1]]['id']

def list_issuers(connection):
    issuers = [[index + 1, issuer['name']]
               for index, issuer in enumerate(_get_issuers(connection))]
    click.echo_via_pager(tabulate(issuers, tablefmt='fancy_grid'))

def add_issuer(connection):
    new_issuer = click.prompt('Please enter a new card issuer')
    command = 'INSERT INTO card_issuers (name) VALUES (?)'
    with connection:
        try:
            connection.execute(command, (new_issuer,))
        except sqlite3.IntegrityError:
            click.secho('Failed to add duplicate card issuer: ' + new_issuer,
                        fg='red')
            exit(1)

def remove_issuer(connection):
    title = 'Please select a card issuer.'
    issuers = _get_issuers(connection)
    if not issuers:
        click.secho('There is no issuer to remove.', fg='red')
        return
    selection = pick_with_cancel(title, [issuer['name'] for issuer in issuers])
    if selection:
        if not click.confirm('Remove ' + selection[0] +
                             ' and all of its related cards, payments, etc.?'):
            return
        command = 'DELETE FROM card_issuers WHERE name = ?'
        with connection:
            connection.execute(command, (selection[0],))
        click.secho('Removed the card issuer: ' + selection[0], fg='green')

def update_issuer(connection):
    title = 'Please select a card issuer.'
    issuers = _get_issuers(connection)
    if not issuers:
        click.secho('There is no issuer to update.', fg='red')
        return
    selection = pick_with_cancel(title, [issuer['name'] for issuer in issuers])
    if selection:
        new_name = click.prompt('Please enter a new name')
        command = 'UPDATE card_issuers SET name = ? WHERE name = ?'
        with connection:
            connection.execute(command, (new_name, selection[0]))
        successful_update_message()
