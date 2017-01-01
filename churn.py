import click

from commands.initialize import init_handler

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize the application"""
    init_handler()

