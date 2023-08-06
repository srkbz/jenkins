import click
from srkbz_jenkins.binaries.jenkins_manager import jenkins_manager


@click.group(name="heh")
def cli():
    pass


@cli.command()
def test():
    jenkins_manager.install("2.417")


cli()
