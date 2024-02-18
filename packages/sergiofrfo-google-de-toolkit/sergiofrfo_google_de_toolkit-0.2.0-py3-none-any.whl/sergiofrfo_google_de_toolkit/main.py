import click
from sergiofrfo_google_de_toolkit.vm import start, stop, connect

@click.group()
def cli():
    pass

if __name__ == '__main__':
    cli()
    print("hello")

cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)
