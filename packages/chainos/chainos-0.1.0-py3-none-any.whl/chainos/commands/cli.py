import click

from chainos.commands.run import run
from chainos.commands.chain import chain
from chainos.commands.task import task


@click.group()
def main():
    pass


main.add_command(run)
main.add_command(chain)
main.add_command(task)


if __name__ == "__main__":
    main()
