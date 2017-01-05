import click

def list_networks(connection):
    command = 'SELECT name FROM card_networks ORDER BY name'
    for row in connection.execute(command):
        click.echo_via_pager(row['name'])

def add_network(connection, name):
    command = 'INSERT INTO card_networks (name) VALUES (?)'
    with connection:
        connection.execute(command, (name,))

def remove_network(connection):
    command = 'DELETE FROM card_networks WHERE name = ?'
