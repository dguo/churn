import click

from . import util, errors

def list_networks():
    try:
        con = util.get_connection()
    except errors.MissingConfigError:
        click.echo('Application is uninitialized. Please run the init command.')
        exit(1)

    for row in con.execute('SELECT name FROM card_networks ORDER BY name'):
        click.secho(row['name'], fg='green')

def networks_handler(list_option):
    """Handle operations for card networks"""
    if list_option:
        list_networks()
