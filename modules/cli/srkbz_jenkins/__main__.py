import click
from srkbz_jenkins.commands.install_command import install_command


@click.group(name="heh")
def cli():
    pass


@cli.command()
def install():
    install_command.run()


cli()
