import click
import requests


@click.group()
def task():
    pass


@task.command()
def create():
    """Create a new task"""
    print("Create a new task")


@task.command()
def search(name):
    """Search for a task"""
    r = requests.get(f"https://api.github.com/search/repositories?q={name}")
    print(r.content)
    print(f"Search for task {name}")


@task.command()
def install(name, version=None):
    """Add a task to the project"""
    print(f"Install task {name}")


@task.command()
def uninstall(name):
    """Remove a task from the project"""
    print(f"Uninstall task {name}")


@task.command()
def update(name, version=None):
    """Update a task in the project"""
    print(f"Update task {name}")
