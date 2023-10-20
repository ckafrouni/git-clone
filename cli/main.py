import click
from g import repository, index


@click.group()
def cli():
    """A simple Git clone."""


@cli.command()
@click.argument("path", default=".")
def init(path: str):
    """Initialize a new repository."""
    repository.g_init(path)


@cli.command()
@click.argument("path")
def add(path: str):
    """Stage a file, or a directory."""
    index.add(path)


if __name__ == "__main__":
    cli()
