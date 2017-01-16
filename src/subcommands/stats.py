import click
from tabulate import tabulate

def list_stats(connection):
    payment_command = 'SELECT cast(sum(amount) AS REAL) / 100 FROM payments'
    total_payments = connection.execute(payment_command).fetchone()[0]

    rewards_command = 'SELECT cast(sum(value) AS REAL) / 100 FROM rewards'
    total_rewards = connection.execute(rewards_command).fetchone()[0]

    reward_rate = round(total_rewards / total_payments * 100, 2)

    stats = [
        ['Total Payments', '${:.2f}'.format(total_payments)],
        ['Total Rewards', '${:.2f}'.format(total_rewards)],
        ['Reward Rate', '{0:.2f}%'.format(reward_rate)]
    ]
    headers = ['Statistic', 'Value']

    click.echo_via_pager(tabulate(stats, headers, 'fancy_grid'))
