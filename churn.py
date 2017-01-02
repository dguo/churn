"""Entry point for the CLI"""

import click

from subcommands.initialize import init_handler

@click.group()
def cli():
    """Top level command handler"""
    pass

@cli.command()
def init():
    """Initialize the application"""
    init_handler()
