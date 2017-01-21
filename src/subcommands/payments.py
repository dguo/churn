import click
from pick import pick
from tabulate import tabulate

from ..util import (pick_with_cancel, prompt_for_date, prompt_for_money,
                    format_money)
from .cards import select_card

def _get_payments(connection):
    command = '''SELECT date(payment_date) as payment_date,
                        card_networks.name,
                        card_issuers.name,
                        cards.name,
                        cast(amount AS FLOAT) / 100 AS amount
                 FROM payments
                 JOIN cards
                 ON cards.id = payments.card_id
                 JOIN card_networks
                 ON card_networks.id = cards.card_network_id
                 JOIN card_issuers
                 ON card_issuers.id = cards.card_issuer_id
                 ORDER BY payment_date
                 '''
    return connection.execute(command).fetchall()

def _prompt_for_payment_date():
    return prompt_for_date('Payment date (YYYY-MM-DD)')

def select_payment(connection, payment_id):
    command = '''SELECT payments.id,
                        date(payment_date) as payment_date,
                        card_networks.name as network,
                        card_issuers.name as issuer,
                        cards.name as card,
                        cast(amount AS FLOAT) / 100 AS amount
                 FROM payments
                 JOIN cards
                 ON cards.id = payments.card_id
                 JOIN card_networks
                 ON card_networks.id = cards.card_network_id
                 JOIN card_issuers
                 ON card_issuers.id = cards.card_issuer_id
                 '''

    if payment_id:
        command += ' WHERE payments.id = ?'
        payment = connection.execute(command, (payment_id,)).fetchone()
        return payment

    command += ' ORDER BY payment_date'

    payments = connection.execute(command).fetchall()
    if not payments:
        return None

    options = [payment['payment_date'] + ' | ' + payment['issuer'] + ' ' +
               payment['card'] + ' | ' + format_money(payment['amount'])
               for payment in payments]

    selection = pick(options + ['(cancel)'], 'Select the payment:')
    index = selection[1]

    return None if index == len(payments) else payments[index]

def list_payments(connection):
    payments = _get_payments(connection)
    headers = ['Date', 'Network', 'Issuer', 'Name', 'Amount']
    click.echo_via_pager(tabulate(payments, headers, 'fancy_grid',
                                  floatfmt=',.2f'))

def add_payment(connection):
    card = select_card(connection, None)
    if not card:
        return
    card_id = card['id']

    payment_date = _prompt_for_payment_date()
    amount = prompt_for_money('Amount')

    command = '''INSERT INTO payments (payment_date, amount, card_id)
                 VALUES (?, ?, ?)'''
    with connection:
        connection.execute(command, (payment_date, amount, card_id))

def remove_payment(connection):
    payment = select_payment(connection, None)
    if not payment:
        click.secho('There is no payment to remove.', fg='red')
        return

    command = 'DELETE FROM payments WHERE id = ?'
    with connection:
        connection.execute(command, (payment['id'],))
    click.secho('Removed the payment.', fg='green')

def update_payment(connection, payment_id):
    payment = select_payment(connection, payment_id)
    if not payment:
        click.secho('There is no payment to update.', fg='red')
        return

    attributes = [
        ('payment_date', 'Payment date: ' + payment['payment_date']),
        ('card_id', 'Card: ' + payment['network'] + ' ' + payment['card']),
        ('amount', 'Amount: ' + format_money(payment['amount']))
    ]

    current_attributes = [attribute[1] for attribute in attributes]

    selected_attribute = pick_with_cancel('Select an attribute to update.',
                                          current_attributes)

    if selected_attribute:
        index = selected_attribute[1]
        name = attributes[index][0]
        if name == 'payment_date':
            value = _prompt_for_payment_date()
        elif name == 'amount':
            value = prompt_for_money('Amount')
        elif name == 'card_id':
            card = select_card(connection, None)
            if not card:
                return
            value = card['id']

        command = 'UPDATE payments SET ' + name + ' = ? WHERE id = ?'
        with connection:
            connection.execute(command, (value, payment['id']))

        update_payment(connection, payment['id'])
