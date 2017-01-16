import configparser
import os
import sqlite3

import click

from .. import util

def _initialize_tables(db_path):
    """Create a SQLite database with the default tables and data"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE card_networks
                 (id INTEGER PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL UNIQUE)''')

    card_networks = [('American Express',), ('Visa',), ('Mastercard',),
                     ('Discover',)]

    c.executemany('INSERT INTO card_networks (name) VALUES (?)', card_networks)

    c.execute('''CREATE TABLE card_issuers
                 (id INTEGER PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL UNIQUE)''')

    card_issuers = [('American Express',), ('Barclays',), ('Bank of America',),
                    ('Capital One',), ('Chase',), ('Citibank',), ('Comenity',),
                    ('Discover',), ('U.S. Bank',), ('Wells Fargo',)]

    c.executemany('INSERT INTO card_issuers (name) VALUES (?)', card_issuers)

    c.execute('''CREATE TABLE cards
                 (id INTEGER PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL UNIQUE,
                  annual_fee INTEGER NOT NULL,
                  opened TEXT NOT NULL,
                  closed TEXT,
                  auto_payments BOOLEAN NOT NULL,
                  card_network_id INTEGER NOT NULL,
                  card_issuer_id INTEGER NOT NULL,
                  FOREIGN KEY(card_network_id)
                      REFERENCES card_networks(id)
                      ON DELETE CASCADE,
                  FOREIGN KEY(card_issuer_id)
                      REFERENCES card_issuers(id)
                      ON DELETE CASCADE
                  )''')

    c.execute('''CREATE TABLE payments
                 (id INTEGER PRIMARY KEY NOT NULL,
                  payment_date TEXT NOT NULL,
                  amount INTEGER NOT NULL,
                  card_id INTEGER NOT NULL,
                  FOREIGN KEY(card_id)
                      REFERENCES cards(id)
                      ON DELETE CASCADE
                  )''')

    c.execute('''CREATE TABLE reward_types
                 (id INTEGER PRIMARY KEY NOT NULL,
                  description TEXT NOT NULL UNIQUE)''')

    reward_types = [('cash back',), ('flight',), ('gift card',), ('hotel',),
                    ('statement credit',)]

    c.executemany('INSERT INTO reward_types (description) VALUES (?)',
                  reward_types)

    c.execute('''CREATE TABLE rewards
                 (id integer PRIMARY KEY NOT NULL,
                  redemption_date TEXT NOT NULL,
                  value INTEGER NOT NULL,
                  description TEXT,
                  card_id INTEGER NOT NULL,
                  reward_type_id INTEGER NOT NULL,
                  FOREIGN KEY(card_id)
                      REFERENCES cards(id)
                      ON DELETE CASCADE,
                  FOREIGN KEY(reward_type_id)
                      REFERENCES reward_types(id)
                      ON DELETE CASCADE
                  )''')

    c.execute('''CREATE TABLE programs
                 (id INTEGER PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL UNIQUE,
                  balance TEXT NOT NULL,
                  expiration TEXT)''')

    conn.commit()
    conn.close()

def initialize_application():
    """Create a config file and database as necessary"""

    config_dir = util.get_config_dir()
    config_path = util.get_config_path()

    if os.path.exists(config_path):
        if not click.confirm(('Churn has already been initialized.\n'
                              'Delete your existing data, and '
                              'reinitialize?')):
            exit(0)

    try:
        os.makedirs(config_dir)
    except FileExistsError:
        pass

    click.echo('Default directory: ' + config_dir)
    use_default = click.confirm('Store your data in the default directory?')

    db_name = 'churn.db'
    db_path = os.path.join(config_dir, db_name)
    if not use_default:
        given_dir = click.prompt('Absolute directory')
        while not os.path.isdir(given_dir):
            click.secho('Invalid directory.', fg='red')
            given_dir = click.prompt('Absolute directory')
        db_path = os.path.join(given_dir, db_name)

    config = configparser.ConfigParser()
    config['database'] = {
        'path': db_path,
        'version': 1
    }

    with open(config_path, 'w') as config_file:
        config.write(config_file)

    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

    _initialize_tables(db_path)
