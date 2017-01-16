import click
from tabulate import tabulate

from ..util import format_money, format_percent

def _get_total_payments(connection):
    command = 'SELECT cast(sum(amount) AS REAL) / 100 FROM payments'
    total_payments = connection.execute(command).fetchone()[0]
    return total_payments if total_payments else 0.0

def _get_total_rewards(connection):
    command = 'SELECT cast(sum(value) AS REAL) / 100 FROM rewards'
    total_rewards = connection.execute(command).fetchone()[0]
    return total_rewards if total_rewards else 0.0

def list_stats(connection):
    total_payments = _get_total_payments(connection)
    total_rewards = _get_total_rewards(connection)

    try:
        reward_rate = round(total_rewards / total_payments * 100, 2)
    except ZeroDivisionError:
        reward_rate = None

    stats = [
        ['Total Payments', format_money(total_payments)],
        ['Total Rewards', format_money(total_rewards)],
        ['Reward Rate',
         format_percent(reward_rate) if reward_rate else 'N/A']
    ]
    headers = ['Statistic', 'Value']

    click.echo_via_pager(tabulate(stats, headers, 'fancy_grid'))
