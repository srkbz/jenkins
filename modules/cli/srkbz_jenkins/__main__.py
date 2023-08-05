import click
from srkbz_jenkins.binaries.java_manager import java_manager


@click.group(name="heh")
def cli():
    pass


@cli.command()
def test():
    java_manager.install("17")


cli()
