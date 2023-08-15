import click
from srkbz_jenkins.commands.install_command import install_command
from srkbz_jenkins.commands.start_command import start_command


@click.group()
def cli():
    pass


@cli.command()
def install():
    install_command.run()


@cli.command()
def start():
    start_command.run()


cli()
