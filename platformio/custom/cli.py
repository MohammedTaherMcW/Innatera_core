import click

from platformio.custom.process import process


@click.group(
    "custom",
    commands=[
       process
    ],
    short_help="Custom CLI commands",
)
def cli():
    pass
