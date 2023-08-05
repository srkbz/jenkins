import click
import tomli

from srkbz_jenkins.config.model import Config


@click.group(name="heh")
def cli():
    pass


@cli.command()
def test():
    with open("config/config.toml", "rb") as f:
        toml_dict = tomli.load(f)
    print(toml_dict)
    print(Config(**toml_dict))


cli()
