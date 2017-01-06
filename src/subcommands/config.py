import configparser
import os
import shutil

import click

from ..util import get_config_path, get_db_path, initialization_message
from .. import errors

def list_config():
    config_path = get_config_path()
    if not os.path.isfile(config_path):
        initialization_message()
        exit(1)

    click.echo('Config path: ' + config_path)

    db_path = get_db_path()
    if not os.path.isfile(db_path):
        click.secho('The data file does not exist.', fg='red')
        exit(1)

    click.echo('Data path:   ' + db_path)

def update_config():
    try:
        old_db_path = get_db_path()
    except errors.MissingConfigError:
        initialization_message()
        exit(1)

    config = configparser.ConfigParser()
    config.read(get_config_path())

    new_db_path = click.prompt('Please enter a new path')
    shutil.move(old_db_path, new_db_path)

    config['database']['path'] = new_db_path
    with open(get_config_path(), 'w') as config_file:
        config.write(config_file)
