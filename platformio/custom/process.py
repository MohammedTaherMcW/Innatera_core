import os
import click


@click.command("process", short_help="Initialize a project or update existing")
@click.option("-e", "--environment", multiple=True, help="Environment(s) to process")
def process(environment):
    print("Hello from custom process")
    for env in environment:
        print(f"Processing environment: {env}")


if __name__ == "__main__":
    process()
