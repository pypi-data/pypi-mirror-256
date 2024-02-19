import click


@click.command()
@click.option("--detach", "-d", is_flag=True, help="Run in detached mode")
def run(detach: bool):
    click.echo("Running stack...")
    print(detach)
