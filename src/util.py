import configparser
from datetime import datetime
from decimal import Decimal
import os
import re
import sqlite3

import click
from pick import pick

from . import errors

DB_NAME = 'churn.db'

def get_config_dir():
    return click.get_app_dir('churn')

def get_config_path():
    return os.path.join(get_config_dir(), 'churn.ini')

def get_db_path():
    config = configparser.ConfigParser()
    try:
        config.read_file(open(get_config_path()))
    except FileNotFoundError:
        raise errors.MissingConfigError
    return config['database']['path']

def get_connection():
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection

def pick_with_cancel(title, choices):
    selection, index = pick(choices + ['(cancel)'], title)
    return None if index == len(choices) else (selection, index)

def initialize_message():
    click.secho('Please run the initialize command first.', fg='red')

def successful_update_message():
    click.secho('Successfully updated.', fg='green')

def prompt_for_date(text):
    value = None
    while not value:
        raw = click.prompt(text)
        try:
            value = datetime.strptime(raw, '%Y-%m-%d').isoformat()
        except ValueError:
            click.echo('Error: ' + raw + ' is not a valid date')
    return value

def prompt_for_money(text):
    value = None
    while not value:
        raw = click.prompt(text)
        if re.match(r'\d+(?:\.\d{1,2})?$', raw):
            value = int(Decimal(raw) * 100)
        else:
            click.echo('Error: ' + raw + ' is not a valid amount')
    return value

def format_money(value):
    return '${:.2f}'.format(value)

def format_percent(value):
    return '{:.2f}%'.format(value)
