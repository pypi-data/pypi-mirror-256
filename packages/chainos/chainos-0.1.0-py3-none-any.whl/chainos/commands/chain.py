import click
import requests


@click.group()
def chain():
    pass


@chain.command()
def create():
    """Create a new chain"""
    print("Create a new chain")


@chain.command()
def search(name):
    """Search for a chain"""
    r = requests.get(f"https://api.github.com/search/repositories?q={name}")
    print(r.content)
    print(f"Search for chain {name}")


@chain.command()
def add(name, version=None):
    """Add a chain to the project"""
    print(f"Install chain {name}")


@chain.command()
def remove(name):
    """Remove a chain from the project"""
    print(f"Uninstall chain {name}")


@chain.command()
def update(name, version=None):
    """Update a chain in the project"""
    print(f"Update chain {name}")
