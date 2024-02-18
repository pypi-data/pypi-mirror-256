import logging.config
import click
from protolog import udp, tcp
import colorama


@click.group()
def cli():
    """
    CLI to run simple protocol loggers by Palmlund Wahlgren Innovative Technology AB
    """



if __name__ == "__main__":
    cli()


cli.add_command(udp.udp)
cli.add_command((tcp.tcp))
