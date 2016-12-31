import sqlite3

import click

def initialize_tables():
    conn = sqlite3.connect('churn.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE card_networks
                 (id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL)''')

    card_networks = [('American Express',), ('Visa',), ('Mastercard',),
                     ('Discover',)]

    c.executemany('INSERT INTO card_networks (name) VALUES (?)', card_networks)

    c.execute('''CREATE TABLE card_issuers
                 (id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL)''')

    card_issuers = [('American Express',), ('Barclays',), ('Bank of America',),
                    ('Capital One',), ('Chase',), ('Citibank',), ('Comenity',),
                    ('Discover',), ('Mastercard',), ('U.S. Bank',)]

    c.executemany('INSERT INTO card_issuers (name) VALUES (?)', card_issuers)

    c.execute('''CREATE TABLE cards
                 (id INTEGER PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL,
                  annual_fee REAL NOT NULL,
                  opened TEXT NOT NULL,
                  closed TEXT,
                  auto_payments BOOLEAN NOT NULL,
                  card_network_id INTEGER NOT NULL,
                  card_issuer_id INTEGER NOT NULL,
                  FOREIGN KEY(card_network_id) REFERENCES card_networks(id),
                  FOREIGN KEY(card_issuer_id) REFERENCES card_issuers(id)
                  )''')

    c.execute('''CREATE TABLE payments
                 (id INTEGER PRIMARY KEY NOT NULL,
                  date TEXT NOT NULL,
                  amount REAL NOT NULL,
                  card_id INTEGER NOT NULL,
                  FOREIGN KEY(card_id) REFERENCES cards(id)
                  )''')

    c.execute('''CREATE TABLE redemption_types
                 (id INTEGER PRIMARY KEY NOT NULL,
                  description TEXT NOT NULL)''')

    redemption_types = [('cash back',), ('flight',), ('gift card',), ('hotel',),
                        ('statement credit',)]

    c.executemany('INSERT INTO redemption_types (description) VALUES (?)',
                  redemption_types)

    c.execute('''CREATE TABLE redemptions
                (id integer PRIMARY KEY NOT NULL,
                 date TEXT NOT NULL,
                 value REAL NOT NULL,
                 card_id INTEGER NOT NULL,
                 description TEXT,
                 redemption_type_id INTEGER NOT NULL,
                 FOREIGN KEY(card_id) REFERENCES cards(id),
                 FOREIGN KEY(redemption_type_id) REFERENCES redemption_types(id)
                 )''')

    conn.commit()
    conn.close()

@click.command()
def cli():
    click.echo('$$$$$')

