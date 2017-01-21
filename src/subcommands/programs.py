import sqlite3

import click
from pick import pick
from tabulate import tabulate

from ..util import pick_with_cancel, prompt_for_date

def _get_programs(connection):
    command = '''SELECT name,
                        balance,
                        CASE WHEN expiration IS NULL
                            THEN 'N/A'
                            ELSE date(expiration)
                        END AS expiration
                 FROM programs
                 ORDER BY name'''
    return connection.execute(command).fetchall()

def _prompt_for_name():
    return click.prompt('Rewards program name')

def _prompt_for_balance():
    return click.prompt('Balance')

def _prompt_for_expiration_date():
    return prompt_for_date('Expiration date (YYYY-MM-DD)')

def select_program(connection, program_id):
    command = '''SELECT id,
                        name,
                        balance,
                        CASE WHEN expiration IS NULL
                            THEN 'N/A'
                            ELSE date(expiration)
                        END AS expiration
                 FROM programs
              '''

    if program_id:
        command += ' WHERE id = ?'
        program = connection.execute(command, (program_id,)).fetchone()
        return program

    command += ' ORDER BY name'

    programs = connection.execute(command).fetchall()
    if not programs:
        return None

    selection = pick([program['name'] for program in programs] + ['(cancel)'],
                     'Please select a rewards program.')
    index = selection[1]

    return None if index == len(programs) else programs[index]

def list_programs(connection):
    programs = _get_programs(connection)
    headers = ['Name', 'Balance', 'Expiration Date']
    click.echo_via_pager(tabulate(programs, headers, 'fancy_grid'))

def add_program(connection):
    name = _prompt_for_name()
    balance = _prompt_for_balance()
    expires = click.confirm('Is there an expiration date')
    expiration_date = _prompt_for_expiration_date() if expires else None
    command = '''INSERT INTO programs (name, balance, expiration)
                 VALUES (?, ?, ?)
              '''
    with connection:
        try:
            connection.execute(command, (name, balance, expiration_date))
        except sqlite3.IntegrityError:
            click.secho('Failed to add duplicate program: ' + name, fg='red')
            exit(1)

def remove_program(connection):
    program = select_program(connection, None)
    if not program:
        click.secho('There is no program to remove.', fg='red')
        return

    command = 'DELETE FROM programs WHERE id = ?'
    with connection:
        connection.execute(command, (program['id'],))
    click.secho('Removed the program: ' + program['name'], fg='green')

def update_program(connection, program_id):
    program = select_program(connection, program_id)
    if not program:
        click.secho('There is no program to update.', fg='red')
        return

    attributes = [
        ('name', 'Name: ' + program['name']),
        ('balance', 'Balance: ' + program['balance']),
        ('expiration', 'Expiration date: ' + program['expiration'])
    ]

    current_attributes = [attribute[1] for attribute in attributes]

    selected_attribute = pick_with_cancel('Select an attribute to update.',
                                          current_attributes)

    if selected_attribute:
        index = selected_attribute[1]
        name = attributes[index][0]
        if name == 'name':
            value = _prompt_for_name()
        elif name == 'balance':
            value = _prompt_for_balance()
        elif name == 'expiration':
            value = _prompt_for_expiration_date()

        command = 'UPDATE programs SET ' + name + ' = ? WHERE id = ?'
        with connection:
            connection.execute(command, (value, program['id']))

        update_program(connection, program['id'])
