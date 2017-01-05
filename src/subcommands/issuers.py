import sqlite3

import click

from ..util import select

def _get_issuers(connection):
    command = 'SELECT name FROM card_issuers ORDER BY name'
    return [row['name'] for row in connection.execute(command)]

def list_issuers(connection):
    click.echo_via_pager('\n'.join(_get_issuers(connection)))

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
    selection = select(title, issuers)
    if selection:
        command = 'DELETE FROM card_issuers WHERE name = ?'
        with connection:
            connection.execute(command, (selection,))
        click.echo('Removed the card issuer: ' + selection)

def update_issuer(connection):
    title = 'Please select a card issuer.'
    issuers = _get_issuers(connection)
    if not issuers:
        click.secho('There is no issuer to update.', fg='red')
        return
    selection = select(title, issuers)
    if selection:
        new_name = click.prompt('Please enter a new name')
        command = 'UPDATE card_issuers SET name = ? WHERE name = ?'
        with connection:
            connection.execute(command, (new_name, selection))
