import configparser
import os
import sqlite3

import click

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
