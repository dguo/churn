import sqlite3

import click
from pick import pick
from tabulate import tabulate

from ..util import pick_with_cancel, prompt_for_date
from .networks import select_network_id
from .issuers import select_issuer_id

def _get_cards(connection):
    command = '''SELECT cards.name,
                        ('$' || annual_fee) AS annual_fee,
                        date(opened),
                        CASE WHEN closed IS NULL
                            THEN 'N/A'
                            ELSE date(closed)
                        END as closed,
                        CASE WHEN auto_payments
                            THEN 'yes'
                            ELSE 'no'
                        END AS auto_payments,
                        card_networks.name AS network_name,
                        card_issuers.name AS issuer_name
                 FROM cards
                 JOIN card_networks
                 ON cards.card_network_id = card_networks.id
                 JOIN card_issuers
                 ON cards.card_issuer_id = card_issuers.id
                 ORDER BY cards.name'''
    return connection.execute(command).fetchall()

def _prompt_for_name():
    return click.prompt('Name')

def _prompt_for_annual_fee():
    return click.prompt('Annual fee', type=int)

def _prompt_for_open_date():
    return prompt_for_date('Date opened (YYYY-MM-DD)')

def _prompt_for_close_date():
    return prompt_for_date('Date closed (YYYY-MM-DD)')

def _promot_for_autopay():
    return click.confirm('Automatic payments')

def select_card(connection, card_id):
    command = '''SELECT cards.id,
                        (card_issuers.name || ' ' || cards.name || ' (' ||
                         card_networks.name || ')') AS description,
                        cards.name,
                        annual_fee,
                        date(opened) AS opened,
                        CASE WHEN closed IS NULL
                            THEN 'N/A'
                            ELSE date(closed)
                        END as closed,
                        CASE WHEN auto_payments
                            THEN 'yes'
                            ELSE 'no'
                        END AS auto_payments,
                        card_networks.name AS network_name,
                        card_issuers.name AS issuer_name
                 FROM cards
                 JOIN card_networks
                 ON cards.card_network_id = card_networks.id
                 JOIN card_issuers
                 ON cards.card_issuer_id = card_issuers.id
                 '''

    if card_id:
        command += ' WHERE cards.id = ?'
        card = connection.execute(command, (card_id,)).fetchone()
        return card

    command += ' ORDER BY description'

    cards = connection.execute(command).fetchall()
    if not cards:
        return None

    selection = pick([card['description'] for card in cards] + ['(cancel)'],
                     'Select the card:')
    index = selection[1]

    return None if index == len(cards) else cards[index]

def list_cards(connection):
    cards = _get_cards(connection)
    headers = ['Name', 'Annual Fee', 'Opened', 'Closed', 'Autopay', 'Network',
               'Issuer']
    click.echo_via_pager(tabulate(cards, headers, 'fancy_grid'))

def add_card(connection):
    name = _prompt_for_name()
    annual_fee = _prompt_for_annual_fee()
    opened = _prompt_for_open_date()
    auto_payments = _promot_for_autopay()
    network_id = select_network_id(connection)
    issuer_id = select_issuer_id(connection)
    command = '''INSERT INTO cards (name, annual_fee, opened, auto_payments,
                                    card_network_id, card_issuer_id)
                 VALUES (?, ?, ?, ?, ?, ?)
              '''
    with connection:
        try:
            card = (name, annual_fee, opened, auto_payments, network_id,
                    issuer_id)
            connection.execute(command, card)
        except sqlite3.IntegrityError:
            click.secho('Failed to add duplicate card: ' + name, fg='red')
            exit(1)

def remove_card(connection):
    card = select_card(connection, None)
    if not card:
        click.secho('There is no card to remove.', fg='red')
        return

    command = 'DELETE FROM cards WHERE id = ?'
    with connection:
        connection.execute(command, (card['id'],))

    click.secho('Removed the card: ' + card['description'], fg='green')

def update_card(connection, card_id):
    card = select_card(connection, card_id)
    if not card:
        click.secho('There is no card to update.', fg='red')
        return

    attributes = [
        ('name', 'Name: ' + card['name']),
        ('annual_fee', 'Annual Fee: ' + str(card['annual_fee'])),
        ('opened', 'Opened: ' + card['opened']),
        ('closed', 'Closed: ' + card['closed']),
        ('auto_payments', 'Autopay: ' + card['auto_payments']),
        ('card_network_id', 'Network: ' + card['network_name']),
        ('card_issuer_id', 'Issuer: ' + card['issuer_name'])
    ]

    current_attributes = [attribute[1] for attribute in attributes]

    selected_attribute = pick_with_cancel('Select an attribute to update.',
                                          current_attributes)

    if selected_attribute:
        index = selected_attribute[1]
        name = attributes[index][0]
        if name == 'name':
            value = _prompt_for_name()
        elif name == 'annual_fee':
            value = _prompt_for_annual_fee()
        elif name == 'opened':
            value = _prompt_for_open_date()
        elif name == 'closed':
            value = _prompt_for_close_date()
        elif name == 'auto_payments':
            value = _promot_for_autopay()
        elif name == 'card_network_id':
            value = select_network_id(connection)
        elif name == 'card_issuer_id':
            value = select_issuer_id(connection)

        command = 'UPDATE cards SET ' + name + ' = ? WHERE id = ?'
        with connection:
            connection.execute(command, (value, card['id']))

        update_card(connection, card['id'])
