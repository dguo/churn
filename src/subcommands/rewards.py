import click
from pick import pick
from tabulate import tabulate

from ..util import (pick_with_cancel, prompt_for_date, prompt_for_money,
                    format_money)
from .cards import select_card
from .reward_types import select_reward_type_id

def _get_rewards(connection):
    command = '''SELECT date(redemption_date) AS redemption_date,
                        cast(value AS FLOAT) / 100 as value,
                        rewards.description,
                        card_issuers.name || ' ' || cards.name AS card,
                        reward_types.description as reward_type
                 FROM rewards
                 JOIN cards
                 ON cards.id = rewards.card_id
                 JOIN card_issuers
                 ON card_issuers.id = cards.card_issuer_id
                 JOIN reward_types
                 ON reward_types.id = rewards.reward_type_id
                 ORDER BY redemption_date
                 '''
    return connection.execute(command).fetchall()

def _prompt_for_redemption_date():
    return prompt_for_date('Reward date (YYYY-MM-DD)')

def _prompt_for_description():
    value = click.prompt('Description', default='', show_default=False)
    return value if value else None

def select_reward(connection, reward_id):
    command = '''SELECT rewards.id,
                        date(redemption_date) AS redemption_date,
                        cast(value AS FLOAT) / 100 AS value,
                        rewards.description,
                        card_issuers.name || ' ' || cards.name AS card,
                        reward_types.description as reward_type
                 FROM rewards
                 JOIN cards
                 ON cards.id = rewards.card_id
                 JOIN card_issuers
                 ON card_issuers.id = cards.card_issuer_id
                 JOIN reward_types
                 ON reward_types.id = rewards.reward_type_id
                 '''

    if reward_id:
        command += ' WHERE rewards.id = ?'
        reward = connection.execute(command, (reward_id,)).fetchone()
        return reward

    command += ' ORDER BY redemption_date'

    rewards = connection.execute(command).fetchall()
    if not rewards:
        return None

    options = [reward['redemption_date'] + ' | ' + reward['card'] +
               ' | ' + format_money(reward['value']) +
               (' | ' + reward['description']
                if reward['description'] else '')
               for reward in rewards]

    selection = pick(options + ['(cancel)'], 'Select the reward:')
    index = selection[1]

    return None if index == len(rewards) else rewards[index]

def list_rewards(connection):
    rewards = _get_rewards(connection)
    headers = ['Date', 'Value', 'Description', 'Card', 'Type']
    click.echo_via_pager(tabulate(rewards, headers, 'fancy_grid',
                                  floatfmt=',.2f'))

def add_reward(connection):
    card = select_card(connection, None)
    if not card:
        return
    card_id = card['id']

    redemption_date = _prompt_for_redemption_date()
    value = prompt_for_money('Value')
    description = _prompt_for_description()
    reward_type_id = select_reward_type_id(connection)

    command = '''INSERT INTO rewards (redemption_date,
                                      value,
                                      description,
                                      card_id,
                                      reward_type_id)
                 VALUES (?, ?, ?, ?, ?)'''
    with connection:
        connection.execute(command, (redemption_date, value, description,
                                     card_id, reward_type_id))

def remove_reward(connection):
    reward = select_reward(connection, None)
    if not reward:
        click.secho('There is no reward to remove.', fg='red')
        return

    command = 'DELETE FROM rewards WHERE id = ?'
    with connection:
        connection.execute(command, (reward['id'],))
    click.secho('Removed the reward.', fg='green')

def update_reward(connection, reward_id):
    reward = select_reward(connection, reward_id)
    if not reward:
        click.secho('There is no reward to update.', fg='red')
        return

    attributes = [
        ('redemption_date', 'Redemption date: ' + reward['redemption_date']),
        ('value', 'Value: ' + format_money(reward['value'])),
        ('description', 'Description: ' + (reward['description'] if
                                           reward['description'] else '')),
        ('card_id', 'Card: ' + reward['card']),
        ('reward_type_id', 'Type: ' +  reward['reward_type'])
    ]

    current_attributes = [attribute[1] for attribute in attributes]

    selected_attribute = pick_with_cancel('Select an attribute to update.',
                                          current_attributes)

    if selected_attribute:
        index = selected_attribute[1]
        name = attributes[index][0]
        if name == 'redemption_date':
            value = _prompt_for_redemption_date()
        elif name == 'value':
            value = prompt_for_money('Value')
        elif name == 'description':
            value = _prompt_for_description()
        elif name == 'card_id':
            card = select_card(connection, None)
            if not card:
                return
            value = card['id']
        elif name == 'reward_type_id':
            value = select_reward_type_id(connection)

        command = 'UPDATE rewards SET ' + name + ' = ? WHERE id = ?'
        with connection:
            connection.execute(command, (value, reward['id']))

        update_reward(connection, reward['id'])
