import click
from platformio.custom.process import process


@click.command("custom", help="Description of my custom command")
@click.pass_context
def cli(ctx):
    # Your command logic here
    click.echo("This is a custom command")
    process()
