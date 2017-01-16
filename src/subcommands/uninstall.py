import os
import shutil

import click

from .. import util, errors

def uninstall_application():
    config_dir = util.get_config_dir()
    config_path = util.get_config_path()
    try:
        db_path = util.get_db_path()
    except errors.MissingConfigError:
        click.echo('There are no files to remove.')
        click.echo('Just run: pip uninstall churn')
        return

    click.secho('This will remove:', fg='red')
    click.secho(config_dir, fg='red')
    click.secho(config_path, fg='red')
    click.secho(db_path, fg='red')
    if not click.confirm('Do you want to continue?'):
        exit(0)

    os.remove(db_path)
    shutil.rmtree(config_dir)

    click.echo('Removed.')
    click.echo('Now run: pip uninstall churn')
