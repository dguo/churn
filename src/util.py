import configparser
import os
import sqlite3

import click
from pick import pick

from . import errors

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
    con = sqlite3.connect(get_db_path())
    con.row_factory = sqlite3.Row
    return con

def pick_with_cancel(title, choices):
    selection, index = pick(choices + ['(cancel)'], title)
    return None if index == len(choices) else (selection, index)

def initialization_message():
    click.secho('Please run the initialize command first.', fg='red')
